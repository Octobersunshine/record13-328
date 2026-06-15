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


def _try_expand_interval(f, a, b, max_expand_steps=50, expand_factor=2.0):
    fa = f(a)
    fb = f(b)

    if fa * fb <= 0:
        return a, b, fa, fb

    width = b - a
    center = (a + b) / 2.0

    for step in range(1, max_expand_steps + 1):
        new_half = width * (expand_factor ** step) / 2.0
        new_a = center - new_half
        new_b = center + new_half

        new_fa = f(new_a)
        new_fb = f(new_b)

        if math.isnan(new_fa) or math.isinf(new_fa):
            continue
        if math.isnan(new_fb) or math.isinf(new_fb):
            continue

        if new_fa * fb <= 0:
            return new_a, b, new_fa, fb
        if fa * new_fb <= 0:
            return a, new_b, fa, new_fb
        if new_fa * new_fb <= 0:
            return new_a, new_b, new_fa, new_fb

    return None, None, fa, fb


def bisection_method(f, a, b, tol=1e-6, max_iter=100, auto_expand=True, max_expand_steps=50):
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
        if auto_expand:
            orig_a, orig_b = a, b
            new_a, new_b, new_fa, new_fb = _try_expand_interval(
                f, a, b, max_expand_steps
            )
            if new_a is not None:
                a, b = new_a, new_b
                fa, fb = new_fa, new_fb
            else:
                expand_radius = (orig_b - orig_a) * (2 ** max_expand_steps - 1) / 2
                expanded_a = orig_a - expand_radius
                expanded_b = orig_b + expand_radius
                raise ValueError(
                    f"区间端点函数值同号且自动扩展区间失败: "
                    f"原始区间 f({orig_a})={fa:.6f}, f({orig_b})={fb:.6f}。"
                    f"已尝试将区间扩展至 [{expanded_a:.2f}, {expanded_b:.2f}] 仍未找到异号区间。"
                    f"请尝试以下方法：\n"
                    f"  1. 手动更换搜索区间，确保 f(a) 与 f(b) 异号\n"
                    f"  2. 先绘制函数图像观察根的大致位置\n"
                    f"  3. 增大 max_expand_steps 参数以允许更大幅度的区间扩展"
                )
        else:
            raise ValueError(
                f"区间端点函数值同号: f({a})={fa:.6f}, f({b})={fb:.6f}。"
                f"二分法要求区间两端点函数值异号以保证至少有一个根存在。"
                f"请尝试更换搜索区间，或设置 auto_expand=True 自动扩展区间。"
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


def _numerical_derivative(f, x, h=None):
    if h is None:
        h = 1e-6 * max(1.0, abs(x))
    xph = x + h
    xmh = x - h
    denom = xph - xmh
    if denom == 0.0:
        h = 1e-6
        xph = x + h
        xmh = x - h
        denom = 2.0 * h
    return (f(xph) - f(xmh)) / denom


def newton_method(f, x0, tol=1e-6, max_iter=100, fallback_to_bisection=True, a=None, b=None):
    if tol <= 0:
        raise ValueError("容差必须大于0")
    if max_iter <= 0:
        raise ValueError("最大迭代次数必须大于0")

    x = float(x0)
    fx = f(x)

    if math.isnan(fx) or math.isinf(fx):
        raise ValueError(f"函数在初始点 {x0} 处无定义或为无穷大")

    if abs(fx) < tol:
        return x, 0

    for i in range(1, max_iter + 1):
        dfx = _numerical_derivative(f, x)

        if math.isnan(dfx) or math.isinf(dfx) or dfx == 0.0:
            if fallback_to_bisection and a is not None and b is not None:
                fa = f(a)
                fb = f(b)
                if fa * fb <= 0:
                    return bisection_method(f, a, b, tol, max_iter)
            raise ZeroDivisionError(
                f"在 x={x:.10f} 处导数为0或无定义（f'={dfx:.2e}），牛顿法无法继续迭代。"
                "请尝试更换初始值或使用二分法。"
            )

        x_next = x - fx / dfx

        if math.isnan(x_next) or math.isinf(x_next):
            if fallback_to_bisection and a is not None and b is not None:
                fa = f(a)
                fb = f(b)
                if fa * fb <= 0:
                    return bisection_method(f, a, b, tol, max_iter)
            raise RuntimeError(
                f"迭代值发散（x={x:.10f}, x_next={x_next}）。请更换初始值或使用二分法。"
            )

        fx_next = f(x_next)

        if math.isnan(fx_next) or math.isinf(fx_next):
            if fallback_to_bisection and a is not None and b is not None:
                fa = f(a)
                fb = f(b)
                if fa * fb <= 0:
                    return bisection_method(f, a, b, tol, max_iter)
            raise ValueError(f"函数在 x={x_next:.10f} 处无定义或为无穷大")

        if abs(fx_next) < tol or abs(x_next - x) < tol:
            return x_next, i

        x = x_next
        fx = fx_next

    if fallback_to_bisection and a is not None and b is not None:
        fa = f(a)
        fb = f(b)
        if fa * fb <= 0:
            return bisection_method(f, a, b, tol, max_iter)

    raise RuntimeError(f"达到最大迭代次数 {max_iter} 仍未收敛")


def find_root(expr_str, a, b, tol=1e-6, max_iter=100, auto_expand=True, max_expand_steps=50, method='bisection'):
    f = parse_expression(expr_str)
    method_lower = method.lower()

    if method_lower == 'bisection':
        root, iterations = bisection_method(f, a, b, tol, max_iter, auto_expand, max_expand_steps)
        return {
            'root': root,
            'function_value': f(root),
            'iterations': iterations,
            'tolerance': tol,
            'interval': [a, b],
            'expression': expr_str,
            'method': 'bisection'
        }
    elif method_lower == 'newton':
        if a >= b:
            raise ValueError("区间左端点必须小于右端点")
        fa = f(a)
        fb = f(b)

        if fa * fb > 0:
            if auto_expand:
                orig_a, orig_b = a, b
                new_a, new_b, new_fa, new_fb = _try_expand_interval(
                    f, a, b, max_expand_steps
                )
                if new_a is not None:
                    a, b = new_a, new_b
                    fa, fb = new_fa, new_fb
                else:
                    raise ValueError(
                        f"区间端点函数值同号: f({orig_a})={fa:.6f}, f({orig_b})={fb:.6f}。"
                        f"牛顿法也需要一个包含根的初始区间。请更换搜索区间。"
                    )

        if abs(fa) < abs(fb):
            x0 = a
        else:
            x0 = b
        if abs(fa) > tol and abs(fb) > tol:
            x0 = (a + b) / 2.0

        root, iterations = newton_method(f, x0, tol, max_iter,
                                         fallback_to_bisection=True, a=a, b=b)
        return {
            'root': root,
            'function_value': f(root),
            'iterations': iterations,
            'tolerance': tol,
            'interval': [a, b],
            'expression': expr_str,
            'method': 'newton'
        }
    else:
        raise ValueError(
            f"未知的方法 '{method}'。支持的方法: 'bisection'（二分法）, 'newton'（牛顿法）。"
        )
