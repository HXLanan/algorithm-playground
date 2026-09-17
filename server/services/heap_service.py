# -*- coding: utf-8 -*-
"""服务层：堆与优先队列。"""
from typing import Dict, Any

from ..algo import heap


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean(values, default):
    if values is None:
        return default
    if not isinstance(values, (list, tuple)):
        raise ValueError("values 必须是数组")
    out = []
    for v in values[:40]:
        try:
            out.append(int(v))
        except (TypeError, ValueError):
            raise ValueError("元素必须是整数")
    return out or default


def demo(values=None, pops=None) -> Dict[str, Any]:
    vals = _clean(values, [5, 2, 8, 1, 9, 3, 7])
    p = min(20, max(1, _to_int(pops, 3)))
    return heap.demo(vals, p)


def sort(values=None) -> Dict[str, Any]:
    vals = _clean(values, [5, 2, 8, 1, 9, 3, 7])
    return heap.heap_sort(vals)
