# -*- coding: utf-8 -*-
"""服务层：分治排序（快速排序 / 归并排序）。"""
from typing import Dict, Any, Optional

from ..algo import divide_sort
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def make_random(n: Optional[int] = None) -> Dict[str, Any]:
    size = _to_int(n, 12)
    size = min(config.MAX_ARRAY_SIZE, max(2, size))
    return {"array": divide_sort.random_array(size), "count": size}


def run(array=None, algo: str = "quick") -> Dict[str, Any]:
    if algo not in divide_sort.SUPPORTED:
        raise ValueError("不支持的算法：%s（可选：quick, merge）" % algo)
    if array is None:
        array = divide_sort.random_array(10)
    if not isinstance(array, (list, tuple)):
        raise ValueError("array 必须是数组")
    try:
        array = [int(v) for v in array]
    except (TypeError, ValueError):
        raise ValueError("数组元素必须都是整数")
    if len(array) < 2:
        raise ValueError("数组至少需要 2 个元素")
    if len(array) > config.MAX_ARRAY_SIZE:
        raise ValueError("数组元素过多（上限 %d）" % config.MAX_ARRAY_SIZE)
    return divide_sort.build_steps(array, algo)
