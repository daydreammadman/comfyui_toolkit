# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ComfyUI Toolkit** is a comprehensive custom node extension for ComfyUI that provides workflow logic control, AI integration, model management, and prompt engineering capabilities. This is NOT just a "logic nodes" package - it's a full-featured toolkit for integrating external AI services into ComfyUI workflows.

## Core Architecture

### Node Registration System

All nodes are registered in `__init__.py` via two dictionaries:
- `NODE_CLASS_MAPPINGS`: Maps internal class names to node classes
- `NODE_DISPLAY_NAME_MAPPINGS`: Maps internal class names to Chinese display names shown in ComfyUI UI

**Critical:** When adding new nodes, you MUST add entries to both dictionaries, or the node won't appear in ComfyUI.

### Configuration Management Pattern

This project uses a **singleton-based configuration loader** (`utils/config_loader.py`) with the following characteristics:

1. **Singleton Pattern**: `ConfigLoader` uses `__new__()` to ensure only one instance exists globally
2. **Caching**: All config reads are cached in `_config_cache` dict to avoid repeated file I/O
3. **Force Reload**: Every config-dependent node calls `force_reload=True` in `INPUT_TYPES()` to enable hot-reloading without ComfyUI restart
4. **Path Resolution**: Config paths are calculated once during initialization relative to the module root

**Key methods:**
- `load_config(config_name, force_reload)`: Load JSON files from `config/`
- `get_model_list(source, model_type, force_reload)`: Extract model arrays from `models.json`
- `get_prompt_list(force_reload)`: Scan `config/prompts/` directory for prompt templates
- `get_prompt_content(filename, force_reload)`: Load individual prompt template

### The AnyType Pattern

`nodes/logic_router.py` implements a critical type system trick for ComfyUI:

```python
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
```

This class bypasses ComfyUI's type checking by always returning `False` for inequality checks. This allows nodes like `LogicRouter4` and `LogicRouter8` to accept ANY ComfyUI data type (IMAGE, STRING, LATENT, MODEL, etc.) without type restrictions.

**Usage:** Instantiate once as `any_type = AnyType("*")` and use as a type specifier in `INPUT_TYPES` and `RETURN_TYPES`.


## File Organization

```
comfyui_toolkit/
├── nodes/              # All node implementations (one file per category)
├── config/
│   ├── models.json     # Model registry (modelscope + local models)
│   └── prompts/        # System prompt templates (JSON files)
├── utils/
│   └── config_loader.py  # Singleton config manager
└── __init__.py         # Node registration (the "switchboard")
```

