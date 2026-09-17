# -*- coding: utf-8 -*-
"""核心算法模块：蚁群算法（Ant Colony Optimization）。

灵感来自蚂蚁觅食：蚂蚁边走边留下"信息素"，路径越短、往返越快，
信息素积累越浓，后续蚂蚁越倾向于走它——正反馈最终收敛到最短路径。

这里用经典的 TSP（旅行商问题）作为演示场景。
"""
import random
from typing import List, Dict, Any, Optional

MAX_CITIES = 20
DEFAULT_ALPHA = 1.0      # 信息素重要程度
DEFAULT_BETA = 3.0       # 距离重要程度（启发式）
DEFAULT_RHO = 0.4        # 信息素挥发率
DEFAULT_Q = 100.0        # 信息素增量系数


def random_cities(n: int = 12, seed: Optional[int] = None) -> List[List[float]]:
    """在单位正方形内随机生成 n 个城市。"""
    rng = random.Random(seed)
    return [[round(rng.uniform(0.05, 0.95), 4), round(rng.uniform(0.05, 0.95), 4)]
            for _ in range(n)]


def _dist(a: List[float], b: List[float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def tour_length(cities: List[List[float]], tour: List[int]) -> float:
    """计算环游总长度。"""
    if len(tour) < 2:
        return 0.0
    total = 0.0
    for i in range(len(tour)):
        total += _dist(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total


def run(cities: Optional[List[List[float]]] = None, ants: int = 20,
        iterations: int = 30, seed: Optional[int] = None,
        alpha: float = DEFAULT_ALPHA, beta: float = DEFAULT_BETA,
        rho: float = DEFAULT_RHO) -> Dict[str, Any]:
    """运行蚁群算法求解 TSP。"""
    rng = random.Random(seed)
    if not cities:
        cities = random_cities(12, seed)
    n = len(cities)
    if n > MAX_CITIES:
        cities = cities[:MAX_CITIES]
        n = MAX_CITIES
    if n < 2:
        return {"error": "至少需要 2 个城市"}

    ants = max(1, min(100, int(ants)))
    iterations = max(1, min(200, int(iterations)))

    # 信息素初始化
    pheromone = [[1.0] * n for _ in range(n)]
    dist = [[_dist(cities[i], cities[j]) for j in range(n)] for i in range(n)]

    best_tour: List[int] = []
    best_len = float("inf")
    history: List[float] = []

    for _ in range(iterations):
        all_tours: List[List[int]] = []
        all_lens: List[float] = []
        for _a in range(ants):
            tour = _build_tour(n, dist, pheromone, alpha, beta, rng)
            length = tour_length(cities, tour)
            all_tours.append(tour)
            all_lens.append(length)
            if length < best_len:
                best_len = length
                best_tour = tour[:]
        # 挥发
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1.0 - rho)
        # 增强
        for tour, length in zip(all_tours, all_lens):
            if length <= 0:
                continue
            add = DEFAULT_Q / length
            for i in range(n):
                a = tour[i]
                b = tour[(i + 1) % n]
                pheromone[a][b] += add
                pheromone[b][a] += add
        history.append(round(best_len, 4))

    return {
        "cities": cities,
        "bestTour": best_tour,
        "bestLength": round(best_len, 4),
        "history": history,
        "iterations": iterations,
        "ants": ants,
        "explain": "信息素 = 集体记忆。短路径被走得更多、留下的信息素更浓，又吸引更多蚂蚁——正反馈让群体自发找到好路线。",
    }


def _build_tour(n: int, dist: List[List[float]], pheromone: List[List[float]],
                alpha: float, beta: float, rng: random.Random) -> List[int]:
    """单只蚂蚁按概率构造一条路径。"""
    start = rng.randrange(n)
    tour = [start]
    unvisited = set(range(n))
    unvisited.discard(start)
    cur = start
    while unvisited:
        weights = []
        for nxt in unvisited:
            d = dist[cur][nxt]
            tau = pheromone[cur][nxt] ** alpha
            eta = (1.0 / d if d > 1e-9 else 1e9) ** beta
            weights.append((nxt, tau * eta))
        total = sum(w for _, w in weights)
        if total <= 0:
            nxt = rng.choice(list(unvisited))
        else:
            r = rng.random() * total
            acc = 0.0
            nxt = weights[-1][0]
            for node, w in weights:
                acc += w
                if acc >= r:
                    nxt = node
                    break
        tour.append(nxt)
        unvisited.discard(nxt)
        cur = nxt
    return tour
