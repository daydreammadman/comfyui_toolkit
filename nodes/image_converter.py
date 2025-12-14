"""
图像转换节点 - Image Converter Nodes

将ComfyUI图像转换为API调用所需的格式
"""

import torch
import numpy as np
from PIL import Image
import io
import base64


class ImageToBase64:
    """
    将ComfyUI图像转换为Base64字符串
    用于调用远程API（如魔塔社区VLM、GPT-4V等）
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "format": (["PNG", "JPEG", "WEBP"], {"default": "PNG"}),
            },
            "optional": {
                "quality": ("INT", {
                    "default": 95,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "include_prefix": ("BOOLEAN", {
                    "default": True,
                    "label_on": "带前缀",
                    "label_off": "纯Base64"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("base64_string",)
    FUNCTION = "convert_to_base64"
    CATEGORY = "Tomoto's Tools/Image"

    def convert_to_base64(self, image, format="PNG", quality=95, include_prefix=True):
        """
        将ComfyUI图像转换为Base64字符串

        Args:
            image: ComfyUI图像张量 [B, H, W, C] 范围0-1
            format: 图像格式 (PNG/JPEG/WEBP)
            quality: 压缩质量 (1-100)，仅对JPEG/WEBP有效
            include_prefix: 是否包含data:image前缀

        Returns:
            Base64编码的字符串
        """
        # 取第一张图像（如果是批次）
        if len(image.shape) == 4:
            image = image[0]

        # 转换为numpy数组 [H, W, C]
        img_np = image.cpu().numpy()

        # 转换为0-255范围
        img_np = (img_np * 255).astype(np.uint8)

        # 转换为PIL Image
        pil_image = Image.fromarray(img_np)

        # 转换为字节流
        buffer = io.BytesIO()

        # 根据格式保存
        if format == "PNG":
            pil_image.save(buffer, format="PNG", optimize=True)
            mime_type = "image/png"
        elif format == "JPEG":
            # JPEG不支持透明通道，需要转换为RGB
            if pil_image.mode == "RGBA":
                pil_image = pil_image.convert("RGB")
            pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
            mime_type = "image/jpeg"
        elif format == "WEBP":
            pil_image.save(buffer, format="WEBP", quality=quality)
            mime_type = "image/webp"

        # 获取字节数据
        img_bytes = buffer.getvalue()

        # Base64编码
        base64_str = base64.b64encode(img_bytes).decode('utf-8')

        # 是否包含data URI前缀
        if include_prefix:
            result = f"data:{mime_type};base64,{base64_str}"
        else:
            result = base64_str

        print(f"[ImageToBase64] Converted to {format}, size: {len(base64_str)} chars")

        return (result,)


class MultiImageToBase64:
    """
    将批次图像转换为多个Base64字符串
    处理批次中的所有图像，返回base64字符串列表或JSON数组
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "format": (["PNG", "JPEG", "WEBP"], {"default": "PNG"}),
                "output_format": (["LIST", "JSON", "NEWLINE_SEPARATED"], {
                    "default": "LIST"
                }),
            },
            "optional": {
                "quality": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "include_prefix": ("BOOLEAN", {
                    "default": True,
                    "label_on": "带前缀",
                    "label_off": "纯Base64"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("base64_strings", "count")
    FUNCTION = "convert_to_base64"
    CATEGORY = "Tomoto's Tools/Image"
    OUTPUT_IS_LIST = (True, False)

    def convert_to_base64(self, images, format="PNG", output_format="LIST", quality=95, include_prefix=True):
        """
        将批次图像转换为Base64字符串列表

        Args:
            images: ComfyUI图像张量 [B, H, W, C] 范围0-1
            format: 图像格式 (PNG/JPEG/WEBP)
            output_format: 输出格式 (LIST/JSON/NEWLINE_SEPARATED)
            quality: 压缩质量 (1-100)，仅对JPEG/WEBP有效
            include_prefix: 是否包含data:image前缀

        Returns:
            Base64编码的字符串列表和图像数量
        """
        import json

        # 确保是4D张量
        if len(images.shape) != 4:
            images = images.unsqueeze(0)

        batch_size = images.shape[0]
        base64_list = []

        # 根据格式设置MIME类型
        if format == "PNG":
            mime_type = "image/png"
        elif format == "JPEG":
            mime_type = "image/jpeg"
        elif format == "WEBP":
            mime_type = "image/webp"

        # 处理每张图像
        for i in range(batch_size):
            # 获取单张图像
            image = images[i]

            # 转换为numpy数组 [H, W, C]
            img_np = image.cpu().numpy()

            # 转换为0-255范围
            img_np = (img_np * 255).astype(np.uint8)

            # 转换为PIL Image
            pil_image = Image.fromarray(img_np)

            # 转换为字节流
            buffer = io.BytesIO()

            # 根据格式保存
            if format == "PNG":
                pil_image.save(buffer, format="PNG", optimize=True)
            elif format == "JPEG":
                # JPEG不支持透明通道，需要转换为RGB
                if pil_image.mode == "RGBA":
                    pil_image = pil_image.convert("RGB")
                pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
            elif format == "WEBP":
                pil_image.save(buffer, format="WEBP", quality=quality)

            # 获取字节数据
            img_bytes = buffer.getvalue()

            # Base64编码
            base64_str = base64.b64encode(img_bytes).decode('utf-8')

            # 是否包含data URI前缀
            if include_prefix:
                result = f"data:{mime_type};base64,{base64_str}"
            else:
                result = base64_str

            base64_list.append(result)

        print(f"[MultiImageToBase64] Converted {batch_size} images to {format}")

        # 根据输出格式返回
        if output_format == "JSON":
            # 返回JSON数组字符串
            json_result = json.dumps(base64_list, ensure_ascii=False)
            return ([json_result], batch_size)
        elif output_format == "NEWLINE_SEPARATED":
            # 返回换行分隔的字符串
            newline_result = "\n".join(base64_list)
            return ([newline_result], batch_size)
        else:  # LIST
            # 返回列表（ComfyUI会自动处理）
            return (base64_list, batch_size)


