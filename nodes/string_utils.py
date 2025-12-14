"""
字符串工具节点 - String Utility Nodes

提供字符串处理和判断功能
"""


class StringIsEmpty:
    """
    字符串判空节点
    判断输入字符串是否为空
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            },
            "optional": {
                "trim_whitespace": ("BOOLEAN", {
                    "default": True,
                    "label_on": "去除空格",
                    "label_off": "保留空格"
                }),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_empty",)
    FUNCTION = "check_empty"
    CATEGORY = "Tomoto's Tools/Utils"

    def check_empty(self, text, trim_whitespace=True):
        """
        判断字符串是否为空

        Args:
            text: 输入字符串
            trim_whitespace: 是否在判断前去除首尾空格

        Returns:
            is_empty: True 或 False
        """
        # 处理 None 的情况
        if text is None:
            text = ""

        # 是否去除空格
        check_text = text.strip() if trim_whitespace else text

        # 判断是否为空
        is_empty = len(check_text) == 0

        print(f"[StringIsEmpty] Input length: {len(text)} chars")
        if trim_whitespace:
            print(f"[StringIsEmpty] After trim: {len(check_text)} chars")
        print(f"[StringIsEmpty] Is empty: {is_empty}")

        return (is_empty,)


class StringLength:
    """
    字符串长度节点
    返回字符串的长度
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("length", "length_text")
    FUNCTION = "get_length"
    CATEGORY = "Tomoto's Tools/Utils"

    def get_length(self, text):
        """
        获取字符串长度

        Args:
            text: 输入字符串

        Returns:
            (length: 整数长度, length_text: 字符串格式的长度)
        """
        if text is None:
            text = ""

        length = len(text)
        length_str = str(length)

        print(f"[StringLength] Text length: {length} chars")

        return (length, length_str)


class StringTrim:
    """
    字符串去除空格节点
    去除首尾或所有空格
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "trim_mode": (["both", "start", "end", "all"], {
                    "default": "both"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("trimmed_text",)
    FUNCTION = "trim_text"
    CATEGORY = "Tomoto's Tools/Utils"

    def trim_text(self, text, trim_mode="both"):
        """
        去除字符串空格

        Args:
            text: 输入字符串
            trim_mode: 去除模式
                - both: 去除首尾空格
                - start: 仅去除开头空格
                - end: 仅去除结尾空格
                - all: 去除所有空格

        Returns:
            去除空格后的字符串
        """
        if text is None:
            text = ""

        if trim_mode == "both":
            result = text.strip()
        elif trim_mode == "start":
            result = text.lstrip()
        elif trim_mode == "end":
            result = text.rstrip()
        elif trim_mode == "all":
            result = text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        else:
            result = text

        print(f"[StringTrim] Mode: {trim_mode}")
        print(f"[StringTrim] Before: {len(text)} chars -> After: {len(result)} chars")

        return (result,)


class StringConditionalSelector:
    """
    字符串条件选择器
    根据布尔值选择输出哪个字符串
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {
                    "default": True,
                }),
                "text_if_true": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "text_if_false": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "select_text"
    CATEGORY = "Tomoto's Tools/Utils"

    def select_text(self, condition, text_if_true, text_if_false):
        """
        根据条件选择字符串

        Args:
            condition: 布尔条件
            text_if_true: 条件为 True 时输出的字符串
            text_if_false: 条件为 False 时输出的字符串

        Returns:
            选中的字符串
        """
        result = text_if_true if condition else text_if_false

        print(f"[StringConditionalSelector] Condition: {condition}")
        print(f"[StringConditionalSelector] Selected: {'text_if_true' if condition else 'text_if_false'}")
        print(f"[StringConditionalSelector] Output length: {len(result)} chars")

        return (result,)
