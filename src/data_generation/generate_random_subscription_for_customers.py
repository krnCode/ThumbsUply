"""
Arquivo para a geração inicial de assinaturas por cliente.
"""

import os
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

    print(customers_df)
    print(subscriptions_plans_df)
