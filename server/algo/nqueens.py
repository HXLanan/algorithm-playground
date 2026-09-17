# -*- coding: utf-8 -*-
"""核心算法模块：N 皇后（回溯法的典范）。

在 n×n 棋盘上放置 n 个皇后，要求互不攻击（不同行、不同列、不同对角线）。
回溯法：逐行尝试，冲突就撤回换一个位置——"摸着石头过河"。

注意：本模块把「统计解的总数」与「收集过程帧」解耦——
解数统计始终完整（不受帧数上限影响），过程帧则限量以免响应过大。
"""
from typing import List, Dict, Any, Optional

MAX_N = 10          # 10 皇后已有 724 个解
MAX_STEPS = 20000   # 过程帧上限（只影响动画，不影响解数统计）
MAX_KEEP_SOLUTIONS = 50   # 最多回传多少个完整解


def solve(n: int, first_only: bool = False,
          max_solutions: int = 5) -> Dict[str, Any]:
    """回溯求解。

    返回：
      - solutionCount: 解的**总数**（完整统计）
      - solutions: 前 max_solutions 个解（供展示）
      - steps: 过程帧（限量，供前端播放"尝试→冲突→撤回"动画）
    """
    if n < 1:
        n = 1
    if n > MAX_N:
        n = MAX_N

    keep = max(1, min(MAX_KEEP_SOLUTIONS, int(max_solutions)))
    solutions: List[List[int]] = []
    steps: List[Dict[str, Any]] = []
    queens = [-1] * n
    cols = set()
    diag1 = set()      # row - col
    diag2 = set()      # row + col
    counters = {"total": 0, "conflicts": 0}

    def record(frame: Dict[str, Any]) -> None:
        """只在未超限时记录过程帧。"""
        if len(steps) < MAX_STEPS:
            steps.append(frame)

    def bt(row: int) -> None:
        if row == n:
            counters["total"] += 1
            if len(solutions) < keep:
                solutions.append(queens[:])
            record({"type": "solution", "row": -1, "col": -1,
                    "board": queens[:], "msg": "找到一个解！（累计 %d 个）" % counters["total"]})
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                counters["conflicts"] += 1
                record({"type": "conflict", "row": row, "col": col,
                        "board": queens[:],
                        "msg": "第 %d 行第 %d 列被攻击，换一列" % (row, col)})
                continue
            queens[row] = col
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            record({"type": "place", "row": row, "col": col,
                    "board": queens[:],
                    "msg": "在第 %d 行第 %d 列放置皇后" % (row, col)})
            bt(row + 1)
            queens[row] = -1
            cols.discard(col); diag1.discard(row - col); diag2.discard(row + col)
            record({"type": "backtrack", "row": row, "col": col,
                    "board": queens[:], "msg": "第 %d 行此路不通，撤回" % row})
            if first_only and counters["total"] > 0:
                return

    bt(0)

    return {
        "n": n,
        "solutions": solutions,
        "solutionCount": counters["total"],       # 完整解数
        "steps": steps,
        "conflicts": counters["conflicts"],
        "truncated": len(steps) >= MAX_STEPS,
        "explain": "回溯法：逐行试探 → 冲突则撤回换位。它的本质是「有剪枝的枚举」，剪枝越狠跑得越快。",
    }
