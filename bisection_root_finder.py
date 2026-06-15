import ast
import math
import operator


SAFE_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'exp': math.exp,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
    'sqrt': math.sqrt,
    'abs': abs,
    'pow': math.pow,
    'e': math.e,
    'pi': math.pi,
}

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node, variables):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        if node.id in SAFE_FUNCTIONS:
            return SAFE_FUNCTIONS[node.id]
        raise NameError(f"未知的变量或函数: {node.id}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"不支持的运算符: {op_type.__name__}")
        return SAFE_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, variables)
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"不支持的运算符: {op_type.__name__}")
        return SAFE_OPERATORS[op_type](operand)
    if isinstance(node, ast.Call):
        func = _eval_node(node.func, variables)
        args = [_eval_node(arg, variables) for arg in node.args]
        return func(*args)
    raise ValueError(f"不支持的表达式节点: {type(node).__name__}")


def parse_expression(expr_str):
    try:
        tree = ast.parse(expr_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"表达式语法错误: {e}") from e

    def evaluate(x):
        return _eval_node(tree.body, {'x': x})

    return evaluate


def bisection_method(f, a, b, tol=1e-6, max_iter=100):
    if tol <= 0:
        raise ValueError("容差必须大于0")
    if max_iter <= 0:
        raise ValueError("最大迭代次数必须大于0")
    if a >= b:
        raise ValueError("区间左端点必须小于右端点")

    fa = f(a)
    fb = f(b)

    if math.isnan(fa) or math.isinf(fa):
        raise ValueError(f"函数在左端点 {a} 处无定义或为无穷大")
    if math.isnan(fb) or math.isinf(fb):
        raise ValueError(f"函数在右端点 {b} 处无定义或为无穷大")

    if fa * fb > 0:
        raise ValueError(
            f"区间端点函数值同号: f({a})={fa:.6f}, f({b})={fb:.6f}。"
            "二分法要求区间两端点函数值异号以保证至少有一个根存在。"
        )

    if abs(fa) < tol:
        return a, 0
    if abs(fb) < tol:
        return b, 0

    for i in range(1, max_iter + 1):
        p = (a + b) / 2.0
        fp = f(p)

        if math.isnan(fp) or math.isinf(fp):
            raise ValueError(f"函数在中点 {p} 处无定义或为无穷大")

        if abs(fp) < tol or (b - a) / 2.0 < tol:
            return p, i

        if fa * fp > 0:
            a = p
            fa = fp
        else:
            b = p
            fb = fp

    raise RuntimeError(f"达到最大迭代次数 {max_iter} 仍未收敛")


def find_root(expr_str, a, b, tol=1e-6, max_iter=100):
    f = parse_expression(expr_str)
    root, iterations = bisection_method(f, a, b, tol, max_iter)
    return {
        'root': root,
        'function_value': f(root),
        'iterations': iterations,
        'tolerance': tol,
        'interval': [a, b],
        'expression': expr_str
    }
