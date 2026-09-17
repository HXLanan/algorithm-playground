# -*- coding: utf-8 -*-
"""核心算法模块：埃拉托斯特尼筛法（素数筛）。

要找 n 以内的所有素数，最朴素的做法是逐个试除（O(n√n)）。
筛法的思路完全不同：**从最小的素数开始，把它的倍数全部划掉**。
剩下的没被划掉的，就是素数。

复杂度 O(n log log n)，非常高效。
"""
from typing import List, Dict, Any


def sieve(n: int = 100, collect_frames: bool = True) -> Dict[str, Any]:
    """筛出 n 以内的所有素数，并记录每一轮的划除过程。"""
    if n < 2:
        return {"n": n, "primes": [], "steps": [], "count": 0,
                "explain": "小于 2 没有素数。"}
    if n > 5000:
        n = 5000

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    steps: List[Dict[str, Any]] = []
    crossed = 0

    i = 2
    limit = int(n ** 0.5)
    while i <= n:
        if is_prime[i]:
            if i <= limit:
                removed = []
                for j in range(i * i, n + 1, i):
                    if is_prime[j]:
                        is_prime[j] = False
                        removed.append(j)
                        crossed += 1
                if collect_frames and len(steps) < 200:
                    steps.append({
                        "prime": i,
                        "removed": removed[:200],
                        "msg": "以 %d 为筛：从 %d² = %d 开始，划掉它的所有倍数（共 %d 个）"
                               % (i, i, i * i, len(removed)),
                    })
        i += 1

    primes = [k for k in range(2, n + 1) if is_prime[k]]
    return {
        "n": n,
        "primes": primes,
        "primeCount": len(primes),
        "steps": steps,
        "crossedCount": crossed,
        "isPrime": is_prime,
        "explain": "为什么从 i² 开始划？因为小于 i² 的 i 的倍数，"
                   "早就被更小的素数划掉了。这一步优化让筛法非常快——"
                   "筛 100 万以内的素数只需几十毫秒。",
    }


def density(n: int = 1000) -> Dict[str, Any]:
    """展示素数的分布密度。"""
    r = sieve(n, collect_frames=False)
    primes = r["primes"]
    buckets = 10
    size = max(1, n // buckets)
    dist = []
    for b in range(buckets):
        lo = b * size + 1
        hi = min(n, (b + 1) * size)
        cnt = sum(1 for p in primes if lo <= p <= hi)
        dist.append({"range": "%d-%d" % (lo, hi), "count": cnt})
    return {
        "n": n,
        "total": len(primes),
        "density": round(len(primes) / n, 4),
        "distribution": dist,
        "explain": "素数越来越稀疏（这正是素数定理描述的规律：π(n) ≈ n / ln n），"
                   "但永远不会停止——欧几里得早在两千年前就证明了素数是无限的。",
    }
