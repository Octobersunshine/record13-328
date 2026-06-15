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
    
    print("\n测试2: 区间端点函数值同号（应抛出错误）")
    try:
        result = find_root("x**2 + 1", -1.0, 1.0)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试3: 无效的表达式语法")
    try:
        result = find_root("x**2 + ", 0, 1)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试4: 未知函数")
    try:
        result = find_root("foo(x) - 1", 0, 1)
        print("✗ 测试失败：应该抛出错误但没有")
    except NameError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试5: 无效区间 (a >= b)")
    try:
        result = find_root("x**2 - 2", 2.0, 1.0)
        print("✗ 测试失败：应该抛出错误但没有")
    except ValueError as e:
        print(f"✓ 正确抛出错误: {e}")
    
    print("\n测试6: 使用 pi 和 e 常量")
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
    test_tolerance()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    main()
