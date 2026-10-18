r"""
线代练习生成器（带 numpy 验算）
================================

用途：随机生成线代练习题，你手算，再对答案。
      --answers 参数控制是否显示答案。

为什么好用：
  1. 题量无限（不会做完就没题）
  2. 立刻对答案（不用翻书）
  3. 难度可调（2 阶到 4 阶）
  4. 和 numpy 学习结合（答案就是用 np.linalg 算的）

用法：
    # 出题（只看题目）
    python 线代出题器.py 行列式 3

    # 出题 + 显示答案
    python 线代出题器.py 行列式 3 --answers

    # 不指定参数 = 出 5 道 3 阶行列式题
    python 线代出题器.py

支持的类型：
    行列式   矩阵乘法   求逆   方程组   特征值   秩

手工做的时候：
    - 拿纸笔算，不要看答案
    - 算完再运行带 --answers 的命令核对
    - 算错的题目记进笔记（只记错题）
"""

import sys
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=100)

# ---------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------

def rand_int_matrix(n, m=None, lo=-5, hi=5, seed=None):
    """生成 n×m 的随机整数矩阵"""
    if m is None:
        m = n
    rng = np.random.default_rng(seed)
    return rng.integers(lo, hi + 1, size=(n, m))


def fmt_matrix(A):
    """把矩阵格式化成立体好看的样子（支持复数）"""
    rows = []
    for row in A:
        cells = []
        for v in row:
            if np.iscomplexobj(v) or isinstance(v, complex):
                v = complex(v)
                if abs(v.imag) < 1e-9:
                    cells.append(f"{v.real:6.2f}    ")
                else:
                    cells.append(f"{v.real:5.2f}{v.imag:+.2f}i")
            else:
                if float(v) == int(v):
                    cells.append(f"{int(v):5d}")
                else:
                    cells.append(f"{float(v):6.2f}")
        rows.append("  " + " ".join(cells))
    return "\n".join(rows)


def fmt_vec(v):
    return "  " + "  ".join(f"{float(x):6.2f}" for x in v)


# ---------------------------------------------------------------
# 各类题型
# ---------------------------------------------------------------

