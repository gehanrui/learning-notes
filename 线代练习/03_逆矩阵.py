"""
线代 第 3 章 · 逆矩阵  ←→  numpy
=================================

对应视频：逆矩阵的定义、伴随矩阵、初等变换求逆

前置：先学完第 2 章（矩阵乘法），因为逆的定义要用到乘法。
"""

import numpy as np

print("=" * 58)
print(" 第 3 章：逆矩阵")
print("=" * 58)

A = np.array([[1, 2],
              [3, 4]])
print("A =", A.tolist())

# ---- 单位矩阵 ----
print("\n【1】先认识单位矩阵 I")
I = np.eye(2)
print("np.eye(2) =")
print(I)
print("→ 对角线是 1，其余是 0。作用相当于数字里的 1")
print("→ 任何矩阵 A @ I = A")

# ---- 逆矩阵 ----
print("\n【2】逆矩阵 A⁻¹")
Ainv = np.linalg.inv(A)
print("np.linalg.inv(A) =")
print(Ainv.round(4))
print()
print("【3】验证定义：A @ A⁻¹ = I")
print((A @ Ainv).round(10))
print("→ 结果就是单位矩阵。这就是逆矩阵的定义")

# ---- 没有逆的情况 ----
print("\n【4】不是所有矩阵都有逆")
S = np.array([[1, 2],
              [2, 4]])
print("S =", S.tolist(), "  ← 两行成比例")
print("np.linalg.det(S) =", round(float(np.linalg.det(S)), 6))
print("→ det = 0，所以 S 没有逆矩阵（叫'奇异矩阵'）")
print("→ 这正是第 1 章'行列式为 0'的用处：判断有没有逆")
print()
try:
    np.linalg.inv(S)
    print("（如果这行执行了，说明 numpy 算出了结果——但那是数值误差）")
except np.linalg.LinAlgError as e:
    print("numpy 报错:", e)
    print("→ 它明确告诉你：这个矩阵不可逆")

print("\n" + "=" * 58)
print(" 自己练")
print("=" * 58)
print("""
  1. np.eye(3) 的逆是什么？（提示：猜一下，再验证）
  2. 求 [[2, 0], [0, 4]] 的逆（提示：对角线取倒数，试试看）
  3. 手算验证：A @ A⁻¹ 是不是真的等于 I
""")
