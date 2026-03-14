from pyadomd import Pyadomd
from config import XMLA_ENDPOINT, DATASET_NAME

def get_connection():

    conn_str = f"""
    Provider=MSOLAP;
    Data Source={XMLA_ENDPOINT};
    Initial Catalog={DATASET_NAME};
    """

    return Pyadomd(conn_str)