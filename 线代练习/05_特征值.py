"""
线代 第 5 章 · 特征值与特征向量  ←→  numpy
============================================

对应视频：向量的内积、特征值与特征向量、相似矩阵

⚠️ 这是全书最重要的一章（对 BCI 而言）。
   CSP 算法（运动想象 BCI 的招牌算法）的数学核心就是它。
"""

import numpy as np

print("=" * 58)
print(" 第 5 章：特征值与特征向量")
print("=" * 58)

print("""
【先讲直觉，别看公式】

矩阵可以理解成"一种变换"。
绝大多数向量被矩阵变换后，方向都会变。

但特殊情况下，某些向量被变换后：
    - 长度变了
    - 方向没变

这些"方向不变"的向量，就叫 特征向量。
长度被放大的倍数，叫 特征值 λ。

公式：  A · v = λ · v
""")

A = np.array([[2, 0],
              [0, 3]])
print("=" * 58)
print(" 先看最简单的例子：对角矩阵")
print("=" * 58)
print("A =")
print(A)
print()
print("试试 v = [1, 0]:")
v1 = np.array([1, 0])
print("  A @ v =", (A @ v1).tolist())
print("  → 变成了 [2, 0]，方向没变（还在水平方向），长度变 2 倍")
print("  → 所以 [1,0] 是特征向量，特征值 λ = 2")
print()
print("试试 v = [0, 1]:")
v2 = np.array([0, 1])
print("  A @ v =", (A @ v2).tolist())
print("  → 变成了 [0, 3]，方向没变，长度变 3 倍")
print("  → 所以 [0,1] 也是特征向量，λ = 3")
print()
print("用 numpy 求：")
vals, vecs = np.linalg.eig(A)
print("  np.linalg.eig(A) 特征值 =", vals.real)
print("→ 对角矩阵的特征值就是对角线元素。结论对上了")

print("\n" + "=" * 58)
print(" 再看一个普通矩阵")
print("=" * 58)
B = np.array([[1, 2],
              [3, 4]])
print("B =", B.tolist())
vals2, vecs2 = np.linalg.eig(B)
print("特征值 =", vals2.round(4))
print("特征向量（每一列是一个）:")
print(vecs2.round(4))

v = vecs2[:, 0]
lam = vals2[0]
print("\n验证定义 A·v = λ·v：")
print("  B @ v  =", (B @ v).round(4))
print("  λ * v  =", (lam * v).round(4))
print("  → 相等，定义成立")

print("\n" + "=" * 58)
print(" ★ 这和 BCI 有什么关系")
print("=" * 58)
print("""
CSP（Common Spatial Pattern，共空间模式）是运动想象 BCI 最经典的算法。
它的数学核心是"广义特征值问题"：  A x = λ B x

它在问的问题是：
  "哪个空间方向上的脑电信号，两类之间的差异最大？"

答案就是特征向量。
  - 特征值大的方向  → 两类差异大  → 有用的特征
  - 特征值小的方向  → 两类差不多  → 丢弃

所以：你现在学的这一章，就是你以后 CSP 算法的基础。
""")

print("=" * 58)
print(" 自己练")
print("=" * 58)
print("""
  1. np.eye(3) 的特征值是什么？（提示：单位矩阵不改变任何向量）
  2. [[0, 1], [1, 0]] 的特征值是什么？
     （提示：这个矩阵把 [x,y] 变成 [y,x]，哪些向量方向不变？）
  3. 手写一个 2x2 矩阵，用 numpy 求它的特征值，再用定义验证
""")
