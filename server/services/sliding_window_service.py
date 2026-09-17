# -*- coding: utf-8 -*-
"""服务层：滑动窗口。"""
from typing import Dict, Any

from ..algo import sliding_window


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_nums(nums, default):
    if nums is None:
        return default
    if not isinstance(nums, (list, tuple)):
        raise ValueError("nums 必须是数组")
    out = []
    for v in nums[:100]:
        try:
            out.append(int(v))
        except (TypeError, ValueError):
            raise ValueError("数组元素必须是整数")
    return out or default


def fixed(nums=None, k=None) -> Dict[str, Any]:
    arr = _clean_nums(nums, [2, 1, 5, 1, 3, 2])
    kk = min(len(arr), max(1, _to_int(k, 3)))
    return sliding_window.fixed_window(arr, kk)


def min_window(nums=None, target=None) -> Dict[str, Any]:
    arr = _clean_nums(nums, [2, 3, 1, 2, 4, 3])
    if any(v < 0 for v in arr):
        raise ValueError("本演示只支持非负数组")
    t = max(1, _to_int(target, 7))
    return sliding_window.min_length_window(arr, t)


def longest(text=None) -> Dict[str, Any]:
    s = str(text) if text is not None else "abcabcbb"
    if not s:
        raise ValueError("字符串不能为空")
    return sliding_window.longest_unique_substring(s)


def default_case() -> Dict[str, Any]:
    return sliding_window.default_case()
