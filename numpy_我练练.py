import numpy as np
# #arr1=np.array([1,2,3])
# print(arr1)
# #arr2=np.array([1.0,2,3])
# print(arr2)
# arr1[0]=2.0
# print(arr1)
# arr2=arr1.astype(float)
# print(arr2)
# import numpy as np
#
# arr_a = np.array([1, 2, 3])
# arr_b = np.array([1, 1, 1])
#
# print("arr_a的形状:", arr_a.shape)
# print("arr_b的形状:", arr_b.shape)
#
# print("arr_a的内容:", arr_a)
# print("arr_b的内容:", arr_b)
# arr1=np.arange(10)
# print(arr1)
# arr2=np.arange(10,20)
# print(arr2)
# arr3=np.ones(10)
# print(arr3)
# arr4=np.ones((2,10))
# print(arr4)
# arr5=arr4.reshape((10,2))
# print(arr5)
# arr1=np.random.randint(3,10,(4,4))
# print(arr1)
# arr2=(100-50)*np.random.random((4,4))+50
# print(arr2)
# print(arr2[[0,2],[2,2]])
# print(arr2[0:3,1:4])
# print(arr2[0:3:2,1:4:2])
# arr1=np.random.random(12).reshape(3,-1)
# print(arr1)
# 第 2 章：矩阵运算
# ==========================================================
# A = [[1, 2], [3, 4]]
# B = [[5, 6], [7, 8]]
#
# 【1】矩阵加法：对应位置相加
# A + B = [[6, 8], [10, 12]]
# → 手算：1+5=6, 2+6=8, 3+7=10, 4+8=12
#
# 【2】矩阵乘法 A @ B   ★本章核心
# A @ B = [[19, 22], [43, 50]]
#
# 手算规则：第 i 行 点乘 第 j 列
#   (1,1): 1*5 + 2*7 = 19
#   (1,2): 1*6 + 2*8 = 22
#   (2,1): 3*5 + 4*7 = 43
#   (2,2): 3*6 + 4*8 = 50
#
# 【3】★ 矩阵乘法不满足交换律（最容易错的地方）
# A @ B = [[19, 22], [43, 50]]
# B @ A = [[23, 34], [31, 46]]
# → 两者不同！普通乘法 3×4 = 4×3，但矩阵不行
#
# 【4】转置 A.T：行变列、列变行
# A     = [[1, 2], [3, 4]]
# A.T   = [[1, 3], [2, 4]]
# → 在 EEG 里：原始数据可能是 通道×时间点，转置后变成 时间点×通道
#
# ==========================================================
#  自己练
# ==========================================================
#
#   手算下面两个，再用 numpy 验证：
#   1. [[1,0],[0,1]] @ A   = ?    （提示：单位矩阵乘任何矩阵等于它本身）
#   2. [[2,0],[0,3]] @ A   = ?    （提示：看看每行被放大了几倍）
#   3. A @ [[2,0],[0,3]]   = ?    （对比上一题，结果一样吗？为什么？）
#
# PS E:\ai_companion>
# arr1=np.array([[1,2],[3,4]])@np.array([[1,0],[0,1]])
# print(arr1)
# arr2=np.array([[2,0],[0,3]])@np.array([[1,2],[3,4]])
# print(arr2)
# arr3=np.array([[1,0],[0,1]])@np.array([[1,2],[3,4]])
# print(arr3)
#
