# ============================================================
#  GitHub 一键配置脚本
#  南通大学 2026 级 电子信息 —— 脑机接口路线
#
#  用法：右键本文件 → "使用 PowerShell 运行"
#       或在终端里执行：  pwsh -NoProfile -File .\setup-github.ps1
#
#  它会做完这些事（全程不需要管理员，不弹 UAC）：
#    1. 下载 PortableGit 到你的用户目录
#    2. 生成 SSH 密钥（ed25519）
#    3. 配置 git 身份
#    4. 把本目录初始化成 git 仓库
#    5. 打印公钥和后续命令
#
#  重要：私钥绝不要提交到 GitHub。本目录的 .gitignore 已经挡掉了。
# ============================================================

$ErrorActionPreference = 'Stop'
$GitHubUser = 'gehanrui'

# 邮箱：优先用传入的，其次问你，最后退回用户名
$GitHubMail = $env:DSH_GITHUB_MAIL
if ([string]::IsNullOrWhiteSpace($GitHubMail)) {
    Write-Host ""
    Write-Host "请输入你注册 GitHub 用的邮箱（直接回车 = 跳过，之后可手动补）：" -ForegroundColor Cyan
    $GitHubMail = (Read-Host "邮箱").Trim()
}
if ([string]::IsNullOrWhiteSpace($GitHubMail)) {
    $GitHubMail = $null
    Write-Host "已跳过邮箱设置。注意：提交记录不会归属到你的 GitHub 账号。" -ForegroundColor Yellow
}

$GitBase = "$env:LOCALAPPDATA\Programs\PortableGit"
$GitExe  = "$GitBase\cmd\git.exe"
$SshDir  = "$env:USERPROFILE\.ssh"
$KeyPath = "$SshDir\id_ed25519"

function Step($n, $t) { Write-Host "`n[$n] $t" -ForegroundColor Cyan }
function Ok($t)   { Write-Host "    OK  $t" -ForegroundColor Green }
function Warn($t) { Write-Host "    注意 $t" -ForegroundColor Yellow }

Write-Host "============================================" -ForegroundColor White
Write-Host " GitHub 一键配置（GitHub 用户：$GitHubUser）" -ForegroundColor White
Write-Host "============================================" -ForegroundColor White

# ---------- 1. 安装 PortableGit ----------
Step 1 "检查 / 安装 Git"

if (Test-Path $GitExe) {
    Ok "Git 已安装：$(& $GitExe --version)"
} else {
    Write-Host "    未检测到 Git，开始下载 PortableGit（约 70 MB，国内可能较慢）..."
    New-Item -ItemType Directory -Force -Path $GitBase | Out-Null

    $rel = Invoke-RestMethod 'https://api.github.com/repos/git-for-windows/git/releases/latest' `
           -Headers @{ 'User-Agent' = 'setup' } -TimeoutSec 60
    $asset = $rel.assets | Where-Object { $_.name -match 'PortableGit-.*-64-bit\.7z\.exe$' } | Select-Object -First 1
    if (-not $asset) { throw "找不到 PortableGit 下载地址，请手动安装：https://git-scm.com/download/win" }

    $tmp = "$env:TEMP\PortableGit-setup.exe"
    Write-Host "    下载 $($asset.name) ..."
    curl.exe -L --ssl-no-revoke -o $tmp $asset.browser_download_url
    if (-not (Test-Path $tmp)) { throw "下载失败。可尝试手动安装：winget install --id Git.Git -e" }

    Write-Host "    解压到 $GitBase ..."
    & $tmp -o"$GitBase" -y | Out-Null
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue

    if (-not (Test-Path $GitExe)) { throw "解压后仍未找到 git.exe" }
    Ok "Git 安装完成：$(& $GitExe --version)"
}

# 加入 PATH（仅当前用户，不需要管理员）
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($userPath -notlike "*$GitBase\cmd*") {
    [Environment]::SetEnvironmentVariable('Path', "$userPath;$GitBase\cmd;$GitBase\usr\bin", 'User')
    Ok "已加入用户 PATH（新开的终端才生效）"
} else {
    Ok "PATH 已包含 Git"
}
$env:Path = "$GitBase\cmd;$GitBase\usr\bin;$env:Path"

# ---------- 2. 生成 SSH 密钥 ----------
Step 2 "SSH 密钥"

if (-not (Test-Path $SshDir)) { New-Item -ItemType Directory -Force -Path $SshDir | Out-Null }

if (Test-Path $KeyPath) {
    Warn "密钥已存在，跳过生成：$KeyPath"
} else {
    # 注意：空密码要传真空参数，写成 '""' 会变成两个引号字符
    & ssh-keygen -t ed25519 -C $GitHubUser -f $KeyPath -N "" | Out-Null
    if (-not (Test-Path "$KeyPath.pub")) { throw "密钥生成失败" }
    Ok "已生成 $KeyPath"
}

# 尝试加载到 ssh-agent（失败不影响使用）
try {
    Start-Service ssh-agent -ErrorAction Stop
    & ssh-add $KeyPath 2>$null | Out-Null
    Ok "密钥已加载到 ssh-agent"
} catch {
    Warn "ssh-agent 未启动（无管理员权限）。不影响使用，但每次推送可能要输密钥密码。"
}

# ---------- 3. 配置 git 身份 ----------
Step 3 "git 身份配置"

& $GitExe config --global user.name  $GitHubUser
if (-not [string]::IsNullOrWhiteSpace($GitHubMail)) {
    & $GitExe config --global user.email $GitHubMail
    Ok "user.email = $GitHubMail"
} else {
    & $GitExe config --global user.email "$GitHubUser@users.noreply.github.com"
    Warn "未填邮箱，已临时用 $GitHubUser@users.noreply.github.com"
    Write-Host "         注册好账号后建议改成真实邮箱：" -ForegroundColor Yellow
    Write-Host "         git config --global user.email `"你的邮箱`"" -ForegroundColor Yellow
}

