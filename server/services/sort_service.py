# -*- coding: utf-8 -*-
"""服务层：排序业务编排。"""
from typing import Dict, Any, Optional

from ..algo import sorting
from .. import config


def make_random(n: Optional[int] = None) -> Dict[str, Any]:
    """生成随机数组（带参数校验）。"""
    if n is None:
        n = 10
    try:
        n = int(n)
    except (TypeError, ValueError):
        n = 10
    if n < 2:
        n = 2
    if n > config.MAX_ARRAY_SIZE:
        n = config.MAX_ARRAY_SIZE
    return {"array": sorting.random_array(n), "count": n}


def run_sort(array=None, algo: str = "bubble") -> Dict[str, Any]:
    """执行排序并返回全过程步骤序列。"""
    if algo not in sorting.SUPPORTED:
        raise ValueError("不支持的算法：%s" % algo)

    if array is None:
        array = sorting.random_array(10)
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

    return sorting.build_steps(array, algo)


def list_algorithms():
    """返回支持的排序算法列表。"""
    return [{"id": k, "name": sorting._ALGO_NAMES[k]} for k in sorting.SUPPORTED]
