# -*- coding: utf-8 -*-
"""服务层：A* 寻路。"""
from typing import Dict, Any, Optional

from ..algo import pathfinding
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _make_maze(rows: int, cols: int, seed: Optional[int] = None):
    """生成带墙的默认地图，让 A* 的启发式优势能显现出来。"""
    import random
    rng = random.Random(seed)
    grid = [[0] * cols for _ in range(rows)]
    # 随机竖墙 + 横墙，留出通道
    for _ in range((rows * cols) // 5):
        r = rng.randrange(rows)
        c = rng.randrange(cols)
        grid[r][c] = 1
    # 保证起点终点为空
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0
    return grid


def search(grid=None, start=None, goal=None, algo="astar",
           diagonal=False, rows=None, cols=None, seed=None) -> Dict[str, Any]:
    """执行搜索；不传 grid 时自动生成迷宫。"""
    if not grid:
        r = min(config.PATH_MAX_DIM, max(5, _to_int(rows, 20)))
        c = min(config.PATH_MAX_DIM, max(5, _to_int(cols, 30)))
        grid = _make_maze(r, c, _to_int(seed, None))
    else:
        if not isinstance(grid, (list, tuple)) or not grid:
            raise ValueError("grid 格式不正确")
        r, c = len(grid), len(grid[0])
        if r > config.PATH_MAX_DIM or c > config.PATH_MAX_DIM:
            raise ValueError("地图过大（上限 %d）" % config.PATH_MAX_DIM)
        try:
            grid = [[1 if int(v) else 0 for v in row] for row in grid]
        except (TypeError, ValueError):
            raise ValueError("grid 元素必须为 0/1")

    rows_n, cols_n = len(grid), len(grid[0])
    s = start if (start and len(start) == 2) else [0, 0]
    g = goal if (goal and len(goal) == 2) else [rows_n - 1, cols_n - 1]
    s = [min(rows_n - 1, max(0, _to_int(s[0], 0))), min(cols_n - 1, max(0, _to_int(s[1], 0)))]
    g = [min(rows_n - 1, max(0, _to_int(g[0], 0))), min(cols_n - 1, max(0, _to_int(g[1], 0)))]

    res = pathfinding.search(grid, (s[0], s[1]), (g[0], g[1]),
                             algo, bool(diagonal))
    res["grid"] = grid
    return res


def compare(grid=None, start=None, goal=None, rows=None, cols=None) -> Dict[str, Any]:
    """四种算法对比。"""
    if not grid:
        r = min(config.PATH_MAX_DIM, max(5, _to_int(rows, 20)))
        c = min(config.PATH_MAX_DIM, max(5, _to_int(cols, 30)))
        grid = _make_maze(r, c, None)
    rows_n, cols_n = len(grid), len(grid[0])
    s = start if (start and len(start) == 2) else [0, 0]
    g = goal if (goal and len(goal) == 2) else [rows_n - 1, cols_n - 1]
    out = pathfinding.compare(grid, (s[0], s[1]), (g[0], g[1]))
    out["grid"] = grid
    return out
