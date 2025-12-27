"""
Arquivo para criação de ferramentas de suporte à API do Supabase
"""

from supabase import create_client, Client


# region ----- Conexão com Supabase -----
# Criar conexão com Supabase
def create_supabase_client(url, key) -> Client:
    """
    Cria uma conexão com o Supabase.

    Returns:
        Client: Conexão com o Supabase.
    """

    return create_client(url, key)


# endregion


# region ----- Funções auxiliares -----
# Atualizar tabela no supabase
def update_supabase_table(supabase_client, table_name: str, data: dict) -> None:
    """
    Atualiza uma tabela no supabase.

    Args:
        supabase_client (Client): Conexão com o Supabase.
        table_name (str): Nome da tabela a ser atualizada.
        data (dict): Dicionário com os dados a serem atualizados.
    """

    supabase_client.table(table_name).upsert(data).execute()


# endregion
