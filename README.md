# DeepSeek RAG 作业项目

## 🎯 项目简介

基于 [deepseek-quickstart](https://github.com/DjangoPeng/deepseek-quickstart) 课程，使用 Milvus 向量数据库和 DeepSeek LLM 构建的 RAG 系统。该系统能够基于私有知识库回答用户问题，实现智能问答功能。

## 🏗️ 系统架构

- **向量数据库**: Milvus (使用 Milvus Lite 本地版本)
- **嵌入模型**: 默认使用 pymilvus 内置的嵌入模型
- **大语言模型**: DeepSeek API
- **知识库**: Milvus FAQ 文档

## 🚀 主要特性

- **语义检索**: 使用向量相似度进行文档检索
- **上下文增强**: 基于检索结果生成准确回答
- **多语言支持**: 支持中英文双语问答
- **可扩展性**: 易于添加新的知识库和问题
- **自定义测试**: 包含 5 个额外的测试用例

## 📁 文件结构

```
deepseek-rag-assignment/
├── README.md                           # 项目介绍（本文件）
├── rag_milvus_deepseek_custom.ipynb   # 主要的 RAG 实现
├── README_RAG.md                       # 详细使用说明
├── requirements.txt                     # 依赖包列表
├── en/faq/                             # 知识库文档
│   ├── operational_faq.md
│   ├── performance_faq.md
│   ├── product_faq.md
│   └── troubleshooting.md
└── screenshots/                         # 运行结果截图（可选）
```

## ⚙️ 安装依赖

```bash
pip install -r requirements.txt
```

## 🔧 环境配置

1. 设置 DeepSeek API Key 环境变量：
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

2. 或者在代码中直接设置：
```python
import os
os.environ["DEEPSEEK_API_KEY"] = "your-api-key-here"
```

## 📖 使用方法

### 1. 启动 Jupyter Notebook

```bash
jupyter notebook
```

### 2. 打开 RAG Notebook

打开 `rag_milvus_deepseek_custom.ipynb` 文件

### 3. 按顺序执行 Cell

1. **安装依赖**: 安装必要的 Python 包
2. **环境配置**: 设置 API Key
3. **数据准备**: 加载 Milvus FAQ 文档
4. **模型初始化**: 初始化嵌入模型和 DeepSeek 客户端
5. **向量化存储**: 将文档转换为向量并存储到 Milvus
6. **RAG 查询**: 测试原始问题
7. **自定义测试**: 测试自定义问题

## 🧪 自定义测试问题

系统包含以下预定义测试问题：

1. "What are the main features of Milvus?"
2. "How does Milvus handle performance optimization?"
3. "What are the common troubleshooting steps for Milvus?"
4. "How does Milvus support different vector types?"
5. "What is the architecture of Milvus?"

## 📚 课程信息

- **课程**: AI 全栈开发快速入门指南
- **作业**: 跑通 RAG 示例代码并修改问题
- **完成时间**: 2025年8月
- **技术栈**: Milvus + DeepSeek + Python + Jupyter

## 🔍 技术细节

### 向量化流程
1. 文档分割: 使用 "# " 作为分隔符
2. 嵌入生成: 将文本转换为高维向量
3. 向量存储: 存储到 Milvus 集合中

### 检索策略
- 使用内积 (IP) 距离度量
- 返回前 3 个最相关文档
- 支持动态字段存储

### 提示工程
- 系统提示: 定义 AI 助手角色
- 用户提示: 包含上下文和问题
- 输出格式: 支持中英文双语回答

## 🐛 故障排除

### 常见问题
1. **API Key 错误**: 检查 DeepSeek API Key 是否正确设置
2. **依赖安装失败**: 确保 Python 版本兼容 (推荐 3.8+)
3. **内存不足**: 减少批处理大小或使用更小的嵌入模型
4. **网络连接问题**: 检查网络连接和防火墙设置

### 性能优化
- 调整 `limit` 参数控制检索结果数量
- 使用更合适的 `metric_type` (IP, L2, COSINE)
- 根据需求选择 `consistency_level`

## 📈 扩展功能

### 添加新的知识库
1. 将新文档放入相应目录
2. 修改 `glob` 路径
3. 重新运行向量化流程

### 自定义问题
在 `custom_questions` 列表中添加新的问题：

```python
custom_questions = [
    "Your question here?",
    # ... 更多问题
]
```

### 集成其他模型
可以轻松替换为其他嵌入模型或 LLM：

```python
# 使用 OpenAI 嵌入模型
embedding_model = milvus_model.dense.OpenAIEmbeddingFunction(
    model_name='text-embedding-3-large',
    api_key='your-openai-key',
    base_url='https://api.openai.com/v1'
)
```

## 📄 许可证

本项目基于原始 deepseek-quickstart 项目，遵循 MIT 开源许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个 RAG 系统。

## 📞 联系方式

如有问题，请通过 GitHub Issues 联系。

---

## 🎉 项目亮点

这个 RAG 系统展示了如何结合向量数据库和大型语言模型来构建智能问答系统，完全符合 AI 全栈开发的学习要求。通过实际项目实践，深入理解了 RAG 技术的核心原理和实现方法。