& $GitExe config --global init.defaultBranch main
& $GitExe config --global core.quotepath false       # 中文文件名不乱码
& $GitExe config --global core.autocrlf false
& $GitExe config --global pull.rebase false
Ok "已写入全局配置"

# ---------- 4. 初始化本地仓库 ----------
Step 4 "初始化本地仓库"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
try {
    if (-not (Test-Path "$here\.git")) {
        & $GitExe init | Out-Null
        Ok "已初始化 $here"
    } else {
        Ok "已是 git 仓库"
    }
    & $GitExe add -A
    & $GitExe commit -m "初始化：学习笔记仓库" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Ok "已创建首次提交"
    } else {
        Warn "没有需要提交的内容，或提交失败（可手动执行 git commit）"
    }

    $remote = & $GitExe remote get-url origin 2>$null
    if (-not $remote) {
        & $GitExe remote add origin "git@github.com:$GitHubUser/learning-notes.git"
        Ok "已设置 remote origin"
    } else {
        Ok "remote origin 已存在：$remote"
    }
} finally {
    Pop-Location
}

# ---------- 5. 打印后续步骤 ----------
Write-Host "`n============================================" -ForegroundColor White
Write-Host " 还差两步，需要你手动做" -ForegroundColor White
Write-Host "============================================" -ForegroundColor White

Write-Host "`n步骤 A：把下面这一整行公钥贴到 GitHub" -ForegroundColor Cyan
Write-Host "  打开 https://github.com/settings/keys  →  New SSH key" -ForegroundColor Gray
Write-Host ""
Get-Content "$KeyPath.pub" -ErrorAction SilentlyContinue
Write-Host ""

Write-Host "步骤 B：在 GitHub 网页上建空仓库" -ForegroundColor Cyan
Write-Host "  https://github.com/new" -ForegroundColor Gray
Write-Host "  仓库名填：learning-notes" -ForegroundColor Gray
Write-Host "  选 Public，不要勾 Add a README file" -ForegroundColor Gray

Write-Host "`n然后回来在这个目录执行：" -ForegroundColor Cyan
Write-Host "  ssh -T git@github.com          # 看到 Hi $GitHubUser! 就说明密钥通了" -ForegroundColor Gray
Write-Host "  git push -u origin main        # 推送" -ForegroundColor Gray
Write-Host "`n如果 22 端口被墙，改用 443：" -ForegroundColor Yellow
Write-Host "  ssh -T -p 443 git@ssh.github.com" -ForegroundColor Gray
Write-Host ""
