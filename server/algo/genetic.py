# -*- coding: utf-8 -*-
"""核心算法模块：遗传算法（小世界进化）。

个体是一对基因 (x, y) ∈ [0,1]²，"金峰"是目标点。
适应度 = 离金峰越近越高。通过 选择 → 交叉 → 变异 迭代进化。

纯标准库实现（random / math），可独立测试。
"""
import math
import random
from typing import List, Dict, Any, Tuple, Optional

GOLD = (0.72, 0.66)      # 金峰位置
MUTATION_RATE = 0.15     # 变异概率
MUTATION_SPAN = 0.03     # 变异扰动幅度
ELITE = 1                # 每代保留的精英个体数


def fitness(x: float, y: float) -> float:
    """适应度：到金峰距离越近值越大，范围约 (0, 1]。"""
    d = math.hypot(x - GOLD[0], y - GOLD[1])
    return 1.0 / (1.0 + d * d)


def random_population(size: int, rng: random.Random) -> List[Tuple[float, float]]:
    """随机撒点初始化种群。"""
    return [(rng.uniform(0.02, 0.98), rng.uniform(0.02, 0.98)) for _ in range(size)]


def _pick(pop: List[Tuple[float, float]], weights: List[float], total: float,
          rng: random.Random) -> Tuple[float, float]:
    """轮盘赌选择：适应度越高越容易被选中。"""
    if total <= 0:
        return pop[rng.randrange(len(pop))]
    r = rng.random() * total
    acc = 0.0
    for ind, wt in zip(pop, weights):
        acc += wt
        if acc >= r:
            return ind
    return pop[-1]


def evolve_generation(pop: List[Tuple[float, float]], rng: random.Random,
                      mutation_rate: float = MUTATION_RATE) -> List[Tuple[float, float]]:
    """进化一代：精英保留 + 轮盘赌选择 + 交叉 + 变异。"""
    scored = sorted(pop, key=lambda p: fitness(p[0], p[1]), reverse=True)
    weights = [fitness(p[0], p[1]) for p in scored]
    total = sum(weights)

    next_gen: List[Tuple[float, float]] = list(scored[:ELITE])   # 精英直接进入下一代

    while len(next_gen) < len(pop):
        pa = _pick(scored, weights, total, rng)
        pb = _pick(scored, weights, total, rng)
        # 交叉：每个基因随机取自父母之一
        cx = pa[0] if rng.random() < 0.5 else pb[0]
        cy = pa[1] if rng.random() < 0.5 else pb[1]
        # 变异：小概率扰动
        if rng.random() < mutation_rate:
            cx += rng.uniform(-MUTATION_SPAN, MUTATION_SPAN)
            cy += rng.uniform(-MUTATION_SPAN, MUTATION_SPAN)
        cx = min(0.99, max(0.01, cx))
        cy = min(0.99, max(0.01, cy))
        next_gen.append((cx, cy))

    return next_gen


def run(pop_size: int = 200, generations: int = 1, seed: Optional[int] = None,
        population: Optional[List[List[float]]] = None) -> Dict[str, Any]:
    """运行遗传算法若干代。

    若传入 population（来自前端上次状态），则在其基础上继续进化，
    这样前端可以做"点一次进化一代"的交互。
    """
    rng = random.Random(seed)
    if population:
        pop = [(float(p[0]), float(p[1])) for p in population]
    else:
        pop = random_population(pop_size, rng)

    for _ in range(max(1, generations)):
        pop = evolve_generation(pop, rng)

    best = max(pop, key=lambda p: fitness(p[0], p[1]))
    scores = [fitness(p[0], p[1]) for p in pop]
    avg = sum(scores) / len(scores)

    return {
        "gold": list(GOLD),
        "population": [[round(x, 4), round(y, 4)] for x, y in pop],
        "size": len(pop),
        "best": {
            "x": round(best[0], 4),
            "y": round(best[1], 4),
            "fitness": round(fitness(best[0], best[1]), 4),
        },
        "average_fitness": round(avg, 4),
        "generations": generations,
    }
