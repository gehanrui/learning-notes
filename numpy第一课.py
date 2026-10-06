"""
numpy 第一课：列表 vs 数组
============================
运行前先猜输出，再运行验证。
    $env:PYTHONIOENCODING='utf-8'
    python numpy第一课.py
"""
import numpy as np

print("=" * 60)
print(" 对比 1：乘法")
print("=" * 60)
lst = [1, 2, 3]
arr = np.array([1, 2, 3])

print("列表 [1,2,3] * 2  =", lst * 2)
print("数组 [1,2,3] * 2  =", arr * 2)
print()
print("→ 列表的 * 是'重复两遍'，数组的 * 是'每个元素都乘 2'")
print("→ 这就是 numpy 存在的理由：整块运算")

print()
print("=" * 60)
print(" 对比 2：加法")
print("=" * 60)
print("列表 [1,2,3] + [4,5,6] =", lst + [4, 5, 6])
try:
    print("数组 [1,2,3] + [4,5,6] =", arr + np.array([4, 5, 6]))
except Exception as e:
    print("出错了:", e)
print()
print("→ 列表的 + 是'拼接'，数组的 + 是'逐元素相加'")

print()
print("=" * 60)
print(" 对比 3：求平方")
print("=" * 60)
squares_list = [x ** 2 for x in lst]        # 列表要写循环（列表推导）
squares_arr = arr ** 2                       # 数组直接算
print("列表求平方（要写循环）:", squares_list)
print("数组求平方（直接写）  :", squares_arr)

print()
print("=" * 60)
print(" 对比 4：速度（100 万个数的平方）")
print("=" * 60)
import time

big_list = list(range(1_000_000))
big_arr = np.arange(1_000_000)

t0 = time.time()
r1 = [x ** 2 for x in big_list]
t1 = time.time() - t0

t0 = time.time()
r2 = big_arr ** 2
t2 = time.time() - t0

print(f"列表推导用时: {t1:.3f} 秒")
print(f"numpy 运算用时: {t2:.4f} 秒")
print(f"→ numpy 快了约 {t1/t2:.0f} 倍")
print()
print("→ 脑电信号动辄几十万个采样点，所以必须用 numpy")

print()
print("=" * 60)
print(" 现在去改上面的代码试试")
print("=" * 60)
print("""
1. 把 lst = [1, 2, 3] 改成 [10, 20, 30]，看数组运算结果
2. 试试 arr / 2、arr - 1、arr ** 0.5
3. 试试 np.array([[1,2],[3,4]]) —— 二维数组长什么样
""")
