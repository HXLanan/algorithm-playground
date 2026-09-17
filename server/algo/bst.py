# -*- coding: utf-8 -*-
"""核心算法模块：二叉搜索树（BST）。

性质：对任意节点，左子树所有值 < 节点值 < 右子树所有值。
因此中序遍历会得到**升序序列**——这是 BST 最有用的性质。

支持插入、查找、删除，并输出每次操作后的树结构快照。
"""
from typing import List, Dict, Any, Optional


class BSTNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int):
        self.val = val
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


def build(values: List[int]) -> Dict[str, Any]:
    """按顺序插入构造 BST，返回树结构与操作过程。"""
    root = None
    steps: List[Dict[str, Any]] = []
    for v in values:
        root, path = _insert(root, v, steps)
    return {
        "root": _serialize(root),
        "values": list(values),
        "steps": steps,
        "height": _height(root),
        "count": _count(root),
        "inorder": _inorder(root),
    }


def _insert(root: Optional[BSTNode], val: int, steps) -> tuple:
    """插入并记录比较路径。"""
    path = []
    if root is None:
        steps.append({"type": "insert", "val": val, "path": [],
                      "msg": "%d 是第一个节点，直接作为根" % val})
        return BSTNode(val), path

    cur = root
    while True:
        path.append(cur.val)
        if val < cur.val:
            steps.append({"type": "compare", "val": val, "at": cur.val,
                          "dir": "left", "path": list(path),
                          "msg": "%d < %d，往左走" % (val, cur.val)})
            if cur.left is None:
                cur.left = BSTNode(val)
                steps.append({"type": "insert", "val": val, "path": list(path),
                              "msg": "左边空位，插入 %d" % val})
                break
            cur = cur.left
        elif val > cur.val:
            steps.append({"type": "compare", "val": val, "at": cur.val,
                          "dir": "right", "path": list(path),
                          "msg": "%d > %d，往右走" % (val, cur.val)})
            if cur.right is None:
                cur.right = BSTNode(val)
                steps.append({"type": "insert", "val": val, "path": list(path),
                              "msg": "右边空位，插入 %d" % val})
                break
            cur = cur.right
        else:
            steps.append({"type": "duplicate", "val": val, "path": list(path),
                          "msg": "%d 已存在，跳过" % val})
            break
    return root, path


def _serialize(node: Optional[BSTNode]) -> Optional[Dict[str, Any]]:
    """把树转成可 JSON 化的嵌套结构。"""
    if node is None:
        return None
    return {"val": node.val,
            "left": _serialize(node.left),
            "right": _serialize(node.right)}


def _height(node: Optional[BSTNode]) -> int:
    if node is None:
        return 0
    return 1 + max(_height(node.left), _height(node.right))


def _count(node: Optional[BSTNode]) -> int:
    if node is None:
        return 0
    return 1 + _count(node.left) + _count(node.right)


def _inorder(node: Optional[BSTNode]) -> List[int]:
    if node is None:
        return []
    return _inorder(node.left) + [node.val] + _inorder(node.right)


def search(values: List[int], target: int) -> Dict[str, Any]:
    """在 BST 中查找，返回比较路径。"""
    root = None
    for v in values:
        root, _ = _insert(root, v, [])
    path = []
    cur = root
    found = False
    while cur is not None:
        path.append(cur.val)
        if target == cur.val:
            found = True
            break
        cur = cur.left if target < cur.val else cur.right
    return {
        "target": target,
        "path": path,
        "found": found,
        "comparisons": len(path),
        "explain": "BST 查找每比较一次就排除一半子树，平均 O(log n)。"
                   "但如果插入的是有序序列，树会退化成链表，变成 O(n)——"
                   "这正是 AVL / 红黑树要解决的问题。",
    }


def balanced_check(values: List[int]) -> Dict[str, Any]:
    """对比有序插入与随机插入的树高差异。"""
    import random
    sorted_vals = sorted(values)
    rng = random.Random(42)
    shuffled = sorted_vals[:]
    rng.shuffle(shuffled)

    r1 = build(sorted_vals)
    r2 = build(shuffled)
    return {
        "sortedInsert": {"height": r1["height"], "count": r1["count"],
                         "values": sorted_vals},
        "randomInsert": {"height": r2["height"], "count": r2["count"],
                         "values": shuffled},
        "explain": "同样的数据，按有序顺序插入会得到一条链（高度=n），"
                   "随机顺序插入则接近平衡（高度≈log n）。顺序决定性能！",
    }
