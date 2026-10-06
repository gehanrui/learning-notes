"""
水平自测 —— 4 道题，10 分钟
=============================

目的：确认你的 Python 基础到底到什么程度。
      会了的部分不用重学，这能省你几十小时。

怎么用：
    1. 每道题先自己写答案（写在纸上或注释里）
    2. 再运行这个脚本看参考答案
    3. 对照一下，看自己差在哪

运行：
    $env:PYTHONIOENCODING='utf-8'
    python 水平自测.py
"""

print("=" * 64)
print(" 水平自测：4 道题")
print("=" * 64)
print("""
先自己写，再看答案。每题想 1-2 分钟。

题 1：写一个 for 循环，打印出 1 到 10 的所有偶数。

题 2：有一个列表 scores = [88, 92, 75, 96, 81]
      写代码算出平均分，并找出最高分。

题 3：写一个函数 count_vowels(s)，返回字符串 s 里英文元音字母
      (a e i o u) 的个数。例如 count_vowels("hello") 应该返回 2。

题 4：用 random 模块写"猜数字游戏"的骨架：
      程序随机想一个 1-100 的数，用户输入猜测，
      程序提示"大了"或"小了"，猜中后输出猜了几次。
""")

print("=" * 64)
print(" 参考答案")
print("=" * 64)

print("""
--------- 题 1 ---------
for i in range(1, 11):
    if i % 2 == 0:
        print(i)

# 或者更简洁：
for i in range(2, 11, 2):
    print(i)

考察点：range 的用法、% 取余、if 判断
""")

print("""--------- 题 2 ---------
scores = [88, 92, 75, 96, 81]
平均分 = sum(scores) / len(scores)
最高分 = max(scores)
print("平均分:", 平均分)
print("最高分:", 最高分)

# 如果不用内置函数，自己写循环：
total = 0
最高 = scores[0]
for s in scores:
    total = total + s
    if s > 最高:
        最高 = s
print("平均分:", total / len(scores), "最高分:", 最高)

考察点：列表遍历、内置函数 sum/len/max、累加逻辑
""")

print("""--------- 题 3 ---------
def count_vowels(s):
    元音 = "aeiou"
    count = 0
    for ch in s:
        if ch in 元音:
            count = count + 1
    return count

print(count_vowels("hello"))      # 2

考察点：函数定义、return、字符串包含判断、循环
""")

print("""--------- 题 4 ---------
import random

target = random.randint(1, 100)
count = 0

print("我想了一个 1-100 的数，你猜：")

while True:
    guess = int(input("请输入你的猜测："))
    count = count + 1

    if guess > target:
        print("大了")
    elif guess < target:
        print("小了")
    else:
        print(f"猜对了！你用了 {count} 次")
        break

考察点：while True + break、input 转 int、if/elif/else、随机数
""")

print("=" * 64)
print(" 怎么判断自己的水平")
print("=" * 64)
print("""
4 题都能写出来（不用完全一样，逻辑对就行）
    → 你的 Python 基础过关，直接学 numpy

题 3、题 4 有一道卡住
    → 补一下函数和循环，一两天就够

题 1、题 2 就卡住
    → 确实需要系统过一遍基础语法

关键区别：能"看懂"别人的代码 ≠ 能"自己写出来"。
        真正的水平看的是能不能自己写。
""")
