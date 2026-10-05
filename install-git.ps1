# 下载并安装 PortableGit（github.com 被阻断，走多个国内镜像）
# 关键点：不用 curl -sS（它的 stderr 会被 PowerShell 当成致命错误），
#         改用 .NET WebClient，并显式启用 TLS 1.2。
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$GitBase = "$env:LOCALAPPDATA\Programs\PortableGit"
$GitExe  = "$GitBase\cmd\git.exe"

if (Test-Path $GitExe) {
    Write-Output "Git 已存在: $(& $GitExe --version)"
    exit 0
}

Write-Output "=== 取下载地址（api.github.com 是通的） ==="
try {
    $rel = Invoke-RestMethod 'https://api.github.com/repos/git-for-windows/git/releases/latest' `
           -Headers @{ 'User-Agent' = 'setup' } -TimeoutSec 60
} catch {
    Write-Output "取版本信息失败: $($_.Exception.Message)"
    exit 1
}
$asset = $rel.assets | Where-Object { $_.name -match 'PortableGit-.*-64-bit\.7z\.exe$' } | Select-Object -First 1
if (-not $asset) { Write-Output "未找到 PortableGit 资源"; exit 1 }

Write-Output "版本: $($rel.tag_name)"
Write-Output "文件: $($asset.name)  ($([math]::Round($asset.size/1MB,1)) MB)"

$original = $asset.browser_download_url
$mirrors = @(
    "https://ghfast.top/$original",
    "https://ghproxy.net/$original",
    "https://gh-proxy.com/$original",
    "https://gh.llkk.cc/$original",
    "https://ghproxy.cc/$original",
    $original
)

$tmp = "$env:TEMP\PortableGit-setup.exe"
$expected = $asset.size
$ok = $false

foreach ($url in $mirrors) {
    $short = $url.Substring(0, [Math]::Min(58, $url.Length))
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        Write-Output "`n尝试 [$short] 第 $attempt 次"
        if (Test-Path $tmp) { Remove-Item $tmp -Force -ErrorAction SilentlyContinue }
        try {
            $wc = New-Object System.Net.WebClient
            $wc.Headers.Add('User-Agent', 'setup')
            $wc.DownloadFile($url, $tmp)
            $size = (Get-Item $tmp).Length
            Write-Output ("  下载完成 {0:N1} MB" -f ($size / 1MB))
            if ($size -ge ($expected * 0.98)) { $ok = $true; break }
            Write-Output "  文件大小不足，换源重试"
        } catch {
            Write-Output "  失败: $($_.Exception.Message)"
        }
    }
    if ($ok) { break }
}

if (-not $ok) {
    Write-Output "`n所有镜像都失败。请手动下载安装：https://git-scm.com/download/win"
    exit 1
}

Write-Output "`n=== 解压到 $GitBase ==="
New-Item -ItemType Directory -Force -Path $GitBase | Out-Null
& $tmp -o"$GitBase" -y | Out-Null
$rc = $LASTEXITCODE
Remove-Item $tmp -Force -ErrorAction SilentlyContinue

if (-not (Test-Path $GitExe)) {
    Write-Output "解压后未找到 git.exe（解压返回码 $rc）"
    exit 1
}

Write-Output "安装成功: $(& $GitExe --version)"

# 加入当前用户 PATH（不需要管理员）
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($userPath -notlike "*$GitBase\cmd*") {
    [Environment]::SetEnvironmentVariable('Path', "$userPath;$GitBase\cmd;$GitBase\usr\bin", 'User')
    Write-Output "已加入用户 PATH（新终端生效）"
} else {
    Write-Output "PATH 已包含 Git"
}
exit 0
