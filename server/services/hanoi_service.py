# -*- coding: utf-8 -*-
"""服务层：汉诺塔。"""
from typing import Dict, Any, Optional

from ..algo import hanoi
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def simulate(disks=None, up_to=None) -> Dict[str, Any]:
    """模拟搬运过程。"""
    n = _to_int(disks, 4)
    if n < 1:
        n = 1
    if n > config.HANOI_MAX_DISKS:
        n = config.HANOI_MAX_DISKS

    up = None
    if up_to is not None:
        up = max(0, _to_int(up_to, 0))
    return hanoi.simulate(n, up)


def move_counts() -> Dict[str, Any]:
    """展示 2^n - 1 的指数增长。"""
    return {"table": hanoi.move_count_table()}
