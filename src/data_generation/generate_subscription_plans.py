"""
Arquivo para a geração de dados fictícios para planos de assinatura.
"""

import os
import uuid
import polars as pl

from dotenv import load_dotenv
from datetime import datetime
from src.utils.helpers import convert_parquet_to_bytes
from src.utils.supabase_tools import (
    create_supabase_client,
    update_supabase_table,
    read_supabase_table,
    upload_file_to_supabase,
)

# region ----- Carregar variáveis de ambiente -----
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
# endregion


# region ----- Criar dataframe com dados dos planos de assinatura -----
def create_subscription_plans_data() -> pl.DataFrame:
    """
    Cria um dataframe com os dados dos planos de assinatura.

    Returns:
        pl.DataFrame: Dataframe com os dados dos planos de assinatura.
    """
    subscription_plans_data = pl.DataFrame(
        data=[
            {
                "subscription_plan_id": str(uuid.uuid4()),
                "created_at": datetime(2020, 1, 1, 0, 0, 0),
                "name": "Howdy",
                "description": """A warm, upbeat hello to brighten the day. 
                    Small acts of encouragement and cheerful nudges to get you started.""".strip(),
                "level": 1,
                "quota": 10,
                "price_monthly": 5.99,
                "price_yearly": 49.99,
                "interval": "monthly",
                "is_active": True,
            },
            {
                "subscription_plan_id": str(uuid.uuid4()),
                "created_at": datetime(2020, 1, 1, 0, 0, 0),
                "name": "College Cheerleaders",
                "description": """A lively, spirited boost from a supportive squad. 
                    Team cheers, upbeat praise, and practical tips to keep motivation high""".strip(),
                "level": 2,
                "quota": 50,
                "price_monthly": 14.99,
                "price_yearly": 149.99,
                "interval": "monthly",
                "is_active": True,
            },
            {
                "subscription_plan_id": str(uuid.uuid4()),
                "created_at": datetime(2020, 1, 1, 0, 0, 0),
                "name": "Stadium Crowd",
                "description": """A chorus of massive, contagious energy. 
                    Dynamic, personalized encouragement at scale, with virtual confetti moments 
                    and high-impact motivation.""".strip(),
                "level": 3,
                "quota": 200,
                "price_monthly": 29.99,
                "price_yearly": 299.99,
                "interval": "monthly",
                "is_active": True,
            },
        ]
    )

    subscription_plans_data = subscription_plans_data.with_columns(
        pl.col("created_at").cast(pl.Datetime)
    )

    return subscription_plans_data


# endregion

# if __name__ == "__main__":
#     subscription_plans_data = create_subscription_plans_data()

#     # Converter datas para strings para serem compatíveis com o supabase
#     subscription_plans_data = subscription_plans_data.with_columns(
#         pl.col("created_at").dt.strftime("%Y-%m-%dT%H:%M:%S")
#     )

#     # Transformar dataframe em dict para ser compatível com o supabase
#     subscription_plans_data_dict = subscription_plans_data.to_dicts()

#     # Transformar dataframe em bytes para fazer o upload no bucket
#     subscription_plans_data_parquet = convert_parquet_to_bytes(
#         df=subscription_plans_data
#     )

#     supabase = create_supabase_client(url=SUPABASE_URL, key=SUPABASE_KEY)

#     upload_file_to_supabase(
#         supabase_client=supabase,
#         file_name_or_path="subscription_plans_inital_load.parquet",
#         file=subscription_plans_data_parquet,
#         bucket_name="initial_load",
#     )

#     update_supabase_table(
#         supabase_client=supabase,
#         table_name="subscription_plans",
#         data=subscription_plans_data_dict,
#     )

#     subscription_plans_data = read_supabase_table(
#         supabase_client=supabase, table_name="subscription_plans"
#     )
