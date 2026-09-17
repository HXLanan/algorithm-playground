# -*- coding: utf-8 -*-
"""服务层：二分查找。"""
from typing import Dict, Any, Optional

from ..algo import binary_search
from .. import config


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def search(nums=None, target=None, size=None, seed=None) -> Dict[str, Any]:
    """二分查找；不传数组时自动生成有序数组。"""
    if not nums:
        import random
        n = min(200, max(4, _to_int(size, 16)))
        rng = random.Random(_to_int(seed, None))
        nums = sorted(rng.sample(range(1, n * 4), n))
    if not isinstance(nums, (list, tuple)):
        raise ValueError("nums 必须是数组")
    try:
        nums = [int(v) for v in nums]
    except (TypeError, ValueError):
        raise ValueError("数组元素必须都是整数")
    if len(nums) < 2:
        raise ValueError("数组至少需要 2 个元素")
    if len(nums) > 2000:
        nums = nums[:2000]

    t = _to_int(target, nums[len(nums) // 2])
    res = binary_search.search(nums, t)
    res["exists"] = res["found"] >= 0
    return res


def lower_bound(nums=None, target=None) -> Dict[str, Any]:
    if not nums:
        nums = [1, 3, 3, 5, 7, 9, 11]
    nums = [int(v) for v in nums]
    t = _to_int(target, 3)
    return binary_search.lower_bound_demo(nums, t)
