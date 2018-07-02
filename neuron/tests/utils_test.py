def test_parse_expr():
    assert utils.parse_expr("(1,)") == (1,)
    assert utils.parse_expr("1") == 1
    assert utils.parse_expr("+1") == 1
    assert utils.parse_expr("-5") == -5
    assert utils.parse_expr("+100") == 100
    assert utils.parse_expr("-500") == -500
    assert utils.parse_expr("101") == 101
    assert utils.parse_expr("101.5") == 101.5
    assert utils.parse_expr("+101.") == 101.0
    assert utils.parse_expr("\"lorem ipsum\"") == "lorem ipsum"
    assert utils.parse_expr("\"123\"") == "123"
    assert utils.parse_expr("(101.5, +152, -3, 'dolor', -3.14159)") == (101.5, 152, -3, "dolor", -3.14159)
    assert utils.parse_expr("((1,), +152, -3, 'dolor', -3.14159, (121, \"sit\"))") == ((1,), +152, -3, 'dolor', -3.14159, (121, "sit"))
    assert utils.parse_expr("(None, 'lorem', True, False)") == (None, "lorem", True, False)
