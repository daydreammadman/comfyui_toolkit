"""
OpenAI节点 - OpenAI Compatible Nodes

支持OpenAI及兼容格式的API调用
包括：OpenAI官方、魔塔社区、通义千问、DeepSeek等
"""

import json
import requests
from typing import Optional, List, Dict, Any


class ChatCompletions:
    """
    OpenAI Chat Completions API调用节点
    支持所有兼容OpenAI格式的API，包括文本对话和视觉理解
    支持单图像或多图像输入（多图像用换行分隔）
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "base_url": ("STRING", {
                    "default": "https://api.openai.com/v1",
                    "multiline": False,
                }),
                "model": ("STRING", {
                    "default": "gpt-4.1-nano",
                    "multiline": False,
                }),
                "user_message": ("STRING", {
                    "default": "Hello!",
                    "multiline": True,
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "default": "You are a helpful assistant.",
                    "multiline": True,
                }),
                "image_url": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "支持单个或多个图像URL，多个URL请用换行分隔"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "max_tokens": ("INT", {
                    "default": 32768,
                    "min": 1,
                    "max": 32768,
                    "step": 1,
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "conversation_history": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "full_response_json", "updated_history")
    FUNCTION = "chat"
    CATEGORY = "Tomoto's Tools/OpenAI"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """
        强制节点每次都重新执行，避免缓存
        返回当前时间戳，确保每次都不同
        """
        import time
        return time.time()

    def chat(
        self,
        api_key: str,
        base_url: str,
        model: str,
        user_message: str,
        system_prompt: str = "You are a helpful assistant.",
        image_url: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        top_p: float = 1.0,
        conversation_history: str = "[]",
    ):
        """
        调用OpenAI Chat Completions API

        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
            user_message: 用户消息
            system_prompt: 系统提示词
            image_url: 图像URL（支持Base64、HTTP URL等）
                      - 单张图像：直接输入URL
                      - 多张图像：每行一个URL，用换行分隔
            temperature: 温度参数
            max_tokens: 最大token数
            top_p: Top-p采样
            conversation_history: 历史对话（JSON格式）

        Returns:
            (助手回复, 完整响应JSON, 更新后的历史)
        """

        try:
            # 解析历史对话
            try:
                history = json.loads(conversation_history) if conversation_history else []
            except json.JSONDecodeError:
                print("[ChatCompletions] Warning: Invalid conversation history, starting fresh")
                history = []

            # 构建消息列表
            messages = []

            # 添加系统提示词
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # 添加历史对话
            messages.extend(history)

            # 构建当前用户消息
            if image_url:
                # 解析多个图像URL（支持换行分隔）
                image_urls = [url.strip() for url in image_url.strip().split('\n') if url.strip()]

                if image_urls:
                    # 多模态消息（包含图像）
                    user_content = [
                        {
                            "type": "text",
                            "text": user_message
                        }
                    ]

                    # 添加所有图像
                    for url in image_urls:
                        user_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        })

                    has_image = True
                    image_count = len(image_urls)
                else:
                    # 如果解析后没有有效URL，按纯文本处理
                    user_content = user_message
                    has_image = False
                    image_count = 0
            else:
                # 纯文本消息
                user_content = user_message
                has_image = False
                image_count = 0

            messages.append({
                "role": "user",
                "content": user_content
            })

            # 构建请求
            url = f"{base_url.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
            }

            print(f"[ChatCompletions] Calling API: {url}")
            print(f"[ChatCompletions] Model: {model}")
            if has_image:
                print(f"[ChatCompletions] Images: {image_count}")
            print(f"[ChatCompletions] User message: {user_message[:50]}...")

            # 发送请求
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            # 提取助手回复
            assistant_message = result["choices"][0]["message"]["content"]

            # 更新历史对话
            updated_history = history + [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_message}
            ]

            # 转为JSON字符串
            updated_history_json = json.dumps(updated_history, ensure_ascii=False, indent=2)
            full_response_json = json.dumps(result, ensure_ascii=False, indent=2)

            print(f"[ChatCompletions] Success! Response length: {len(assistant_message)} chars")

            return (assistant_message, full_response_json, updated_history_json)

        except requests.exceptions.RequestException as e:
            error_msg = f"API请求失败: {str(e)}"
            print(f"[ChatCompletions] Error: {error_msg}")
            return (error_msg, "{}", "[]")

        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(f"[ChatCompletions] Error: {error_msg}")
            return (error_msg, "{}", "[]")

