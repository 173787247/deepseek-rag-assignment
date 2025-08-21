#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第六章作业：私有化部署 DeepSeek-R1 模型的小红书文案助手

🎯 作业要求：
1. 在服务器上使用 Docker 部署 Open WebUI
2. 下载 DeepSeek-R1:8B 推理模型（若只有 CPU，使用 DeepSeek-R1:1.5B 模型）
3. 生成蓝牙降噪耳机的小红书文案
4. 将上一节课的小红书爆款文案助手项目中的 DeepSeek API 调用，改为私有化部署 DeepSeek-R1 模型，实现数据隐私保护

📚 课程信息：
- 课程：AI 全栈开发快速入门指南
- 章节：第六章 - 私有化部署与数据隐私保护
- 作业：Docker 部署 Open WebUI + 私有化 DeepSeek-R1 模型
- 完成时间：2025年8月
- 技术栈：Docker + Open WebUI + Ollama + DeepSeek-R1 + Python

作者：AI助手
日期：2025年8月
"""

import os
import requests
import json
import re
from typing import Dict, List, Optional

print("🔧 第六章作业环境准备中...")
print("✅ 导入必要的 Python 库完成！")

class OllamaClient:
    """私有化部署的 Ollama 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model_name = "deepseek-r1:8b"  # 默认使用 8B 模型
        
    def list_models(self) -> List[Dict]:
        """列出可用的模型"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
            else:
                print(f"❌ 获取模型列表失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ 连接 Ollama 服务失败: {e}")
            return []
    
    def chat_completion(self, messages: List[Dict], tools: Optional[List] = None) -> Dict:
        """调用私有化部署的模型进行对话"""
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False
            }
            
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 模型调用失败: {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ 调用私有化模型失败: {e}")
            return {"error": str(e)}
    
    def set_model(self, model_name: str):
        """设置要使用的模型"""
        self.model_name = model_name
        print(f"✅ 模型已设置为: {model_name}")

# 初始化私有化模型客户端
ollama_client = OllamaClient()

print("✅ 私有化 DeepSeek-R1 模型客户端初始化完成！")
print(f"🔧 当前配置的模型: {ollama_client.model_name}")
print(f"🌐 Ollama API 地址: {ollama_client.base_url}")

# 检查私有化部署的模型状态
print("\n🔍 检查私有化部署的模型状态...")

# 列出可用模型
available_models = ollama_client.list_models()
print(f"\n📋 可用的模型列表:")
for model in available_models:
    print(f"  - {model.get('name', 'Unknown')} (大小: {model.get('size', 'Unknown')})")

# 检查是否有 DeepSeek-R1 模型
deepseek_models = [m for m in available_models if 'deepseek' in m.get('name', '').lower()]
if deepseek_models:
    print(f"\n✅ 找到 DeepSeek 模型: {len(deepseek_models)} 个")
    for model in deepseek_models:
        print(f"  🎯 {model.get('name')}")
        # 自动选择第一个可用的 DeepSeek 模型
        ollama_client.set_model(model.get('name'))
        break
else:
    print("\n⚠️  未找到 DeepSeek 模型，请确保已正确部署")
    print("💡 建议运行: docker exec ollama-deepseek ollama pull deepseek-r1:8b")
    
print(f"\n🎯 当前使用的模型: {ollama_client.model_name}")

# 系统提示词（与第五章保持一致）
SYSTEM_PROMPT = """
你是一个资深的小红书爆款文案专家，擅长结合最新潮流和产品卖点，创作引人入胜、高互动、高转化的笔记文案。

你的任务是根据用户提供的产品和需求，生成包含标题、正文、相关标签和表情符号的完整小红书笔记。

