# -*- coding: utf-8 -*-
"""核心算法模块：动态规划（0-1 背包）。

问题：容量为 W 的背包，n 件物品各有重量 wᵢ 和价值 vᵢ，每件**只能选或不选**，
求能装下的最大总价值。

DP 定义：dp[i][j] = 只考虑前 i 件物品、容量为 j 时的最大价值
转移：  dp[i][j] = max(dp[i-1][j],                    ← 不放第 i 件
                       dp[i-1][j-wᵢ] + vᵢ)            ← 放第 i 件（前提装得下）
"""
from typing import List, Dict, Any


def solve(weights: List[int], values: List[int], capacity: int) -> Dict[str, Any]:
    """求解 0-1 背包，返回 DP 表与每个单元格的推导过程。"""
    n = len(weights)
    if n == 0 or capacity <= 0:
        return {"maxValue": 0, "table": [], "picked": [], "steps": [],
                "explain": "无物品或容量为 0，答案自然是 0。"}

    # dp[i][j]: 前 i 件、容量 j 的最大价值
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    trace: List[Dict[str, Any]] = []

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for j in range(capacity + 1):
            skip = dp[i - 1][j]
            if w <= j:
                take = dp[i - 1][j - w] + v
                if take > skip:
                    dp[i][j] = take
                    trace.append({
                        "i": i, "j": j, "choice": "take",
                        "value": take, "skip": skip,
                        "msg": "容量 %d 装得下物品 %d（重 %d 值 %d）：放进去更划算（%d > %d）"
                               % (j, i, w, v, take, skip),
                    })
                else:
                    dp[i][j] = skip
                    trace.append({
                        "i": i, "j": j, "choice": "skip",
                        "value": skip, "take": take,
                        "msg": "容量 %d：放进去（%d）不如不放（%d）" % (j, take, skip),
                    })
            else:
                dp[i][j] = skip
                trace.append({
                    "i": i, "j": j, "choice": "toolight",
                    "value": skip,
                    "msg": "容量 %d 装不下物品 %d（需 %d）" % (j, i, w),
                })

    # 回溯找出选了哪些物品
    picked = []
    j = capacity
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            picked.append(i)
            j -= weights[i - 1]
    picked.reverse()

    return {
        "weights": list(weights),
        "values": list(values),
        "capacity": capacity,
        "maxValue": dp[n][capacity],
        "table": dp,
        "picked": picked,
        "pickedItems": [{"index": i, "w": weights[i - 1], "v": values[i - 1]}
                        for i in picked],
        "steps": trace,
        "explain": "DP 的本质是「记住已经算过的子问题」。"
                   "这里 dp[i][j] 只依赖上一行的两个格子，所以填充顺序很重要——"
                   "从左到右、从上到下，保证用到的值都算好了。",
    }


def default_case() -> Dict[str, Any]:
    """返回一组便于演示的默认数据。"""
    return {
        "weights": [2, 3, 4, 5],
        "values": [3, 4, 5, 6],
        "capacity": 8,
    }


def random_case(n: int = 5, seed: int = None) -> Dict[str, Any]:
    import random
    rng = random.Random(seed)
    return {
        "weights": [rng.randint(1, 6) for _ in range(n)],
        "values": [rng.randint(2, 12) for _ in range(n)],
        "capacity": rng.randint(6, 14),
    }
