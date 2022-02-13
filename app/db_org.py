from typing import Any, Dict, Tuple

from psycopg2.errors import UniqueViolation
from postgres import Postgres

from illu_db import init_db


def create_org(name: str) -> Tuple[bool, Dict[str, Any]]:
    """
    creates an organization

    name:
        The name of org to create

    returns:
        Tuple containing...
        boolean indicating success or failure of insertion and selection transaction
        dictionary containing org column names and values
    """
    db: Postgres = init_db()

    success: bool = False
    result: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        try:
            cursor.run(
                "INSERT INTO my_schema.organization(org_name) VALUES(%(org_name)s)",
                org_name=name,
            )
            result = cursor.one(
                "SELECT * FROM my_schema.organization WHERE org_name=%(org_name)s",
                org_name=name,
                back_as=dict,
            )
            success = True
        except UniqueViolation:
            pass

    return success, result


def delete_org(name: str) -> bool:
    """
    deletes and organization

    name:
        The name of the org to delete

    returns:
        boolean indicating whether the deletion succeeded
    """

    db: Postgres = init_db()

    success: bool = False
    with db.get_cursor() as cursor:
        cursor.run(
            "DELETE FROM my_schema.organization WHERE org_name=%(org_name)s",
            org_name=name,
        )
        success = True

    return success
