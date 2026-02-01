"""
Arquivo para a geração inicial de assinaturas por cliente.
"""

import os
import uuid
import numpy as np
import polars as pl

from dotenv import load_dotenv
from src.utils.supabase_tools import create_supabase_client, read_supabase_table

# region ----- Carregar variáveis de ambiente -----
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
# endregion


if __name__ == "__main__":
    # region ----- Conexão com Supabase -----
    supabase_client = create_supabase_client(supabase_url, supabase_key)
    # endregion

    # region ----- Tabelas Supabase-----
    customers = read_supabase_table(
        supabase_client=supabase_client, table_name="customers"
    )
    subscriptions_plans = read_supabase_table(
        supabase_client=supabase_client, table_name="subscription_plans"
    )
    # endregion

    # region ----- Transformar em dataframes -----
    customers_df = pl.DataFrame(customers)
    subscriptions_plans_df = pl.DataFrame(subscriptions_plans)
    # endregion

    # region ----- Transformar Subs em Lista -----
    subscriptions_plans_list: list = subscriptions_plans_df[
        "subscription_plan_id"
    ].to_list()
    print(subscriptions_plans_list)
    # endregion

    # region ----- Selecionar Sub aleatório para Customers -----
    subscription_weights: list[float] = [0.7, 0.2, 0.1]

    customer_subscription: pl.DataFrame = customers_df.with_columns(
        subscription_plan_id=pl.Series(
            np.random.choice(
                subscriptions_plans_list, size=len(customers_df), p=subscription_weights
            )
        )
    )

    # TODO: Finalizar a criação da tabela de snapshor de eventos
    events: pl.DataFrame = customer_subscription.select(
        [
            pl.lit(None).alias("subscription_event_id"),
            pl.col("customer_id"),
            pl.col("subscription_plan_id"),
            pl.lit("signup").alias("event_type"),
            pl.col("billing_cycle"),
            pl.lit(None).alias("price_at_event"),
            pl.col("created_at").alias("valid_from"),
            pl.lit(None).alias("valid_to"),
        ]
    )

    print(events)
