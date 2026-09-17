# -*- coding: utf-8 -*-
"""服务层：曼德勃罗集分形。"""
from typing import Dict, Any, Optional

from ..algo import mandelbrot
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _to_float(v, default):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def render(width=None, height=None, cx=None, cy=None,
           zoom=None, max_iter=None) -> Dict[str, Any]:
    """渲染一块区域。"""
    w = min(config.MANDEL_MAX_W, max(16, _to_int(width, 120)))
    h = min(config.MANDEL_MAX_H, max(12, _to_int(height, 80)))
    return mandelbrot.render(
        width=w, height=h,
        center_x=_to_float(cx, -0.5),
        center_y=_to_float(cy, 0.0),
        zoom=_to_float(zoom, 1.0),
        max_iter=_to_int(max_iter, 60),
    )


def preset_views() -> Dict[str, Any]:
    """几个著名的缩放视点。"""
    return {"views": [
        {"id": "full", "name": "全景", "cx": -0.5, "cy": 0.0, "zoom": 1.0},
        {"id": "seahorse", "name": "海马谷", "cx": -0.743643887, "cy": 0.131825904, "zoom": 200.0},
        {"id": "elephant", "name": "大象谷", "cx": 0.2820, "cy": 0.0100, "zoom": 120.0},
        {"id": "spiral", "name": "螺旋", "cx": -0.7269, "cy": 0.1889, "zoom": 80.0},
        {"id": "triple", "name": "三叉", "cx": -1.25066, "cy": 0.02012, "zoom": 60.0},
    ]}


def orbit(cx=None, cy=None, steps=None) -> Dict[str, Any]:
    """单点迭代轨迹。"""
    return mandelbrot.orbit(
        _to_float(cx, -0.4), _to_float(cy, 0.6),
        min(200, max(1, _to_int(steps, 30))))
