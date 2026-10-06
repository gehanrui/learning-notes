"""
Python 分阶练习 —— 从"完全看不懂"到"能看懂 sine_demo.py"
============================================================

为什么要写这个文件：
    你运行 sine_demo.py 时"大部分看不懂"，不是因为 FFT 难，
    而是因为它把 15 个基础语法点挤在了一起：
        np.arange / zip / def / 列表推导 / 数组切片 / rfft ...
    这些都还没学，当然看不懂。

    这个文件把它们拆成 8 个台阶。每级只教 1-2 个新东西，
    而且每一步都有输出，你能看到自己在干什么。

怎么用：
    不要一次看完。每天做一级，改一改，看输出变了没有。
    运行命令（在 E:\\ai_companion 目录下）：

        $env:PYTHONIOENCODING='utf-8'
        python python_分阶练习.py

    运行后会依次输出全部 8 级的结果。看懂一级，再往下看一级。
"""

print("=" * 64)
print(" 第 1 级：变量和打印")
print("=" * 64)
# 变量 = 给一个值起个名字。f = 10 的意思是"f 代表 10"
f = 8                     # 频率，单位 Hz（赫兹 = 每秒振动次数）
amplitude = 1.0             # 振幅（波有多高）
print("频率 f =", f, "Hz")
print("振幅 =", amplitude)
print()
print("→ 试着改：把 f 改成 8，再运行一次")
print("→ 你改了它，后面所有结果都会跟着变（这就是变量的意义）")


print()
print("=" * 64)
print(" 第 2 级：算一个正弦波的值（不用数组）")
print("=" * 64)
# 正弦波的公式：y = A × sin(2π × f × t)
# 其中 t 是时间。我们只算 5 个时间点，先感受一下
import math                 # math 是 Python 自带的数学工具包

print("时间 t(秒)   sin 的值")
for t in [0, 0.025, 0.05, 0.075, 0.1]:
    y = amplitude * math.sin(2 * math.pi * f * t)
    print(f"   {t:.3f}      {y:+.4f}")

print()
print("→ 关键理解：正弦波就是一个随 t 上下起伏的数")
print("→ 10 Hz 表示 1 秒里起伏 10 次")
print("→ 注意 for 循环：它把列表里的每个值依次取出来，叫做一次'迭代'")


print()
print("=" * 64)
print(" 第 3 级：列表和循环 —— 从 5 个点变成很多点")
print("=" * 64)
# 上一级手写了 5 个时间点。如果要 500 个呢？不能手写，要用循环生成
sample_rate = 250           # 采样率：每秒记录 250 个点（EEG 常用值）
duration = 1.0              # 记录 1 秒

times = []                  # 先建一个空列表
n_points = int(sample_rate * duration)      # 250 × 1 = 250 个点
for i in range(n_points):                   # range(250) 依次给出 0,1,2,...,249
    times.append(i / sample_rate)           # 第 i 个点的时间 = i / 采样率

print("一共生成", len(times), "个时间点")
print("前 5 个时间点:", [round(x, 4) for x in times[:5]])
print("最后 1 个时间点:", round(times[-1], 4), "秒")
print()
print("→ times[:5] 叫'切片'：取前 5 个。times[-1] 是最后一个")
print("→ 列表推导 [round(x,4) for x in ...] 是'对每个元素做同一件事'的简写")
print("→ 试着改：把 duration 改成 2.0，看点的数量变成多少")


print()
print("=" * 64)
print(" 第 4 级：NumPy 数组 —— 为什么要用它")
print("=" * 64)
import numpy as np

# 上一级用 for 循环一个个算，很啰嗦。NumPy 让你一次性对整个数组做运算
t = np.arange(0, 1.0, 1.0 / sample_rate)    # 和上面的 times 一样，但一行搞定
print("np.arange 生成的数组:", t[:5], "...")
print("数组长度:", len(t))
print("数组的类型:", type(t))

signal = amplitude * np.sin(2 * np.pi * f * t)     # 整条波形，一行算完
print("signal 前 5 个值:", np.round(signal[:5], 4))
print()
print("→ 关键区别：列表是'一个一个存'，数组是'一整块算'")
print("   np.sin(数组) 会对数组里每个元素求 sin，不需要 for 循环")
print("→ 这就是 NumPy 存在的理由：快、写法短")


print()
print("=" * 64)
print(" 第 5 级：把波画出来（这才是保存图片的三行核心）")
print("=" * 64)
import matplotlib
matplotlib.use("Agg")           # 不弹窗口，只存文件
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(t[:100], signal[:100])              # 只画前 100 个点（放大看更清楚）
ax.set_xlabel("时间 (秒)")
ax.set_ylabel("幅值")
ax.set_title(f"第 5 级：{f} Hz 正弦波")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("stage5_wave.png", dpi=110)
print("已保存 stage5_wave.png —— 打开看看，这就是你画的波")
print()
print("→ 你只要记住三行：plt.subplots() → ax.plot() → fig.savefig()")
print("→ 试着改：把 t[:100] 改成 t[:250]，波会画得更长")


