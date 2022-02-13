import os
from typing import Optional

from postgres import Postgres
from dotenv import load_dotenv

DB: Optional[Postgres] = None


def init_db() -> Postgres:
    """
    Checks if the database is initialized and initializes it if it hasn't been
    Use this at the start of each of your db queries

    returns:
        Postgres db instance
    """
    global DB

    if DB is None:
        load_dotenv()
        DB = Postgres(url=os.environ["LOCAL_PG_CONN"])
    return DB
