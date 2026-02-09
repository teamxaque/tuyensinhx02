# Git Setup and Push Script
# Hướng dẫn push code lên GitHub

Write-Host "🚀 OpenAI Agent Chat - GitHub Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Git đã được cài đặt chưa
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git chưa được cài đặt!" -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Git từ: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git đã được cài đặt" -ForegroundColor Green

# Kiểm tra file .env có tồn tại không
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  File .env chưa tồn tại!" -ForegroundColor Yellow
    Write-Host "Tạo file .env từ template..." -ForegroundColor Yellow
    Copy-Item ".env.template" ".env"
    Write-Host "✅ Đã tạo file .env" -ForegroundColor Green
    Write-Host "⚠️  Vui lòng thêm OPENAI_API_KEY vào file .env trước khi tiếp tục!" -ForegroundColor Yellow
    Read-Host "Nhấn Enter sau khi đã cập nhật .env"
}

# Kiểm tra .env có chứa API key thật chưa
$envContent = Get-Content ".env" -Raw
if ($envContent -match "YOUR_OPENAI_API_KEY") {
    Write-Host "⚠️  File .env vẫn chứa placeholder!" -ForegroundColor Yellow
    Write-Host "Vui lòng thay YOUR_OPENAI_API_KEY bằng API key thật!" -ForegroundColor Yellow
    $continue = Read-Host "Bạn có muốn tiếp tục không? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

Write-Host ""
Write-Host "📝 Cấu hình Git..." -ForegroundColor Cyan

# Kiểm tra Git đã được khởi tạo chưa
if (-not (Test-Path ".git")) {
    Write-Host "Khởi tạo Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Đã khởi tạo Git repository" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository đã tồn tại" -ForegroundColor Green
}

# Hỏi thông tin GitHub repository
Write-Host ""
Write-Host "📦 Thông tin GitHub Repository" -ForegroundColor Cyan
Write-Host "Vui lòng tạo repository mới trên GitHub: https://github.com/new" -ForegroundColor Yellow
Write-Host ""

$repoUrl = Read-Host "Nhập URL của GitHub repository (ví dụ: https://github.com/username/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ URL không hợp lệ!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Chuẩn bị commit..." -ForegroundColor Cyan

# Add all files
git add .

# Commit
$commitMessage = Read-Host "Nhập commit message (Enter để dùng mặc định: 'Initial commit')"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit: OpenAI Agent Chat Interface"
}

git commit -m $commitMessage

Write-Host "✅ Đã tạo commit" -ForegroundColor Green

# Add remote
Write-Host ""
Write-Host "🔗 Thêm remote repository..." -ForegroundColor Cyan

# Kiểm tra remote đã tồn tại chưa
$remoteExists = git remote | Select-String -Pattern "origin"
if ($remoteExists) {
    Write-Host "Remote 'origin' đã tồn tại, cập nhật URL..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

Write-Host "✅ Đã thêm remote repository" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "🚀 Push code lên GitHub..." -ForegroundColor Cyan

git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 Thành công! Code đã được push lên GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Các bước tiếp theo:" -ForegroundColor Cyan
    Write-Host "1. Deploy Backend lên Railway hoặc Render" -ForegroundColor Yellow
    Write-Host "2. Deploy Frontend lên Vercel" -ForegroundColor Yellow
    Write-Host "3. Xem hướng dẫn chi tiết trong DEPLOYMENT.md" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Repository URL: $repoUrl" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Có lỗi xảy ra khi push!" -ForegroundColor Red
    Write-Host "Vui lòng kiểm tra:" -ForegroundColor Yellow
    Write-Host "- URL repository có đúng không?" -ForegroundColor Yellow
    Write-Host "- Bạn đã đăng nhập Git chưa? (git config --global user.name)" -ForegroundColor Yellow
    Write-Host "- Repository trên GitHub đã được tạo chưa?" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Nhấn Enter để đóng"
