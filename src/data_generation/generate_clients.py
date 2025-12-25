"""
Arquivo para a geração de dados fictícios para clientes, utilizando Faker
"""

import requests as r
import polars as pl

# region ----- Config API -----
BASE_URL: str = "https://randomuser.me/api/"
nationalities: str = "br,ca,fr,gb,us"
results: int = 50
include: str = "gender,name,location,email,registered,cell,picture,nat"
# endregion


if __name__ == "__main__":
    # Pegar dados da API
    response: dict = r.get(
        BASE_URL
        + "?nat="
        + nationalities
        + "&inc="
        + include
        + "&results="
        + str(results)
    ).json()

    print(response)

    # Tratar os dados recebidos para Series, e criar um dataframe
    results = response["results"]
    clients_data = pl.DataFrame(
        {
            "gender": pl.Series([x["gender"] for x in results]),
            "first_name": pl.Series([x["name"]["first"] for x in results]),
            "last_name": pl.Series([x["name"]["last"] for x in results]),
            "location_city": pl.Series([x["location"]["city"] for x in results]),
            "location_state": pl.Series([x["location"]["state"] for x in results]),
            "location_country": pl.Series([x["location"]["country"] for x in results]),
            "email": pl.Series([x["email"] for x in results]),
            "registered": pl.Series([x["registered"]["date"] for x in results]),
            "email": pl.Series([x["email"] for x in results]),
            "cell": pl.Series([x["cell"] for x in results]),
            "picture": pl.Series([x["picture"]["large"] for x in results]),
            "nat": pl.Series([x["nat"] for x in results]),
        }
    )

    clients_data.write_csv("clients.csv")

    print(clients_data)
