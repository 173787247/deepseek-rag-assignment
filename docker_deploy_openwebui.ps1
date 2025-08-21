# 第六章作业：Docker 部署 Open WebUI 和 DeepSeek-R1 模型
# 作者：AI助手
# 日期：2025年8月

Write-Host "🚀 开始部署 Open WebUI 和 DeepSeek-R1 模型..." -ForegroundColor Green

# 检查 Docker 是否安装
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker 已安装: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 Docker Compose 是否安装
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose 已安装: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose 未安装，请先安装 Docker Compose" -ForegroundColor Red
    exit 1
}

# 创建项目目录
$projectDir = "openwebui-deepseek"
if (!(Test-Path $projectDir)) {
    New-Item -ItemType Directory -Path $projectDir | Out-Null
}
Set-Location $projectDir

Write-Host "📁 项目目录: $projectDir" -ForegroundColor Blue

# 创建 docker-compose.yml 文件
$dockerComposeContent = @"
version: '3.8'

services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui-deepseek
    restart: unless-stopped
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - WEBUI_SECRET_KEY=your-secret-key-here
      - DEFAULT_MODELS=deepseek-r1:8b,deepseek-r1:1.5b
      - ENABLE_SIGNUP=true
      - ENABLE_LOGIN_FORM=true
    volumes:
      - ./data:/app/backend/data
      - ./models:/app/backend/models
    depends_on:
      - ollama
    networks:
      - openwebui-network

  ollama:
    image: ollama/ollama:latest
    container_name: ollama-deepseek
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ./ollama:/root/.ollama
    networks:
      - openwebui-network

networks:
  openwebui-network:
    driver: bridge

volumes:
  ollama:
  data:
  models:
"@

$dockerComposeContent | Out-File -FilePath "docker-compose.yml" -Encoding UTF8
Write-Host "✅ docker-compose.yml 文件创建完成" -ForegroundColor Green

# 创建 .env 文件
$envContent = @"
# Open WebUI 环境变量
WEBUI_SECRET_KEY=your-secret-key-here
OLLAMA_BASE_URL=http://ollama:11434
DEFAULT_MODELS=deepseek-r1:8b,deepseek-r1:1.5b
ENABLE_SIGNUP=true
ENABLE_LOGIN_FORM=true

# Ollama 配置
OLLAMA_HOST=0.0.0.0
OLLAMA_ORIGINS=*
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ .env 文件创建完成" -ForegroundColor Green

# 启动服务
Write-Host "🚀 启动 Open WebUI 和 Ollama 服务..." -ForegroundColor Green
docker-compose up -d

# 等待服务启动
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 下载 DeepSeek-R1 模型
Write-Host "📥 开始下载 DeepSeek-R1 模型..." -ForegroundColor Green

# 检测系统架构
$arch = (Get-WmiObject -Class Win32_Processor).Architecture
if ($arch -eq 0) {
    Write-Host "🖥️  检测到 x86_64 架构，下载 DeepSeek-R1:8B 模型" -ForegroundColor Blue
    docker exec ollama-deepseek ollama pull deepseek-r1:8b
} elseif ($arch -eq 9) {
    Write-Host "🖥️  检测到 ARM64 架构，下载 DeepSeek-R1:1.5B 模型" -ForegroundColor Blue
    docker exec ollama-deepseek ollama pull deepseek-r1:1.5b
} else {
    Write-Host "🖥️  未知架构，下载 DeepSeek-R1:1.5B 模型（推荐）" -ForegroundColor Blue
    docker exec ollama-deepseek ollama pull deepseek-r1:1.5b
}

Write-Host "✅ 模型下载完成！" -ForegroundColor Green

# 显示服务状态
Write-Host "📊 服务状态：" -ForegroundColor Blue
docker-compose ps

Write-Host ""
Write-Host "🎉 部署完成！" -ForegroundColor Green
Write-Host "🌐 Open WebUI 访问地址：http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Ollama API 地址：http://localhost:11434" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 使用说明：" -ForegroundColor Yellow
Write-Host "1. 打开浏览器访问 http://localhost:3000" -ForegroundColor White
Write-Host "2. 注册新账户或使用默认账户登录" -ForegroundColor White
Write-Host "3. 在模型选择中选择 DeepSeek-R1 模型" -ForegroundColor White
Write-Host "4. 开始使用私有化部署的 DeepSeek 模型" -ForegroundColor White
Write-Host ""
Write-Host "🔍 检查模型状态：" -ForegroundColor Yellow
Write-Host "docker exec ollama-deepseek ollama list" -ForegroundColor White
Write-Host ""
Write-Host "🛑 停止服务：" -ForegroundColor Yellow
Write-Host "docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "🔄 重启服务：" -ForegroundColor Yellow
Write-Host "docker-compose restart" -ForegroundColor White
