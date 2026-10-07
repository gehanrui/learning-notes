"""
线代 × numpy 对照练习
======================

用途：每学一个线代概念，就用这个脚本验证自己手算的答案。

运行：
    $env:PYTHONIOENCODING='utf-8'
    python 线代与numpy对照.py
"""

import numpy as np
np.set_printoptions(precision=4, suppress=True)

print("=" * 62)
print(" 线代 × numpy 对照表")
print("=" * 62)
print("""
  线代概念              numpy 代码              数学记号
  ------------------------------------------------------------
  矩阵加法              A + B                   A + B
  矩阵乘法              A @ B                   AB
  转置                  A.T                     Aᵀ
  求逆                  np.linalg.inv(A)        A⁻¹
  行列式                np.linalg.det(A)        det(A) / |A|
  解方程组              np.linalg.solve(A, b)   解 Ax = b
  特征值/特征向量        np.linalg.eig(A)        Av = λv
  单位矩阵              np.eye(n)               I
  矩阵的秩              np.linalg.matrix_rank(A) rank(A)
""")

print("=" * 62)
print(" 练习 1：矩阵乘法（手算完再运行对答案）")
print("=" * 62)
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print("A =", A.tolist())
print("B =", B.tolist())
print("A @ B =", (A @ B).tolist())
print()
print("手算方法：第 i 行 点乘 第 j 列")
print("  第1行第1列: 1*5 + 2*7 =", 1*5+2*7)
print("  第1行第2列: 1*6 + 2*8 =", 1*6+2*8)
print("  第2行第1列: 3*5 + 4*7 =", 3*5+4*7)
print("  第2行第2列: 3*6 + 4*8 =", 3*6+4*8)

print()
print("=" * 62)
print(" 练习 2：矩阵乘法不满足交换律（A@B ≠ B@A）")
print("=" * 62)
print("A @ B =", (A @ B).tolist())
print("B @ A =", (B @ A).tolist())
print("→ 两者不同。这和普通乘法（3×4 = 4×3）完全不一样，是线代最容易错的地方")

print()
print("=" * 62)
print(" 练习 3：逆矩阵与单位矩阵")
print("=" * 62)
print("A 的逆 =")
print(np.linalg.inv(A))
print("A @ A⁻¹ =")
print(A @ np.linalg.inv(A))
print("→ 结果是对角线为 1、其余为 0 的单位矩阵 I，这就是逆的定义")

print()
print("=" * 62)
print(" 练习 4：行列式与可逆性")
print("=" * 62)
print("det(A) =", round(np.linalg.det(A), 4))
S = np.array([[1, 2], [2, 4]])          # 第二行是第一行的 2 倍
print("奇异矩阵 S =", S.tolist())
print("det(S) =", round(np.linalg.det(S), 4))
print("rank(S) =", np.linalg.matrix_rank(S), "（应为 1，不是满秩）")
print("→ det = 0 表示矩阵不可逆（奇异）。原因：两行成比例，信息冗余")

print()
print("=" * 62)
print(" 练习 5：特征值 —— BCI 的 CSP 算法靠它")
print("=" * 62)
vals, vecs = np.linalg.eig(A)
print("特征值 =", vals.round(4))
print("特征向量（每一列是一个）:")
print(vecs.round(4))
print()
v = vecs[:, 0]
print("验证第 1 个特征向量 v =", v.round(4))
print("  A @ v =", (A @ v).round(4))
print("  λ * v =", (vals[0] * v).round(4))
print("  → 相等，这就是 Av = λv")
print()
print("含义：矩阵 A 作用在特征向量 v 上，只把长度放大 λ 倍，不改变方向")

print()
print("=" * 62)
print(" 下一步：把上面的数字改成别的，自己出题")
print("=" * 62)
print("""
  1. 把 A 改成 [[2, 0], [0, 3]]，看特征值是什么（提示：对角矩阵的特征值就是对角元素）
  2. 把 A 改成 [[0, 1], [1, 0]]，看特征向量（这是"交换两个坐标"的变换）
  3. 用 np.linalg.solve 解 2x + 3y = 8,  x - y = -1

  每题都用笔先算，再运行验证。
""")
