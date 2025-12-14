"""
JSON 解析器节点 - JSON Parser Nodes

解析 AI 输出的 JSON 字符串
"""

import json
import re


class SDPromptParser:
    """
    Stable Diffusion 提示词解析器
    解析包含 positive_prompt 和 negative_prompt 的 JSON 输出
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "raw_json")
    FUNCTION = "parse_json"
    CATEGORY = "Tomoto's Tools/Utils"

    def parse_json(self, json_string):
        """
        解析 SD 提示词 JSON

        Args:
            json_string: JSON 字符串

        Returns:
            (正向提示词, 反向提示词, 原始JSON)
        """
        if not json_string or not json_string.strip():
            print("[SDPromptParser] Warning: Empty input")
            return ("", "", "{}")

        # 清理输入：移除可能的 Markdown 代码块标记
        cleaned = json_string.strip()

        # 移除 ```json 和 ``` 标记
        if cleaned.startswith("```"):
            # 匹配 ```json 或 ``` 开头
            cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
            # 移除结尾的 ```
            cleaned = re.sub(r'\n?```\s*$', '', cleaned)

        try:
            # 解析 JSON
            data = json.loads(cleaned)

            # 提取字段
            positive_prompt = data.get("positive_prompt", "")
            negative_prompt = data.get("negative_prompt", "")

            # 格式化原始 JSON（美化）
            raw_json = json.dumps(data, ensure_ascii=False, indent=2)

            print(f"[SDPromptParser] Success!")
            print(f"[SDPromptParser] Positive length: {len(positive_prompt)} chars")
            print(f"[SDPromptParser] Negative length: {len(negative_prompt)} chars")

            return (positive_prompt, negative_prompt, raw_json)

        except json.JSONDecodeError as e:
            error_msg = f"JSON 解析失败: {str(e)}"
            print(f"[SDPromptParser] Error: {error_msg}")
            print(f"[SDPromptParser] Input was: {cleaned[:200]}...")
            return (error_msg, "", cleaned)

        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(f"[SDPromptParser] Error: {error_msg}")
            return (error_msg, "", cleaned)


class GenericJSONParser:
    """
    通用 JSON 解析器
    解析任意 JSON 并提取指定字段
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "field_name": ("STRING", {
                    "default": "result",
                    "multiline": False,
                }),
            },
            "optional": {
                "fallback_value": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("field_value", "full_json")
    FUNCTION = "parse_json"
    CATEGORY = "Tomoto's Tools/Utils"

    def parse_json(self, json_string, field_name, fallback_value=""):
        """
        解析 JSON 并提取指定字段

        Args:
            json_string: JSON 字符串
            field_name: 要提取的字段名（支持嵌套，如 "data.result"）
            fallback_value: 字段不存在时的默认值

        Returns:
            (字段值, 完整JSON)
        """
        if not json_string or not json_string.strip():
            print("[GenericJSONParser] Warning: Empty input")
            return (fallback_value, "{}")

        # 清理输入
        cleaned = json_string.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
            cleaned = re.sub(r'\n?```\s*$', '', cleaned)

        try:
            # 解析 JSON
            data = json.loads(cleaned)

            # 提取字段（支持嵌套）
            value = self._get_nested_field(data, field_name, fallback_value)

            # 如果值不是字符串，转换为 JSON 字符串
            if not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False)

            # 格式化完整 JSON
            full_json = json.dumps(data, ensure_ascii=False, indent=2)

            print(f"[GenericJSONParser] Extracted field '{field_name}': {value[:100]}...")

            return (value, full_json)

        except json.JSONDecodeError as e:
            error_msg = f"JSON 解析失败: {str(e)}"
            print(f"[GenericJSONParser] Error: {error_msg}")
            return (fallback_value, cleaned)

        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(f"[GenericJSONParser] Error: {error_msg}")
            return (fallback_value, cleaned)

    def _get_nested_field(self, data, field_path, fallback):
        """
        获取嵌套字段值

        Args:
            data: JSON 数据
            field_path: 字段路径，如 "data.result" 或 "user.name"
            fallback: 默认值

        Returns:
            字段值或默认值
        """
        try:
            # 分割路径
            keys = field_path.split('.')
            value = data

            # 逐层访问
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return fallback

                if value is None:
                    return fallback

            return value

        except Exception:
            return fallback
