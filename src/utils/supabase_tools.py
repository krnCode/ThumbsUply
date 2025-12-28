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
    Atualiza uma tabela no supabase. Esta função utiliza o método upsert do supabase.
    (UPSERT: Atualiza dados que já existem ou insere novos dados)

    Args:
        supabase_client (Client): Conexão com o Supabase.
        table_name (str): Nome da tabela a ser atualizada.
        data (dict): Dicionário com os dados a serem atualizados.
    """

    supabase_client.table(table_name).upsert(data).execute()


# Ler tabela no supabase
def read_supabase_table(supabase_client, table_name: str) -> dict:
    """
    Ler uma tabela no supabase.

    Args:
        supabase_client (Client): Conexão com o Supabase.
        table_name (str): Nome da tabela a ser lida.

    Returns:
        dict: Dicionário com os dados da tabela.
    """

    return supabase_client.table(table_name).select("*").execute().data


# Enviar arquivos para o supabase
def upload_file_to_supabase(
    supabase_client, file_name_or_path: str, file: str, bucket_name: str
) -> str:
    """
    Envia um arquivo para o supabase. O tipo de conteúdo do arquivo enviado é "application/octet-stream"
    para garantir compatibilidade.

    Args:
        supabase_client (Client): Conexão com o Supabase.
        file (str): Caminho do arquivo a ser enviado ou nome do arquivo em bytes (se for salvo em memória).
        bucket_name (str): Nome do bucket no supabase.

    Returns:
        str: URL do arquivo enviado.
    """

    return supabase_client.storage.from_(bucket_name).upload(
        file_name_or_path,
        file,
        file_options={"contentType": "application/octet-stream"},
    )


# endregion
