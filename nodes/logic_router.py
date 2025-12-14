"""
逻辑路由器节点 - Logic Router Nodes

提供多路选择功能，从多个输入中选择一个输出
"""


# --- 核心技巧：定义万能类型 ---
class AnyType(str):
    """
    这是一个特殊的类。
    不管 ComfyUI 拿什么类型（String, Image, Latent）来和它比对，
    它都会返回 False (代表没有不匹配)，从而骗过类型检查。
    """
    def __ne__(self, __value: object) -> bool:
        return False


# 实例化一个万能对象，用 "*" 作为显示名称
any_type = AnyType("*")


class LogicRouter4:
    """
    4路选择器：通过Radio单选按钮选择输出哪一个输入。
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 下拉菜单/Radio按钮
                "select": (["Input 1", "Input 2", "Input 3", "Input 4"],),
            },
            "optional": {
                # 使用我们定义的万能类型，而不是普通的字符串 "*"
                "input_1": (any_type, ),
                "input_2": (any_type, ),
                "input_3": (any_type, ),
                "input_4": (any_type, ),
            }
        }

    # 输出也是万能类型
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("selected_output",)
    FUNCTION = "route_data"
    CATEGORY = "Tomoto's Tools/Logic"

    def route_data(self, select, input_1=None, input_2=None, input_3=None, input_4=None):
        # 打印调试信息，方便你看控制台发生了什么
        print(f"LogicRouter4: Selecting {select}")

        if select == "Input 1":
            return (input_1,)
        elif select == "Input 2":
            return (input_2,)
        elif select == "Input 3":
            return (input_3,)
        elif select == "Input 4":
            return (input_4,)

        # 如果出错，返回 None
        return (None,)


class LogicRouter8:
    """
    8路选择器：通过下拉菜单选择输出哪一个输入。
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 下拉菜单
                "select": (["Input 1", "Input 2", "Input 3", "Input 4",
                           "Input 5", "Input 6", "Input 7", "Input 8"],),
            },
            "optional": {
                "input_1": (any_type, ),
                "input_2": (any_type, ),
                "input_3": (any_type, ),
                "input_4": (any_type, ),
                "input_5": (any_type, ),
                "input_6": (any_type, ),
                "input_7": (any_type, ),
                "input_8": (any_type, ),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("selected_output",)
    FUNCTION = "route_data"
    CATEGORY = "Tomoto's Tools/Logic"

    def route_data(self, select, input_1=None, input_2=None, input_3=None, input_4=None,
                   input_5=None, input_6=None, input_7=None, input_8=None):
        print(f"LogicRouter8: Selecting {select}")

        inputs = {
            "Input 1": input_1,
            "Input 2": input_2,
            "Input 3": input_3,
            "Input 4": input_4,
            "Input 5": input_5,
            "Input 6": input_6,
            "Input 7": input_7,
            "Input 8": input_8,
        }

        return (inputs.get(select),)


# --- 动态输入支持 ---
class ContainsAnyDict(dict):
    """
    特殊字典，让 __contains__ 永远返回 True
    这样 ComfyUI 会接受任意名称的动态输入
    """
    def __contains__(self, key):
        return True


class DynamicRouter:
    """
    动态路由器：支持任意数量和名称的输入
    可以通过索引（1, 2, 3...）或输入名称来选择输出

    使用说明：
    1. 这个节点可以接收任意数量的输入连接
    2. 在前端连接输入时，ComfyUI 会自动创建输入槽
    3. 可以通过索引（从1开始）或输入名称来选择输出
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "select_mode": (["by_index", "by_name"], {
                    "default": "by_index"
                }),
                "selection": ("STRING", {
                    "default": "1",
                    "multiline": False,
                }),
            },
            "optional": ContainsAnyDict()  # 接受任意动态输入
        }

    RETURN_TYPES = (any_type, "STRING")
    RETURN_NAMES = ("output", "info")
    FUNCTION = "route_dynamic"
    CATEGORY = "Tomoto's Tools/Logic"

    def route_dynamic(self, select_mode, selection, **kwargs):
        """
        动态路由逻辑

        Args:
            select_mode: 选择模式 ("by_index" 或 "by_name")
            selection: 选择值（索引或名称）
            **kwargs: 所有动态输入都在这里
        """
        # 打印接收到的所有输入
        print(f"[DynamicRouter] Received {len(kwargs)} dynamic inputs:")
        print(kwargs)
        for key, value in kwargs.items():
            value_type = type(value).__name__
            print(f"  - {key}: {value_type}")

        # 如果没有输入，返回错误
        if not kwargs:
            error_msg = "No inputs connected!"
            print(f"[DynamicRouter] Error: {error_msg}")
            return (None, error_msg)

        # 根据选择模式路由
        result = None
        info = ""

        if select_mode == "by_index":
            # 按索引选择
            try:
                index = int(selection)
                # 将字典转换为列表（按键排序）
                sorted_keys = sorted(kwargs.keys())

                if 1 <= index <= len(sorted_keys):
                    selected_key = sorted_keys[index - 1]
                    result = kwargs[selected_key]
                    info = f"Selected input #{index} (key: '{selected_key}')"
                    print(f"[DynamicRouter] {info}")
                else:
                    info = f"Index {index} out of range (1-{len(sorted_keys)})"
                    print(f"[DynamicRouter] Error: {info}")
            except ValueError:
                info = f"Invalid index: '{selection}'"
                print(f"[DynamicRouter] Error: {info}")

        elif select_mode == "by_name":
            # 按名称选择
            if selection in kwargs:
                result = kwargs[selection]
                info = f"Selected input by name: '{selection}'"
                print(f"[DynamicRouter] {info}")
            else:
                available_keys = ', '.join(sorted(kwargs.keys()))
                info = f"Key '{selection}' not found. Available: {available_keys}"
                print(f"[DynamicRouter] Error: {info}")

        return (result, info)
