"""
线代 第 4 章 · 线性方程组  ←→  numpy
=====================================

对应视频：齐次/非齐次线性方程组、矩阵的秩、解的判定

前置：第 2 章（矩阵）、第 3 章（逆）
"""

import numpy as np

print("=" * 58)
print(" 第 4 章：线性方程组")
print("=" * 58)

print("""
【从初中知识开始】

    2x + y = 5
    x  + 3y = 10

这是初中的二元一次方程组。线代做的事是：
把它写成矩阵形式  A @ x = b
""")

A = np.array([[2, 1],
              [1, 3]])
b = np.array([5, 10])
print("A =", A.tolist(), "   b =", b.tolist())
print("→ 求解 A @ x = b，就是解上面那个方程组")

print("\n【1】用 numpy 直接解")
x = np.linalg.solve(A, b)
print("np.linalg.solve(A, b) =", x.round(4))
print()
print("验证：")
print("  2*%.2f + 1*%.2f = %.2f   （应为 5）" % (x[0], x[1], 2*x[0] + 1*x[1]))
print("  1*%.2f + 3*%.2f = %.2f  （应为 10）" % (x[0], x[1], 1*x[0] + 3*x[1]))

print("\n【2】另一种解法：x = A⁻¹ @ b")
print("（这是数学上的公式，但 numpy 里更推荐用 solve）")
x2 = np.linalg.inv(A) @ b
print("np.linalg.inv(A) @ b =", x2.round(4))
print("→ 和 solve 结果相同")

print("\n【3】★ 秩（rank）与解的存在性")
print("""
秩 = 矩阵里'真正独立的信息'有几行。
判断方程组有没有解、有几个解，就靠比较 rank(A) 和 rank([A|b])。
""")
print("rank(A) =", np.linalg.matrix_rank(A))

S = np.array([[1, 2],
              [2, 4]])              # 两行成比例
print("\n再看一个'信息冗余'的例子：")
print("S =", S.tolist(), "  ← 第二行是第一行的 2 倍")
print("rank(S) =", np.linalg.matrix_rank(S), "（应为 1，不是 2）")
print("det(S)  =", round(float(np.linalg.det(S)), 6))
print("→ 秩 < 行数，det = 0，没有唯一解")

print("\n" + "=" * 58)
print(" 自己练")
print("=" * 58)
print("""
  1. 解方程组  3x + y = 7,  x + 2y = 4
     先手算，再用 np.linalg.solve 验证

  2. 解方程组  x + y = 3,  2x + 2y = 6
     （提示：第二个方程是第一个的 2 倍。用 solve 会怎样？这说明什么？）

  3. 用 np.linalg.matrix_rank 看看 np.eye(3) 的秩
""")
