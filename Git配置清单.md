# Git + GitHub 配置清单（南通大学 2026 级 电子信息）

> 目标：让 `git` 命令可用、把 SSH 密钥配好、把第一个仓库推上 GitHub。
> 你当前**不是管理员**，所以走 PortableGit 装到用户目录，全程不需要 UAC 弹窗。

---

## 0. 前置状态（2026-02 实测）

| 项目 | 状态 |
|---|---|
| GitHub 网络（443 端口） | ✅ 通（github.com / api.github.com / ssh.github.com） |
| 本机 TLS | ✅ 正常（浏览器可正常访问 HTTPS） |
| `git` | ❌ 未安装 |
| `gh`（GitHub CLI） | ❌ 未安装 |
| 现有 SSH 密钥 | ❌ 无 `~/.ssh` 目录 |
| 管理员权限 | ❌ 无（因此用 PortableGit，不用安装包） |
| winget | ✅ 可用（需要管理员时会弹 UAC） |

---

## 1. 安装 Git（PortableGit，免管理员）

```powershell
# 1) 建目录
$base = "$env:LOCALAPPDATA\Programs\PortableGit"
New-Item -ItemType Directory -Force -Path $base | Out-Null

# 2) 查最新版下载地址
$rel = Invoke-RestMethod 'https://api.github.com/repos/git-for-windows/git/releases/latest' `
       -Headers @{ 'User-Agent' = 'setup' }
$asset = $rel.assets | Where-Object { $_.name -match 'PortableGit-.*-64-bit\.7z\.exe$' }
Write-Output $asset.browser_download_url

# 3) 下载（约 70 MB）
curl.exe -L --ssl-no-revoke -o "$env:TEMP\PortableGit.exe" $asset.browser_download_url

# 4) 自解压到目标目录
& "$env:TEMP\PortableGit.exe" -o"$base" -y

# 5) 验证
& "$base\cmd\git.exe" --version
```

**加入 PATH（当前用户，不需要管理员）**：

```powershell
$base = "$env:LOCALAPPDATA\Programs\PortableGit"
$old = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($old -notlike "*$base\cmd*") {
  [Environment]::SetEnvironmentVariable('Path', "$old;$base\cmd;$base\usr\bin", 'User')
}
```

> 之后**新开一个终端**，`git --version` 就应该有输出了。

**如果你其实是管理员**，想省事也可以：
`winget install --id Git.Git -e --source winget`

---

## 2. 配置 Git 身份

```powershell
git config --global user.name  "你的GitHub用户名"
git config --global user.email "你注册GitHub用的邮箱"
git config --global init.defaultBranch main
git config --global core.quotepath false      # 中文文件名不乱码
git config --global core.autocrlf false       # 别自动改行尾，避免跨平台混乱
git config --global pull.rebase false
git config --global credential.helper manager # 记住账号密码

# 检查
git config --global --list
```

⚠️ `user.name` 和邮箱要和你 GitHub 账号一致，否则提交记录不会算到你头上。

---

## 3. 生成 SSH 密钥（推荐用 SSH，比 HTTPS 稳）

```powershell
# 用你注册 GitHub 的邮箱
ssh-keygen -t ed25519 -C "你注册GitHub用的邮箱" -f "$env:USERPROFILE\.ssh\id_ed25519" -N '""'
```

- `-t ed25519`：现代算法，比 RSA 更短更安全
- `-f`：保存到 `C:\Users\葛\.ssh\id_ed25519`
- `-N '""'`：空密码（学习期方便；想更安全就去掉这个参数，设个密码）

**查看公钥**（复制整行，从 `ssh-ed25519` 开始到邮箱结束）：

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
```

**启动 ssh-agent 并添加密钥**（否则每次推送都要输密码）：

```powershell
Set-Service -Name ssh-agent -StartupType Automatic   # 需要管理员；失败就跳过
Start-Service ssh-agent
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
```

> 如果 `ssh-agent` 起不来（无管理员权限），不添加也能用，只是每次输密码。

---

## 4. 把公钥添加到 GitHub

1. 打开 https://github.com/settings/keys
2. 点 **New SSH key**
3. **Title** 填 `LAPTOP-S1UKVJ13`（能认出是哪台电脑就行）
4. **Key type** 选 `Authentication Key`
5. **Key** 粘贴刚才复制的整行公钥
6. 点 **Add SSH key**

**测试连接**：

```powershell
ssh -T git@github.com
```

第一次会问 `Are you sure you want to continue connecting?` → 输入 `yes`。
成功的话会显示：
`Hi 你的用户名! You've successfully authenticated, but GitHub does not provide shell access.`

---

## 5. 建第一个仓库并推上去

先在 GitHub 网页上建一个空仓库：
- 打开 https://github.com/new
- **Repository name**：`learning-notes`
- 选 **Public**（要作为作品集给导师看，必须是公开的）
- ⚠️ **不要**勾选 "Add a README file"（避免和本地冲突）
- 点 **Create repository**

然后本地：

```powershell
# 进你的工作目录
cd E:\ai_companion

# 写一个 README
@"
# learning-notes
南通大学 2026 级 电子信息 —— 学习笔记与项目记录

## 目标
脑机接口（BCI）方向：非侵入式 EEG 解码 + BCI 系统实现

## 进度
- [ ] Python 基础
- [ ] 高数 / 线代 先修
- [ ] 项目一：EMG 手势识别
- [ ] 项目二：EEG 运动想象解码
"@ | Out-File -Encoding utf8 README.md

git init
git add README.md
git commit -m "初始化：学习笔记仓库"
git branch -M main
git remote add origin git@github.com:你的用户名/learning-notes.git
git push -u origin main
```

**刷新 GitHub 页面**，你应该能看到 README 了。**这就是你的第一个作品集仓库。**

---

## 6. 日常使用（记住这 5 条就够）

```powershell
git status                 # 看哪些文件改了
git add .                  # 把所有改动加入暂存
git commit -m "说明改了什么"  # 提交
git push                   # 推到 GitHub
git log --oneline          # 看提交历史
```

**建议节奏**：每周至少提交 1 次。**空白的 GitHub 等于没有 GitHub。**

---

## 7. 你的目标仓库结构（四年后应该长这样）

```
learning-notes/          ← 学习笔记
emg-gesture/             ← 项目一（大一暑假）
eeg-motor-imagery/       ← 项目二（大二暑假）★ 最重要
ssvep-speller/           ← 项目三（大三下）
bci-paper-notes/         ← 论文笔记
```

每个项目仓库都要有 **README + 代码 + 结果图 + 复现说明**。
导师和面试官只看 GitHub，不看你说什么。

---

## 8. 常见坑

| 问题 | 解决 |
|---|---|
| `git` 命令找不到 | 关掉终端重开；或检查 PATH 是否加对 |
| `Permission denied (publickey)` | 公钥没加到 GitHub，或 ssh-agent 没加载密钥 |
| `Connection timed out` 到 22 端口 | SSH 走 443：`ssh -T -p 443 git@ssh.github.com` |
| 推送要输密码但一直失败 | GitHub 不支持密码推送；必须用 SSH 密钥或 Personal Access Token |
| 中文文件名显示乱码 | `git config --global core.quotepath false` |
| 提交记录不算到自己账号 | `user.email` 和 GitHub 账号邮箱不一致 |

---

*本清单与《BCI四年计划_南通大学2026级.md》配套使用。*
