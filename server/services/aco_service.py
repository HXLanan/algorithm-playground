# -*- coding: utf-8 -*-
"""服务层：蚁群算法（TSP）。"""
from typing import Dict, Any

from ..algo import aco
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def run(cities=None, ants=None, iterations=None, seed=None,
        new_cities=None, count=None) -> Dict[str, Any]:
    """运行蚁群算法。new_cities 为真时重新随机生成城市。"""
    if new_cities or not cities:
        n = min(config.ACO_MAX_CITIES, max(3, _to_int(count, 12)))
        cities = aco.random_cities(n, _to_int(seed, None))
    else:
        if not isinstance(cities, (list, tuple)) or len(cities) < 2:
            raise ValueError("cities 至少需要 2 个城市")
        try:
            cities = [[float(p[0]), float(p[1])] for p in cities]
        except (TypeError, ValueError, IndexError):
            raise ValueError("城市坐标格式不正确")

    a = min(100, max(1, _to_int(ants, 20)))
    it = min(200, max(1, _to_int(iterations, 30)))
    res = aco.run(cities, a, it, _to_int(seed, None))
    res["cities"] = cities
    return res
