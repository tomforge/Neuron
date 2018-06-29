RE_IDENT = r"^[^\d\W]\w*\Z"
RE_INT = r"^(\+|-)?\d+\Z"
RE_FLOAT = r"^(\+|-)?\d+.?\d*\Z"
RE_STRING_SINGLE = r"""^'([^']|\\')*'\Z"""
RE_STRING_DOUBLE = r"""^"([^"]|\\")*"\Z"""

def enclosedBy(str, charBegin, charEnd=None):
    if charEnd is None:
        charEnd = charBegin
    return len(str) > 1 and str.startswith(char) and str.endswith(char)

def parseExpr(expr):
    """
    Parses the given expression string.
    Accepts:
        1. null
        2. strings
        3. tuple
        4. function (or call)
        5. int
        6. float
    """
    expr = expr.strip()
    if not expr:
        return null
    elif enclosedBy(expr, "'") or enclosedBy(expr, '"'):
        return expr[1:-1]
    elif enclosedBy(expr, "(", ")"):
        return parseTupleExpr(expr[1:-1])
    elif expr[0].isalpha():
        return parseFuncExpr(expr)
    else:
        try:
            return int(expr)
        except ValueError:
            try:
                return float(expr)
            except ValueError:
               raise ValueError("Invalid expression!") 
                
def parseFuncExpr(expr):
    openBracket = expr.find("(")
    funcName = expr if openBracket == -1 else expr[:openBracket]
    if funcName not in funcList:
        raise ValueError("Unsupported function")
    else:
        func = funcList[funcName]

    if openBracket == -1:
        return func

    funcArgs = expr[openBracket:]
    if funcArgs.endswith(")"):
        argList = parseTupleExpr(funcArgs[1:-1])

    raise ValueError("Invalid expressions!")
        

def parseTupleExpr(expr):
    pass
