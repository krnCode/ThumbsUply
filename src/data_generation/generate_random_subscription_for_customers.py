"""
Arquivo para a geração inicial de assinaturas por cliente.
"""

import os
import uuid
import random
import numpy as np
import polars as pl

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


# if __name__ == "__main__":
#     # region ----- Conexão com Supabase -----
#     supabase_client = create_supabase_client(supabase_url, supabase_key)
#     # endregion

#     # region ----- Tabelas Supabase-----
#     customers = read_supabase_table(
#         supabase_client=supabase_client, table_name="customers"
#     )
#     subscriptions_plans = read_supabase_table(
#         supabase_client=supabase_client, table_name="subscription_plans"
#     )
#     # endregion

#     # region ----- Transformar em dataframes -----
#     customers_df = pl.DataFrame(customers)
#     subscriptions_plans_df = pl.DataFrame(subscriptions_plans)
#     # endregion

#     # region ----- Transformar Subs em Lista -----
#     subscriptions_plans_list: list = subscriptions_plans_df[
#         "subscription_plan_id"
#     ].to_list()
#     # endregion

#     # region ----- Selecionar Sub aleatório para Customers -----
#     subscription_weights: list[float] = [0.7, 0.2, 0.1]
#     billing_cycle_weights: list[float] = [0.7, 0.3]
#     # endregion

#     customer_subscription: pl.DataFrame = customers_df.with_columns(
#         subscription_plan_id=pl.Series(
#             np.random.choice(
#                 subscriptions_plans_list, size=len(customers_df), p=subscription_weights
#             )
#         )
#     )

#     # Criar tabela inicial de eventos, depois incluir os dados necessários
#     initial_events: pl.DataFrame = customer_subscription.select(
#         [
#             pl.lit(None).alias("subscription_event_id"),
#             pl.col("customer_id"),
#             pl.col("subscription_plan_id"),
#             pl.lit("signup").alias("event_type"),
#             pl.lit(None).alias("billing_cycle"),
#             pl.lit(None).alias("price_at_event"),
#             pl.col("created_at").alias("valid_from"),
#             pl.lit(None).alias("valid_to"),
#         ]
#     )

#     # print(initial_events)

#     # Criar resultados para serem inseridos no dataframe
#     subs_uuid: list[str] = [
#         str(uuid.uuid4()) for x in range(len(customer_subscription))
#     ]

#     billing_cycle: list[str] = random.choices(
#         ["monthly", "yearly"],
#         weights=billing_cycle_weights,
#         k=len(customer_subscription),
#     )

#     # Para incluir corretamente o valor conforme o período de faturamento, será
#     # necessário juntar os dataframes de assinaturas e eventos e selecionar o valor
#     # correto para cada assinatura
#     initial_events: pl.DataFrame = initial_events.with_columns(
#         subscription_event_id=pl.Series(subs_uuid),
#         billing_cycle=pl.Series(billing_cycle),
#     )

#     initial_events = initial_events.join(
#         subscriptions_plans_df, on="subscription_plan_id", how="left"
#     ).select(
#         [
#             pl.col("subscription_event_id"),
#             pl.col("customer_id"),
#             pl.col("subscription_plan_id"),
#             pl.col("event_type"),
#             pl.col("billing_cycle"),
#             pl.when(pl.col("billing_cycle").str.contains("monthly"))
#             .then(pl.col("price_monthly"))
#             .otherwise(pl.col("price_yearly"))
#             .alias("price_at_event"),
#             pl.col("valid_from"),
#             pl.col("valid_to"),
#         ]
#     )

#     # Transformar dataframe em dict para ser compatível com o supabase
#     initial_events_dict = initial_events.to_dicts()

#     update_supabase_table(
#         supabase_client=supabase_client,
#         table_name="subscription_events",
#         data=initial_events_dict,
#     )

#     subscription_events_data = read_supabase_table(
#         supabase_client=supabase_client, table_name="subscription_events"
#     )
#     subscription_events_data = pl.DataFrame(subscription_events_data)
#     parquet_bytes = convert_parquet_to_bytes(df=subscription_events_data)

#     upload_file_to_supabase(
#         supabase_client=supabase_client,
#         file_name_or_path="subscription_events.parquet",
#         file=parquet_bytes,
#         bucket_name="initial_load",
#     )
