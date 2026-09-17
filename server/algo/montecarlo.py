# -*- coding: utf-8 -*-
"""核心算法模块：蒙特卡罗方法估算 π。

原理：在单位正方形内随机撒点，落在内切圆（半径 0.5，圆心 0.5,0.5）
中的比例 ≈ 圆面积 / 正方形面积 = (π/4) / 1，所以 π ≈ 4 × 命中比例。

用随机性解决确定性问题——概率算法的直观示例。
"""
import math
import random
from typing import List, Dict, Any, Optional

MAX_POINTS = 200000


def estimate(total: int = 3000, seed: Optional[int] = None,
             keep_points: int = 1500) -> Dict[str, Any]:
    """撒 total 个点估算 π。

    keep_points 控制返回给前端的点数量（避免响应过大），
    统计仍用全部点，保证精度。
    """
    if total < 1:
        total = 1
    if total > MAX_POINTS:
        total = MAX_POINTS

    rng = random.Random(seed)
    inside = 0
    pts = []                 # 保留用于可视化的点
    keep_every = max(1, total // keep_points)

    for i in range(total):
        x = rng.random()
        y = rng.random()
        hit = (x - 0.5) ** 2 + (y - 0.5) ** 2 <= 0.25
        if hit:
            inside += 1
        if i % keep_every == 0 and len(pts) < keep_points:
            pts.append([round(x, 4), round(y, 4), 1 if hit else 0])

    ratio = inside / total
    pi_est = 4.0 * ratio
    return {
        "total": total,
        "inside": inside,
        "ratio": ratio,
        "pi": pi_est,
        "error": abs(pi_est - math.pi),
        "points": pts,
        "explain": "撒点越多，估计越准——但精度只按 1/√N 提升：想把误差减半，点数要翻 4 倍。",
    }


def convergence(seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """展示随撒点数增加，π 估计值如何逐步收敛。"""
    rng = random.Random(seed)
    marks = [10, 50, 100, 500, 1000, 5000, 10000, 50000]
    out = []
    inside = 0
    n = 0
    mi = 0
    for n in range(1, marks[-1] + 1):
        x = rng.random(); y = rng.random()
        if (x - 0.5) ** 2 + (y - 0.5) ** 2 <= 0.25:
            inside += 1
        if mi < len(marks) and n == marks[mi]:
            est = 4.0 * inside / n
            out.append({"n": n, "pi": round(est, 5),
                        "error": round(abs(est - math.pi), 5)})
            mi += 1
    return out
