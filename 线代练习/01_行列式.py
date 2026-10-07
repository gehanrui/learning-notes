"""
线代 第 1 章 · 行列式  ←→  numpy
================================

对应视频：第一节 ~ 第八节（二阶三阶行列式、n阶行列式、性质、展开、克莱姆法则）

先读完这一章，再运行这个文件。
"""

import numpy as np

print("=" * 58)
print(" 第 1 章：行列式")
print("=" * 58)

# ---- 二阶行列式：手算就能做 ----
print("\n【二阶行列式】")
print("""
    |a  b|
    |c  d|   =  a*d - b*c      ← 对角线相乘再相减
""")
A = np.array([[1, 2],
              [3, 4]])
print("A =", A.tolist())
print("手算: 1*4 - 2*3 =", 1*4 - 2*3)
print("numpy: np.linalg.det(A) =", round(float(np.linalg.det(A)), 4))
print("→ 两行是不同的，行列式不为 0")

# ---- 行列式为 0 的含义 ----
print("\n" + "=" * 58)
print(" 重点：行列式 = 0 意味着什么")
print("=" * 58)
S = np.array([[1, 2],
              [2, 4]])          # 第二行 = 第一行 × 2
print("S =", S.tolist(), "   ← 第二行是第一行的 2 倍")
print("np.linalg.det(S) =", round(float(np.linalg.det(S)), 6))
print()
print("→ 行列式为 0，说明这两行'成比例'，信息冗余")
print("→ 术语叫'矩阵奇异（singular）'，它没有逆矩阵")
print("→ 这个判断在后面解方程组时极重要：det=0 就没有唯一解")

# ---- 三阶行列式 ----
print("\n" + "=" * 58)
print(" 三阶行列式")
print("=" * 58)
B = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 10]])
print("B =")
print(B)
print("np.linalg.det(B) =", round(float(np.linalg.det(B)), 4))
print()
print("→ 三阶的行列式手算要用'展开'（第五、六节的内容）")
print("→ numpy 直接给结果。所以：手算练理解，numpy 用来对答案")

print("\n" + "=" * 58)
print(" 自己练：改数字，看 det 怎么变")
print("=" * 58)
print("""
  1. 把 S 改成 [[1, 2], [2, 5]]（不再成比例），det 是多少？
  2. 把 B 的第 3 行改成 [7, 8, 9]，det 变了吗？（提示：想想为什么）
  3. 单位矩阵 np.eye(3) 的 det 是多少？
""")
