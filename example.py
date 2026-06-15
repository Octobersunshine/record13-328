from bisection_root_finder import find_root


def main():
    print("二分法求根服务使用示例")
    print("=" * 50)
    
    examples = [
        ("x**2 - 2", 1.0, 2.0),
        ("cos(x) - x", 0.0, 1.0),
        ("exp(x) - 3*x", 0.0, 1.0),
    ]
    
    for expr, a, b in examples:
        print(f"\n求解方程: {expr} = 0")
        print(f"搜索区间: [{a}, {b}]")
        try:
            result = find_root(expr, a, b, tol=1e-8)
            print(f"  近似根: {result['root']:.10f}")
            print(f"  f(根) = {result['function_value']:.2e}")
            print(f"  迭代次数: {result['iterations']}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "=" * 50)
    print("自定义输入示例:")
    expr = input("请输入函数表达式（用 x 作为变量）: ").strip()
    a = float(input("请输入区间左端点: "))
    b = float(input("请输入区间右端点: "))
    
    try:
        result = find_root(expr, a, b)
        print(f"\n结果:")
        print(f"  根 = {result['root']:.10f}")
        print(f"  f(根) = {result['function_value']:.2e}")
        print(f"  迭代次数 = {result['iterations']}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
