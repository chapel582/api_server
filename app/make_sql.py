from typing import Any, Dict, List, Literal, Optional

BOOL_OPERATOR = Literal["AND", "OR"]


class SqlParam:
    param_key: str
    col_name: str
    value: Any

    def __init__(self, col_name: str, value: Any, param_key: Optional[str] = None):
        self.col_name = col_name
        self.value = value
        if param_key is None:
            self.param_key = self.col_name
        else:
            self.param_key = param_key


def make_where_sql_col(
    param_dict: Dict[str, Any],
    where_args: List[SqlParam],
    where_operator: BOOL_OPERATOR,
) -> str:
    """
    make a where expression for sql

    param_dict:
    The mutable param_dict that will be passed into the db 'run' function

    where_args:
    the column, value pairs for the expressions

    where_operator:
    the boolean operator between the expressions

    returns:
    string of the where expression
    """
    result = ""
    if len(where_args) > 0:
        # NOTE: remove None valued where args first
        valid_where_args: List[SqlParam] = []
        for arg in where_args:
            if not (arg.value is None):
                valid_where_args.append(arg)
                param_dict[arg.param_key] = arg.value

        if len(valid_where_args) > 0:
            result += "WHERE "
            for index in range(len(valid_where_args) - 1):
                arg = valid_where_args[index]
                result += f"{arg.col_name}=%({arg.param_key})s {where_operator} "
            arg = valid_where_args[-1]
            result += f"{arg.col_name}=%({arg.param_key})s"

    return result


def make_where_sql(where_dict: Dict[str, Any], where_operator: BOOL_OPERATOR):
    """ """
    where_args: List[SqlParam] = []
    for key, value in where_dict.items():
        where_args.append(SqlParam(param_key=key, col_name=key, value=value))
    return make_where_sql_col({}, where_args, where_operator)


def make_update_sql(
    param_dict: Dict[str, Any],
    table_name: str,
    update_args: List[SqlParam],
    where_args: List[SqlParam],
    where_operator: BOOL_OPERATOR,
) -> str:
    """
    param_dict:
    table_name:
    update_args:
    where_args:
    where_operator:
    returns:
    """
    result: str = ""
    if len(update_args) > 0:
        # NOTE: remove the None valued where args first so we don't prepend string unnecessarily
        valid_update_args: List[SqlParam] = []
        for arg in update_args:
            if not (arg.value is None):
                valid_update_args.append(arg)
                param_dict[arg.param_key] = arg.value

        if len(valid_update_args) > 0:
            result += f"UPDATE {table_name} SET "

            for index in range(len(valid_update_args) - 1):
                arg = valid_update_args[index]
                result += f"{arg.col_name}=%({arg.param_key})s, "
            arg = valid_update_args[-1]
            result += f"{arg.col_name}=%({arg.param_key})s"

            if len(where_args) > 0:
                where_string: str = make_where_sql_col(
                    param_dict, where_args, where_operator
                )
                if len(where_string) != 0:
                    result += " " + where_string

    return result
