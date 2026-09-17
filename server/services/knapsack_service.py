# -*- coding: utf-8 -*-
"""服务层：0-1 背包（动态规划）。"""
from typing import Dict, Any

from ..algo import knapsack


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_list(v, default, name):
    if v is None:
        return default
    if not isinstance(v, (list, tuple)):
        raise ValueError("%s 必须是数组" % name)
    out = []
    for x in v[:20]:
        try:
            out.append(int(x))
        except (TypeError, ValueError):
            raise ValueError("%s 元素必须是整数" % name)
    return out or default


def solve(weights=None, values=None, capacity=None) -> Dict[str, Any]:
    w = _clean_list(weights, [2, 3, 4, 5], "weights")
    v = _clean_list(values, [3, 4, 5, 6], "values")
    if len(w) != len(v):
        raise ValueError("weights 与 values 长度必须一致")
    if any(x <= 0 for x in w):
        raise ValueError("重量必须为正整数")
    cap = _to_int(capacity, 8)
    if cap < 1:
        raise ValueError("容量必须为正整数")
    if cap > 200:
        cap = 200
    return knapsack.solve(w, v, cap)


def random_case(n=None, seed=None) -> Dict[str, Any]:
    size = min(10, max(2, _to_int(n, 5)))
    return knapsack.random_case(size, _to_int(seed, None))


def default_case() -> Dict[str, Any]:
    return knapsack.default_case()
