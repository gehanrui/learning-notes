"""
numpy 第 1 周练习：数组是什么（可直接运行）
=============================================

这是一个「可以真正运行」的版本。
你原来 数组.py 里的代码被 ''' 包住了，所以跑起来没有输出——
三引号在 Python 里是「多行字符串」，不是注释，里面的代码不会执行。

运行：
    $env:PYTHONIOENCODING='utf-8'
    python 数组练习.py

每天做一步，改参数，看输出。
"""

import numpy as np

print("=" * 60)
print(" 第 1 步：创建数组")
print("=" * 60)

a = np.array([1, 2, 3])                    # 一维
b = np.array([[1, 2, 3], [4, 5, 6]])       # 二维
c = np.zeros(5)                            # 5 个 0
d = np.ones((2, 3))                        # 2 行 3 列，全是 1
e = np.arange(10)                          # 0~9
f = np.arange(0, 20, 5)                    # 0,5,10,15
g = np.linspace(0, 1, 5)                   # 0~1 之间均匀 5 个点
h = np.eye(3)                              # 3×3 单位矩阵

print("a = np.array([1,2,3])      ->", a)
print("b = np.array([[1,2,3],[4,5,6]])")
print(b)
print("c = np.zeros(5)            ->", c)
print("d = np.ones((2,3))         ->")
print(d)
print("e = np.arange(10)          ->", e)
print("f = np.arange(0,20,5)      ->", f)
print("g = np.linspace(0,1,5)     ->", g)
print("h = np.eye(3)              ->")
print(h)

print()
print("=" * 60)
print(" 第 2 步：看属性（shape / dtype / ndim / size）")
print("=" * 60)


def show(name, arr):
    print(f"  {name:<22} shape={str(arr.shape):<10} dtype={str(arr.dtype):<8} "
          f"ndim={arr.ndim}  size={arr.size}")


show("a = [1,2,3]", a)
show("b = 2×3", b)
show("c = np.zeros(5)", c)
show("d = np.ones((2,3))", d)
show("e = np.arange(10)", e)
show("g = np.linspace(0,1,5)", g)
show("h = np.eye(3)", h)

print()
print("  ★ 重点理解 shape：")
print("     a.shape = (3,)    ← 1 个数字 = 一维数组，有 3 个元素")
print("     b.shape = (2, 3)  ← 2 个数字 = 二维数组，2 行 3 列")
print("     h.shape = (3, 3)  ← 3 行 3 列")
print()
print("  ★ 规律：shape 里各数字相乘 = size")
print(f"     b.shape = (2,3)，2×3 = 6，b.size = {b.size}   ✓")
print(f"     a.shape = (3,)，3 = 3，a.size = {a.size}      ✓")

print()
print("=" * 60)
print(" 第 3 步：dtype（元素类型）")
print("=" * 60)
print("  np.array([1, 2, 3]).dtype        =", np.array([1, 2, 3]).dtype, "  ← 整数")
print("  np.array([1.0, 2, 3]).dtype      =", np.array([1.0, 2, 3]).dtype, "  ← 有小数点就是浮点")
print("  np.array([1, 2, 3], dtype=float).dtype =",
      np.array([1, 2, 3], dtype=float).dtype)

print()
print("  ★ 注意这个坑：整数数组赋值小数会被截断")
i1 = np.array([1, 2, 3])
i1[0] = 2.7                      # 想存 2.7，但数组是整数类型
print("     arr = np.array([1,2,3])  （整数数组）")
print("     arr[0] = 2.7")
print("     print(arr) ->", i1, "  ← 2.7 变成了 2，小数被丢掉了！")
i2 = np.array([1.0, 2.0, 3.0])
i2[0] = 2.7
print("     如果一开始用 np.array([1.0,2.0,3.0])（浮点数组）：")
print("     arr[0] = 2.7 ->", i2, "  ← 正常保留")

print()
print("=" * 60)
print(" 第 4 步：reshape（改变形状）")
print("=" * 60)
arr = np.arange(10)
print("  原始 arr = np.arange(10) ->", arr, " shape =", arr.shape)
r1 = arr.reshape((2, 5))
print("  arr.reshape((2,5))      ->")
print(r1, "  shape =", r1.shape)
r2 = arr.reshape((5, 2))
print("  arr.reshape((5,2))      ->")
print(r2, "  shape =", r2.shape)
print()
print("  ★ reshape 的元素总数必须不变：2×5 = 10，5×2 = 10 ✓")
print("    如果写 arr.reshape((3,4))，3×4=12 ≠ 10，会报错")

print()
print("=" * 60)
print(" 动手改（这是最重要的一步）")
print("=" * 60)
print("""
  1. 把 a 改成 np.array([1,2,3,4,5])，重新运行，看 a.shape 变成什么？
  2. 把 d = np.ones((2,3)) 改成 np.ones((4,2))，看输出怎么变？
  3. 把 g = np.linspace(0,1,5) 改成 np.linspace(0,10,11)，猜猜输出是什么，再运行验证
  4. 试试 np.arange(5) 和 np.arange(5.0) 的 dtype 有什么不同？

  每个都先「猜」，再运行。猜错的地方就是你要重点看的地方。
""")
