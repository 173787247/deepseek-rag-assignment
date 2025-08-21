# 第六章作业：私有化部署 DeepSeek-R1 模型的小红书文案助手

## 🎯 作业要求

1. **在服务器上使用 Docker 部署 Open WebUI**
2. **下载 DeepSeek-R1:8B 推理模型**（若只有 CPU，使用 DeepSeek-R1:1.5B 模型）
3. **生成蓝牙降噪耳机的小红书文案**
4. **将上一节课的小红书爆款文案助手项目中的 DeepSeek API 调用，改为私有化部署 DeepSeek-R1 模型，实现数据隐私保护**

## 📚 课程信息

- **课程**：AI 全栈开发快速入门指南
- **章节**：第六章 - 私有化部署与数据隐私保护
- **作业**：Docker 部署 Open WebUI + 私有化 DeepSeek-R1 模型
- **完成时间**：2025年8月
- **技术栈**：Docker + Open WebUI + Ollama + DeepSeek-R1 + Python

## 🚀 技术架构

### 整体架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Python 脚本   │    │   Ollama API    │    │  DeepSeek-R1    │
│  (第六章作业)    │◄──►│   (本地服务)    │◄──►│   (本地模型)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  产品数据库     │    │  Docker 容器    │    │  模型文件存储    │
│ (蓝牙耳机信息)  │    │ (Open WebUI)    │    │  (本地磁盘)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 核心组件

1. **Docker 容器化部署**
   - Open WebUI：提供 Web 界面
   - Ollama：运行 DeepSeek-R1 模型

2. **私有化模型**
   - DeepSeek-R1:8B（推荐）
   - DeepSeek-R1:1.5B（CPU 环境）

3. **Python 客户端**
   - OllamaClient 类：与本地模型通信
   - 产品数据库：蓝牙耳机详细信息
   - 文案生成函数：使用私有化模型

## 📁 文件结构

```
第六章作业/
├── docker_deploy_openwebui.sh          # Linux/macOS 部署脚本
├── docker_deploy_openwebui.ps1        # Windows PowerShell 部署脚本
├── rednote_ch6_assignment.py          # 第六章作业主程序
├── README_CHAPTER6.md                 # 本章作业说明文档
└── requirements.txt                    # Python 依赖包
```

## 🐳 Docker 部署步骤

### 1. 环境准备

确保已安装：
- Docker Desktop
- Docker Compose

### 2. 执行部署脚本

**Linux/macOS:**
```bash
chmod +x docker_deploy_openwebui.sh
./docker_deploy_openwebui.sh
```

**Windows:**
```powershell
.\docker_deploy_openwebui.ps1
```

### 3. 自动部署流程

脚本会自动：
1. 创建项目目录
2. 生成 docker-compose.yml 和 .env 文件
3. 启动 Open WebUI 和 Ollama 服务
4. 下载 DeepSeek-R1 模型
5. 显示服务状态和访问信息

### 4. 访问地址

- **Open WebUI**: http://localhost:3000
- **Ollama API**: http://localhost:11434

## 🔧 Python 环境配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行作业

```bash
python rednote_ch6_assignment.py
```

## 📱 蓝牙耳机产品数据库

### 支持的产品

| 产品名称 | 品牌 | 价格区间 | 主要特点 |
|---------|------|----------|----------|
| AirPods Pro | Apple | 1800-2200元 | 主动降噪、空间音频、防水防汗 |
| Sony WH-1000XM5 | Sony | 2800-3200元 | 业界领先降噪、30小时续航 |
| Bose QuietComfort 45 | Bose | 2200-2600元 | 经典降噪技术、舒适佩戴 |
| 华为 FreeBuds Pro 3 | 华为 | 1400-1800元 | 双单元动圈、智能降噪 |
| 小米 Buds 4 Pro | 小米 | 800-1200元 | 双动圈单元、智能降噪 |

### 产品信息包含

- 品牌信息
- 主要特点
- 续航能力
- 连接技术
- 目标用户
- 价格区间
- 特色功能

## 🤖 私有化模型调用

### OllamaClient 类

```python
class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model_name = "deepseek-r1:8b"
    
    def list_models(self) -> List[Dict]:
        """列出可用的模型"""
    
    def chat_completion(self, messages: List[Dict], tools: Optional[List] = None) -> Dict:
        """调用私有化部署的模型进行对话"""
    
    def set_model(self, model_name: str):
        """设置要使用的模型"""
```

### 模型调用流程

1. **初始化客户端**：连接到本地 Ollama 服务
2. **检查模型状态**：列出可用模型并自动选择
3. **发送请求**：通过 HTTP API 调用本地模型
4. **处理响应**：解析模型输出并生成文案

## 🔒 数据隐私保护优势

### 与云端 API 对比

