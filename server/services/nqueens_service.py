# -*- coding: utf-8 -*-
"""服务层：N 皇后。"""
from typing import Dict, Any

from ..algo import nqueens
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def solve(n=None, first_only=False, max_solutions=5) -> Dict[str, Any]:
    """求解 N 皇后并返回过程帧。"""
    size = _to_int(n, 6)
    if size < 1:
        size = 1
    if size > config.NQUEENS_MAX_N:
        size = config.NQUEENS_MAX_N

    ms = _to_int(max_solutions, 5)
    ms = min(20, max(1, ms))
    return nqueens.solve(size, bool(first_only), ms)


def counts() -> Dict[str, Any]:
    """1..8 皇后的解的数量（经典序列）。"""
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    return {
        "table": [{"n": k, "solutions": v} for k, v in sorted(known.items())],
        "explain": "n=2、3 无解；n=8 有 92 个解。解的数量增长极快，这也是为什么用回溯而不是暴力枚举全排列。",
    }