def gen_determinant(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 计算下列 {n} 阶行列式")
    print("=" * 62)
    print()
    answers = []
    for i in range(count):
        A = rand_int_matrix(n, seed=seed + i)
        answers.append(np.linalg.det(A))
        print(f"题 {i+1}:")
        print(fmt_matrix(A))
        print()
    if show_answers:
        print("-" * 62)
        print(" 答案")
        print("-" * 62)
        for i, v in enumerate(answers, 1):
            print(f"  题 {i}: det = {v:.4g}" + ("  （矩阵奇异，行列式为 0）" if abs(v) < 1e-9 else ""))


def gen_multiply(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 计算下列矩阵乘法 A @ B（{n}×{n}）")
    print("=" * 62)
    print()
    answers = []
    for i in range(count):
        A = rand_int_matrix(n, seed=seed + i * 2)
        B = rand_int_matrix(n, seed=seed + i * 2 + 1)
        answers.append(A @ B)
        print(f"题 {i+1}:")
        print("A =")
        print(fmt_matrix(A))
        print("B =")
        print(fmt_matrix(B))
        print()
    if show_answers:
        print("-" * 62)
        print(" 答案（A @ B）")
        print("-" * 62)
        for i, M in enumerate(answers, 1):
            print(f"  题 {i}:")
            print(fmt_matrix(M))
            print()


def gen_inverse(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 求下列 {n} 阶矩阵的逆矩阵（不可逆的请指出）")
    print("=" * 62)
    print()
    items = []
    for i in range(count):
        # 用"单位矩阵 + 小扰动"保证大概率可逆，偶尔混入奇异矩阵
        A = rand_int_matrix(n, seed=seed + i)
        if count >= 3 and i == count - 1 and n >= 2:  # 题量够多时，最后一道故意做成奇异矩阵
            A = A.copy()
            A[-1] = A[0] * 2
        items.append(A)
        print(f"题 {i+1}:")
        print(fmt_matrix(A))
        print()
    if show_answers:
        print("-" * 62)
        print(" 答案")
        print("-" * 62)
        for i, A in enumerate(items, 1):
            det = np.linalg.det(A)
            if abs(det) < 1e-9:
                print(f"  题 {i}: det = 0，矩阵不可逆（奇异矩阵）")
            else:
                print(f"  题 {i}: A⁻¹ =")
                print(fmt_matrix(np.linalg.inv(A)))
            print()


def gen_solve(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 解下列线性方程组 A @ x = b（{n} 元）")
    print("=" * 62)
    print()
    items = []
    for i in range(count):
        A = rand_int_matrix(n, seed=seed + i)
        x_true = rand_int_matrix(n, 1, lo=-3, hi=3, seed=seed + 100 + i).flatten()
        b = (A @ x_true).astype(int)
        items.append((A, b, x_true))
        print(f"题 {i+1}:")
        # 用方程形式显示（更适合手算）
        for r in range(n):
            terms = []
            for c in range(n):
                coef = int(A[r, c])
                if coef == 0:
                    continue
                var = f"x{c+1}"
                if coef == 1:
                    terms.append(var)
                elif coef == -1:
                    terms.append("-" + var)
                else:
                    terms.append(f"{coef}{var}")
            eq = " + ".join(terms).replace("+ -", "- ")
            print(f"    {eq} = {int(b[r])}")
        print()
    if show_answers:
        print("-" * 62)
        print(" 答案")
        print("-" * 62)
        for i, (A, b, xt) in enumerate(items, 1):
            try:
                x = np.linalg.solve(A.astype(float), b.astype(float))
                sol = ", ".join(f"x{j+1} = {v:.4g}" for j, v in enumerate(x))
                print(f"  题 {i}: {sol}")
            except np.linalg.LinAlgError:
                print(f"  题 {i}: det = 0，无唯一解")
        print()
        print("  提示：这些题是反推出来的，所以答案一定是整数。")


def gen_eigen(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 求下列 {n} 阶矩阵的特征值与特征向量")
    print("=" * 62)
    print()
    print(" （这些矩阵是'反向构造'的：特征值都是整齐的整数，手算得出来）")
    print()

    rng = np.random.default_rng(seed)
    items = []
    for i in range(count):
        # 反向构造：A = P · D · P⁻¹
        # D 是对角矩阵（对角线就是特征值），P 是可逆的整数矩阵
        # 这样 A 的特征值必然等于 D 的对角线元素（整数，手算得出来）
        while True:
            eig_vals = rng.integers(-4, 6, size=n)          # 特征值（整数）
            P = rng.integers(-2, 3, size=(n, n))            # 构造用的可逆矩阵
            if abs(np.linalg.det(P)) < 0.5:
                continue
            A = P @ np.diag(eig_vals) @ np.linalg.inv(P)
            # 只采用同时满足两个条件的矩阵：
            #   1) A 是整数矩阵（题目好看）
            #   2) 元素不太大（|a| <= 9），否则手算特征方程会疯
            if np.allclose(A, np.round(A), atol=1e-8):
                Ai = np.round(A).astype(int)
                if np.max(np.abs(Ai)) <= 9:
                    A = Ai
                    break
        items.append(A)

        print(f"题 {i+1}:")
        print(fmt_matrix(A))
        print()

    if show_answers:
        print("-" * 62)
        print(" 答案（特征值）")
        print("-" * 62)
        for i, A in enumerate(items, 1):
            vals = np.linalg.eigvals(A)
            vals_real = [round(float(np.real(v)), 4) for v in vals]
            print(f"  题 {i}: 特征值 = {sorted(vals_real, reverse=True)}")
        print()
        print("  （顺序可能和你算的不同，这正常；重根也正常）")
        print()
        print("  怎么自己验算：")
        print("     import numpy as np")
        print("     A = np.array([[题目的数字]])")
        print("     vals, vecs = np.linalg.eig(A)")
        print("     print(vals)")
        print("     # 验证 Av = λv：")
        print("     print(A @ vecs[:, 0], vals[0] * vecs[:, 0])")


def gen_rank(n, count, show_answers, seed):
    print("=" * 62)
    print(f" 求下列矩阵的秩 rank(A)（{n} 阶）")
    print("=" * 62)
    print()
    items = []
    for i in range(count):
        A = rand_int_matrix(n, seed=seed + i)
        if i == 0 and n >= 2:
            A = A.copy()
            A[-1] = A[0] * 3        # 第一道做成秩不足的情形
        items.append(A)
        print(f"题 {i+1}:")
        print(fmt_matrix(A))
        print()
    if show_answers:
        print("-" * 62)
        print(" 答案")
        print("-" * 62)
        for i, A in enumerate(items, 1):
            print(f"  题 {i}: rank = {np.linalg.matrix_rank(A)}")
        print()
        print("  提示：秩 = 线性无关的行（或列）的个数")


# ---------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------

GENERATORS = {
    "行列式": gen_determinant,
    "矩阵乘法": gen_multiply,
    "求逆": gen_inverse,
    "方程组": gen_solve,
    "特征值": gen_eigen,
    "秩": gen_rank,
}


def main():
    raw = sys.argv[1:]
    args = [a for a in raw if not a.startswith("--")]
    show_answers = "--answers" in raw or "-a" in raw

    # 支持 --seed N：用来复现同一批题
    seed = None
    if "--seed" in raw:
        idx = raw.index("--seed")
        if idx + 1 < len(raw):
            try:
                seed = int(raw[idx + 1])
                # 把种子值从 args 里剔除（它是 --seed 的参数，不是位置参数）
                args = [a for a in args if a != str(seed)]
            except ValueError:
                print("--seed 后面要跟一个整数")
                return

    kind = args[0] if len(args) > 0 else "行列式"
    size = int(args[1]) if len(args) > 1 else 3
    count = int(args[2]) if len(args) > 2 else 5

    if kind not in GENERATORS:
        print(f"不认识的类型：{kind}")
        print(f"可用类型：{', '.join(GENERATORS.keys())}")
        print()
        print("用法：python 线代出题器.py 类型 阶数 题数 [--answers] [--seed N]")
        return

    if size < 2 or size > 4:
        print("阶数只支持 2、3、4（再大手算没意义）")
        return

    if seed is None:
        seed = np.random.randint(1, 10**6)

    print()
    print("=" * 62)
    print(f" 线代练习 · {kind} · {size} 阶 · {count} 道")
    print("=" * 62)
    print(f" 随机种子 = {seed}")
    print()

    GENERATORS[kind](size, count, show_answers, seed)

    if not show_answers:
        print("=" * 62)
        print(" 做完后，用同一个种子看答案（题完全一样）：")
        print()
        print(f"   python 线代出题器.py {kind} {size} {count} --seed {seed} --answers")
        print()
        print(f" 或者要出全新的一批题（换种子就行）：")
        print(f"   python 线代出题器.py {kind} {size} {count}")
        print("=" * 62)


if __name__ == "__main__":
    main()
