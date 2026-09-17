# -*- coding: utf-8 -*-
"""服务层：约瑟夫环。"""
from typing import Dict, Any

from ..algo import josephus


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def simulate(n=None, k=None) -> Dict[str, Any]:
    size = min(josephus.MAX_SIM_N, max(1, _to_int(n, 10)))
    step = max(1, _to_int(k, 3))
    return josephus.simulate(size, step)


def formula(n=None, k=None) -> Dict[str, Any]:
    size = min(josephus.MAX_FORMULA_N, max(1, _to_int(n, 100000)))
    step = max(1, _to_int(k, 3))
    return josephus.formula(size, step)


def default_case() -> Dict[str, Any]:
    return josephus.default_case()
