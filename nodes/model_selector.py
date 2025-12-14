"""
模型选择器节点 - Model Selector Nodes

提供从配置文件中选择模型的功能
"""

# 使用相对导入
from ..utils.config_loader import config_loader


# ========== 魔塔社区模型选择器 ==========

class ModelScopeT2ISelector:
    """魔塔社区 - 文生图模型选择器"""

    @classmethod
    def INPUT_TYPES(cls):
        # 每次都重新读取配置
        models = config_loader.get_model_list("modelscope", "text_to_image", force_reload=True)
        return {
            "required": {
                "model": (models, {"default": models[0] if models else ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)
    FUNCTION = "select_model"
    CATEGORY = "Tomoto's Tools/Models/ModelScope"

    def select_model(self, model):
        print(f"[ModelScopeT2I] Selected model: {model}")
        return (model,)



# ========== 本地模型选择器 ==========

class LocalT2ISelector:
    """本地 - 文生图模型选择器"""

    @classmethod
    def INPUT_TYPES(cls):
        # 每次都重新读取配置
        models = config_loader.get_model_list("local", "text_to_image", force_reload=True)
        return {
            "required": {
                "model": (models, {"default": models[0] if models else ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "select_model"
    CATEGORY = "Tomoto's Tools/Models/Local"

    def select_model(self, model):
        print(f"[LocalT2I] Selected model: {model}")
        return (model,)


class LocalLLMSelector:
    """本地 - LLM模型选择器"""

    @classmethod
    def INPUT_TYPES(cls):
        # 每次都重新读取配置
        models = config_loader.get_model_list("local", "llm", force_reload=True)
        return {
            "required": {
                "model": (models, {"default": models[0] if models else ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "select_model"
    CATEGORY = "Tomoto's Tools/Models/Local"

    def select_model(self, model):
        print(f"[LocalLLM] Selected model: {model}")
        return (model,)

