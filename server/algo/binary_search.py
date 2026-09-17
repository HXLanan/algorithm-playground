# -*- coding: utf-8 -*-
"""核心算法模块：二分查找。

在**有序数组**中查找目标，每次砍掉一半搜索范围 → O(log n)。
每次比较都能扔掉一半候选，这是它比线性查找快得多的根本原因。
"""
from typing import List, Dict, Any, Optional


def search(nums: List[int], target: int) -> Dict[str, Any]:
    """标准二分查找，返回过程帧。"""
    a = sorted(nums)
    steps: List[Dict[str, Any]] = []
    lo, hi = 0, len(a) - 1
    found = -1
    comparisons = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        steps.append({
            "lo": lo, "hi": hi, "mid": mid, "arr": list(a),
            "type": "probe",
            "msg": "当前范围 [%d, %d]，取中点 %d（值 %d）" % (lo, hi, mid, a[mid]),
            "comparisons": comparisons,
        })
        if a[mid] == target:
            found = mid
            steps.append({
                "lo": lo, "hi": hi, "mid": mid, "arr": list(a),
                "type": "found",
                "msg": "🎯 命中！%d 就在索引 %d" % (target, mid),
                "comparisons": comparisons,
            })
            break
        elif a[mid] < target:
            steps.append({
                "lo": lo, "hi": hi, "mid": mid, "arr": list(a),
                "type": "right",
                "msg": "%d < %d，目标只可能在右半边，丢弃左半" % (a[mid], target),
                "comparisons": comparisons,
            })
            lo = mid + 1
        else:
            steps.append({
                "lo": lo, "hi": hi, "mid": mid, "arr": list(a),
                "type": "left",
                "msg": "%d > %d，目标只可能在左半边，丢弃右半" % (a[mid], target),
                "comparisons": comparisons,
            })
            hi = mid - 1

    import math
    return {
        "target": target,
        "array": a,
        "found": found,
        "index": found,
        "steps": steps,
        "comparisons": comparisons,
        "maxPossible": int(math.log2(len(a))) + 1 if a else 0,
        "linearWorst": len(a),
        "explain": "每次比较都能排除一半，所以 n 个元素最多只需约 log₂n 次比较。"
                   "100 万个元素也只要 20 次！",
    }


def lower_bound_demo(nums: List[int], target: int) -> Dict[str, Any]:
    """查找第一个 >= target 的位置（二分的重要变体）。"""
    a = sorted(nums)
    lo, hi = 0, len(a)
    steps = []
    while lo < hi:
        mid = (lo + hi) // 2
        steps.append({
            "lo": lo, "hi": hi, "mid": mid,
            "msg": "a[%d]=%d %s target=%d → 收缩区间" % (
                mid, a[mid], ">=" if a[mid] >= target else "<", target),
        })
        if a[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return {"array": a, "target": target, "index": lo, "steps": steps,
            "explain": "lower_bound 找的是「第一个不小于 target 的位置」，是二分最实用的变体。"}
