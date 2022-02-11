import os
from typing import Any, Dict, Optional, Tuple

from psycopg2.errors import UniqueViolation
from postgres import Postgres
from dotenv import load_dotenv

DB: Optional[Postgres] = None


def init_db() -> Postgres:
    global DB

    if DB is None:
        load_dotenv()
        DB = Postgres(url=os.environ["LOCAL_PG_CONN"])
    return DB


def create_org(name: str) -> Tuple[bool, Dict[str, Any]]:
    """
    name:
        The name of org to create

    returns:
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
    name:
        The name of the org to delete
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


def create_user(
    phone_prefix: str,
    phone: str,
    user_name: str,
    pw_hash: str,
    jwt: Optional[str] = None,
    org_id: Optional[int] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    phone_prefix:
        The phone number country code

    phone:
        The phone number of the user

    user_name:
        the display name of the user

    pw_hash:
        the user's password hash

    jwt:
        TODO: fill me in

    org_id:
        the organization that the user is a member of
    """

    db: Postgres = init_db()

    success: bool = False
    result: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        cursor.run(
            """
                INSERT INTO my_schema.illu_user(
                    phone_prefix, phone, user_name, pw_hash, jwt, org_id
                )
                VALUES(
                    %(phone_prefix)s,
                    %(phone)s,
                    %(user_name)s,
                    %(pw_hash)s,
                    %(jwt)s,
                    %(org_id)s
                )
            """,
            phone_prefix=phone_prefix,
            phone=phone,
            user_name=user_name,
            pw_hash=pw_hash,
            jwt=jwt,
            org_id=org_id,
        )
        result = cursor.one(
            """
                SELECT
                    id, phone_prefix, phone, user_name, org_id
                FROM
                    my_schema.illu_user
                WHERE
                    phone_prefix=%(phone_prefix)s AND phone=%(phone)s
            """,
            phone_prefix=phone_prefix,
            phone=phone,
            back_as=dict,
        )
        success = True

    return success, result


def delete_user(phone_prefix: str, phone: str) -> bool:
    db: Postgres = init_db()

    success: bool = False
    with db.get_cursor() as cursor:
        cursor.run(
            "DELETE FROM my_schema.illu_user WHERE phone_prefix=%(phone_prefix)s AND phone=%(phone)s",
            phone_prefix=phone_prefix,
            phone=phone,
        )
        success = True

    return success
