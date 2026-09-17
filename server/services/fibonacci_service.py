# -*- coding: utf-8 -*-
"""服务层：斐波那契（兔子农场）业务编排。"""
from typing import Dict, Any, Optional

from ..algo import fib
from .. import config


def get_sequence(months: Optional[int] = None) -> Dict[str, Any]:
    """返回 0..months 月的兔子数据。"""
    if months is None:
        months = 20
    try:
        months = int(months)
    except (TypeError, ValueError):
        months = 20
    if months < 0:
        months = 0
    if months > config.MAX_FIB_MONTH:
        months = config.MAX_FIB_MONTH
    return fib.build_sequence(months)


def compare_cost(n: Optional[int] = None) -> Dict[str, Any]:
    """对比递归与迭代的调用次数，展示"递归为何慢爆"。

    调用次数由数学公式 O(n) 直接算出，不做真实的指数级递归，因此可放心取较大的 n。
    """
    if n is None:
        n = 25
    try:
        n = int(n)
    except (TypeError, ValueError):
        n = 25
    if n < 1:
        n = 1
    if n > 50:
        n = 50
    result = fib.recursion_cost(n)
    result["note"] = "朴素递归的调用次数约等于 2·F(n)，呈指数增长；迭代只需 O(n) 次。"
    return result
