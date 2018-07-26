import importlib
import json
import re
import logging
logger = logging.getLogger("utils")

PATTERN_NUMERIC = re.compile(r"[+-]?\d+\.?\d*")
PATTERN_STRING_SINGLE = re.compile(r"'([^']|\\')*'")
PATTERN_STRING_DOUBLE = re.compile(r'"([^"]|\\")*"')
PATTERN_IDENT = re.compile(r"[^\d\W]\w*")
LITERAL_KW_LIST = {
    "None": None,
    "True": True,
    "False": False
}


def parse_module_string(module_string):
    """
    Parse module string (from neuron.settings)
    into module name and class name
    """
    module_name, class_name = module_string.rsplit('.', 1)
    return "neuron.modules." + module_name, class_name


def get_class(module_string):
    module_name, class_name = parse_module_string(module_string)
    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)


def construct_event_json(event, data):
    """
    Helper function to construct a payload for sending to clients
    """
    return json.dumps([event, data], ensure_ascii=False).encode('utf8')


def parse_expr(expr):
    """
    Helper function to match the full string as a python expression
    :param expr:
    :return: The python expression represented by the string
    :raises ValueError: If no match can be found
    """
    if expr:
        logger.debug("Expr: " + str(expr) + " -> " + str(type(expr)))
    else:
        logger.debug("Expr: None")
    res, remainder = match_expr(expr)
    logger.debug(res)
    logger.debug("Remaining: " + remainder)
    if remainder:
        raise ValueError("Invalid expression!")
    else:
        return res


def match_expr(expr):
    """
    :param expr: The expression string
    :return: The python expression matched at the beginning of the given string, and the remaining unmatched portion
    :raises ValueError: If no match found
    """
    if not expr:
        return None, ""
    elif expr[0].isalpha():
        try:
            return match_ident(expr)
        except ValueError:
            return match_string_expr(expr)
    elif expr[0] == "'" or expr[0] == '"':
        return match_string_expr(expr)
    elif expr[0] == "(" or expr[0] == "[":
        return match_tuple_and_list_expr(expr, expr[0] == "[")
    else:
        return match_numeric_expr(expr)


def match_numeric_expr(expr):
    """ Matches ints and floats """
    match = PATTERN_NUMERIC.match(expr)
    if not match:
        raise ValueError("Invalid expression!")
    else:
        remaining = expr[match.span()[1]:]
        try:
            return float(match.group(0)), remaining
        except ValueError:
            return int(match.group(0)), remaining


def match_string_expr(expr):
    """ Matches strings enclosed by single or double quotes """
    if expr[0] == "'":
        match = PATTERN_STRING_SINGLE.match(expr)
    else:
        match = PATTERN_STRING_DOUBLE.match(expr)

    if not match:
        raise ValueError("Invalid expression!")
    else:
        # Since it's already a python string, just strip the quotes
        return match.group(0)[1:-1], expr[match.span()[1]:]


def match_tuple_and_list_expr(expr, is_list):
    """ Matches a tuple/list of expressions, comma separated and enclosed by round brackets"""
    terminating_char = "]" if is_list else ")"
    child_list = []
    # Strip the leading open bracket
    expr = expr[1:].lstrip()
    while expr and expr[0] != terminating_char:
        child, expr = match_expr(expr)
        child_list.append(child)
        expr = expr.lstrip()
        if expr[0] == ",":
            expr = expr[1:].lstrip()
        elif expr[0] != terminating_char:
            raise ValueError("Invalid expression!")

    if not expr:
        raise ValueError("Invalid expression!")
    else:
        return tuple(child_list), expr[1:].lstrip()


def match_ident(expr):
    match = PATTERN_IDENT.match(expr)
    remaining = expr[match.span()[1]:]
    try:
        return LITERAL_KW_LIST[match.group(0)], remaining
    except KeyError:
        raise ValueError("Invalid expression!")
