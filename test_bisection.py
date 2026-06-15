from bisection_root_finder import find_root, bisection_method, parse_expression
import math


def run_test(name, expr, a, b, expected_root=None, tol=1e-6):
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"表达式: {expr}")
    print(f"区间: [{a}, {b}]")
    print(f"{'-'*60}")
    try:
        result = find_root(expr, a, b, tol=tol)
        print(f"近似根: {result['root']:.10f}")
        print(f"函数值: {result['function_value']:.2e}")
        print(f"迭代次数: {result['iterations']}")
        print(f"容差: {result['tolerance']}")
        
        if expected_root is not None:
            error = abs(result['root'] - expected_root)
            print(f"与预期根的误差: {error:.2e}")
            if error < tol * 10:
                print("✓ 测试通过")
            else:
                print("✗ 测试失败：误差超出容差范围")
        else:
            if abs(result['function_value']) < tol * 10:
                print("✓ 测试通过")
            else:
                print("✗ 测试失败：函数值未收敛到0")
    except Exception as e:
        print(f"✗ 发生错误: {e}")


def test_polynomial():
    print("\n" + "="*60)
    print("一、多项式方程测试")
    print("="*60)
    
    run_test(
        "二次方程 x² - 2 = 0 (求√2)",
        "x**2 - 2",
        1.0, 2.0,
        expected_root=math.sqrt(2)
    )
    
    run_test(
        "三次方程 x³ - x - 2 = 0",
        "x**3 - x - 2",
        1.0, 2.0,
        expected_root=1.5213797068045676
    )
    
    run_test(
        "五次多项式 x⁵ - x⁴ + 2x³ - x² + x - 3 = 0",
        "x**5 - x**4 + 2*x**3 - x**2 + x - 3",
        0.0, 2.0
    )


def test_transcendental():
    print("\n" + "="*60)
    print("二、超越方程测试")
    print("="*60)
    
    run_test(
        "三角方程 cos(x) - x = 0",
        "cos(x) - x",
        0.0, 1.0,
        expected_root=0.7390851332151607
    )
    
    run_test(
        "指数方程 exp(x) - x² = 0",
        "exp(x) - x**2",
        -1.0, 0.0,
        expected_root=-0.7034674224983917
    )
    
    run_test(
        "对数方程 log(x) - 1 = 0 (求 e)",
        "log(x) - 1",
        1.0, 4.0,
        expected_root=math.e
    )


def test_special_functions():
    print("\n" + "="*60)
    print("三、特殊函数测试")
    print("="*60)
    
    run_test(
        "sqrt(x) - 2 = 0",
        "sqrt(x) - 2",
        1.0, 9.0,
        expected_root=4.0
    )
    
    run_test(
        "sin(x) = 0 (求 π)",
        "sin(x)",
        2.0, 4.0,
        expected_root=math.pi
    )
    
    run_test(
        "tan(x) = 0 (求 π)",
        "tan(x)",
        2.0, 4.0,
        expected_root=math.pi
    )


def test_edge_cases():
    print("\n" + "="*60)
    print("四、边界情况与错误处理测试")
    print("="*60)
    
    print("\n测试1: 端点恰好是根")
    try:
        f = parse_expression("x**2 - 4")
        root, iters = bisection_method(f, -2.0, 1.0)
        print(f"区间 [-2, 1]，f(-2)=0，直接返回根: {root}，迭代次数: {iters}")
        print("✓ 测试通过")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n测试2: 区间端点函数值同号，但根存在（应自动扩展区间）")
    try:
        result = find_root("x**2 - 2", 1.0, 1.5, tol=1e-6)
        error = abs(result['root'] - math.sqrt(2))
        if error < 1e-5:
            print(f"✓ 自动扩展区间成功，根: {result['root']:.10f}，误差: {error:.2e}")
        else:
            print(f"✗ 自动扩展区间后误差过大: {error:.2e}")
    except Exception as e:
        print(f"✗ 自动扩展区间失败: {e}")

    print("\n测试3: 区间端点同号且无实数根（x²+1 永远为正，应抛出错误）")
    try:
        result = find_root("x**2 + 1", -1.0, 1.0)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        short_msg = str(e)[:80]
        print(f"✓ 正确抛出错误（含换区间提示）: {short_msg}...")
    
    print("\n测试4: 无效的表达式语法")
    try:
        result = find_root("x**2 + ", 0, 1)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试5: 未知函数")
    try:
        result = find_root("foo(x) - 1", 0, 1)
        print("✗ 测试失败：应该抛出错误但没有")
    except NameError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试6: 无效区间 (a >= b)")
    try:
        result = find_root("x**2 - 2", 2.0, 1.0)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试7: 使用 pi 和 e 常量")
    run_test(
        "x - pi = 0",
        "x - pi",
        3.0, 4.0,
        expected_root=math.pi
    )
    
    run_test(
        "x - e = 0",
        "x - e",
        2.0, 3.0,
        expected_root=math.e
    )


