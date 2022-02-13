from typing import Any, Dict, List

from make_sql import make_where_sql_col, make_where_sql, make_update_sql, SqlParam


def test_make_where_sql_col_empty_and():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = []

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == ""
    assert param_dict == {}


def test_make_where_sql_col_empty_or():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = []

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == ""
    assert param_dict == {}


def test_make_where_sql_col_one():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55)
    ]

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == "WHERE test=%(old_test)s"
    assert param_dict == {"old_test": 55}


def test_make_where_sql_col_one_or():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55)
    ]

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == "WHERE test=%(old_test)s"
    assert param_dict == {"old_test": 55}


def test_make_where_sql_col_multiple():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55),
        SqlParam(param_key="old_test_2", col_name="test2", value="string"),
    ]

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == "WHERE test=%(old_test)s AND test2=%(old_test_2)s"
    assert param_dict == {"old_test": 55, "old_test_2": "string"}


def test_make_where_sql_col_multiple_or():
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55),
        SqlParam(param_key="old_test_2", col_name="test2", value="string"),
    ]

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == "WHERE test=%(old_test)s OR test2=%(old_test_2)s"
    assert param_dict == {"old_test": 55, "old_test_2": "string"}


def test_make_where_sql_empty():
    """ """
    where_dict: Dict[str, Any] = {}

    result: str = make_where_sql(where_dict, "AND")
    assert result == ""


def test_make_where_sql_one():
    """ """
    where_dict: Dict[str, Any] = {"test": 55}

    result: str = make_where_sql(where_dict, "AND")
    assert result == "WHERE test=%(test)s"


def test_make_where_sql_multiple():
    """ """
    where_dict: Dict[str, Any] = {"test": 55, "test2": "string"}

    result: str = make_where_sql(where_dict, "AND")
    assert result == "WHERE test=%(test)s AND test2=%(test2)s"


def test_make_update_sql_empty():
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = []
    where_args: List[SqlParam] = []

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert result == ""
    assert param_dict == {}


def test_make_update_sql_one():
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value", param_key="new_column1")
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="oldvalue", param_key="column1")
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result
        == "UPDATE my_schema.table SET column1=%(new_column1)s WHERE column1=%(column1)s"
    )
    assert param_dict == {"column1": "oldvalue", "new_column1": "value"}


def test_make_update_sql_multiple():
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value", param_key="new_column1"),
        SqlParam(col_name="column2", value=55),
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="oldvalue", param_key="old_column1")
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result
        == "UPDATE my_schema.table SET column1=%(new_column1)s, column2=%(column2)s WHERE column1=%(old_column1)s"
    )
    assert param_dict == {
        "old_column1": "oldvalue",
        "new_column1": "value",
        "column2": 55,
    }


def test_make_update_sql_no_where():
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value"),
        SqlParam(col_name="column2", value=55),
    ]
    where_args: List[SqlParam] = []

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result == "UPDATE my_schema.table SET column1=%(column1)s, column2=%(column2)s"
    )
    assert param_dict == {"column1": "value", "column2": 55}
