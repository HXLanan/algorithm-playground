# -*- coding: utf-8 -*-
"""服务层：素数筛。"""
from typing import Dict, Any

from ..algo import prime_sieve


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def sieve(n=None) -> Dict[str, Any]:
    size = _to_int(n, 100)
    if size < 2:
        size = 2
    if size > 5000:
        size = 5000
    return prime_sieve.sieve(size)


def density(n=None) -> Dict[str, Any]:
    size = _to_int(n, 1000)
    size = min(5000, max(100, size))
    return prime_sieve.density(size)
