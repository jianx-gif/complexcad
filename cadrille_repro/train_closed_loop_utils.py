# -*- coding: utf-8 -*-
"""闭环联合输入的共享预处理 (训练与推理同一函数)."""
import os


def load_drawing(path, max_tokens):
    """工程图 PNG -> RGB, 裁掉白边, 缩放到 <= max_tokens 个 28x28 视觉 token."""
    from PIL import Image, ImageChops
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.paste(im, mask=im.split()[3]); im = bg.convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255)))
    box = diff.getbbox()
    if box:
        pad = 20
        im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
    scale = min(1.0, (max_tokens * 28 * 28 / (im.width * im.height)) ** 0.5)
    w = max(28, int(im.width * scale) // 28 * 28); h = max(28, int(im.height * scale) // 28 * 28)
    return im.resize((w, h), Image.LANCZOS)


