r"""
水平自测答案 —— 整理版（可直接运行）
=====================================

来源：D:\2\py01\.venv\diyitian.py（你的原始答案）

原始文件的问题：每一题都被 ''' 三引号包起来了。
    三引号在 Python 里表示"多行字符串"，所以那些代码只是文字，
    不会被执行 —— 运行时屏幕上只会打印最后一行 print("idfjgvj")。

这个文件把三引号去掉，代码就能真正运行了。
"""

import random

# ==========================================================
# 第 1 题：打印 1 到 10 的所有偶数
# ==========================================================
print("=" * 50)
print("第 1 题：1 到 10 的偶数")
print("=" * 50)

# 你的写法（多做了一步判断）
for i in range(0, 10):
    if i % 2 == 0:
        print(i, end=" ")
print()

# 更简洁的写法：range 的第三个参数是"步长"，直接每次加 2
# 这样就不用逐个判断了，效率更高
for i in range(0, 10, 2):
    print(i, end=" ")
print()
print("→ 两种写法都输出 0 2 4 6 8。第二种省掉了 if 判断（步长直接跳过奇数）")


# ==========================================================
# 第 2 题：算平均分和最高分
# ==========================================================
print()
print("=" * 50)
print("第 2 题：平均分和最高分")
print("=" * 50)

scores = [88, 92, 75, 96, 81]
print("平均分:", sum(scores) / len(scores))
print("最高分:", max(scores))
print("→ 你的答案完全正确，一行搞定")


# ==========================================================
# 第 3 题：统计元音字母个数
# ==========================================================
print()
print("=" * 50)
print("第 3 题：统计元音字母")
print("=" * 50)


def count_vowels(s):
    """你的写法：用字符串的 count() 方法逐个累加"""
    n = s.count('a') + s.count('e') + s.count('i') + s.count('o') + s.count('u')
    return n


print('count_vowels("asdfddff") =', count_vowels("asdfddff"))
print('count_vowels("hello")    =', count_vowels("hello"))

# 另一种写法：循环逐个字符判断
def count_vowels_v2(s):
    count = 0
    for ch in s:
        if ch in "aeiou":
            count = count + 1
    return count


print('count_vowels_v2("hello") =', count_vowels_v2("hello"))
print("→ 你的写法更短。{0} 的写法更通用（想加半元音 y 时更好改）".format("循环"))


# ==========================================================
# 第 4 题：猜数字游戏
# ==========================================================
print()
print("=" * 50)
print("第 4 题：猜数字游戏")
print("=" * 50)
print("→ 下面这段被注释掉了，因为它需要你在终端里输入")
print("→ 想玩的话，把最外层的 ''' 去掉再运行")
print()


def guess_number():
    """猜数字游戏

    改进点（对比你的原版）：
      1. 变量名：i → target（目标数），n → guess（猜测）
         原版用 i 当目标数、n 当猜测，容易看混
      2. 加了计数器 count，能显示猜了几次
         原版固定输出"第一次就猜对了"，无论猜了几次都不准确
      3. 去掉了循环末尾多余的 continue
         （continue 是"跳过本次循环剩余部分"，但在 if/elif/else 末尾
           它后面已经没有代码了，所以是多余的）
    """
    target = random.randint(1, 100)
    count = 0

    print("我想了一个 1 到 100 的数字，你猜：")

    while True:
        guess = int(input("请输入你的猜测："))
        count = count + 1

        if guess > target:
            print("太大了")
        elif guess < target:
            print("太小了")
        else:
            print(f"恭喜你，猜对了！你一共用了 {count} 次")
            break


# 取消下面这行的注释就能玩（在终端里运行本文件时）
# guess_number()


print()
print("=" * 50)
print("总结")
print("=" * 50)
print("""
四道题全部正确 ✅

你的水平：
  - for 循环、range、条件判断     → 会
  - 列表、内置函数 sum/len/max    → 会
  - 函数定义、return              → 会
  - while True + break、input     → 会

所以：Python 基础语法这块，你不需要再系统学一遍。
直接进入 numpy 即可（见《numpy四周计划.md》）。

三个小习惯可以改进：
  1. 别用 ''' 把练习代码包起来 —— 那样代码不会运行
     想把某段代码"停用"，用 # 注释，或者用编辑器的注释快捷键
  2. 变量名用有意义的名字：target 比 i 清楚，guess 比 n 清楚
  3. continue 只在你后面还有代码、想跳过时才用
""")
