"""
Arquivo para a geração de dados fictícios para clientes, utilizando a API do RandomUser.me
"""

import uuid
import requests as r
import polars as pl
import os

from dotenv import load_dotenv
from datetime import datetime
from src.utils.helpers import generate_random_date
from src.utils.supabase_tools import create_supabase_client, update_supabase_table


# region ----- Carregar variáveis de ambiente -----
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
# endregion


# region ----- Funções -----
# Criar dataframe com dados dos clientes utilizando RandomUer.me API
def create_customers_data(response) -> pl.DataFrame:
    """
    Cria um dataframe com os dados dos clientes.
    A API do RandomUser.me é utilizada para obter os dados dos clientes.
    O objeto de resposta é convertido em um dataframe.

    Args:
        response (requests.Response): Resposta da API do RandomUser.me.

    Returns:
        pl.DataFrame: Dataframe com os dados dos clientes.
    """
    results = response["results"]
    customers_data = pl.DataFrame(
        {
            "customer_id": pl.Series([str(uuid.uuid4()) for x in range(len(results))]),
            "created_at": pl.Series(
                [generate_random_date() for x in range(len(results))]
            ),
            "first_name": pl.Series([x["name"]["first"] for x in results]),
            "last_name": pl.Series([x["name"]["last"] for x in results]),
            "gender": pl.Series([x["gender"] for x in results]),
            "email": pl.Series([x["email"] for x in results]),
            "nationationality": pl.Series([x["nat"] for x in results]),
            "location_country": pl.Series([x["location"]["country"] for x in results]),
            "location_state": pl.Series([x["location"]["state"] for x in results]),
            "location_city": pl.Series([x["location"]["city"] for x in results]),
            "cellphone_number": pl.Series([x["cell"] for x in results]),
            "customer_thumbnail": pl.Series([x["picture"]["large"] for x in results]),
        }
    )

    customers_data = customers_data.with_columns(pl.col("created_at").cast(pl.Datetime))

    return customers_data


# endregion


# region ----- Config API -----
BASE_URL: str = "https://randomuser.me/api/"
nationalities: str = "br,ca,fr,gb,us"
results: int = 400
include: str = "gender,name,location,email,cell,picture,nat"

response: dict = r.get(
    BASE_URL + "?nat=" + nationalities + "&inc=" + include + "&results=" + str(results)
).json()
# endregion


if __name__ == "__main__":
    customers_data = create_customers_data(response)
    # Converter datas para strings para serem compatíveis com o supabase
    customers_data = customers_data.with_columns(
        pl.col("created_at").dt.strftime("%Y-%m-%dT%H:%M:%S")
    )
    # Transformar dataframe em dict para ser compatível com o supabase
    customers_data_dict = customers_data.to_dicts()

    supabase = create_supabase_client(url=SUPABASE_URL, key=SUPABASE_KEY)
    update_supabase_table(
        supabase_client=supabase,
        table_name="customers",
        data=customers_data_dict,
    )
    # print(customers_data)
