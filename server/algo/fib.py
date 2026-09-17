# -*- coding: utf-8 -*-
"""核心算法模块：斐波那契数列（兔子农场）。

典故：每对兔子出生后第 2 个月起，每月生出一对新兔子，永不死。
由此得到 F(n) = F(n-1) + F(n-2)，F(1)=1, F(2)=1。

纯标准库实现。
"""
from typing import List, Dict, Any, Optional

MAX_MONTH = 40


def fib_iterative(n: int) -> int:
    """迭代法求第 n 个斐波那契数（O(n) 时间、O(1) 空间）。"""
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def fib_recursive(n: int, counter: Optional[Dict[str, int]] = None) -> int:
    """朴素递归法（用于教学对比：调用次数呈指数增长）。

    counter 用于累计调用次数，展示"为什么递归会爆炸"。
    注意：调用次数随 n 指数增长，n 较大时开销极高（这正是要演示的现象）。
    """
    if counter is not None:
        counter["calls"] = counter.get("calls", 0) + 1
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    return fib_recursive(n - 1, counter) + fib_recursive(n - 2, counter)


def count_recursive_calls(n: int) -> int:
    """仅统计朴素递归的调用次数，不真的做指数级计算。

    数学事实：朴素递归求 fib(n) 的调用次数恰好是 2*F(n) - 1。
    验证：n=3 → 2*2-1 = 3；n=5 → 2*5-1 = 9（与手工展开一致）。
    这样即便 n 很大也能瞬间给出结果，避免服务被拖死。
    """
    if n <= 0:
        return 1
    return 2 * fib_iterative(n) - 1


def build_sequence(months: int = 20) -> Dict[str, Any]:
    """构造 0..months 月的兔子数据序列。

    返回每个月：总量、本月新生、以及递推关系说明。
    """
    if months < 0:
        months = 0
    if months > MAX_MONTH:
        months = MAX_MONTH

    details: List[Dict[str, Any]] = []
    for m in range(0, months + 1):
        total = fib_iterative(m)
        if m == 0:
            newborn = 0            # 还没有兔子
        elif m == 1:
            newborn = 1            # 第 1 月：投放 1 对初始兔子（作为起点）
        else:
            newborn = fib_iterative(m) - fib_iterative(m - 1)   # = F(m-2)
        details.append({
            "month": m,
            "total": total,              # 现有兔子总对数
            "newborn": newborn,          # 本月新增的对数
            "formula": ("F(%d) = F(%d) + F(%d) = %d + %d" % (
                m, m - 1, m - 2, fib_iterative(m - 1), fib_iterative(m - 2))
                if m >= 2 else "起始条件"),
        })

    return {
        "months": months,
        "seq": [d["total"] for d in details],
        "details": details,
        "closed_form_hint": "F(n) 相邻两项之比趋近黄金比 φ ≈ 1.618",
    }


def recursion_cost(n: int) -> Dict[str, int]:
    """对比递归与迭代的调用次数，展示指数级开销。

    用数学公式直接算出调用次数，不做真实的指数级递归，保证响应迅速。
    """
    return {
        "n": n,
        "recursive_calls": count_recursive_calls(n),
        "iterative_calls": max(0, n - 2),
    }
