# -*- coding: utf-8 -*-
"""服务层：康威生命游戏。"""
from typing import Dict, Any, Optional

from ..algo import life
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def new_grid(rows=None, cols=None, density=None, seed=None,
             pattern: Optional[str] = None) -> Dict[str, Any]:
    """创建初始网格：随机撒点，或摆放指定图案。"""
    rows = min(config.LIFE_MAX_DIM, max(5, _to_int(rows, 30)))
    cols = min(config.LIFE_MAX_DIM, max(5, _to_int(cols, 45)))

    if pattern and pattern in life.PATTERNS:
        g = life.empty_grid(rows, cols)
        life.place_pattern(g, pattern, top=rows // 2 - 3, left=cols // 2 - 3)
    else:
        d = density
        try:
            d = float(d) if d is not None else 0.28
        except (TypeError, ValueError):
            d = 0.28
        d = min(0.95, max(0.02, d))
        g = life.random_grid(rows, cols, d, seed=_to_int(seed, None))

    return {
        "grid": g,
        "rows": rows,
        "cols": cols,
        "alive": life._population(g),
        "pattern": pattern or "random",
    }


def evolve(grid, generations=1) -> Dict[str, Any]:
    """演化若干代。"""
    if not grid or not isinstance(grid, (list, tuple)):
        raise ValueError("grid 不能为空")
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows < 2 or cols < 2:
        raise ValueError("网格至少 2x2")
    if rows > config.LIFE_MAX_DIM or cols > config.LIFE_MAX_DIM:
        raise ValueError("网格过大（上限 %d）" % config.LIFE_MAX_DIM)

    try:
        g = [[1 if int(v) else 0 for v in row] for row in grid]
    except (TypeError, ValueError):
        raise ValueError("网格元素必须为 0/1")

    gens = min(500, max(1, _to_int(generations, 1)))
    return life.run(g, gens)


def patterns() -> Dict[str, Any]:
    """可选的经典图案。"""
    return {
        "patterns": [{"id": k, "name": life.PATTERN_NAMES.get(k, k)}
                     for k in life.PATTERNS]
    }
