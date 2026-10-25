r"""
运放入门演示：为什么需要放大
=============================

零基础看懂运放的第一步，不是看 datasheet，是理解"放大"这件事本身。

这个脚本做一件事：
    把一条"微弱的脑电信号"画出来，再把"放大后"的信号画出来，
    让你亲眼看到运放到底在干什么。

运行：
    $env:PYTHONIOENCODING='utf-8'
    python 运放入门演示.py

看懂这个图，你就理解了运放存在的唯一理由。
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------
# 造一条"脑电信号"
# ---------------------------------------------------------------
fs = 250.0                      # 采样率 250 Hz（EEG 常用）
t = np.arange(0, 2.0, 1/fs)     # 2 秒

# 脑电信号的量级：几十微伏
# 这里模拟 10 Hz 的 alpha 波，幅度 50 微伏
eeg_uV = 50e-6 * np.sin(2 * np.pi * 10 * t)
eeg_uV += 5e-6 * np.random.default_rng(0).standard_normal(t.size)   # 加一点噪声

# ---------------------------------------------------------------
# 运放的放大作用
# ---------------------------------------------------------------
GAIN = 100000                   # 放大倍数：10 万倍
amplified_V = eeg_uV * GAIN     # 结果单位变成伏特

print("=" * 62)
print(" 运放干的事：放大")
print("=" * 62)
print()
print(f"  原始脑电信号幅度:  {np.max(np.abs(eeg_uV))*1e6:.1f} 微伏 (μV)")
print(f"  换算成伏特:        {np.max(np.abs(eeg_uV)):.8f} V")
print()
print(f"  放大倍数:          {GAIN:,} 倍")
print(f"  放大后幅度:        {np.max(np.abs(amplified_V)):.3f} 伏特 (V)")
print()
print("  ★ 关键对比：")
print(f"     原始: {np.max(np.abs(eeg_uV)):.8f} V  ← 太小了，ADC 读不出来")
print(f"     放大: {np.max(np.abs(amplified_V)):.3f} V  ← 可以采集了")
print()

# ---------------------------------------------------------------
# 画图
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(10, 7))

# 上图：原始信号
ax1 = axes[0]
ax1.plot(t, eeg_uV * 1e6, linewidth=0.8, color="#c53030")
ax1.set_ylabel("电压 (微伏 μV)")
ax1.set_title("① 电极测到的原始脑电信号 —— 幅度只有几十微伏")
ax1.grid(alpha=0.3)
ax1.set_xlabel("时间 (秒)")
ax1.text(0.02, 0.95, "这个信号如果直接送给 ADC，会被噪声淹没",
         transform=ax1.transAxes, fontsize=10, va="top",
         bbox=dict(boxstyle="round", facecolor="#fff5f5", alpha=0.9))

# 下图：放大后
ax2 = axes[1]
ax2.plot(t, amplified_V, linewidth=0.8, color="#2b6cb0")
ax2.set_ylabel("电压 (伏特 V)")
ax2.set_title(f"② 经过运放放大 {GAIN:,} 倍之后 —— 可以用来采集了")
ax2.grid(alpha=0.3)
ax2.set_xlabel("时间 (秒)")
ax2.text(0.02, 0.95, f"波形完全一样，只是幅度变大了 {GAIN:,} 倍",
         transform=ax2.transAxes, fontsize=10, va="top",
         bbox=dict(boxstyle="round", facecolor="#f0f7ff", alpha=0.9))

fig.suptitle("运放的作用：把微弱的信号放大到能用的程度", fontsize=14)
fig.tight_layout()
fig.savefig("运放_放大示意.png", dpi=110, bbox_inches="tight")
print("  已保存: 运放_放大示意.png")
print()

# ---------------------------------------------------------------
print("=" * 62)
print(" 这就是运放存在的全部理由")
print("=" * 62)
print("""
  电极贴在头骨上，测到的电压只有 10 ~ 100 微伏（μV）。

  1 微伏 = 0.000001 伏特

  而常见的 ADC（模数转换器）需要 0 ~ 3.3 伏的输入才能工作。
  也就是说：信号至少要放大几万倍。

  干这件事的器件，就是【运算放大器】。

  你的脑机接口目标，第一道硬件关卡就是这个。

  所以你那篇报告的结论可以这样写（用自己的话）：
     "运放是生物电信号采集链路的第一个环节。脑电信号量级极小，
      必须经过低噪声、高共模抑制比的放大，才能被后续电路处理。"

""" + "=" * 62)

# ---------------------------------------------------------------
print()
print("=" * 62)
print(" 下一步做什么")
print("=" * 62)
print("""
  现在你知道"为什么需要运放"了。下一步是"运放怎么做到放大"。

  推荐顺序（不要跳到 datasheet）：
    1. 看一个 10 分钟的科普视频：B站搜「运算放大器 通俗」
    2. 打开 Falstad 电路仿真器（浏览器就能用）：
       https://www.falstad.com/circuit/circuitjs.html
       在 Examples 里找 Op-Amp，能看到电压实时变化
    3. 手算一个反相放大器：
       Vout = -(R2/R1) × Vin
       取 R1=1kΩ, R2=10kΩ, Vin=0.1V → Vout = -1V
       再到 Falstad 里搭出来，对一下答案

  做完这三步，你再看 datasheet 的"输入失调电压""CMRR"，就看得懂了。
""")
