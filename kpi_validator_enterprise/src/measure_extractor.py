import pandas as pd
from xmla_connector import get_connection

def extract_measures():

    query = """
    SELECT MEASURE_NAME, EXPRESSION
    FROM $SYSTEM.MDSCHEMA_MEASURES
    """

    with get_connection() as conn:

        with conn.cursor().execute(query) as cur:

            df = pd.DataFrame(cur.fetchall(),
                columns=[c.name for c in cur.description])

    return df