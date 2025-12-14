"""
系统提示词选择器 - System Prompt Selector

从配置文件中选择预设的系统提示词
"""

from ..utils.config_loader import config_loader


class SystemPromptSelector:
    """系统提示词选择器"""

    @classmethod
    def INPUT_TYPES(cls):
        # 每次都重新读取提示词列表
        prompt_list = config_loader.get_prompt_list(force_reload=True)

        # 构建选项列表（显示名称）
        if not prompt_list:
            options = ["(无可用提示词)"]
            default = options[0]
        else:
            options = [p["name"] for p in prompt_list]
            default = options[0]

        return {
            "required": {
                "prompt_name": (options, {"default": default}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "name", "description")
    FUNCTION = "select_prompt"
    CATEGORY = "Tomoto's Tools/Prompts"

    def select_prompt(self, prompt_name):
        """
        选择系统提示词

        Args:
            prompt_name: 提示词名称

        Returns:
            (提示词内容, 名称, 描述)
        """
        # 获取提示词列表
        prompt_list = config_loader.get_prompt_list(force_reload=True)

        # 查找对应的文件名
        filename = None
        for p in prompt_list:
            if p["name"] == prompt_name:
                filename = p["filename"]
                break

        if not filename:
            print(f"[SystemPromptSelector] Warning: Prompt not found: {prompt_name}")
            return ("", prompt_name, "")

        # 读取提示词内容
        prompt_data = config_loader.get_prompt_content(filename, force_reload=True)

        name = prompt_data.get("name", "")
        description = prompt_data.get("description", "")
        prompt = prompt_data.get("prompt", "")

        print(f"[SystemPromptSelector] Selected prompt: {name}")
        print(f"[SystemPromptSelector] Description: {description}")

        return (prompt, name, description)
