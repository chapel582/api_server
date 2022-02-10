import os
from typing import Any, Dict, Optional

from postgres import Postgres
from dotenv import load_dotenv

DB: Optional[Postgres] = None


def init_db() -> Postgres:
    global DB

    if DB is None:
        load_dotenv()
        DB = Postgres(url=os.environ["LOCAL_PG_CONN"])
    return DB


def create_org(name: str) -> Dict[str, Any]:
    """
    name:
        The name of org to create

    returns:
        dictionary containing org column names and values
    """
    db: Postgres = init_db()
    # result: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        cursor.run(
            "INSERT INTO my_schema.organization(org_name) VALUES(%(org_name)s)",
            org_name=name,
        )
        result = cursor.one(
            "SELECT * FROM my_schema.organization WHERE org_name=%(org_name)s",
            org_name=name,
            back_as=dict,
        )

    return result
