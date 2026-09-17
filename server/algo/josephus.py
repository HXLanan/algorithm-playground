# -*- coding: utf-8 -*-
"""核心算法模块：约瑟夫环。

n 个人围成一圈，从第 1 个人开始报数，每报到第 k 个人就出列，
然后从下一个人重新报数，直到所有人出列。求出列顺序。

朴素做法：用链表模拟，O(n·k)。
数学解法：有递推公式 f(n) = (f(n-1) + k) % n，可以 O(n) 直接算出最后幸存者。
"""
from typing import List, Dict, Any

MAX_SIM_N = 2000        # 朴素模拟的规模上限（O(n·k)）；更大规模请用 formula()
MAX_FORMULA_N = 100000  # 递推解法的规模上限


def simulate(n: int, k: int, collect_frames: bool = True) -> Dict[str, Any]:
    """模拟出列过程。

    注意：n 的上限（MAX_SIM_N）只用于**限制模拟规模**，
    因为朴素模拟是 O(n·k)；需要更大规模时请用 formula() 的 O(n) 递推。
    """
    if n < 1:
        n = 1
    if n > MAX_SIM_N:
        n = MAX_SIM_N
    if k < 1:
        k = 1

    people = list(range(1, n + 1))
    order: List[int] = []
    frames: List[Dict[str, Any]] = []
    idx = 0
    round_no = 0

    while people:
        idx = (idx + k - 1) % len(people)
        out = people.pop(idx)
        order.append(out)
        round_no += 1
        if collect_frames and len(frames) < 300:
            frames.append({
                "out": out,
                "remaining": list(people),
                "round": round_no,
                "msg": "第 %d 个出列：%d（剩余 %d 人）" % (round_no, out, len(people)),
            })

    return {
        "n": n,
        "k": k,
        "order": order,
        "last": order[-1] if order else None,
        "frames": frames,
        "explain": "模拟法直观但慢（O(n·k)）。数学递推只需一行："
                   "f(1)=0，f(n)=(f(n-1)+k) % n，最后 +1 转成 1-based 编号。"
                   "用 formula() 可以轻松处理 n = 10 万以上的规模。",
    }


def formula(n: int, k: int) -> Dict[str, Any]:
    """数学递推解法：直接算出最后幸存者。"""
    if n < 1:
        n = 1
    if k < 1:
        k = 1
    if n > 100000:
        n = 100000

    f = 0
    steps = []
    for i in range(2, n + 1):
        f = (f + k) % i
        if i <= 20 or i == n:
            steps.append({
                "i": i,
                "f": f + 1,
                "msg": "f(%d) = (f(%d) + %d) %% %d = %d → 1-based 编号 %d"
                       % (i, i - 1, k, i, f, f + 1),
            })

    return {
        "n": n,
        "k": k,
        "survivor": f + 1,
        "steps": steps,
        "explain": "这个递推之所以成立：删掉一个人后，问题规模变为 n-1，"
                   "但编号起点变了 k 位。把新编号映射回旧编号，就得到 (f(n-1)+k) % n。"
                   "于是 O(n·k) 的模拟被压缩成 O(n) 的递推。",
    }


def default_case() -> Dict[str, Any]:
    return {"n": 10, "k": 3}
