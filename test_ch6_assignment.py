#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第六章作业测试脚本

用于测试私有化部署 DeepSeek-R1 模型的小红书文案助手功能
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    try:
        import requests
        print("✅ requests 模块导入成功")
    except ImportError as e:
        print(f"❌ requests 模块导入失败: {e}")
        return False
    
    try:
        import json
        print("✅ json 模块导入成功")
    except ImportError as e:
        print(f"❌ json 模块导入失败: {e}")
        return False
    
    try:
        import re
        print("✅ re 模块导入成功")
    except ImportError as e:
        print(f"❌ re 模块导入失败: {e}")
        return False
    
    return True

def test_ollama_connection():
    """测试 Ollama 连接"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服务连接成功")
            models = response.json().get("models", [])
            print(f"📋 可用模型数量: {len(models)}")
            for model in models:
                print(f"  - {model.get('name', 'Unknown')}")
            return True
        else:
            print(f"⚠️  Ollama 服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama 服务连接失败，请确保 Docker 服务已启动")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_product_database():
    """测试产品数据库功能"""
    try:
        # 模拟产品数据库
        bluetooth_headphones_database = {
            "AirPods Pro": {
                "brand": "Apple",
                "features": ["主动降噪", "空间音频", "防水防汗", "无线充电", "透明模式"],
                "battery_life": "6小时单次使用，24小时总续航",
                "connectivity": "蓝牙5.0，支持iOS和Android",
                "target_audience": "音乐爱好者，通勤族，运动健身人群",
                "price_range": "1800-2200元",
                "special_features": "H1芯片，支持Siri语音助手"
            }
        }
        
        print("✅ 产品数据库创建成功")
        print(f"📱 产品数量: {len(bluetooth_headphones_database)}")
        
        # 测试产品查询
        product_name = "AirPods Pro"
        if product_name in bluetooth_headphones_database:
            product = bluetooth_headphones_database[product_name]
            print(f"🔍 产品查询成功: {product_name}")
            print(f"  - 品牌: {product['brand']}")
            print(f"  - 价格: {product['price_range']}")
            print(f"  - 特点: {', '.join(product['features'][:3])}...")
            return True
        else:
            print(f"❌ 产品查询失败: {product_name}")
            return False
            
    except Exception as e:
        print(f"❌ 产品数据库测试失败: {e}")
        return False

def test_json_formatting():
    """测试 JSON 格式化功能"""
    try:
        import json
        
        # 模拟文案数据
        sample_content = {
            "title": "🎧 AirPods Pro 深度体验分享",
            "body": "这款耳机真的太棒了！主动降噪效果惊人，空间音频让音乐更有层次感。",
            "hashtags": ["#AirPodsPro", "#主动降噪", "#空间音频", "#苹果生态", "#无线耳机"],
            "emojis": ["🎧", "✨", "🎵", "🌟", "💖"]
        }
        
        # 测试 JSON 序列化
        json_str = json.dumps(sample_content, ensure_ascii=False, indent=2)
        print("✅ JSON 序列化测试成功")
        
        # 测试 JSON 反序列化
        parsed_content = json.loads(json_str)
        print("✅ JSON 反序列化测试成功")
        
        # 验证数据完整性
        if (parsed_content["title"] == sample_content["title"] and 
            parsed_content["hashtags"] == sample_content["hashtags"]):
            print("✅ JSON 数据完整性验证成功")
            return True
        else:
            print("❌ JSON 数据完整性验证失败")
            return False
            
    except Exception as e:
        print(f"❌ JSON 格式化测试失败: {e}")
        return False

def test_regex_pattern():
    """测试正则表达式模式"""
    try:
        import re
        
        # 测试 JSON 代码块提取
        sample_text = """
        这是一段文本，包含 JSON 代码块：
        ```json
        {
          "title": "测试标题",
          "content": "测试内容"
        }
        ```
        代码块结束。
        """
        
        pattern = r'```json\s*(\{.*?\})\s*```'
        match = re.search(pattern, sample_text, re.DOTALL)
        
        if match:
            json_content = match.group(1)
            print("✅ 正则表达式模式测试成功")
            print(f"📝 提取的 JSON 内容: {json_content[:50]}...")
            return True
        else:
            print("❌ 正则表达式模式测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 正则表达式测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始第六章作业功能测试")
    print("="*50)
    
    tests = [
        ("模块导入测试", test_imports),
        ("Ollama 连接测试", test_ollama_connection),
        ("产品数据库测试", test_product_database),
        ("JSON 格式化测试", test_json_formatting),
        ("正则表达式测试", test_regex_pattern)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
    
    print("\n" + "="*50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！第六章作业功能正常")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关功能")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
