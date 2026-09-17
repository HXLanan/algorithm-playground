# -*- coding: utf-8 -*-
"""核心算法模块：二叉堆与优先队列。

堆是一棵"完全二叉树"，满足堆序性质：父节点 ≤ 子节点（小根堆）。
用数组存储时，节点 i 的孩子是 2i+1 和 2i+2 —— 不需要指针。

两个核心操作（都以 O(log n) 完成）：
  · 上浮 sift-up  ：插入新元素后往上调整
  · 下沉 sift-down：取出堆顶后把末尾元素放上来往下调整
"""
from typing import List, Dict, Any, Optional


class MinHeap:
    def __init__(self):
        self.a: List[int] = []
        self.steps: List[Dict[str, Any]] = []

    def push(self, v: int) -> None:
        self.a.append(v)
        i = len(self.a) - 1
        self.steps.append({"type": "push", "heap": list(self.a), "i": i,
                           "msg": "把 %d 放到数组末尾（索引 %d），开始上浮" % (v, i)})
        while i > 0:
            parent = (i - 1) // 2
            self.steps.append({"type": "compare", "heap": list(self.a),
                               "i": i, "j": parent,
                               "msg": "比较 %d 与父节点 %d" % (self.a[i], self.a[parent])})
            if self.a[i] < self.a[parent]:
                self.a[i], self.a[parent] = self.a[parent], self.a[i]
                self.steps.append({"type": "swap", "heap": list(self.a),
                                   "i": i, "j": parent,
                                   "msg": "子节点更小，与父节点交换（上浮）"})
                i = parent
            else:
                self.steps.append({"type": "stable", "heap": list(self.a), "i": i,
                                   "msg": "已满足堆序，停止上浮"})
                break

    def pop(self) -> Optional[int]:
        if not self.a:
            return None
        top = self.a[0]
        last = self.a.pop()
        self.steps.append({"type": "pop", "heap": list(self.a), "i": 0,
                           "msg": "取出堆顶 %s" % top})
        if self.a:
            self.a[0] = last
            self.steps.append({"type": "move", "heap": list(self.a), "i": 0,
                               "msg": "把末尾的 %d 放到堆顶，开始下沉" % last})
            self._sift_down(0)
        return top

    def _sift_down(self, i: int) -> None:
        n = len(self.a)
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            smallest = i
            if l < n and self.a[l] < self.a[smallest]:
                smallest = l
            if r < n and self.a[r] < self.a[smallest]:
                smallest = r
            self.steps.append({"type": "compare", "heap": list(self.a),
                               "i": i, "j": smallest,
                               "msg": "比较父节点与较小孩子"})
            if smallest == i:
                self.steps.append({"type": "stable", "heap": list(self.a), "i": i,
                                   "msg": "已满足堆序，停止下沉"})
                break
            self.a[i], self.a[smallest] = self.a[smallest], self.a[i]
            self.steps.append({"type": "swap", "heap": list(self.a),
                               "i": i, "j": smallest,
                               "msg": "与更小的孩子交换（下沉）"})
            i = smallest


def demo(values: List[int], pops: int = 3) -> Dict[str, Any]:
    """演示：插入若干元素，再弹出若干次。"""
    h = MinHeap()
    for v in values:
        h.push(v)
    heap_after_push = list(h.a)

    popped = []
    for _ in range(min(pops, len(h.a))):
        v = h.pop()
        if v is not None:
            popped.append(v)

    return {
        "input": list(values),
        "heapAfterPush": heap_after_push,
        "popped": popped,
        "heapAfterPop": list(h.a),
        "steps": h.steps,
        "explain": "堆只保证「根是最小值」，不保证整体有序。"
                   "所以取最小值只要 O(1)，而插入/删除只要 O(log n)。"
                   "这就是优先队列、堆排序、Top-K 问题的基石。",
    }


def heap_sort(values: List[int]) -> Dict[str, Any]:
    """用堆实现排序（堆排序）。"""
    h = MinHeap()
    steps: List[Dict[str, Any]] = []
    for v in values:
        h.push(v)
    steps.extend(h.steps)
    out = []
    while h.a:
        out.append(h.pop())
    steps.extend(h.steps[len(steps):])
    return {
        "input": list(values),
        "sorted": out,
        "steps": steps,
        "explain": "把所有元素插入堆，再反复取堆顶，就得到了升序序列。"
                   "整体复杂度 O(n log n)，且不需要额外数组。",
    }
