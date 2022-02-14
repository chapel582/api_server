from typing import Any, Dict, List, Optional, Tuple

from postgres import Postgres
from psycopg2.errors import UniqueViolation

from illu_db import init_db
from make_sql import make_where_sql, make_update_sql, SqlParam


def create_site(name: str, org_id: int) -> Tuple[bool, Dict[str, Any]]:
    """ """

    db: Postgres = init_db()

    success: bool = False
    result: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        try:
            cursor.run(
                """
                    INSERT INTO
                        my_schema.site(name, org_id, is_active)
                    VALUES(
                        %(name)s, %(org_id)s, %(is_active)s
                    )
                """,
                name=name,
                org_id=org_id,
                is_active=True,
            )
            result = cursor.one(
                "SELECT * FROM my_schema.site WHERE name=%(name)s AND org_id=%(org_id)s",
                name=name,
                org_id=org_id,
                back_as=dict,
            )
            success = True
        except UniqueViolation:
            pass

    return success, result


def get_site(
    site_id: Optional[int] = None,
    name: Optional[str] = None,
    org_id: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> Tuple[bool, List[Dict[str, Any]]]:
    """ """
    db: Postgres = init_db()

    params = {
        "id": site_id,
        "name": name,
        "org_id": org_id,
        "is_active": is_active,
    }
    success: bool = False
    with db.get_cursor() as cursor:
        result = cursor.all(
            "SELECT * FROM my_schema.site " + make_where_sql(params, "AND"),
            params,
            back_as=dict,
        )
        success = True

    return success, result


def update_site(
    site_id: Optional[int] = None,
    name: Optional[str] = None,
    new_name: Optional[str] = None,
    org_id: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> bool:
    """ """
    db: Postgres = init_db()

    success: bool = False
    param_dict: Dict[str, Any] = {}
    with db.get_cursor() as cursor:
        update_args: List[SqlParam] = [
            SqlParam(col_name="name", value=new_name, param_key="new_name"),
            SqlParam(col_name="org_id", value=org_id),
            SqlParam(col_name="is_active", value=is_active),
        ]
        where_args: List[SqlParam] = [
            SqlParam(col_name="id", value=site_id),
            SqlParam(col_name="name", value=name, param_key="old_site_name"),
        ]
        update_sql: str = make_update_sql(
            param_dict=param_dict,
            table_name="my_schema.site",
            update_args=update_args,
            where_args=where_args,
            where_operator="AND",
        )
        if len(update_sql) != 0:
            cursor.run(update_sql, param_dict)
        success = True

    return success


def delete_site(site_id: Optional[str] = None, name: Optional[str] = None) -> bool:
    """ """
    db: Postgres = init_db()

    success: bool = False
    where_params: Dict[str, Any] = {"id": site_id, "name": name}
    with db.get_cursor() as cursor:
        cursor.run(
            "DELETE FROM my_schema.site " + make_where_sql(where_params, "AND"),
            where_params,
        )
        success = True

    return success
