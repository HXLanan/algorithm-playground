# -*- coding: utf-8 -*-
"""核心算法模块：排序。

为前端"逐帧播放"服务：本模块不返回最终结果，而是返回**每一步的完整快照**，
前端拿到步骤序列后即可播放、暂停、单步、回退。

纯标准库实现，不依赖 Flask，可独立单元测试。
"""
from typing import List, Dict, Any, Optional

SUPPORTED = ("bubble", "selection", "insertion")

_ALGO_NAMES = {
    "bubble": "冒泡排序",
    "selection": "选择排序",
    "insertion": "插入排序",
}


def random_array(n: int, seed: Optional[int] = None) -> List[int]:
    """生成 1..n 的乱序数组。"""
    import random
    rng = random.Random(seed)
    arr = list(range(1, n + 1))
    rng.shuffle(arr)
    return arr


def _step(steps: List[Dict[str, Any]], arr: List[int], desc: str,
          a: int = -1, b: int = -1, mark: int = -1,
          compares: int = 0, writes: int = 0) -> None:
    """记录一帧：当前数组快照 + 高亮位置 + 解说 + 统计。"""
    steps.append({
        "list": list(arr),      # 快照（前端直接画）
        "desc": desc,           # 解说文字
        "a": a,                 # 正在比较的位置 1（琥珀色）
        "b": b,                 # 正在比较的位置 2（琥珀色）
        "mark": mark,           # 本步关注/写入的单个位置（品红）
        "c": compares,          # 累计比较次数
        "w": writes,            # 累计写入/交换次数
    })


def build_steps(array: List[int], algo: str = "bubble") -> Dict[str, Any]:
    """构造排序全过程的步骤序列。

    返回：
        {
          "algo": "bubble",
          "algoName": "冒泡排序",
          "input": [...],
          "sorted": [...],
          "steps": [ {list, desc, a, b, mark, c, w}, ... ],
          "totalCompares": int,
          "totalWrites": int,
        }
    """
    if algo not in SUPPORTED:
        raise ValueError("不支持的排序算法: %s（可选：%s）" % (algo, ", ".join(SUPPORTED)))

    a = list(array)
    n = len(a)
    steps: List[Dict[str, Any]] = []
    c = 0
    w = 0

    if algo == "bubble":
        c, w = _bubble(a, steps)
    elif algo == "selection":
        c, w = _selection(a, steps)
    else:
        c, w = _insertion(a, steps)

    return {
        "algo": algo,
        "algoName": _ALGO_NAMES[algo],
        "input": list(array),
        "sorted": list(a),
        "steps": steps,
        "totalCompares": c,
        "totalWrites": w,
        "count": n,
    }


def _bubble(a: List[int], steps: List[Dict[str, Any]]):
    """冒泡排序：相邻两两比较，大的往后冒。"""
    n = len(a)
    c = w = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            c += 1
            _step(steps, a, "比较位置 %d 与 %d（%d / %d）" % (j, j + 1, a[j], a[j + 1]),
                  a=j, b=j + 1, compares=c, writes=w)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                w += 1
                swapped = True
                _step(steps, a, "交换：较大的 %d 泡到右边" % a[j + 1],
                      a=j, b=j + 1, compares=c, writes=w)
        # 本轮结束，末尾 i+1 个已定序
        _step(steps, a, "第 %d 轮结束，最右 %d 位已确定" % (i + 1, i + 1),
              mark=n - i - 1, compares=c, writes=w)
        if not swapped:
            _step(steps, a, "本轮未发生交换 → 已经有序，提前结束（这是冒泡的优化点）",
                  compares=c, writes=w)
            break
    return c, w


def _selection(a: List[int], steps: List[Dict[str, Any]]):
    """选择排序：每轮选出最小者换到最前。"""
    n = len(a)
    c = w = 0
    for i in range(n - 1):
        min_idx = i
        _step(steps, a, "本轮从位置 %d 开始找最小值" % i, a=i, mark=i,
              compares=c, writes=w)
        for j in range(i + 1, n):
            c += 1
            _step(steps, a, "比较候选最小 %d 与 %d" % (a[min_idx], a[j]),
                  a=min_idx, b=j, compares=c, writes=w)
            if a[j] < a[min_idx]:
                min_idx = j
                _step(steps, a, "发现更小值 %d，更新最小位置为 %d" % (a[j], j),
                      mark=j, compares=c, writes=w)
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            w += 1
            _step(steps, a, "把最小值 %d 放到位置 %d" % (a[i], i),
                  a=i, b=min_idx, compares=c, writes=w)
    return c, w


def _insertion(a: List[int], steps: List[Dict[str, Any]]):
    """插入排序：把元素逐个插入前面已排好的序列。"""
    n = len(a)
    c = w = 0
    for i in range(1, n):
        key = a[i]
        _step(steps, a, "取出位置 %d 的 %d 作为“新牌”" % (i, key), mark=i,
              compares=c, writes=w)
        j = i - 1
        while j >= 0:
            c += 1
            _step(steps, a, "比较：%d 与手上的 %d" % (a[j], key),
                  a=j, b=i, compares=c, writes=w)
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            w += 1
            _step(steps, a, "把较大的 %d 右移一位" % a[j + 1], mark=j + 1,
                  compares=c, writes=w)
            j -= 1
        if a[j + 1] != key:
            a[j + 1] = key
            w += 1
            _step(steps, a, "把新牌 %d 插入到位置 %d" % (key, j + 1), mark=j + 1,
                  compares=c, writes=w)
    return c, w
