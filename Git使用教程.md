# Git / GitHub 入门（写给完全零基础）

**对象**：gehanrui（南通大学 2026 级 电子信息）
**你的仓库**：https://github.com/gehanrui/learning-notes

---

## 一、一句话理解：Git 是"存档"，GitHub 是"网盘"

| 名词 | 是什么 | 类比 |
|---|---|---|
| **Git** | 装在**你电脑上**的软件，负责记录文件的历史版本 | 游戏里的**存档**功能 |
| **GitHub** | 一个**网站**，存放你上传的 Git 仓库 | **网盘** / 作品集展示柜 |
| **仓库（repository / repo）** | 一个被 Git 管理的文件夹 | 一个存档档位 |
| **commit（提交）** | 一次存档 | 存了一个档 |
| **push（推送）** | 把本地存档**上传**到 GitHub | 把存档同步到云端 |
| **pull（拉取）** | 把 GitHub 上的更新**下载**到本地 | 从云端同步下来 |

**`git push` 就是：把你在自己电脑上做的东西，上传到 GitHub 服务器。**

---

## 二、核心心智模型：三个区域

这是理解 Git 的**唯一关键**。文件在 Git 里有三个位置：

```
① 工作区              ② 暂存区              ③ 仓库（本地）        ④ GitHub（远端）
你正在编辑的文件   --add-->  准备提交的清单  --commit-->  存档记录  --push-->  云端
                    git add                git commit            git push
```

| 区域 | 含义 | 对应命令 |
|---|---|---|
| **① 工作区** | 你正在改的文件，改了 Git 就知道，但还没准备提交 | —— |
| **② 暂存区** | 你挑选出来"这次要存档的改动" | `git add` |
| **③ 本地仓库** | 已经存好的档，**只在你电脑上** | `git commit` |
| **④ GitHub** | 上传到网上的档，别人能看到 | `git push` |

**为什么要分 `add` 和 `commit` 两步？** 因为一次存档里可能只想包含部分改动。比如你同时改了 A 和 B 两个文件，但只想先存档 A——`add A` 再 `commit` 就够了。**刚开始你永远是 `git add .`（全部），不用纠结。**

---

## 三、日常五条命令（记住这五个就够用 90%）

### ① `git status` —— 先看现在什么情况

```powershell
git status
```

输出示例（你刚才的真实输出）：

```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
       每天的进度.md          ← 新文件，Git 还没管它

nothing added to commit but untracked files present
```

**养成习惯：每次操作前先 `git status`。** 它告诉你现在有什么变化。

### ② `git add .` —— 把改动放进暂存区

```powershell
git add .            # 当前目录所有改动
git add 文件名.md     # 只加某个文件
```

**没有输出是正常的。** 用 `git status --short` 可以看结果：

```
A  每天的进度.md      ← A 表示 Added（新加的）
M  某个文件.md        ← M 表示 Modified（改过的）
```

### ③ `git commit -m "说明"` —— 存档

```powershell
git commit -m "记录：GitHub 环境搭建完成"
```

输出示例：

```
[main d3d83b7] 记录：GitHub 环境搭建完成
 1 file changed, 8 insertions(+)
```

`d3d83b7` 是这个存档的**编号**（每次都不一样）。

> ⚠️ **`-m` 后面的说明必须写，而且要有意义。**
> 好的：`"项目一：完成 EMG 三分类，准确率 92%"`
> 坏的：`"更新"`、`"aaa"`、`"改了一下"`
> **导师和面试官会看你的提交记录**，糟糕的说明会显得很不专业。

### ④ `git push` —— 上传到 GitHub

```powershell
git push
```

输出示例：

```
   61be2ef..d3d83b7  main -> main
```

**到这一步，刷新 GitHub 网页才能看到更新。** 只 commit 不 push，GitHub 上是没有的。

### ⑤ `git log --oneline` —— 看历史存档

```powershell
git log --oneline
```

输出示例（你的真实历史）：

```
d3d83b7 记录：GitHub 环境搭建完成
61be2ef 修复：SSH 密钥生成参数与中文路径下的 ssh 配置
6900f9f 初始化：脑机接口学习笔记与四年计划
```

**这就是你的成长轨迹。** 四年后这个列表会很长——那正是你想要的。

---

## 四、完整流程演示（照着做一遍）

假设你写了一个 Python 练习脚本 `hello.py`，想传到 GitHub：

```powershell
# 1. 进入你的文件夹
cd E:\ai_companion

# 2. 看看现在有什么变化
git status

# 3. 把所有改动放进暂存区
git add .

# 4. 存档（写清楚这次做了什么）
git commit -m "Python 练习：画出第一条正弦波"

# 5. 上传到 GitHub
git push

# 6. 看历史确认
git log --oneline
```

**就这六步，重复四年。**

---

## 五、你的环境有个特殊配置（重要，别删）

你的 Windows 用户名是中文（`葛`），这会导致 Git 自带的 ssh 出问题。所以我们已经做了一次配置：

```powershell
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

**如果哪天 push 报错 `Permission denied (publickey)` 或 `Could not create directory '/c/Users/...`，就是这条配置丢了。** 重新执行上面这条命令即可。

查看所有全局配置：

```powershell
git config --global --list
```

---

## 六、最容易搞混的两件事

### ① 改了文件 ≠ 存档了 ≠ 上传了

