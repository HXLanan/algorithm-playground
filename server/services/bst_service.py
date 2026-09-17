# -*- coding: utf-8 -*-
"""服务层：二叉搜索树。"""
from typing import Dict, Any

from ..algo import bst


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_values(values, default):
    if values is None:
        return default
    if not isinstance(values, (list, tuple)):
        raise ValueError("values 必须是数组")
    out = []
    for v in values[:30]:
        try:
            out.append(int(v))
        except (TypeError, ValueError):
            raise ValueError("元素必须是整数")
    return out or default


def build(values=None) -> Dict[str, Any]:
    vals = _clean_values(values, [50, 30, 70, 20, 40, 60, 80])
    return bst.build(vals)


def search(values=None, target=None) -> Dict[str, Any]:
    vals = _clean_values(values, [50, 30, 70, 20, 40, 60, 80])
    t = _to_int(target, 40)
    return bst.search(vals, t)


def balanced(values=None) -> Dict[str, Any]:
    vals = _clean_values(values, list(range(1, 16)))
    return bst.balanced_check(vals)
