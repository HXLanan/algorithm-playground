# -*- coding: utf-8 -*-
"""核心算法模块：康威生命游戏（元胞自动机）。

三条规则就能涌现出滑翔机、振荡子等复杂结构：
  1. 活细胞邻居 < 2  → 孤独而死
  2. 活细胞邻居 2或3 → 继续存活
  3. 活细胞邻居 > 3  → 拥挤而死
  4. 死细胞邻居 = 3  → 繁殖复活

纯标准库实现（这里用一个纯 Python 的网格演化，逻辑直观可读）。
"""
from typing import List, Dict, Any, Optional

# 常用图案（RLE 风格简化为坐标列表）
PATTERNS = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "block": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "toad": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
    "beacon": [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)],
    "pulsar": [
        (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
        (0, 2), (5, 2), (7, 2), (12, 2),
        (0, 3), (5, 3), (7, 3), (12, 3),
        (0, 4), (5, 4), (7, 4), (12, 4),
        (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
        (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
        (0, 8), (5, 8), (7, 8), (12, 8),
        (0, 9), (5, 9), (7, 9), (12, 9),
        (0, 10), (5, 10), (7, 10), (12, 10),
        (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12),
    ],
    "lwss": [(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)],
}

PATTERN_NAMES = {
    "glider": "滑翔机（会斜着飞）",
    "blinker": "闪烁器（周期2振荡）",
    "block": "方块（静止不变）",
    "toad": "蟾蜍（周期2振荡）",
    "beacon": "信标（周期2振荡）",
    "pulsar": "脉冲星（周期3，大型）",
    "lwss": "轻型飞船（会横着飞）",
}


def empty_grid(rows: int, cols: int) -> List[List[int]]:
    """创建全死网格。"""
    return [[0] * cols for _ in range(rows)]


def random_grid(rows: int, cols: int, density: float = 0.3,
                seed: Optional[int] = None) -> List[List[int]]:
    """随机撒活细胞。"""
    import random
    rng = random.Random(seed)
    return [[1 if rng.random() < density else 0 for _ in range(cols)]
            for _ in range(rows)]


def place_pattern(grid: List[List[int]], pattern: str,
                  top: int = 1, left: int = 1) -> List[List[int]]:
    """把一个图案放到网格指定位置（越界自动忽略）。"""
    cells = PATTERNS.get(pattern)
    if not cells:
        return grid
    rows, cols = len(grid), len(grid[0])
    for dr, dc in cells:
        r, c = top + dr, left + dc
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = 1
    return grid


def count_neighbors(grid: List[List[int]], r: int, c: int) -> int:
    """统计八邻域中的活细胞数（环形边界）。"""
    rows, cols = len(grid), len(grid[0])
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            total += grid[(r + dr) % rows][(c + dc) % cols]
    return total


def step(grid: List[List[int]]) -> List[List[int]]:
    """演化一代。"""
    rows, cols = len(grid), len(grid[0])
    new = empty_grid(rows, cols)
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            if grid[r][c] == 1:
                new[r][c] = 1 if (n == 2 or n == 3) else 0
            else:
                new[r][c] = 1 if n == 3 else 0
    return new


def run(grid: List[List[int]], generations: int = 1) -> Dict[str, Any]:
    """演化若干代，返回最终网格与每一代的人口数。"""
    g = [row[:] for row in grid]
    history = [_population(g)]
    frames = [g]
    for _ in range(max(0, generations)):
        g = step(g)
        history.append(_population(g))
        # 只保留最近若干帧，避免响应过大
        if len(frames) < 60:
            frames.append(g)
    return {
        "grid": g,
        "population": history,
        "frames": frames,
        "generations": generations,
        "alive": history[-1],
    }


def _population(grid: List[List[int]]) -> int:
    return sum(sum(row) for row in grid)