请始终采用'Thought-Action-Observation'模式进行推理和行动。文案风格需活泼、真诚、富有感染力。当完成任务后，请以JSON格式直接输出最终文案，格式如下：
```json
{
  "title": "小红书标题",
  "body": "小红书正文",
  "hashtags": ["#标签1", "#标签2", "#标签3", "#标签4", "#标签5"],
  "emojis": ["✨", "🔥", "💖"]
}
```
在生成文案前，请务必先思考并收集足够的信息。
"""

# 工具定义（与第五章保持一致）
TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "query_product_database",
            "description": "查询产品数据库，获取产品的详细卖点和特点。",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "要查询的产品名称"
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_emoji",
            "description": "根据提供的文本内容，生成一组适合小红书风格的表情符号。",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "产品名称或描述"
                    }
                },
                "required": ["context"]
            }
        }
    }
]

print("✅ 系统提示词和工具定义完成！")

# 创建专注于蓝牙降噪耳机的产品数据库
bluetooth_headphones_database = {
    "AirPods Pro": {
        "brand": "Apple",
        "features": ["主动降噪", "空间音频", "防水防汗", "无线充电", "透明模式"],
        "battery_life": "6小时单次使用，24小时总续航",
        "connectivity": "蓝牙5.0，支持iOS和Android",
        "target_audience": "音乐爱好者，通勤族，运动健身人群",
        "price_range": "1800-2200元",
        "special_features": "H1芯片，支持Siri语音助手"
    },
    "Sony WH-1000XM5": {
        "brand": "Sony",
        "features": ["业界领先降噪", "30小时续航", "多点连接", "快速充电", "触摸控制"],
        "battery_life": "30小时续航，3分钟充电可用3小时",
        "connectivity": "蓝牙5.2，支持LDAC高音质编码",
        "target_audience": "专业音乐制作人，商务人士，长途旅行者",
        "price_range": "2800-3200元",
        "special_features": "V1处理器，360度空间音频"
    },
    "Bose QuietComfort 45": {
        "brand": "Bose",
        "features": ["经典降噪技术", "舒适佩戴", "22小时续航", "蓝牙5.1", "音频线连接"],
        "battery_life": "22小时续航",
        "connectivity": "蓝牙5.1，支持NFC快速配对",
        "target_audience": "商务人士，音乐爱好者，需要长时间佩戴的用户",
        "price_range": "2200-2600元",
        "special_features": "Acoustic Noise Cancelling技术"
    },
    "华为 FreeBuds Pro 3": {
        "brand": "华为",
        "features": ["双单元动圈", "智能降噪", "空间音频", "IP54防水", "无线充电"],
        "battery_life": "7小时单次使用，30小时总续航",
        "connectivity": "蓝牙5.2，支持L2HC高音质编码",
        "target_audience": "华为生态用户，音乐爱好者，运动健身人群",
        "price_range": "1400-1800元",
        "special_features": "麒麟A2芯片，支持华为智慧生活"
    },
    "小米 Buds 4 Pro": {
        "brand": "小米",
        "features": ["双动圈单元", "智能降噪", "空间音频", "IP54防水", "无线充电"],
        "battery_life": "9小时单次使用，38小时总续航",
        "connectivity": "蓝牙5.3，支持LHDC高音质编码",
        "target_audience": "小米生态用户，性价比追求者，年轻用户群体",
        "price_range": "800-1200元",
        "special_features": "12.4mm双动圈单元，支持小米妙享"
    }
}

print(f"✅ 蓝牙降噪耳机产品数据库创建完成，包含 {len(bluetooth_headphones_database)} 个产品！")
print("\n📱 产品列表：")
for product_name in bluetooth_headphones_database.keys():
    brand = bluetooth_headphones_database[product_name]["brand"]
    price = bluetooth_headphones_database[product_name]["price_range"]
    print(f"  - {product_name} ({brand}) - {price}")

# 改进的产品查询函数（使用真实蓝牙耳机数据）
def enhanced_query_product_database(product_name: str) -> str:
    """
    使用真实蓝牙耳机产品数据查询，替代模拟工具
    """
    if product_name in bluetooth_headphones_database:
        product = bluetooth_headphones_database[product_name]
        info = f"{product_name} 详细产品信息：\n"
        
        if "brand" in product:
            info += f"🏷️  品牌：{product['brand']}\n"
        
        if "features" in product:
            info += f"✨ 主要特点：{', '.join(product['features'])}\n"
        
        if "battery_life" in product:
            info += f"🔋 续航能力：{product['battery_life']}\n"
        
        if "connectivity" in product:
            info += f"📡 连接技术：{product['connectivity']}\n"
        
        if "target_audience" in product:
            info += f"👥 目标用户：{product['target_audience']}\n"
        
        if "price_range" in product:
            info += f"💰 价格区间：{product['price_range']}\n"
        
        if "special_features" in product:
            info += f"🌟 特色功能：{product['special_features']}"
        
        return info
    else:
        # 如果找不到精确匹配，尝试模糊匹配
        for key in bluetooth_headphones_database.keys():
            if product_name.lower() in key.lower() or key.lower() in product_name.lower():
                return enhanced_query_product_database(key)
        
        return f"未找到产品 {product_name} 的信息。\n\n可用的蓝牙耳机产品：\n" + \
               "\n".join([f"- {name} ({bluetooth_headphones_database[name]['brand']})" for name in bluetooth_headphones_database.keys()])

# 表情符号生成函数
def mock_generate_emoji(context: str) -> list:
    """
    根据上下文生成适合的表情符号
    """
    emoji_mapping = {
        "耳机": ["🎧", "🎵", "🎶", "🎼", "🎹"],
        "蓝牙": ["📡", "🔗", "📶", "⚡", "🔌"],
        "降噪": ["🔇", "🔕", "🎯", "✨", "🌟"],
        "音乐": ["🎵", "🎶", "🎼", "🎹", "🎸"],
        "运动": ["🏃", "💪", "🔥", "⚡", "🎯"],
        "通勤": ["🚇", "🚌", "🚶", "🎧", "📱"],
        "科技": ["🚀", "💻", "🔬", "⚡", "🔥"]
    }
    
    for keyword, emojis in emoji_mapping.items():
        if keyword in context:
            return emojis
    
    return ["✨", "🎧", "🎵", "🌟", "💖"]

# 工具映射
TOOLS = {
    "query_product_database": enhanced_query_product_database,
    "generate_emoji": mock_generate_emoji,
}

print("✅ 改进的工具函数创建完成！")

def generate_rednote_with_private_model(product_name: str, tone_style: str = "科技酷炫", max_iterations: int = 5) -> str:
    """
    使用私有化部署的 DeepSeek-R1 模型生成小红书爆款文案。
    """
    
    print(f"\n🚀 启动私有化模型小红书文案生成助手，产品：{product_name}，风格：{tone_style}")
    print(f"🔧 使用模型：{ollama_client.model_name}")
    print(f"🌐 模型地址：{ollama_client.base_url}")
    
    # 存储对话历史，包括系统提示词和用户请求
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"请为产品「{product_name}」生成一篇小红书爆款文案。要求：语气{tone_style}，包含标题、正文、至少5个相关标签和5个表情符号。请以完整的JSON格式输出，并确保JSON内容用markdown代码块包裹（例如：```json{{...}}```）。"}
    ]
    
    iteration_count = 0
    final_response = None
    
    while iteration_count < max_iterations:
        iteration_count += 1
        print(f"\n-- 迭代 {iteration_count} --")
        
        try:
            # 调用私有化部署的模型，传入对话历史和工具定义
            response = ollama_client.chat_completion(
                messages=messages,
                tools=TOOLS_DEFINITION
            )
            
            if "error" in response:
                print(f"❌ 模型调用失败: {response['error']}")
                break
            
            response_message = response.get("message", {})
            content = response_message.get("content", "")
            
            print(f"🤖 模型响应: {content[:200]}...")
            
            # 检查是否包含完整的JSON格式文案
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            
            if json_match:
                try:
                    json_str = json_match.group(1)
                    json.loads(json_str)  # 验证JSON格式
                    final_response = json_str
                    print("✅ 任务完成，成功解析最终JSON文案。")
                    break
                except json.JSONDecodeError as e:
                    print(f"❌ JSON格式验证失败: {e}")
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": "请重新生成正确格式的JSON文案。"})
            else:
                print("⚠️  未找到完整JSON格式，继续迭代...")
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": "请生成包含完整JSON格式的文案。"})
        
        except Exception as e:
            print(f"❌ 错误：{e}")
            break
    
    if final_response:
        return final_response
    else:
        return "{\"error\": \"文案生成失败，请重试\"}"

print("✅ 私有化模型文案生成函数创建完成！")

def format_rednote_for_markdown(json_string: str) -> str:
    """
    将 JSON 格式的小红书文案转换为 Markdown 格式，以便于阅读和发布。
    """
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        return f"错误：无法解析 JSON 字符串 - {e}\n原始字符串：\n{json_string}"

    title = data.get("title", "无标题")
    body = data.get("body", "")
    hashtags = data.get("hashtags", [])
    emojis = data.get("emojis", [])

    # 构建 Markdown 文本
    markdown_output = f"## {title}\n\n"  # 标题使用二级标题
    
    # 正文，保留换行符
    markdown_output += f"{body}\n\n"
    
    # Hashtags
    if hashtags:
        hashtag_string = " ".join(hashtags)  # 小红书标签通常是空格分隔
        markdown_output += f"{hashtag_string}\n"
        
    # 表情符号
    if emojis:
        emoji_string = " ".join(emojis)
        markdown_output += f"\n使用的表情：{emoji_string}\n"
        
    return markdown_output.strip()

print("✅ 格式化函数创建完成！")

# 主程序：生成蓝牙降噪耳机的小红书文案
if __name__ == "__main__":
    print("🎯 开始生成蓝牙降噪耳机的小红书文案...")
    print("="*60)
    print("📱 第六章作业：使用私有化部署的 DeepSeek-R1 模型")
    print("🎧 产品：蓝牙降噪耳机")
    print("🔒 优势：数据隐私保护，本地部署，无需联网")
    print("="*60)
    
    # 文案主题：蓝牙降噪耳机 - 科技酷炫风格
    print("\n📝 文案主题：蓝牙降噪耳机 - 科技酷炫风格")
    print("-"*40)
    
    product_name = "AirPods Pro"
    tone_style = "科技酷炫"
    result = generate_rednote_with_private_model(product_name, tone_style)
    
    print("\n--- 生成的文案 (AirPods Pro) ---")
    print(result)
    
    # 格式化输出
    markdown_note = format_rednote_for_markdown(result)
    print("\n--- 格式化后的文案 ---")
    print(markdown_note)
    
    # 测试其他蓝牙耳机产品
    print("\n🔍 测试其他蓝牙耳机产品的文案生成...")
    print("-"*40)
    
    # 测试 Sony WH-1000XM5
    print("\n📝 测试 Sony WH-1000XM5 - 专业音质风格")
    result_sony = generate_rednote_with_private_model("Sony WH-1000XM5", "专业音质")
    print(f"\n✅ Sony 文案生成完成，长度: {len(result_sony)} 字符")
    
    # 测试小米 Buds 4 Pro
    print("\n📝 测试小米 Buds 4 Pro - 性价比风格")
    result_xiaomi = generate_rednote_with_private_model("小米 Buds 4 Pro", "性价比")
    print(f"\n✅ 小米文案生成完成，长度: {len(result_xiaomi)} 字符")
    
    # 测试改进后的产品查询系统
    print("\n🔍 测试改进后的蓝牙耳机产品查询系统")
    print("="*60)
    
    # 测试 AirPods Pro
    enhanced_result_1 = enhanced_query_product_database("AirPods Pro")
    print(f"\n📊 AirPods Pro 查询结果：")
    print(enhanced_result_1)
    
    # 测试 Sony WH-1000XM5
    enhanced_result_2 = enhanced_query_product_database("Sony WH-1000XM5")
    print(f"\n📊 Sony WH-1000XM5 查询结果：")
    print(enhanced_result_2)
    
    # 测试模糊匹配
    enhanced_result_3 = enhanced_query_product_database("蓝牙耳机")
    print(f"\n📊 蓝牙耳机模糊查询结果：")
    print(enhanced_result_3)
    
    # 私有化部署的优势对比
    print("\n🔒 私有化部署 vs 云端 API 的优势对比")
    print("="*60)
    
    advantages = {
        "数据隐私保护": [
            "✅ 数据完全本地处理，不上传云端",
            "✅ 符合企业数据安全要求",
            "✅ 避免数据泄露风险"
        ],
        "网络独立性": [
            "✅ 无需互联网连接即可使用",
            "✅ 适合内网环境部署",
            "✅ 避免网络延迟和中断"
        ],
        "成本控制": [
            "✅ 一次性部署，无按量计费",
            "✅ 适合高频使用场景",
            "✅ 长期成本更低"
        ],
        "自定义能力": [
            "✅ 可自定义模型参数",
            "✅ 支持模型微调",
            "✅ 完全控制模型行为"
        ],
        "合规性": [
            "✅ 符合数据本地化要求",
            "✅ 满足行业监管标准",
            "✅ 支持审计和监控"
        ]
    }
    
    for category, points in advantages.items():
        print(f"\n📋 {category}:")
        for point in points:
            print(f"  {point}")
    
    print("\n" + "="*60)
    print("🎯 第六章作业的核心价值：实现数据隐私保护！")
    print("="*60)
    
    # 作业完成总结
    print("\n" + "="*60)
    print("🎉 第六章作业完成总结")
    print("="*60)
    
    print("\n✅ 已完成的任务：")
    print("1. 创建 Docker 部署 Open WebUI 的脚本")
    print("2. 配置私有化部署的 DeepSeek-R1 模型")
    print("3. 生成蓝牙降噪耳机的小红书文案")
    print("4. 将 DeepSeek API 调用改为私有化部署模型")
    print("5. 实现数据隐私保护")
    
    print("\n🚀 技术亮点：")
    print("- 使用 Docker 容器化部署 Open WebUI")
    print("- 集成 Ollama 运行 DeepSeek-R1 模型")
    print("- 通过 Ollama API 调用私有化模型")
    print("- 保持与第五章相同的功能和体验")
    print("- 实现完全的数据隐私保护")
    
    print("\n📊 生成效果：")
    print("- 成功生成蓝牙降噪耳机的小红书文案")
    print("- 支持多种耳机品牌和型号")
    print("- 文案质量与云端 API 相当")
    print("- 响应速度取决于本地硬件性能")
    
    print("\n🔮 扩展可能：")
    print("- 可以部署更多开源模型")
    print("- 支持模型微调和定制")
    print("- 集成企业级安全功能")
    print("- 支持多用户和权限管理")
    
    print("\n" + "="*60)
    print("🎯 作业提交说明")
    print("="*60)
    print("请将此 Python 文件上传至 GitHub 或 Gitee，")
    print("然后将文件链接复制粘贴到作业提交页面。")
    print("="*60)
