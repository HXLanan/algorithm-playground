# -*- coding: utf-8 -*-
"""服务层：快速幂。"""
from typing import Dict, Any

from ..algo import fast_power


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def power(base=None, exp=None, mod=None) -> Dict[str, Any]:
    b = _to_int(base, 2)
    e = _to_int(exp, 10)
    m = _to_int(mod, 0)

    if e < 0:
        raise ValueError("指数需为非负整数")
    if e > 100000:
        e = 100000
    if abs(b) > 10 ** 9:
        b = b % (10 ** 9)
    if m < 0:
        m = 0

    return fast_power.power(b, e, m)


def compare() -> Dict[str, Any]:
    return {"table": fast_power.compare_table()}
