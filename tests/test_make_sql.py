from typing import Any, Dict, List

from make_sql import make_where_sql_col, make_where_sql, make_update_sql, SqlParam


def test_make_where_sql_col_empty_and() -> None:
    """
    test the make_where_sql_col function with no parameters and the 'AND' operator
    """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = []

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == ""
    assert param_dict == {}


def test_make_where_sql_col_empty_or() -> None:
    """
    test the make_where_sql_col function with no parameters and the 'OR' operator
    """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = []

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == ""
    assert param_dict == {}


def test_make_where_sql_col_one() -> None:
    """
    test the make_where_sql_col with a single expression and the 'AND' operator
    """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55)
    ]

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == "WHERE test=%(old_test)s"
    assert param_dict == {"old_test": 55}


def test_make_where_sql_col_one_or() -> None:
    """
    test make_where_sql_col with a single expression and the 'OR' operator
    """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55)
    ]

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == "WHERE test=%(old_test)s"
    assert param_dict == {"old_test": 55}


def test_make_where_sql_col_multiple() -> None:
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55),
        SqlParam(param_key="old_test_2", col_name="test2", value="string"),
    ]

    result: str = make_where_sql_col(param_dict, where_args, "AND")
    assert result == "WHERE test=%(old_test)s AND test2=%(old_test_2)s"
    assert param_dict == {"old_test": 55, "old_test_2": "string"}


def test_make_where_sql_col_multiple_or() -> None:
    """ """
    param_dict: Dict[str, Any] = {}
    where_args: List[SqlParam] = [
        SqlParam(param_key="old_test", col_name="test", value=55),
        SqlParam(param_key="old_test_2", col_name="test2", value="string"),
    ]

    result: str = make_where_sql_col(param_dict, where_args, "OR")
    assert result == "WHERE test=%(old_test)s OR test2=%(old_test_2)s"
    assert param_dict == {"old_test": 55, "old_test_2": "string"}


def test_make_where_sql_empty() -> None:
    """ """
    where_dict: Dict[str, Any] = {}

    result: str = make_where_sql(where_dict, "AND")
    assert result == ""


def test_make_where_sql_one() -> None:
    """ """
    where_dict: Dict[str, Any] = {"test": 55}

    result: str = make_where_sql(where_dict, "AND")
    assert result == "WHERE test=%(test)s"


def test_make_where_sql_multiple() -> None:
    """ """
    where_dict: Dict[str, Any] = {"test": 55, "test2": "string"}

    result: str = make_where_sql(where_dict, "AND")
    assert result == "WHERE test=%(test)s AND test2=%(test2)s"


def test_make_update_sql_empty() -> None:
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = []
    where_args: List[SqlParam] = []

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert result == ""
    assert param_dict == {}


def test_make_update_sql_one() -> None:
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


def test_make_update_sql_multiple() -> None:
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


def test_make_update_sql_none_args() -> None:
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value", param_key="new_column1"),
        SqlParam(col_name="column2", value=None),
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="oldvalue", param_key="old_column1")
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result
        == "UPDATE my_schema.table SET column1=%(new_column1)s WHERE column1=%(old_column1)s"
    )
    assert param_dict == {"old_column1": "oldvalue", "new_column1": "value"}


def test_make_update_sql_mixed_none_args() -> None:
    """ """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value", param_key="new_column1"),
        SqlParam(col_name="column2", value=None),
        SqlParam(col_name="column3", value=32),
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="oldvalue", param_key="old_column1")
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result
        == "UPDATE my_schema.table SET column1=%(new_column1)s, column3=%(column3)s WHERE column1=%(old_column1)s"
    )
    assert param_dict == {
        "old_column1": "oldvalue",
        "new_column1": "value",
        "column3": 32,
    }


def test_make_update_sql_no_where() -> None:
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


def test_make_update_sql_no_where_nones() -> None:
    """
    Test make_update_sql when there are where entries, but they are all none
    """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value"),
        SqlParam(col_name="column2", value=55),
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value=None, param_key="old_column1")
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result == "UPDATE my_schema.table SET column1=%(column1)s, column2=%(column2)s"
    )
    assert param_dict == {"column1": "value", "column2": 55}


def test_make_update_sql_where_mixed_nones() -> None:
    """
    Test make_update_sql when there are where entries, but some are none
    """
    param_dict: Dict[str, Any] = {}
    update_args: List[SqlParam] = [
        SqlParam(col_name="column1", value="value"),
        SqlParam(col_name="column2", value=55),
    ]
    where_args: List[SqlParam] = [
        SqlParam(col_name="column1", value=None, param_key="old_column1"),
        SqlParam(col_name="column2", value=56, param_key="old_column2"),
        SqlParam(col_name="column3", value=None, param_key="old_column3"),
    ]

    result: str = make_update_sql(
        param_dict, "my_schema.table", update_args, where_args, "AND"
    )
    assert (
        result
        == "UPDATE my_schema.table SET column1=%(column1)s, column2=%(column2)s WHERE column2=%(old_column2)s"
    )
    assert param_dict == {"column1": "value", "column2": 55, "old_column2": 56}
