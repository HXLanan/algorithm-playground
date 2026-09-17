# -*- coding: utf-8 -*-
"""核心算法模块：曼德勃罗集分形。

对复平面上的每个点 c，迭代 z_{n+1} = z_n^2 + c（z_0 = 0）。
若 |z| 始终有界（不发散到无穷），则 c 属于曼德勃罗集。

它的边界具有无限细节——放大任意倍数都能看到新的结构，
是"简单规则产生无限复杂"的最美例证。
"""
from typing import List, Dict, Any, Optional

MAX_ITER = 200


def render(width: int = 120, height: int = 80,
           center_x: float = -0.5, center_y: float = 0.0,
           zoom: float = 1.0, max_iter: int = 80) -> Dict[str, Any]:
    """渲染一块曼德勃罗集区域。

    返回二维的"逃逸迭代次数"网格，前端据此上色。
    限制分辨率以保证响应速度（这是 CPU 密集型计算）。
    """
    if width < 8:
        width = 8
    if height < 8:
        height = 8
    if width > 300:
        width = 300
    if height > 200:
        height = 200
    if max_iter < 10:
        max_iter = 10
    if max_iter > MAX_ITER:
        max_iter = MAX_ITER
    if zoom < 0.0001:
        zoom = 0.0001

    # 视野：默认宽 3.0
    span = 3.0 / zoom
    aspect = width / float(height)
    x0 = center_x - span / 2.0
    y0 = center_y - (span / aspect) / 2.0
    dx = span / width
    dy = (span / aspect) / height

    grid: List[List[int]] = []
    inside_count = 0
    for j in range(height):
        row = []
        cy = y0 + j * dy
        for i in range(width):
            cx = x0 + i * dx
            zx = 0.0
            zy = 0.0
            it = 0
            while it < max_iter:
                zx2 = zx * zx
                zy2 = zy * zy
                if zx2 + zy2 > 4.0:
                    break
                zy = 2.0 * zx * zy + cy
                zx = zx2 - zy2 + cx
                it += 1
            if it >= max_iter:
                inside_count += 1
            row.append(it)
        grid.append(row)

    return {
        "width": width,
        "height": height,
        "center": [center_x, center_y],
        "zoom": zoom,
        "maxIter": max_iter,
        "grid": grid,
        "insideCount": inside_count,
        "total": width * height,
        "explain": "黑色区域是「集合内部」（永不逃逸）；彩色表示逃逸速度——越亮逃逸越快。放大边界能看到无限自相似结构。",
    }


def orbit(cx: float = -0.4, cy: float = 0.6, steps: int = 30) -> Dict[str, Any]:
    """展示单个点的迭代轨迹（z 序列），用于讲"逃逸"的过程。"""
    if steps < 1:
        steps = 1
    if steps > 200:
        steps = 200
    zx, zy = 0.0, 0.0
    pts = [[0.0, 0.0]]
    escaped = False
    for _ in range(steps):
        zx2 = zx * zx
        zy2 = zy * zy
        if zx2 + zy2 > 4.0:
            escaped = True
            break
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
        pts.append([round(zx, 5), round(zy, 5)])
    return {
        "c": [cx, cy],
        "points": pts,
        "escaped": escaped,
        "iterations": len(pts) - 1,
    }
