# VS Code 已配置完成（2026-10-05）

## 装好了什么

| 项目 | 状态 |
|---|---|
| **VS Code** | 1.140.0（用户版，装在 `C:\Users\葛\AppData\Local\Programs\Microsoft VS Code`） |
| **中文语言包** | `ms-ceintl.vscode-language-pack-zh-hans` ✅ 界面已是中文 |
| **Python 扩展** | `ms-python.python` v2026.6.0 ✅ |
| Pylance（代码补全） | `ms-python.vscode-pylance` v2026.4.1 ✅ |
| 调试器 | `ms-python.debugpy` v2026.6.0 ✅ |
| Python 环境管理 | `ms-python.vscode-python-envs` v1.38.0 ✅ |
| **解释器已锁定** | `D:\p\python.exe`（Python 3.13.9） |
| **.py 文件关联** | 双击 `.py` 直接打开 VS Code ✅ |

## 已经帮你设好的配置

写在 `C:\Users\葛\AppData\Roaming\Code\User\settings.json`：

| 设置 | 值 | 为什么 |
|---|---|---|
| `python.defaultInterpreterPath` | `D:\p\python.exe` | **关键。** 你系统里有个微软商店的假 Python（`WindowsApps\python.exe`，0 字节），不锁死会选错导致运行失败 |
| `terminal.integrated.env.windows` | `PYTHONIOENCODING=utf-8` | **解决中文乱码**，以后不用手动敲那行编码命令 |
| `files.autoSave` | `afterDelay`（1 秒） | 自动保存，避免"改了代码忘了存"这个最常见的坑 |
| `editor.wordWrap` | `on` | 长行自动换行，看代码不用横向滚动 |
| `editor.fontSize` | 14 | 舒服的字号 |
| `git.autofetch` | `true` | 自动同步 GitHub 状态 |

## 现在怎么打开

**方式一（推荐）**：文件资源管理器 → 地址栏输入 `E:\ai_companion` → 回车 → 地址栏再输入 `code .` → 回车
（注意 `code` 后面有个空格和**点**，表示"用 VS Code 打开当前文件夹"）

**方式二**：开始菜单搜 `Visual Studio Code` → 打开 → 文件 → 打开文件夹 → 选 `E:\ai_companion`

**方式三**：右键任意 `.py` 文件 → 打开方式 → Visual Studio Code

> `code` 命令在新开的终端里才可用（PATH 已配好，但当前已开的终端不认）。

## 打开后做两件事

### 1. 确认解释器选对了

按 `Ctrl + Shift + P` → 输入 `Python: Select Interpreter` → 回车

**应该看到并选中 `D:\p\python.exe`**（Python 3.13.9）。

如果看到的是 `WindowsApps` 那个，**不要选它**——那是个空壳，选了会报错。

### 2. 运行第一个脚本

1. 打开 `python_分阶练习.py`
2. 点**右上角的 ▶ 三角按钮**
3. 下方会弹出"终端"面板，输出就显示在那里

**首次运行 VS Code 可能会提示"选择 Python 环境"或问你是否信任此文件夹**——选"是/信任"，那是正常的安全提示（因为文件夹里有 `.py` 文件）。

## 界面速览（常用的四个区域）

```
┌──────────┬────────────────────────────┬──────────┐
│ 活动栏   │  编辑区（代码在这里）       │  预览    │
│ (左侧)   │                            │          │
│ 文件     │                            │          │
│ 搜索     │                            │          │
│ 源代码   │                            │          │
│ 调试     │                            │          │
│ 扩展     │                            │          │
└──────────┴────────────────────────────┴──────────┘
                    终端面板（输出显示在这）
```

| 快捷键 | 作用 |
|---|---|
| `Ctrl + S` | 保存（现在会自动保存，但习惯还是要养成） |
| `Ctrl + ~` | 打开/关闭终端面板 |
| `Ctrl + Shift + P` | 命令面板（不知道功能在哪就按这个搜） |
| `Ctrl + B` | 显示/隐藏左侧栏 |
| `Ctrl + Z` | 撤销（改代码改坏了救回来） |
| `F5` | 调试运行 |
| `Ctrl + F` | 在当前文件里搜索 |

## 接下来

按《Python与VSCode学习指南.md》的计划走：

| 天 | Python 20 分钟做什么 |
|---|---|
| **Day 1（今天）** | ~~装 VS Code~~ ✅ **已完成，直接跳到 Day 2 的内容** |
| Day 2 | 视频学：print、变量、数据类型 |
| Day 3 | 视频学：input、if/else |
| Day 4 | 视频学：for、while |
| Day 5 | 视频学：列表 |
| Day 6 | 视频学：函数 def |
| Day 7 | 自己动手写"猜数字游戏" |

**今天环境已经装完，你可以提前开始 Day 2 的内容，或者把今天当作休息日。**

## 一个提醒

你 Downloads 里有个 `TraeCode_CN-Setup-x64.exe`（字节的 AI 编辑器，2026/9/6 下载的，361 MB）。它也是 VS Code 内核，能用，而且自带 AI 助手。**但建议先用原版 VS Code**，原因：

1. 你以后复现 BCI 论文代码、看 GitHub 项目说明，**教程都是按 VS Code 写的**
2. 原版插件生态最全（MNE、Jupyter 等都优先支持）
3. TraeCode 可以留着以后当"AI 辅助工具"用，不冲突

---

*配套文档：《Python与VSCode学习指南.md》《怎么运行Python脚本.md》《第一周任务.md》*