def test_auto_expand():
    print("\n" + "="*60)
    print("六、同号区间自动扩展测试")
    print("="*60)

    print("\n测试1: 初始区间完全在根的一侧（x²-2，区间 [1.0, 1.5]）")
    try:
        result = find_root("x**2 - 2", 1.0, 1.5, tol=1e-8)
        error = abs(result['root'] - math.sqrt(2))
        status = "✓" if error < 1e-6 else "✗"
        print(f"  {status} 自动扩展成功，根: {result['root']:.10f}，误差: {error:.2e}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    print("\n测试2: 初始区间在根的负半侧（x²-2，区间 [-3, -1.5]）")
    try:
        result = find_root("x**2 - 2", -3.0, -1.5, tol=1e-8)
        error = abs(result['root'] - (-math.sqrt(2)))
        status = "✓" if error < 1e-6 else "✗"
        print(f"  {status} 自动扩展成功，根: {result['root']:.10f}，误差: {error:.2e}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    print("\n测试3: sin(x) 区间 [0.5, 1.0]，同号，自动扩展会找到 x≈0 的根")
    try:
        result = find_root("sin(x)", 0.5, 1.0, tol=1e-8)
        if abs(result['function_value']) < 1e-6:
            print(f"  ✓ 自动扩展成功，找到根: {result['root']:.10f}（f(root)≈0）")
        else:
            print(f"  ✗ 自动扩展后函数值未收敛: f({result['root']})={result['function_value']:.2e}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    print("\n测试4: 禁用自动扩展（auto_expand=False），同号区间应报错")
    try:
        result = find_root("x**2 - 2", 1.5, 2.0, auto_expand=False)
        print(f"  ✗ 应该抛出错误但没有，根: {result['root']}")
    except ValueError as e:
        has_hint = "更换搜索区间" in str(e) or "auto_expand" in str(e)
        status = "✓" if has_hint else "✗"
        print(f"  {status} 正确抛出含换区间提示的错误")

    print("\n测试5: 无实数根的方程（x²+1，自动扩展也应失败）")
    try:
        result = find_root("x**2 + 1", -1.0, 1.0)
        print(f"  ✗ 应该抛出错误但没有")
    except ValueError as e:
        has_hint = "更换搜索区间" in str(e) or "扩展区间失败" in str(e)
        status = "✓" if has_hint else "✗"
        print(f"  {status} 正确抛出含换区间提示的错误")

    print("\n测试6: cos(x) - x 区间 [0.1, 0.3]，同号但根在 0.739")
    try:
        result = find_root("cos(x) - x", 0.1, 0.3, tol=1e-8)
        error = abs(result['root'] - 0.7390851332151607)
        status = "✓" if error < 1e-6 else "✗"
        print(f"  {status} 自动扩展成功，根: {result['root']:.10f}，误差: {error:.2e}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")


def test_tolerance():
    print("\n" + "="*60)
    print("五、不同容差精度测试")
    print("="*60)
    
    expr = "x**2 - 2"
    a, b = 1.0, 2.0
    expected = math.sqrt(2)
    
    for tol in [1e-2, 1e-4, 1e-6, 1e-10]:
        print(f"\n容差 = {tol}:")
        try:
            result = find_root(expr, a, b, tol=tol)
            error = abs(result['root'] - expected)
            print(f"  根: {result['root']:.12f}")
            print(f"  迭代次数: {result['iterations']}")
            print(f"  实际误差: {error:.2e}")
            if error < tol * 10:
                print(f"  ✓ 误差满足要求")
            else:
                print(f"  ✗ 误差不满足要求")
        except Exception as e:
            print(f"  ✗ 错误: {e}")


def main():
    print("="*60)
    print("二分法求根服务 - 综合测试")
    print("="*60)
    
    test_polynomial()
    test_transcendental()
    test_special_functions()
    test_edge_cases()
    test_auto_expand()
    test_tolerance()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    main()
