"""
savefig 实验 —— 一张图，导出成四种格式
==========================================

目的：搞清楚 fig.savefig() 到底在干什么，以及为什么要学它。

运行：
    $env:PYTHONIOENCODING='utf-8'
    python savefig实验.py

运行后会在当前目录生成四个文件，你可以对比看差别。
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 让中文正常显示
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 注意：网上有些人会写 plt.rcParams["savefig.metadata"] = {...}
# 来"固定图片元数据"。但在 matplotlib 3.11 里没有这个 rcParam，会直接 KeyError。
# 实测（3.11.2）：同一个 figure 连续 savefig 两次，PNG 的 SHA256 本来就一致，
# 不需要任何额外设置。这里就不再画蛇添足了。

print("=" * 60)
print(" savefig 实验")
print("=" * 60)

# ---------- 1. 造数据：一段 8 Hz 的 Alpha 波 ----------
fs = 250.0
t = np.arange(0, 1.0, 1.0 / fs)
signal = 1.0 * np.sin(2 * np.pi * 8 * t) + 0.3 * np.random.default_rng(0).standard_normal(t.size)

# ---------- 2. 画图（这一段是"画什么"） ----------
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(t[:200], signal[:200], linewidth=0.9)
ax.set_xlabel("时间 (秒)")
ax.set_ylabel("幅值")
ax.set_title("8 Hz Alpha 波（带噪声）")
ax.grid(alpha=0.3)
fig.tight_layout()

print("""
画图和保存是两个独立步骤：

    fig, ax = plt.subplots(...)      ← 创建画布
    ax.plot(...)                     ← 往上画东西
    fig.savefig("图.png")            ← 存成文件

注意：到 savefig 之前，这张图只存在于"内存"里，磁盘上什么都没有。
""")

# ---------- 3. 同一张图，存成四种格式 ----------
print("=" * 60)
print(" 导出四种格式（代码完全一样，只改文件名）")
print("=" * 60)

files = [
    ("savefig_示例.png",  "PNG  位图，日常看图用，GitHub 上也是这个"),
    ("savefig_示例.svg",  "SVG  矢量图，放大不糊，放论文用"),
    ("savefig_示例.pdf",  "PDF  矢量图，投稿期刊常用"),
    ("savefig_示例_高清.png", "PNG + dpi=300，分辨率更高，文件更大"),
]

fig.savefig("savefig_示例.png")
fig.savefig("savefig_示例.svg")
fig.savefig("savefig_示例.pdf")
fig.savefig("savefig_示例_高清.png", dpi=300)

import os
for name, desc in files:
    size = os.path.getsize(name)
    print(f"  {name:<24} {size/1024:>7.1f} KB   {desc}")

print("""
→ 观察重点：
  1. .svg 和 .pdf 通常比 .png 小（矢量图只存"线条"，不存"像素"）
  2. dpi 越高，PNG 文件越大（存的像素更多）
  3. 用图片查看器打开 png，用浏览器打开 svg —— 都试试，感受差别
""")

# ---------- 4. 常用参数演示 ----------
print("=" * 60)
print(" 常用参数")
print("=" * 60)

# dpi：分辨率
fig.savefig("savefig_dpi100.png", dpi=100)
fig.savefig("savefig_dpi300.png", dpi=300)
print(f"  dpi=100  → {os.path.getsize('savefig_dpi100.png')/1024:.1f} KB")
print(f"  dpi=300  → {os.path.getsize('savefig_dpi300.png')/1024:.1f} KB")
print("  → dpi 翻 3 倍，文件大很多。屏幕看图用 100-150，论文用 300")

# bbox_inches：裁掉多余白边
fig.savefig("savefig_有白边.png")
fig.savefig("savefig_紧边距.png", bbox_inches="tight")
print()
print("  savefig_有白边.png   ← 默认，四周有留白")
print("  savefig_紧边距.png   ← bbox_inches='tight'，白边被裁掉")
print("  → 放进论文或 PPT 时用 'tight'，避免图片周围一圈空白")

# transparent：透明背景
fig.savefig("savefig_透明.png", transparent=True)
print()
print("  savefig_透明.png     ← 背景透明，叠在深色 PPT 上不会出现白框")

print()
print("=" * 60)
print(" 总结：以后你只需要记住这一行")
print("=" * 60)
print("""
    fig.savefig("文件名.png", dpi=150, bbox_inches="tight")

    - 文件名：扩展名决定格式（.png / .svg / .pdf）
    - dpi：清晰度（屏幕 100-150，论文 300）
    - bbox_inches="tight"：去掉多余白边

其他参数需要时再查：https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
""")


# ============================================================
# 实测补充：三种格式在 git 里的表现不同
# ============================================================
# 同一个 figure 反复 savefig：
#   PNG  → 字节完全一致（三次哈希相同），适合提交到 git
#   SVG  → 每次字节都不同（内容一样但序列化有差异），会产生无意义的 git 差异
#   PDF  → 同样可能每次不同
#
# 实用结论：
#   - 要提交到 GitHub 的结果图  → 用 PNG
#   · 放进论文/PPT              → 用 SVG 或 PDF，但不必都提交