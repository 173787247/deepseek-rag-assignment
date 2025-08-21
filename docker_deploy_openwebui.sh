#!/bin/bash

# 第六章作业：Docker 部署 Open WebUI 和 DeepSeek-R1 模型
# 作者：AI助手
# 日期：2025年8月

echo "🚀 开始部署 Open WebUI 和 DeepSeek-R1 模型..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建项目目录
mkdir -p openwebui-deepseek
cd openwebui-deepseek

# 创建 docker-compose.yml 文件
cat > docker-compose.yml << 'EOF'
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
EOF

echo "✅ docker-compose.yml 文件创建完成"

# 创建 .env 文件
cat > .env << 'EOF'
# Open WebUI 环境变量
WEBUI_SECRET_KEY=your-secret-key-here
OLLAMA_BASE_URL=http://ollama:11434
DEFAULT_MODELS=deepseek-r1:8b,deepseek-r1:1.5b
ENABLE_SIGNUP=true
ENABLE_LOGIN_FORM=true

# Ollama 配置
OLLAMA_HOST=0.0.0.0
OLLAMA_ORIGINS=*
EOF

echo "✅ .env 文件创建完成"

# 启动服务
echo "🚀 启动 Open WebUI 和 Ollama 服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 下载 DeepSeek-R1 模型
echo "📥 开始下载 DeepSeek-R1 模型..."

# 检测系统架构
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
    echo "🖥️  检测到 x86_64 架构，下载 DeepSeek-R1:8B 模型"
    docker exec ollama-deepseek ollama pull deepseek-r1:8b
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    echo "🖥️  检测到 ARM64 架构，下载 DeepSeek-R1:1.5B 模型"
    docker exec ollama-deepseek ollama pull deepseek-r1:1.5b
else
    echo "🖥️  未知架构，下载 DeepSeek-R1:1.5B 模型（推荐）"
    docker exec ollama-deepseek ollama pull deepseek-r1:1.5b
fi

echo "✅ 模型下载完成！"

# 显示服务状态
echo "📊 服务状态："
docker-compose ps

echo ""
echo "🎉 部署完成！"
echo "🌐 Open WebUI 访问地址：http://localhost:3000"
echo "🔧 Ollama API 地址：http://localhost:11434"
echo ""
echo "📝 使用说明："
echo "1. 打开浏览器访问 http://localhost:3000"
echo "2. 注册新账户或使用默认账户登录"
echo "3. 在模型选择中选择 DeepSeek-R1 模型"
echo "4. 开始使用私有化部署的 DeepSeek 模型"
echo ""
echo "🔍 检查模型状态："
echo "docker exec ollama-deepseek ollama list"
echo ""
echo "🛑 停止服务："
echo "docker-compose down"
echo ""
echo "🔄 重启服务："
echo "docker-compose restart"
