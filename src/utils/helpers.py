"""
Arquivo com funções auxiliares utilizadas no projeto.
"""

import random
import polars as pl

from io import BytesIO
from datetime import datetime, timedelta


# region ----- Funções auxiliares -----
# Gerar datas aleatórias para o cadastro de clientes
def generate_random_date(
    start_date: datetime = None, end_date: datetime = None
) -> datetime:
    """
    Gera uma data aleatória entre 2020 até a data atual.

    Args:
        start_date (datetime): Data inicial da geração de dados.
        Se não for informado, será definido como 2020-01-01.

        end_date (datetime): Data final da geração de dados.
        Se não for informado, será definido como a data atual.

    Returns:
        datetime: Data aleatória.
    """
    start_date = start_date or datetime(2020, 1, 1, 0, 0, 0)
    end_date = end_date or datetime.now()

    delta = end_date - start_date
    total_seconds = int(delta.total_seconds())

    random_seconds = random.randint(0, total_seconds)

    return start_date + timedelta(seconds=random_seconds)


# Converter arquivo parquet para bytes
def convert_parquet_to_bytes(df: pl.DataFrame) -> bytes:
    """
    Converte um arquivo parquet para bytes.

    Args:
        file_path (str): Caminho do arquivo parquet a ser convertido.

    Returns:
        BytesIO: Bytes do arquivo parquet.
    """
    buffer: BytesIO = BytesIO()
    df.write_parquet(buffer)

    return buffer.getvalue()


# endregion
