# -*- coding: utf-8 -*-
"""核心算法模块：滑动窗口。

用途：在数组/字符串中寻找满足条件的**连续子区间**。
核心思想：用两个指针维护一个窗口，右指针扩张、左指针收缩，
避免"枚举所有区间"的 O(n²) 暴力。

本模块演示三个经典问题：
  1. 定长窗口：长度为 k 的子数组最大和
  2. 不定长窗口：和 ≥ target 的最短子数组（求最短）
  3. 不定长窗口：无重复字符的最长子串（求最长）
"""
from typing import List, Dict, Any, Optional


def fixed_window(nums: List[int], k: int) -> Dict[str, Any]:
    """定长窗口：长度恰好为 k 的子数组最大和。"""
    n = len(nums)
    if k <= 0 or k > n:
        return {"error": "k 必须在 1..n 之间", "steps": []}

    steps: List[Dict[str, Any]] = []
    s = sum(nums[:k])
    best = s
    best_i = 0
    steps.append({
        "lo": 0, "hi": k - 1, "sum": s, "best": best, "bestRange": [0, k - 1],
        "msg": "初始窗口 [0, %d]，和为 %d" % (k - 1, s),
    })

    for i in range(k, n):
        s += nums[i] - nums[i - k]
        lo, hi = i - k + 1, i
        if s > best:
            best = s
            best_i = lo
            steps.append({
                "lo": lo, "hi": hi, "sum": s, "best": best, "bestRange": [lo, hi],
                "msg": "窗口右移：加入 %d、移出 %d，和变为 %d（新最大值！）"
                       % (nums[i], nums[i - k], s),
            })
        else:
            steps.append({
                "lo": lo, "hi": hi, "sum": s, "best": best, "bestRange": [best_i, best_i + k - 1],
                "msg": "窗口右移：加入 %d、移出 %d，和变为 %d（未超过 %d）"
                       % (nums[i], nums[i - k], s, best),
            })

    return {
        "type": "fixed",
        "nums": list(nums),
        "k": k,
        "maxSum": best,
        "bestRange": [best_i, best_i + k - 1],
        "steps": steps,
        "explain": "定长窗口只需 O(1) 时间滑动：加入右端元素、移除左端元素。"
                   "总计 O(n)，而暴力枚举每个窗口是 O(n·k)。",
    }


def min_length_window(nums: List[int], target: int) -> Dict[str, Any]:
    """不定长窗口：和 ≥ target 的最短连续子数组（求最短）。"""
    n = len(nums)
    steps: List[Dict[str, Any]] = []
    lo = 0
    s = 0
    best = n + 1
    best_range = None

    for hi in range(n):
        s += nums[hi]
        steps.append({
            "lo": lo, "hi": hi, "sum": s, "best": best if best <= n else None,
            "msg": "右指针扩到 %d，窗口和 = %d" % (hi, s),
        })
        while s >= target and lo <= hi:
            if hi - lo + 1 < best:
                best = hi - lo + 1
                best_range = [lo, hi]
                steps.append({
                    "lo": lo, "hi": hi, "sum": s, "best": best,
                    "msg": "和 ≥ %d，更新最短长度为 %d" % (target, best),
                })
            s -= nums[lo]
            lo += 1
            steps.append({
                "lo": lo, "hi": hi, "sum": s,
                "best": best if best <= n else None,
                "msg": "尝试收缩左边界（移出 %d），和降到 %d" % (nums[lo - 1], s),
            })

    ok = best <= n
    return {
        "type": "min",
        "nums": list(nums),
        "target": target,
        "minLength": best if ok else 0,
        "bestRange": best_range,
        "steps": steps,
        "explain": "求「最短」用不定长窗口：右指针负责扩张直到满足条件，"
                   "左指针负责收缩直到不满足。因为两个指针都只前进不后退，总共 O(n)。",
    }


def longest_unique_substring(s: str) -> Dict[str, Any]:
    """不定长窗口：无重复字符的最长子串（求最长）。"""
    s = str(s)[:200]
    steps: List[Dict[str, Any]] = []
    last = {}            # 字符 -> 最后出现的下标
    lo = 0
    best = 0
    best_range = None

    for hi, ch in enumerate(s):
        if ch in last and last[ch] >= lo:
            steps.append({
                "lo": lo, "hi": hi, "ch": ch, "best": best,
                "msg": "字符 %r 重复（上次在 %d），左指针跳到 %d" % (ch, last[ch], last[ch] + 1),
            })
            lo = last[ch] + 1
        last[ch] = hi
        cur = hi - lo + 1
        if cur > best:
            best = cur
            best_range = [lo, hi]
            steps.append({
                "lo": lo, "hi": hi, "ch": ch, "best": best,
                "msg": "窗口 [%d, %d] 无重复，长度 %d（新纪录）" % (lo, hi, cur),
            })

    return {
        "type": "longest",
        "text": s,
        "length": best,
        "substring": s[best_range[0]:best_range[1] + 1] if best_range else "",
        "bestRange": best_range,
        "steps": steps,
        "explain": "求「最长」同样用双指针，但左指针可以直接跳到「重复字符的下一位」，"
                   "而不必一格一格挪——这就是滑动窗口的精髓。",
    }


def default_case() -> Dict[str, Any]:
    return {
        "nums": [2, 3, 1, 2, 4, 3],
        "k": 3,
        "target": 7,
        "text": "abcabcbb",
    }
