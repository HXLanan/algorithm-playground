# -*- coding: utf-8 -*-
"""核心算法模块：汉诺塔（递归的经典范式）。

规则：三根柱子 A/B/C，n 个由小到大叠放的圆盘，每次只能移动一个盘，
且大盘不能压在小盘上。目标：把 A 上全部圆盘搬到 C。

最少移动次数 = 2^n - 1（又一个指数爆炸，与麦粒棋盘遥相呼应）。
"""
from typing import List, Dict, Any, Optional

MAX_DISKS = 12          # 12 盘 = 4095 步，步骤序列仍可接受
MAX_STEPS = 8192


def solve(n: int) -> List[Dict[str, Any]]:
    """生成移动步骤序列（迭代式，避免深递归）。"""
    steps: List[Dict[str, Any]] = []
    # 用显式栈模拟递归： (n, from, to, aux, stage)
    stack = [(n, "A", "C", "B", 0)]
    while stack:
        cnt, frm, to, aux, stage = stack.pop()
        if cnt == 0:
            continue
        if cnt == 1:
            steps.append({"disk": 1, "from": frm, "to": to})
            if len(steps) > MAX_STEPS:
                break
            continue
        if stage == 0:
            # 先处理 n-1: from -> aux，再移动 n，再处理 n-1: aux -> to
            stack.append((cnt, frm, to, aux, 1))          # 稍后做移动
            stack.append((cnt - 1, frm, aux, to, 0))      # 先做左半
        else:
            steps.append({"disk": cnt, "from": frm, "to": to})
            stack.append((cnt - 1, aux, to, frm, 0))      # 再做右半
            if len(steps) > MAX_STEPS:
                break
    return steps


def simulate(n: int, up_to: Optional[int] = None) -> Dict[str, Any]:
    """模拟整个搬运过程，给出每一步的三柱状态快照。"""
    steps = solve(n)
    if up_to is not None:
        steps = steps[:max(0, up_to)]

    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}   # 大数在底
    snapshots = [{"pegs": _copy(pegs), "move": None, "index": 0}]

    for i, mv in enumerate(steps, start=1):
        disk = pegs[mv["from"]].pop()
        pegs[mv["to"]].append(disk)
        snapshots.append({"pegs": _copy(pegs), "move": mv, "index": i})

    return {
        "disks": n,
        "totalMoves": (1 << n) - 1,       # 理论最少步数
        "steps": steps,
        "snapshots": snapshots,
        "solved": len(steps) == (1 << n) - 1,
        "explain": "最少移动次数 = 2^n - 1，增长极快：n=10 需 1023 步，n=64 需 1.8×10^19 步（即麦粒棋盘的那个天文数字）。",
    }


def _copy(pegs: Dict[str, List[int]]) -> Dict[str, List[int]]:
    return {k: v[:] for k, v in pegs.items()}


def move_count_table(sizes: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    """展示不同盘数所需的移动次数（指数增长）。"""
    if sizes is None:
        sizes = [1, 2, 3, 5, 8, 10, 16, 20, 32, 64]
    out = []
    for n in sizes:
        v = (1 << n) - 1
        s = str(v)
        out.append({
            "n": n,
            "moves": v,
            "moves_str": s if len(s) <= 12 else "%s.%se%d" % (s[0], s[1:3], len(s) - 1),
        })
    return out
