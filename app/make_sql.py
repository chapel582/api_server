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
    """ """
    result = ""
    if len(where_args) > 0:
        result += "WHERE "
        for index in range(len(where_args) - 1):
            arg = where_args[index]
            if not (arg.value is None):
                result += f"{arg.col_name}=%({arg.param_key})s {where_operator} "
                param_dict[arg.param_key] = arg.value

        arg = where_args[len(where_args) - 1]
        result += f"{arg.col_name}=%({arg.param_key})s"
        param_dict[arg.param_key] = arg.value

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
    """ """
    result: str = ""
    if len(update_args) > 0:
        result += f"UPDATE {table_name} SET "

        for index in range(len(update_args) - 1):
            arg = update_args[index]
            if not (arg.value is None):
                result += f"{arg.col_name}=%({arg.param_key})s, "
                param_dict[arg.param_key] = arg.value

        arg = update_args[len(update_args) - 1]
        result += f"{arg.col_name}=%({arg.param_key})s"
        param_dict[arg.param_key] = arg.value

        if len(where_args) > 0:
            result += " "
            result += make_where_sql_col(param_dict, where_args, where_operator)

    return result
