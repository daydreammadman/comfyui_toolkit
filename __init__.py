"""
ComfyUI Toolkit - ComfyUI 工具集

提供工作流逻辑控制、AI集成、模型管理、提示词管理等全方位功能
"""

from .nodes.logic_router import LogicRouter4, LogicRouter8
from .nodes.model_selector import (
    ModelScopeT2ISelector,
    ModelScopeImageEditSelector,
    LocalT2ISelector,
    LocalLLMSelector,

)
from .nodes.image_converter import (
    ImageToBase64,
    MultiImageToBase64,
)
from .nodes.openai_nodes import (
    ChatCompletions,
)
from .nodes.prompt_selector import (
    SystemPromptSelector,
)
from .nodes.json_parser import (
    SDPromptParser,
    GenericJSONParser,
)
from .nodes.string_utils import (
    StringIsEmpty,
    StringLength,
    StringTrim,
    StringConditionalSelector,
    StringJoin,
)

# 节点类映射
NODE_CLASS_MAPPINGS = {
    # 逻辑路由器
    "LogicRouter4": LogicRouter4,
    "LogicRouter8": LogicRouter8,

    # 魔塔社区模型选择器
    "ModelScopeT2ISelector": ModelScopeT2ISelector,
    "ModelScopeImageEditSelector": ModelScopeImageEditSelector,


    # 本地模型选择器
    "LocalT2ISelector": LocalT2ISelector,
    "LocalLLMSelector": LocalLLMSelector,


    # 图像转换器
    "ImageToBase64": ImageToBase64,
    "MultiImageToBase64": MultiImageToBase64,

    # OpenAI兼容API
    "ChatCompletions": ChatCompletions,

    # 提示词选择器
    "SystemPromptSelector": SystemPromptSelector,

    # JSON 解析器
    "SDPromptParser": SDPromptParser,
    "GenericJSONParser": GenericJSONParser,

    # 字符串工具
    "StringIsEmpty": StringIsEmpty,
    "StringLength": StringLength,
    "StringTrim": StringTrim,
    "StringConditionalSelector": StringConditionalSelector,
    "StringJoin": StringJoin,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    # 逻辑路由器
    "LogicRouter4": "万能选择器 (4路)",
    "LogicRouter8": "万能选择器 (8路)",

    # 魔塔社区模型选择器
    "ModelScopeT2ISelector": "模型选择器-魔塔文生图",
    "ModelScopeImageEditSelector": "模型选择器-魔塔图像编辑",


    # 本地模型选择器
    "LocalT2ISelector": "模型选择器-本地文生图",
    "LocalLLMSelector": "模型选择器-本地LLM",


    # 图像转换器
    "ImageToBase64": "图像转Base64",
    "MultiImageToBase64": "批量图像转Base64",

    # OpenAI兼容API
    "ChatCompletions": "聊天(OpenAI)",

    # 提示词选择器
    "SystemPromptSelector": "系统提示词选择器",

    # JSON 解析器
    "SDPromptParser": "SD提示词解析器",
    "GenericJSONParser": "JSON解析器",

    # 字符串工具
    "StringIsEmpty": "字符串判空",
    "StringLength": "字符串长度",
    "StringTrim": "字符串去空格",
    "StringConditionalSelector": "字符串条件选择",
    "StringJoin": "字符串连接",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
