# -*- coding: utf-8 -*-
"""服务层：蒙特卡罗估算 π。"""
from typing import Dict, Any

from ..algo import montecarlo
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def estimate(total=None, seed=None) -> Dict[str, Any]:
    """撒点估算 π。"""
    t = _to_int(total, 3000)
    if t < 10:
        t = 10
    if t > config.MONTE_CARLO_MAX:
        t = config.MONTE_CARLO_MAX
    s = _to_int(seed, None)
    return montecarlo.estimate(t, s)


def convergence(seed=None) -> Dict[str, Any]:
    """收敛曲线。"""
    return {"curve": montecarlo.convergence(_to_int(seed, None))}
