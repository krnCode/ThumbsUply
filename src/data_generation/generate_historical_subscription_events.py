"""
Arquivo para a geração eventos históricos de assinaturas, desde o início da entrada
do cliente até a data da geração do código.
"""

import uuid
import os
import polars as pl
import numpy as np
from datetime import date

from dotenv import load_dotenv
from src.utils.helpers import convert_parquet_to_bytes
from src.utils.supabase_tools import (
    create_supabase_client,
    read_supabase_table,
    update_supabase_table,
    upload_file_to_supabase,
)


# region ----- Carregar variáveis de ambiente -----
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
# endregion


# region ----- Definir data limite -----
target_date = date.today()
# endregion


# region ----- Funções suporte -----
def generate_historical_events(initial_events_df: pl.DataFrame) -> pl.DataFrame:
    """
    Função que gera eventos históricos de assinaturas, desde o início da entrada
    do cliente até a data da geração do código.

    Args:
        initial_events (pl.DataFrame): DataFrame com os dados iniciais de assinaturas.

    Returns:
        pl.DataFrame: DataFrame com os dados históricos de assinaturas.
    """

    # Criar linha do tempo por cliente
    timeline_df: pl.DataFrame = initial_events_df.with_columns(
        pl.date_ranges(
            start=pl.col("valid_from").cast(pl.Datetime),
            end=target_date,
            interval="1mo",
            eager=False,
        ).alias("simulation_date")
    ).explode("simulation_date")

    # Gerar as probabilidades de assinaturas para cada mês
    np.random.seed(42)
    timeline_df = timeline_df.with_columns(
        dice=pl.Series(np.random.random(len(timeline_df)))
    )

    # Aplicar de forma aleatória as probabilidades de eventos conforme regras de negócio
    # simulated_events: pl.DataFrame = timeline_df.with_columns(
    #     generated_event=pl.when(pl.col("dice") < 0.03)
    #     .then(pl.lit("churn"))
    #     .when(pl.col("dice") < 0.05)
    #     .then(pl.lit("upgrade"))
    #     .when(pl.col("dice") < 0.06)
    #     .then(pl.lit("downgrade"))
    #     .otherwise(pl.lit("active"))
    # )

    simulated_events: pl.DataFrame = timeline_df.with_columns(
        event_type=pl.when(pl.col("dice") < 0.03)
        .then(pl.lit("churn"))
        .when(pl.col("dice") < 0.05)
        .then(pl.lit("upgrade"))
        .when(pl.col("dice") < 0.06)
        .then(pl.lit("downgrade"))
        .otherwise(pl.lit("active"))
    )

    # Filtrar meses onde existem apenas mudança de estado
    action_events: pl.DataFrame = simulated_events.filter(
        pl.col("event_type") != "active"
    )

    # Atualizar data valid_from com a data da ocorrência do evento
    action_events = action_events.with_columns(
        valid_from=pl.col("simulation_date").cast(pl.Datetime)
    )

    # Remover eventos após churn (evitar eventos em assinaturas que já foram canceladas)
    action_events = (
        action_events.with_columns(
            churn_flag=pl.when(pl.col("event_type") == "churn").then(1).otherwise(0)
        )
        .with_columns(
            past_churns=pl.col("churn_flag")
            .cum_sum()
            .shift(1)
            .fill_null(0)
            .over("customer_id")
        )
        .filter(pl.col("past_churns") == 0)
    )

    # Limpar colunas temporárias para não quebrar o schema
    action_events = action_events.drop(
        ["simulation_date", "dice", "past_churns", "churn_flag"]
    )

    return action_events


def build_scd2_timeline(all_events_df: pl.DataFrame) -> pl.DataFrame:
    """
    Função que gera um timeline de eventos SCD2 desordenado, e os ordena
    cronologicamente, por cliente.

    Args:
        all_events (pl.DataFrame): DataFrame com todos os eventos de assinaturas.

    Returns:
        pl.DataFrame: DataFrame com os eventos históricos de assinaturas.
    """

    # Ordenar e particionar os eventos
    df_sorted: pl.DataFrame = all_events_df.sort(["customer_id", "valid_from"])

    # Ligar eventos da mesma partição
    df_chained: pl.DataFrame = df_sorted.with_columns(
        valid_to=pl.col("valid_from").shift(-1).over("customer_id")
    )

    # Tratar casos finais (último evento) e churn
    df_final: pl.DataFrame = df_chained.with_columns(
        valid_to=pl.when(pl.col("event_type") == "churn")
        .then(pl.col("valid_from"))
        .otherwise(pl.col("valid_to"))
    )

    # Schema conforme supabase
    columns_schema = [
        "subscription_event_id",
        "customer_id",
        "subscription_plan_id",
        "event_type",
        "billing_cycle",
        "price_at_event",
        "valid_from",
        "valid_to",
    ]

    return df_final


# endregion

if __name__ == "__main__":
    # region ----- Conexão com Supabase -----
    supabase_client = create_supabase_client(supabase_url, supabase_key)
    # endregion

    # region ----- Tabelas Supabase-----
    subscriptions_events = read_supabase_table(
        supabase_client=supabase_client, table_name="subscription_events"
    )
    # endregion

    # region ----- Transformar em dataframes -----
    initial_events_df = pl.DataFrame(subscriptions_events)
    # initial_events_df = initial_events_df.with_columns(
    #     pl.col("valid_from")
    #     .cast(pl.Utf8)
    #     .str.to_datetime(strict=False)
    #     .dt.replace_time_zone(None),
    #     pl.col("valid_to")
    #     .cast(pl.Utf8)
    #     .str.to_datetime(strict=False)
    #     .dt.replace_time_zone(None),
    # )
    # endregion

    initial_events_df = initial_events_df.with_columns(
        pl.col("valid_from")
        .cast(pl.Utf8)
        .str.to_datetime(time_zone="UTC", strict=False)
        .dt.replace_time_zone(None),
        pl.col("valid_to")
        .cast(pl.Utf8)
        .str.to_datetime(time_zone="UTC", strict=False)
        .dt.replace_time_zone(None),
    )

    mutations_df = generate_historical_events(initial_events_df)

    if len(mutations_df) > 0:
        all_events_df: pl.DataFrame = pl.concat(
            [initial_events_df, mutations_df], how="diagonal"
        )

        final_scd2_df: pl.DataFrame = build_scd2_timeline(all_events_df)

        print(final_scd2_df)
        final_scd2_df.write_excel("final_scd2.xlsx")
