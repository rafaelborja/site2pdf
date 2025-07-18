import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import site2pdf


def get_is_valid_link():
    src = inspect.getsource(site2pdf)
    module_ast = ast.parse(src)
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'main':
            for inner in node.body:
                if isinstance(inner, ast.FunctionDef) and inner.name == 'is_valid_link':
                    # Build a module from inner function
                    fn_ast = ast.Module(body=[inner], type_ignores=[])
                    compiled = compile(fn_ast, filename="<ast>", mode="exec")
                    ns = {}
                    exec(compiled, ns)
                    return ns['is_valid_link']
    raise RuntimeError('is_valid_link not found')


is_valid_link = get_is_valid_link()


def test_anchor_link_is_invalid():
    assert is_valid_link('#section') is False


def test_mailto_link_is_invalid():
    assert is_valid_link('mailto:test@example.com') is False


def test_http_link_is_valid():
    assert is_valid_link('https://example.com/page') is True
