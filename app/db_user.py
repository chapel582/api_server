from typing import Any, Dict, List, Optional, Tuple

from postgres import Postgres
from psycopg2.errors import UniqueViolation

from illu_db import init_db
from make_sql import make_where_sql, make_update_sql, SqlParam

# NOTE: SELECT_USER is a common way to access and return the non-secret parts of the user data
SELECT_USER: str = (
    "SELECT id, phone_prefix, phone, user_name, org_id FROM my_schema.illu_user "
)


def create_user(
    phone_prefix: str,
    phone: str,
    user_name: str,
    pw_hash: str,
    jwt: Optional[str] = None,
    org_id: Optional[int] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    creates a user

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

    returns:
        Tuple containing...
        boolean indicating the success of the insert and select transaction
        Dictionary containing most of the user data, excluding some secrets
    """

    db: Postgres = init_db()

    success: bool = False
    result: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        try:
            cursor.run(
                """
                    INSERT INTO
                        my_schema.illu_user(
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
                SELECT_USER + "WHERE phone_prefix=%(phone_prefix)s AND phone=%(phone)s",
                phone_prefix=phone_prefix,
                phone=phone,
                back_as=dict,
            )
            success = True
        except UniqueViolation:
            pass

    return success, result


def get_user(
    user_id: Optional[int] = None,
    phone_prefix: Optional[str] = None,
    phone: Optional[str] = None,
    user_name: Optional[str] = None,
    org_id: Optional[int] = None,
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    gets the user based on WHERE AND on the defined parameters

    returns
        Tuple containing...
        boolean indicating whether the read succeeded
        List containing users who matched the where expression
    """
    db: Postgres = init_db()

    params = {
        "id": user_id,
        "phone_prefix": phone_prefix,
        "phone": phone,
        "user_name": user_name,
        "org_id": org_id,
    }
    success: bool = False
    with db.get_cursor() as cursor:
        result = cursor.all(
            SELECT_USER + make_where_sql(params, "AND"),
            params,
            back_as=dict,
        )
        success = True

    return success, result


def update_user(
    phone_prefix: str,
    phone: str,
    new_phone_prefix: Optional[str] = None,
    new_phone: Optional[str] = None,
    user_name: Optional[str] = None,
    pw_hash: Optional[str] = None,
    jwt: Optional[str] = None,
    org_id: Optional[int] = None,
) -> bool:
    """
    creates a user

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

    returns:
        boolean indicating the success of the insert and select transaction
    """

    db: Postgres = init_db()

    success: bool = False
    param_dict: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        update_args: List[SqlParam] = [
            SqlParam(
                col_name="phone_prefix",
                value=new_phone_prefix,
                param_key="new_phone_prefix",
            ),
            SqlParam(col_name="phone", value=new_phone),
            SqlParam(col_name="user_name", value=user_name),
            SqlParam(col_name="pw_hash", value=pw_hash),
            SqlParam(col_name="jwt", value=jwt),
            SqlParam(col_name="org_id", value=org_id),
        ]
        where_args: List[SqlParam] = [
            SqlParam(
                col_name="phone_prefix",
                value=phone_prefix,
                param_key="old_phone_prefix",
            ),
            SqlParam(col_name="phone", value=phone, param_key="old_phone"),
        ]
        update_sql: str = make_update_sql(
            param_dict=param_dict,
            table_name="my_schema.illu_user",
            update_args=update_args,
            where_args=where_args,
            where_operator="AND",
        )
        if len(update_sql) != 0:
            cursor.run(update_sql, param_dict)
        success = True

    return success


def delete_user(phone_prefix: str, phone: str) -> bool:
    """
    deletes a user

    phone_prefix:
        The user's phone number country code
    phone:
        The user's phone number

    returns:
        boolean indicating the success or failure of the deletion
    """
    db: Postgres = init_db()

    success: bool = False
    with db.get_cursor() as cursor:
        cursor.run(
            """
                DELETE FROM
                    my_schema.illu_user
                WHERE
                    phone_prefix=%(phone_prefix)s AND phone=%(phone)s
            """,
            phone_prefix=phone_prefix,
            phone=phone,
        )
        success = True

    return success
