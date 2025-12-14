"""
配置加载工具 - Config Loader Utility

提供配置文件读取、缓存和刷新功能
"""

import json
import os
from typing import Dict, List, Any


class ConfigLoader:
    """配置文件加载器，支持缓存和自动刷新"""

    _instance = None
    _config_cache = {}

    def __new__(cls):
        """单例模式，确保全局只有一个实例"""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            # 初始化时计算 config 目录路径
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls._instance._config_dir = os.path.join(current_dir, "config")
        return cls._instance

    def get_config_path(self, config_name: str = "models.json") -> str:
        """
        获取配置文件的绝对路径

        Args:
            config_name: 配置文件名，默认为 models.json

        Returns:
            配置文件的绝对路径
        """
        return os.path.join(self._config_dir, config_name)

    def load_config(self, config_name: str = "models.json", force_reload: bool = False) -> Dict:
        """
        加载配置文件

        Args:
            config_name: 配置文件名
            force_reload: 是否强制重新加载（忽略缓存）

        Returns:
            配置字典
        """
        # 如果缓存中有且不强制刷新，直接返回缓存
        if config_name in self._config_cache and not force_reload:
            return self._config_cache[config_name]

        config_path = self.get_config_path(config_name)

        # 检查文件是否存在
        if not os.path.exists(config_path):
            print(f"[ConfigLoader] Warning: Config file not found: {config_path}")
            return {}

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 缓存配置
                self._config_cache[config_name] = config
                print(f"[ConfigLoader] Loaded config: {config_name}")
                return config
        except json.JSONDecodeError as e:
            print(f"[ConfigLoader] Error: Invalid JSON in {config_path}: {e}")
            return {}
        except Exception as e:
            print(f"[ConfigLoader] Error loading config {config_path}: {e}")
            return {}

    def get_model_list(self, source: str, model_type: str, force_reload: bool = False) -> List[str]:
        """
        获取模型列表

        Args:
            source: 模型来源，如 "modelscope" 或 "local"
            model_type: 模型类型，如 "text_to_image", "llm", "vlm"
            force_reload: 是否强制重新加载

        Returns:
            模型名称列表
        """
        config = self.load_config("models.json", force_reload)

        try:
            models = config.get(source, {}).get(model_type, [])
            if not models:
                print(f"[ConfigLoader] Warning: No models found for {source}/{model_type}")
                return ["(配置为空)"]
            return models
        except Exception as e:
            print(f"[ConfigLoader] Error getting model list: {e}")
            return ["(加载失败)"]

    def clear_cache(self):
        """清除所有缓存"""
        self._config_cache.clear()
        print("[ConfigLoader] Cache cleared")

    def get_prompt_list(self, force_reload: bool = False) -> List[Dict[str, str]]:
        """
        获取所有提示词列表（名称和文件名的映射）

        Args:
            force_reload: 是否强制重新扫描目录

        Returns:
            提示词信息列表，每项包含 {name, filename, description}
        """
        cache_key = "_prompt_list"

        # 如果缓存中有且不强制刷新，直接返回缓存
        if cache_key in self._config_cache and not force_reload:
            return self._config_cache[cache_key]

        prompts_dir = os.path.join(self._config_dir, "prompts")

        # 检查目录是否存在
        if not os.path.exists(prompts_dir):
            print(f"[ConfigLoader] Warning: Prompts directory not found: {prompts_dir}")
            return []

        prompt_list = []

        try:
            # 遍历目录中的所有 JSON 文件
            for filename in os.listdir(prompts_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(prompts_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            prompt_list.append({
                                "name": data.get("name", filename),
                                "filename": filename,
                                "description": data.get("description", "")
                            })
                    except Exception as e:
                        print(f"[ConfigLoader] Warning: Failed to load {filename}: {e}")

            # 缓存结果
            self._config_cache[cache_key] = prompt_list
            print(f"[ConfigLoader] Loaded {len(prompt_list)} prompts")
            return prompt_list

        except Exception as e:
            print(f"[ConfigLoader] Error scanning prompts directory: {e}")
            return []

    def get_prompt_content(self, filename: str, force_reload: bool = False) -> Dict[str, str]:
        """
        获取指定提示词文件的完整内容

        Args:
            filename: 提示词文件名
            force_reload: 是否强制重新加载

        Returns:
            提示词数据字典，包含 name, description, prompt
        """
        cache_key = f"_prompt_{filename}"

        # 如果缓存中有且不强制刷新，直接返回缓存
        if cache_key in self._config_cache and not force_reload:
            return self._config_cache[cache_key]

        filepath = os.path.join(self._config_dir, "prompts", filename)

        # 检查文件是否存在
        if not os.path.exists(filepath):
            print(f"[ConfigLoader] Warning: Prompt file not found: {filepath}")
            return {
                "name": "(文件不存在)",
                "description": "",
                "prompt": ""
            }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 缓存数据
                self._config_cache[cache_key] = data
                print(f"[ConfigLoader] Loaded prompt: {data.get('name', filename)}")
                return data
        except json.JSONDecodeError as e:
            print(f"[ConfigLoader] Error: Invalid JSON in {filepath}: {e}")
            return {
                "name": "(JSON格式错误)",
                "description": "",
                "prompt": ""
            }
        except Exception as e:
            print(f"[ConfigLoader] Error loading prompt {filepath}: {e}")
            return {
                "name": "(加载失败)",
                "description": "",
                "prompt": ""
            }


# 创建全局单例
config_loader = ConfigLoader()