print()
print("=" * 64)
print(" 第 6 级：函数 —— 把重复的东西打包")
print("=" * 64)
# 上面造波的 3 行代码会反复用。用 def 打包起来，以后一行调用
def make_wave(freq, amp, seconds, fs=250):
    """造一条正弦波。freq=频率, amp=振幅, seconds=时长, fs=采样率"""
    tt = np.arange(0, seconds, 1.0 / fs)
    return tt, amp * np.sin(2 * np.pi * freq * tt)

t1, wave1 = make_wave(10, 1.0, 0.5)         # 10 Hz
t2, wave2 = make_wave(23, 0.6, 0.5)         # 23 Hz
print("用函数造了两条波，长度分别是", len(wave1), "和", len(wave2))
print()
print("→ def 定义函数，return 把结果交出去")
print("→ 函数 = 给一段代码起名字，以后用名字调用它")
print("→ 这就是 sine_demo.py 里 make_signal() 的作用")


print()
print("=" * 64)
print(" 第 7 级：FFT —— 从波形里找出频率")
print("=" * 64)
# FFT 是数学家发明的算法。你现在不需要理解它的原理，
# 只需要知道：给它一段波形，它告诉你里面有哪些频率成分。
combined = wave1 + wave2            # 把 10 Hz 和 23 Hz 加在一起

spectrum = np.fft.rfft(combined)                    # 做 FFT
freqs = np.fft.rfftfreq(len(combined), 1.0 / 250)   # 每个结果对应的频率
magnitude = np.abs(spectrum)                        # 取绝对值 = 能量大小

print("FFT 输出的数组长度:", len(spectrum))
print("对应的频率:", np.round(freqs, 1))

# 找出能量最大的位置
peak_index = np.argmax(magnitude[1:]) + 1     # 跳过第 0 个（直流分量）
print()
print("能量最强的频率是:", round(freqs[peak_index], 1), "Hz")
print()
print("→ 结果应该接近 10 或 23 之一（哪个振幅大就是哪个，这里 10 Hz 振幅 1.0 更大）")
print("→ np.argmax() = 找出最大值在哪个位置")
print("→ 到这里你已经掌握了 sine_demo.py 的核心逻辑")


print()
print("=" * 64)
print(" 第 8 级：把它们连起来（等价于 sine_demo.py 的简化版）")
print("=" * 64)
t3, sig3 = make_wave(8, 1.0, 1.0)           # 8 Hz —— Alpha 波的起点
t4, sig4 = make_wave(13, 0.8, 1.0)          # 13 Hz —— Alpha 波的终点
noise = 0.5 * np.random.default_rng(0).standard_normal(len(sig3))
final = sig3 + sig4 + noise                 # 信号 + 噪声（模拟真实脑电）

fig2, ax2 = plt.subplots(figsize=(9, 3))
ax2.plot(t3[:150], final[:150], linewidth=0.9, color="#c53030")
ax2.set_xlabel("时间 (秒)")
ax2.set_ylabel("幅值")
ax2.set_title("第 8 级：8 Hz + 13 Hz + 噪声（Alpha 波频段，就是真实脑电的样子）")
ax2.grid(alpha=0.3)
fig2.tight_layout()
fig2.savefig("stage8_alpha.png", dpi=110)
print("已保存 stage8_alpha.png —— 这就是真实脑电的样子：看不出规律")

spec2 = np.abs(np.fft.rfft(final))
freqs2 = np.fft.rfftfreq(len(final), 1.0 / 250)
mask = (freqs2 >= 1) & (freqs2 <= 40)
top = freqs2[mask][np.argsort(spec2[mask])[::-1][:3]]
print("FFT 检测到的主要频率:", np.round(sorted(top), 1), "Hz")
print()
print("→ 时域图看不出规律，FFT 之后峰就清楚了 —— 这就是 FFT 的价值")
print("→ 8-13 Hz 是 Alpha 波。想象运动时它会减弱，这叫 ERD。")
print("→ 你现在理解的东西，就是 BCI 解码的第一步。")


print()
print("=" * 64)
print(" 全部 8 级完成")
print("=" * 64)
print("""
下一步建议（不要急）：
  1. 每天重做 1 级，不看代码先猜输出是什么
  2. 改参数：f 从 10 改成 8 / 13 / 30，观察图怎么变
  3. 只有第 7 级（FFT）需要"接受它是个黑盒"，
     等大二学了《信号与系统》你会真正理解它
  4. 现在不要试图理解 FFT 的数学原理 —— 那是大二的事
""")
