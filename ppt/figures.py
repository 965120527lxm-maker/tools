"""Raster figure placement."""

from __future__ import annotations

import os

from pptx.util import Inches


def add_figure_on_slide(
    slide,
    img_path,
    left=Inches(0.6),
    top=Inches(1.55),
    max_width=Inches(12.0),
    max_height=Inches(5.0),
):
    """Place a raster figure, preserving aspect ratio and centering it in the
    (left, top, max_width, max_height) box. Returns (pic, w, h) or None."""
    if not os.path.exists(img_path):
        return None
    from PIL import Image

    with Image.open(img_path) as img:
        img_w, img_h = img.size
    aspect = img_w / img_h
    if aspect > max_width / max_height:
        width = max_width
        height = width / aspect
    else:
        height = max_height
        width = height * aspect
    pic_left = left + (max_width - width) / 2
    pic_top = top + (max_height - height) / 2
    pic = slide.shapes.add_picture(img_path, pic_left, pic_top, width=width, height=height)
    return pic, width, height