| 你做了 | 电脑上有记录吗 | GitHub 上有吗 |
|---|---|---|
| 用记事本改了文件并保存 | ❌ 没有 | ❌ 没有 |
| `git add` + `git commit` | ✅ 有 | ❌ 没有 |
| 再 `git push` | ✅ 有 | ✅ 有 |

**只保存文件是不算的**，必须 commit + push。

### ② `.gitignore` 是干什么的

仓库里有个 `.gitignore` 文件，写在上面的东西**永远不会被上传**。目前已经挡住了：

- **SSH 私钥**（`id_ed25519`）—— 传上去等于把钥匙公开
- **EEG 数据集**（`*.edf`、`*.bdf`、`data/` 等）—— 文件太大，而且含被试隐私
- **模型权重**（`*.pt`、`*.pth`）—— 太大
- `__pycache__/`、`.venv/` 等临时文件

**以后你处理的脑电数据绝对不要上传**，这是学术伦理问题，不是技术问题。

---

## 七、出错了怎么办

### 场景 1：commit 的说明写错了，想改

```powershell
git commit --amend -m "改正后的说明"
```
（只能改**最近一次**，且还没 push 的话最简单）

### 场景 2：改乱了某个文件，想恢复到上次 commit 的样子

```powershell
git restore 文件名.md
```
⚠️ **会丢掉你未提交的修改**，用之前想清楚。

### 场景 3：add 错了文件，想撤出暂存区

```powershell
git restore --staged 文件名.md
```

### 场景 4：想看某个文件改了什么

```powershell
git diff 文件名.md
```

### 场景 5：想看某次提交具体改了什么

```powershell
git show d3d83b7
```

---

## 八、常见报错速查

| 报错 | 原因 | 解决 |
|---|---|---|
| `Permission denied (publickey)` | SSH 密钥没生效 / `core.sshCommand` 丢了 | 重设 `core.sshCommand`，再 `ssh -T git@github.com` 测 |
| `Could not create directory '/c/Users/...` | 中文用户名 + Git 自带 ssh | 同上，改用系统 OpenSSH |
| `Please tell me who you are` | 没配 user.name / user.email | `git config --global user.email "yd261125@qq.com"` |
| `nothing to commit, working tree clean` | 你没有改任何东西，或已提交过 | 正常，不是错误 |
| `failed to push some refs` | GitHub 上有你本地没有的提交 | 先 `git pull` 再 `git push` |
| `src refspec main does not match any` | 还没 commit 过任何东西 | 先 `git add .` + `git commit` |
| `fatal: not a git repository` | 当前目录不是仓库 | `cd` 到 `E:\ai_companion` |
| `Host key verification failed` | github.com 的主机密钥没确认 | `ssh -T git@github.com` 输入 `yes` |

---

## 九、四个必须养成的习惯

1. **每次操作前先 `git status`。**
   看清状态再动手，能避免 80% 的困惑。

2. **commit 说明写清楚。**
   这是给四年后的自己和未来的导师看的。

3. **每周至少 push 一次。**
   **空白的 GitHub 等于没有 GitHub。** 你的目标是让导师看到一个连续四年的轨迹，不是期末突击。

4. **大文件、数据、密钥绝不提交。**
   `.gitignore` 已经帮你挡了大部分，但你自己要有意识。

---

## 十、以后会用到（现在不用学）

这些概念你**现在完全不用管**，等真正需要时再学：

| 概念 | 用途 | 什么时候学 |
|---|---|---|
| **分支（branch）** | 并行开发不同功能，不影响主线 | 大三做项目时 |
| **Pull Request（PR）** | 向别人的仓库提交代码贡献 | 参与开源项目时 |
| **`git clone`** | 把别人的仓库下载到本地 | 大二读开源代码时（**这个会很快用到**） |
| **`git fork`** | 复制别人的仓库到自己账号 | 同上 |
| **GitHub Issues** | 记录待办和 bug | 项目变大时 |
| **GitHub Actions** | 自动跑测试、自动部署 | 大三以后 |
| **README 写法** | 项目介绍、结果图、复现说明 | **大一暑假做项目一时就要用** |

**最优先学会的其实是 `git clone`** —— 等你要复现 BCI 论文代码时，第一步永远是：

```powershell
git clone https://github.com/某人的仓库.git
```

---

## 十一、把 GitHub 当作品集用（这才是重点）

GitHub 不只是"网盘"。**对你的保研/考研目标，它的作用是让导师在见你之前就相信你能干活。**

| 做法 | 效果 |
|---|---|
| 每个项目一个仓库 | 导师能直接看到你的代码水平 |
| README 写清"做了什么、准确率多少、怎么复现" | 证明你的工作**可验证**，这是科研的基本素养 |
| 提交记录连续、说明清晰 | 证明你的**习惯**，不是临时突击 |
| 有结果图（混淆矩阵、准确率对比） | 一眼看出你真的跑出了结果 |

**对照南通大学推免的规则**：加分项要**公开答辩（全程录音录像）**。到时候你打开 GitHub 页面就能讲——这比口头说"我做过"强太多。

---

## 十二、下一步

环境已就绪：

- ✅ Git 2.55.0
- ✅ SSH 密钥（已加到 GitHub）
- ✅ 仓库 [learning-notes](https://github.com/gehanrui/learning-notes)
- ✅ 已推送 3 次提交

**接下来该装 Python**（Anaconda / Miniconda），这是八月份做第一个项目（EMG 手势识别）的前提。

---

*配套文档：《BCI四年计划_南通大学2026级.md》《一页速查卡.md》《环境搭建记录.md》*
