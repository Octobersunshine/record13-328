from bisection_root_finder import find_root


def main():
    print("二分法 & 牛顿法求根服务使用示例")
    print("=" * 60)
    
    examples = [
        ("x**2 - 2", 1.0, 2.0),
        ("cos(x) - x", 0.0, 1.0),
        ("exp(x) - 3*x", 0.0, 1.0),
    ]
    
    for expr, a, b in examples:
        print(f"\n求解方程: {expr} = 0")
        print(f"搜索区间: [{a}, {b}]")
        
        try:
            res_bis = find_root(expr, a, b, method='bisection', tol=1e-10)
            res_new = find_root(expr, a, b, method='newton', tol=1e-10)
            print(f"  [二分法] 根={res_bis['root']:.12f}, 迭代={res_bis['iterations']}次, f(root)={res_bis['function_value']:.2e}")
            print(f"  [牛顿法] 根={res_new['root']:.12f}, 迭代={res_new['iterations']}次, f(root)={res_new['function_value']:.2e}")
            print(f"  -> 牛顿法少迭代 {res_bis['iterations'] - res_new['iterations']} 次")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "=" * 60)
    print("自定义输入示例:")
    expr = input("请输入函数表达式（用 x 作为变量）: ").strip()
    a = float(input("请输入区间左端点: "))
    b = float(input("请输入区间右端点: "))
    method = input("请选择方法 (bisection/newton，默认 newton): ").strip() or "newton"
    
    try:
        result = find_root(expr, a, b, method=method)
        print(f"\n结果 ({result['method']}):")
        print(f"  根 = {result['root']:.10f}")
        print(f"  f(根) = {result['function_value']:.2e}")
        print(f"  迭代次数 = {result['iterations']}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
