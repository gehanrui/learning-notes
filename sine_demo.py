"""
第一个信号处理练习：时域 → FFT → 频域
=========================================

这个脚本看起来简单，但它就是脑机接口（BCI）里最核心的动作。

为什么重要：
    运动想象 EEG 解码的第一步，永远是"把时域信号变成频域/功率谱"。
    Alpha 波（8-13 Hz）在想象运动时会减弱，这叫 ERD（事件相关去同步）。
    你要能看出"哪个频率的能量变了"，才能做 BCI。
    而"看出频率"这件事，靠的就是 FFT。

运行方式：
    python sine_demo.py
输出：
    fig1_sine_wave.png   时域图
    fig2_spectrum.png    频域图
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")          # 不弹窗口，直接存文件（适合脚本运行）
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 0. 让中文能正常显示（否则图上中文会变成方框）
# ---------------------------------------------------------------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def make_signal(freqs, amps, fs=250.0, duration=2.0, noise=0.5, seed=0):
    """
    造一个"合成脑电信号"。

    参数
    ----
    freqs   : 各个成分的频率（Hz）
    amps    : 对应的振幅
    fs      : 采样率（Hz）。EEG 常用 250 或 500 Hz
              为什么至少 250？奈奎斯特采样定理：fs 必须 > 2×最高频率
    duration: 信号时长（秒）
    noise   : 噪声强度（模拟真实的脑电噪声）
    seed    : 随机种子，保证每次运行结果一样（科研必须可复现）
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, duration, 1.0 / fs)          # 时间轴

    signal = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        signal += a * np.sin(2 * np.pi * f * t)   # 叠加各个频率成分

    signal += noise * rng.standard_normal(t.size)  # 加噪声
    return t, signal


def compute_spectrum(signal, fs):
    """
    对信号做 FFT，得到频率和对应的振幅。

    这是整个 BCI 领域用得最多的一段代码。
    """
    n = signal.size
    fft_vals = np.fft.rfft(signal)                 # 实数信号的 FFT
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)         # 每个点对应的频率

    # 归一化：让振幅的数值有物理意义（不然会随信号长度变化）
    amplitude = np.abs(fft_vals) / n
    amplitude[1:-1] *= 2                           # 除直流和奈奎斯特外都要乘 2
    return freqs, amplitude


def main():
    FS = 250.0                     # 采样率 250 Hz（EEG 常用）
    TRUE_FREQS = [10.0, 23.0]      # 我偷偷埋进去的两个频率
    TRUE_AMPS = [1.0, 0.6]

    print("=" * 60)
    print("第一个信号处理练习")
    print("=" * 60)
    print(f"采样率      : {FS} Hz")
    print(f"真实频率    : {TRUE_FREQS} Hz  ← 我埋进去的，看脚本能不能找回来")
    print()

    # ---- 1. 造信号 ----
    t, sig = make_signal(TRUE_FREQS, TRUE_AMPS, fs=FS, duration=2.0, noise=0.5)
    print(f"信号长度    : {sig.size} 个采样点（{t[-1]:.1f} 秒 × {FS} Hz）")

    # ---- 2. 时域图 ----
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(t[:500], sig[:500], linewidth=0.9, color="#2b6cb0")
    ax.set_xlabel("时间 (秒)")
    ax.set_ylabel("幅值")
    ax.set_title("时域波形（只看前 2 秒里的前 500 个点）")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("fig1_sine_wave.png", dpi=120)
    print("\n[输出] fig1_sine_wave.png  —— 时域图")
    print("       注意：光看这张图，你完全看不出里面有 10 Hz 和 23 Hz")

    # ---- 3. FFT 找频率 ----
    freqs, amp = compute_spectrum(sig, FS)

    # ---- 4. 频域图 ----
    fig2, ax2 = plt.subplots(figsize=(10, 3.5))
    ax2.plot(freqs, amp, linewidth=1.2, color="#c53030")
    ax2.set_xlim(0, 60)
    ax2.set_xlabel("频率 (Hz)")
    ax2.set_ylabel("振幅")
    ax2.set_title("频域（FFT 之后）—— 峰在哪里，频率就在哪里")
    ax2.grid(alpha=0.3)

    for f, a in zip(TRUE_FREQS, TRUE_AMPS):
        ax2.axvline(f, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
        ax2.annotate(f"{f:.0f} Hz", xy=(f, a), xytext=(f + 1.5, a + 0.05),
                     fontsize=10, color="#2d3748")
    fig2.tight_layout()
    fig2.savefig("fig2_spectrum.png", dpi=120)
    print("[输出] fig2_spectrum.png    —— 频域图")

    # ---- 5. 自动找出峰值频率（这才是能用的算法） ----
    # 只看 1-50 Hz 范围（EEG 关心的频段，也避开直流分量）
    mask = (freqs >= 1) & (freqs <= 50)
    f_band, a_band = freqs[mask], amp[mask]

    # 找局部极大值，按振幅排序，取前 2 个
    order = np.argsort(a_band)[::-1]
    peaks = []
    for idx in order:
        f = f_band[idx]
        if all(abs(f - p) > 2.0 for p in peaks):   # 峰之间至少隔 2 Hz
            peaks.append(f)
        if len(peaks) == 2:
            break

    print()
    print("=" * 60)
    print("FFT 自动检测到的频率：")
    for i, p in enumerate(sorted(peaks), 1):
        print(f"  第 {i} 个峰: {p:.1f} Hz")
    print(f"真实频率        : {TRUE_FREQS}")
    print("=" * 60)

    err = max(abs(sorted(peaks)[i] - TRUE_FREQS[i]) for i in range(2))
    print(f"\n最大误差: {err:.2f} Hz")

    if err < 2.0:
        print("\n✅ 成功！你的环境完全可用。")
        print("   你刚刚做的事，和 BCI 里分析脑电功率谱是同一件事。")
    else:
        print("\n⚠️ 误差偏大，检查一下采样率设置。")

    print("\n下一步（这就是你大一上的任务）：")
    print("  1. 把 TRUE_FREQS 改成 [8.0, 13.0]，看看还能不能找回来")
    print("     —— 8-13 Hz 就是 Alpha 波，BCI 里最重要的频段之一")
    print("  2. 把 noise 从 0.5 改成 3.0，观察峰还清不清楚")
    print("     —— 这就是真实脑电的困境：信号弱、噪声大")
    print("  3. 把 FS 改成 30 Hz，看 23 Hz 还能不能检测出来")
    print("     —— 验证奈奎斯特采样定理")


if __name__ == "__main__":
    main()