| 特性 | 私有化部署 | 云端 API |
|------|------------|----------|
| **数据隐私** | ✅ 完全本地处理 | ❌ 数据上传云端 |
| **网络依赖** | ✅ 无需互联网 | ❌ 需要稳定网络 |
| **成本控制** | ✅ 一次性部署 | ❌ 按量计费 |
| **自定义能力** | ✅ 完全控制 | ❌ 有限定制 |
| **合规性** | ✅ 符合本地化要求 | ❌ 依赖第三方 |

### 核心价值

1. **数据安全**：敏感信息不上传，完全本地处理
2. **网络独立**：内网环境可用，避免网络中断
3. **成本效益**：长期使用成本更低
4. **合规要求**：满足行业监管和审计需求

## 📝 文案生成功能

### 支持的风格

- 科技酷炫
- 专业音质
- 性价比
- 时尚潮流
- 商务专业

### 输出格式

```json
{
  "title": "小红书标题",
  "body": "小红书正文内容",
  "hashtags": ["#标签1", "#标签2", "#标签3", "#标签4", "#标签5"],
  "emojis": ["✨", "🎧", "🎵", "🌟", "💖"]
}
```

### 生成流程

1. **产品查询**：从数据库获取产品信息
2. **模型调用**：使用私有化 DeepSeek-R1 模型
3. **迭代优化**：多次生成确保质量
4. **格式验证**：确保输出符合要求
5. **Markdown 转换**：便于阅读和发布

## 🧪 测试用例

### 1. 基础功能测试

- 模型连接测试
- 产品数据库查询
- 文案生成功能
- 格式转换功能

### 2. 产品测试

- AirPods Pro（科技酷炫风格）
- Sony WH-1000XM5（专业音质风格）
- 小米 Buds 4 Pro（性价比风格）

### 3. 边界测试

- 模糊产品名称匹配
- 模型调用失败处理
- JSON 格式验证

## 🚨 故障排除

### 常见问题

1. **Docker 服务启动失败**
   - 检查 Docker Desktop 是否运行
   - 确认端口 3000 和 11434 未被占用

2. **模型下载失败**
   - 检查网络连接
   - 确认磁盘空间充足
   - 手动运行：`docker exec ollama-deepseek ollama pull deepseek-r1:8b`

3. **Python 脚本运行失败**
   - 确认依赖包已安装
   - 检查 Ollama 服务是否正常运行
   - 验证模型是否已下载

### 调试命令

```bash
# 检查 Docker 容器状态
docker-compose ps

# 查看容器日志
docker-compose logs ollama
docker-compose logs openwebui

# 检查模型状态
docker exec ollama-deepseek ollama list

# 测试 Ollama API
curl http://localhost:11434/api/tags
```

## 📊 性能指标

### 响应时间

- **模型加载**：首次启动 10-30 秒
- **文案生成**：5-15 秒（取决于硬件性能）
- **产品查询**：< 1 秒

### 资源占用

- **内存**：8B 模型约需 8-16GB RAM
- **存储**：模型文件约 4-8GB
- **CPU**：推理时占用较高

## 🔮 扩展功能

### 短期扩展

1. **更多产品类型**：添加其他数码产品
2. **多语言支持**：支持英文、日文等
3. **文案风格**：增加更多个性化风格

### 长期扩展

1. **模型微调**：针对特定领域优化
2. **批量生成**：支持批量文案生成
3. **质量评估**：自动评估文案质量
4. **用户管理**：多用户权限控制

## 📋 作业提交要求

### 必需文件

1. **Docker 部署脚本**：`docker_deploy_openwebui.sh` 或 `docker_deploy_openwebui.ps1`
2. **Python 代码**：`rednote_ch6_assignment.py`
3. **执行截图**：显示代码运行结果
4. **README 文档**：`README_CHAPTER6.md`

### 提交方式

1. 将代码和截图文件上传至 GitHub 或 Gitee
2. 在作业提交页面粘贴文件链接
3. 确保代码可以正常运行并生成文案

### 评分标准

- **功能完整性**：40%（Docker 部署、模型调用、文案生成）
- **代码质量**：30%（代码结构、错误处理、文档）
- **创新性**：20%（私有化部署、数据隐私保护）
- **演示效果**：10%（运行截图、文案质量）

## 🎉 完成状态

- [x] Docker 部署脚本创建
- [x] Python 代码实现
- [x] 产品数据库设计
- [x] 私有化模型集成
- [x] 文案生成功能
- [x] 文档说明编写

**第六章作业已完成，可以提交！** 🎯✨

---

**作者**：AI助手  
**完成时间**：2025年8月  
**技术栈**：Docker + Open WebUI + Ollama + DeepSeek-R1 + Python  
**核心价值**：实现数据隐私保护，本地部署 AI 模型
