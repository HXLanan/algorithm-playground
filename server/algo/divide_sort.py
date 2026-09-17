# -*- coding: utf-8 -*-
"""核心算法模块：分治类排序（快速排序 / 归并排序）。

与 sorting.py（简单排序）分开，因为这两者用到**分治**思想：
  · 快速排序：选基准 → 分区 → 递归左右
  · 归并排序：对半切 → 递归 → 合并有序段

同样返回"逐步快照"供前端逐帧播放。
"""
from typing import List, Dict, Any, Optional

SUPPORTED = ("quick", "merge")
_NAMES = {"quick": "快速排序", "merge": "归并排序"}


def random_array(n: int, seed: Optional[int] = None) -> List[int]:
    import random
    rng = random.Random(seed)
    a = list(range(1, n + 1))
    rng.shuffle(a)
    return a


def _rec(steps, arr, desc, a=-1, b=-1, mark=-1, lo=-1, hi=-1,
         compares=0, writes=0):
    steps.append({
        "list": list(arr), "desc": desc,
        "a": a, "b": b, "mark": mark,
        "lo": lo, "hi": hi,          # 当前处理的区间（用于高亮范围）
        "c": compares, "w": writes,
    })


def build_steps(array: List[int], algo: str = "quick") -> Dict[str, Any]:
    """构造分治排序的步骤序列。"""
    if algo not in SUPPORTED:
        raise ValueError("不支持的算法：%s" % algo)

    a = list(array)
    steps: List[Dict[str, Any]] = []
    counters = {"c": 0, "w": 0}

    if algo == "quick":
        _quick(a, 0, len(a) - 1, steps, counters)
    else:
        _merge_sort(a, 0, len(a) - 1, steps, counters)

    return {
        "algo": algo,
        "algoName": _NAMES[algo],
        "input": list(array),
        "sorted": list(a),
        "steps": steps,
        "totalCompares": counters["c"],
        "totalWrites": counters["w"],
        "count": len(array),
    }


def _quick(a: List[int], lo: int, hi: int, steps, cnt) -> None:
    """快速排序（Lomuto 分区）。"""
    if lo >= hi:
        if lo == hi:
            _rec(steps, a, "区间只剩 1 个元素，天然有序", mark=lo, lo=lo, hi=hi,
                 compares=cnt["c"], writes=cnt["w"])
        return

    pivot = a[hi]
    _rec(steps, a, "选定基准值 %d（区间 [%d, %d] 的最右端）" % (pivot, lo, hi),
         mark=hi, lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])

    i = lo
    for j in range(lo, hi):
        cnt["c"] += 1
        _rec(steps, a, "比较 %d 与基准 %d" % (a[j], pivot), a=j, b=hi, lo=lo, hi=hi,
             compares=cnt["c"], writes=cnt["w"])
        if a[j] < pivot:
            if i != j:
                a[i], a[j] = a[j], a[i]
                cnt["w"] += 1
                _rec(steps, a, "%d < %d，换到左区" % (a[i], pivot), a=i, b=j,
                     lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])
            i += 1
    a[i], a[hi] = a[hi], a[i]
    cnt["w"] += 1
    _rec(steps, a, "基准 %d 归位到索引 %d" % (pivot, i), mark=i, lo=lo, hi=hi,
         compares=cnt["c"], writes=cnt["w"])

    _quick(a, lo, i - 1, steps, cnt)
    _quick(a, i + 1, hi, steps, cnt)


def _merge_sort(a: List[int], lo: int, hi: int, steps, cnt) -> None:
    """归并排序。"""
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    _rec(steps, a, "把区间 [%d, %d] 对半切成 [%d,%d] 和 [%d,%d]" %
         (lo, hi, lo, mid, mid + 1, hi), lo=lo, hi=hi,
         compares=cnt["c"], writes=cnt["w"])
    _merge_sort(a, lo, mid, steps, cnt)
    _merge_sort(a, mid + 1, hi, steps, cnt)
    _merge(a, lo, mid, hi, steps, cnt)


def _merge(a: List[int], lo: int, mid: int, hi: int, steps, cnt) -> None:
    """合并两个有序段。"""
    left = a[lo:mid + 1]
    right = a[mid + 1:hi + 1]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        cnt["c"] += 1
        if left[i] <= right[j]:
            a[k] = left[i]
            _rec(steps, a, "比较后取左边较小的 %d 放到位置 %d" % (left[i], k),
                 mark=k, lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])
            i += 1
        else:
            a[k] = right[j]
            _rec(steps, a, "比较后取右边较小的 %d 放到位置 %d" % (right[j], k),
                 mark=k, lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])
            j += 1
        cnt["w"] += 1
        k += 1
    while i < len(left):
        a[k] = left[i]
        cnt["w"] += 1
        _rec(steps, a, "左边剩余 %d 直接填入位置 %d" % (left[i], k),
             mark=k, lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])
        i += 1; k += 1
    while j < len(right):
        a[k] = right[j]
        cnt["w"] += 1
        _rec(steps, a, "右边剩余 %d 直接填入位置 %d" % (right[j], k),
             mark=k, lo=lo, hi=hi, compares=cnt["c"], writes=cnt["w"])
        j += 1; k += 1
    _rec(steps, a, "区间 [%d, %d] 已合并为有序段" % (lo, hi), lo=lo, hi=hi,
         compares=cnt["c"], writes=cnt["w"])
