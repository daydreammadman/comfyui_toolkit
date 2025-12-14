# ComfyUI Toolkit - ComfyUI 工具集

ComfyUI 综合工具集，提供工作流逻辑控制、AI集成、模型管理、提示词管理等全方位功能。

## 📦 项目结构

```
comfyui_toolkit/
├── __init__.py                 # 主入口，注册所有节点
├── README.md                   # 项目说明
│
├── config/                     # 配置文件目录
│   ├── models.json            # 模型列表配置
│   └── prompts/               # 提示词模板目录
│
├── nodes/                      # 节点实现目录
│   ├── logic_router.py        # 逻辑路由器节点
│   ├── model_selector.py      # 模型选择器节点
│   ├── openai_nodes.py        # OpenAI API节点
│   ├── prompt_selector.py     # 提示词选择器节点
│   ├── json_parser.py         # JSON解析器节点
│   ├── string_utils.py        # 字符串工具节点
│   └── image_converter.py     # 图像转换节点
│
└── utils/                      # 工具函数目录
    └── config_loader.py       # 配置加载工具
```

---

## 🎯 节点列表

### 1. 逻辑路由器系列

#### 万能选择器 (4路) - LogicRouter4

从 4 个输入中选择一个输出，使用 **Radio 单选按钮**选择。

**特性：**
- ✅ 支持**任意数据类型**（图像、文本、潜空间、模型等）
- ✅ 所有输入端口**可选**，只连接需要的即可
- ✅ Radio 单选按钮，界面直观

**输入：**
- `input_1` - `input_4`: 任意类型（可选）
- `select`: Radio 单选按钮（Input 1-4）

**输出：**
- `selected_output`: 选中的输入值

**使用场景：**
- 在多个模型/参数/图像之间快速切换
- 工作流 A/B/C/D 测试
- 条件分支输出

---

#### 万能选择器 (8路) - LogicRouter8

从 8 个输入中选择一个输出，使用**下拉框**选择。

功能与 4 路相同，提供更多输入选项。

---

### 2. 模型选择器系列

#### 魔塔社区模型选择器

从配置文件中选择魔塔社区的模型，支持：

- **模型选择器-魔塔文生图** (`ModelScopeT2ISelector`)
- **模型选择器-魔塔图像编辑** (`ModelScopeImageEditSelector`)
- **模型选择器-魔塔LLM** (`ModelScopeLLMSelector`)
- **模型选择器-魔塔VLM** (`ModelScopeVLMSelector`)

**特性：**
- ✅ 从 `config/models.json` 读取模型列表
- ✅ 下拉框/Radio 选择（取决于模型数量）
- ✅ 支持**配置刷新**按钮，无需重启 ComfyUI
- ✅ 输出模型 ID 字符串，可连接到其他节点

**输入：**
- `model`: 模型选择（下拉框/Radio）
- `refresh`: 刷新配置按钮（可选）

**输出：**
- `model_name`: 模型 ID 字符串（如 `"Qwen/Qwen2.5-7B-Instruct"`）

---

#### 本地模型选择器

从配置文件中选择本地模型，支持：

- **模型选择器-本地文生图** (`LocalT2ISelector`)
- **模型选择器-本地LLM** (`LocalLLMSelector`)
- **模型选择器-本地VLM** (`LocalVLMSelector`)

**特性：**
- ✅ 管理本地模型文件路径
- ✅ 支持配置刷新
- ✅ 输出模型路径字符串

---

### 3. 字符串工具系列

#### 字符串连接 - StringJoin

将两个字符串用换行符连接。

**输入：**
- `text1`: 第一个字符串（多行文本）
- `text2`: 第二个字符串（多行文本）

**输出：**
- `output`: 用换行符连接的字符串

**使用场景：**
- 合并多段提示词
- 拼接系统提示和用户输入
- 组合多个文本片段

#### 其他字符串工具

- **字符串判空** (`StringIsEmpty`) - 判断字符串是否为空
- **字符串长度** (`StringLength`) - 获取字符串长度
- **字符串去空格** (`StringTrim`) - 去除首尾或所有空格
- **字符串条件选择** (`StringConditionalSelector`) - 根据布尔值选择字符串

---

## 📝 配置文件使用

### 编辑模型列表

编辑 `config/models.json` 文件：

```json
{
  "modelscope": {
    "text_to_image": [
      "AI-ModelScope/stable-diffusion-v1-5",
      "ZhipuAI/CogView3-Plus",
      "Kwai-Kolors/Kolors"
    ],
    "image_edit": [
      "Qwen/Qwen-Image-Edit-2509",
      "black-forest-labs/FLUX.2-dev"
    ],
    "llm": [
      "Qwen/Qwen2.5-7B-Instruct",
      "THUDM/glm-4-9b-chat"
    ],
    "vlm": [
      "Qwen/Qwen2-VL-7B-Instruct",
      "OpenGVLab/InternVL2-8B"
    ]
  },
  "local": {
    "text_to_image": [
      "sd15_v1.safetensors",
      "sdxl_base.safetensors"
    ],
    "llm": [
      "qwen2.5-7b-instruct",
      "llama-3.1-8b"
    ],
    "vlm": [
      "qwen2-vl-7b-instruct"
    ]
  }
}
```

### 刷新配置

修改配置文件后：
1. **方法一**：点击节点上的 "刷新配置" 按钮（推荐）
2. **方法二**：重启 ComfyUI

---

## 🚀 安装

1. 将此文件夹放置在 `ComfyUI/custom_nodes/` 目录下
2. 重启 ComfyUI
3. 在节点菜单中找到 `Tomoto's Tools` 分类

---

## 💡 使用示例

### 示例 1：逻辑路由器 - 快速切换模型

```
┌─────────────────────┐
│ Load Checkpoint A   │──┐
└─────────────────────┘  │
                         ├──► ┌──────────────────┐
┌─────────────────────┐  │    │ LogicRouter4     │
│ Load Checkpoint B   │──┘    │                  │
└─────────────────────┘       │ ○ Input 1        │
                              │ ● Input 2  ◄─选择│
                              │ ○ Input 3        │
                              │ ○ Input 4        │
                              │                  │
                              │   output ────────┤──► KSampler
                              └──────────────────┘
```

### 示例 2：模型选择器 - 管理魔塔模型

```
┌──────────────────────────────┐
│ 模型选择器-魔塔LLM            │
│                              │
│ Model: ▼ Qwen2.5-7B-Instruct │ ◄─ 从配置文件加载
│        - Qwen2.5-14B         │
│        - GLM-4-9B            │
│                              │
│ [刷新配置]                    │
│                              │
│ model_name ──────────────────┤──► 其他节点
└──────────────────────────────┘
```

---

## 🛠️ 扩展开发

### 添加新的模型类型

1. 在 `config/models.json` 添加新分类
2. 在 `nodes/model_selector.py` 创建新节点类
3. 在 `__init__.py` 注册新节点

### 添加其他配置文件

1. 在 `config/` 目录创建新 JSON 文件
2. 使用 `config_loader.load_config("your_config.json")` 加载

---

## 📄 许可

MIT License

---

## 🙋 常见问题

**Q: 修改配置文件后需要重启 ComfyUI 吗？**

A: 不需要！点击节点上的"刷新配置"按钮即可。

**Q: 为什么我的模型列表显示"(配置为空)"？**

A: 检查 `config/models.json` 文件格式是否正确，并确保对应的分类有内容。



---

**作者**: Tomoto

**版本**: 2.1.0

**更新日期**: 2025-12-14

