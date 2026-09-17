# -*- coding: utf-8 -*-
"""核心算法模块：指数爆炸（麦粒棋盘）。

典故：棋盘第 1 格放 1 粒、第 2 格 2 粒、第 3 格 4 粒……
每格是前一格的 2 倍，共 64 格。国王答应后才发现这是天文数字。

本模块用 Python 原生 int（任意精度）计算，不存在溢出问题。
"""
from typing import List, Dict, Any, Optional

CELLS = 64
GRAIN_GRAM = 0.03                 # 每粒小麦约 0.03 克
WORLD_WHEAT_TON_PER_YEAR = 780_000_000   # 全球年产小麦（吨）


def grain_at(cell: int) -> int:
    """第 cell 格（1-based）的麦粒数 = 2^(cell-1)。"""
    if cell < 1:
        return 0
    return 1 << (cell - 1)


def build_board(cells: int = CELLS) -> Dict[str, Any]:
    """构造棋盘数据：每格粒数、累计粒数、重量类比。"""
    rows: List[Dict[str, Any]] = []
    total = 0
    for i in range(1, cells + 1):
        g = grain_at(i)
        total += g
        rows.append({
            "cell": i,
            "grain": g,
            "grain_str": _short(g),
            "cumulative": total,
            "cumulative_str": _short(total),
        })

    grams = total * GRAIN_GRAM
    tons = grams / 1_000_000.0
    years = tons / WORLD_WHEAT_TON_PER_YEAR

    return {
        "cells": cells,
        "rows": rows,
        "total_grain": total,
        "total_grain_str": _short(total),
        "total_tons": tons,
        "total_tons_str": _short(int(tons)),
        "world_years": years,
        "explain": (
            "第 64 格需要 2^63 粒，全盘合计 2^64 - 1 粒。"
            "这就是指数增长 O(2^n)：前期看似平缓，越过临界点后瞬间吞没一切。"
        ),
    }


def _short(v: int) -> str:
    """把超长整数缩写成 1.23eX 形式，便于展示。"""
    s = str(v)
    if len(s) <= 8:
        return s
    return "%s.%se%d" % (s[0], s[1:3], len(s) - 1)


def complexity_table(sizes: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    """对比不同复杂度在规模 n 下的运算量，直观显示指数之恐怖。"""
    if sizes is None:
        sizes = [10, 20, 30, 40, 50, 64]
    table = []
    for n in sizes:
        table.append({
            "n": n,
            "O_n": n,
            "O_n2": n * n,
            "O_2n": 1 << n,
            "O_2n_str": _short(1 << n),
        })
    return table
