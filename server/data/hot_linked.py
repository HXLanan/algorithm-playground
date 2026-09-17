# -*- coding: utf-8 -*-
"""题库数据层（Hot 100 补充·1）：链表题。

对应 LeetCode 热题 HOT 100 中的链表部分。
"""

LINKED = [
    {
        "slug": "add-two-numbers", "lcId": 2, "title": "两数相加",
        "difficulty": "中等", "tags": ["链表", "数学", "递归"], "category": "链表",
        "visualizer": None, "visHint": None,
        "desc": "给你两个非空的链表，表示两个非负的整数。它们每位数字都是按照逆序的方式存储的，并且每个节点只能存储一位数字。请你将两个数相加，并以相同形式返回一个表示和的链表。你可以假设除了数字 0 之外，这两个数都不会以 0 开头。",
        "examples": [
            {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]",
             "explain": "342 + 465 = 807"},
            {"input": "l1 = [0], l2 = [0]", "output": "[0]"},
            {"input": "l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]", "output": "[8,9,9,9,0,0,0,1]"},
        ],
        "hints": ["逐位相加并处理进位", "两个链表长度不同时，短的补 0", "注意最后可能还有进位"],
        "funcName": "add_two_numbers",
        "testCases": [
            {"args": [[2, 4, 3], [5, 6, 4]], "expect": [7, 0, 8]},
            {"args": [[0], [0]], "expect": [0]},
            {"args": [[9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]], "expect": [8, 9, 9, 9, 0, 0, 0, 1]},
        ],
        "solutions": [
            {"name": "模拟竖式加法", "time": "O(max(m,n))", "space": "O(1)",
             "idea": "用两个指针同步遍历两条链表，逐位相加并维护进位 carry。某条链表走完后按 0 处理，最后若 carry 仍为 1 需要再补一个节点。",
             "code": """def add_two_numbers(l1, l2):
    res = []
    i = j = 0
    carry = 0
    while i < len(l1) or j < len(l2) or carry:
        a = l1[i] if i < len(l1) else 0
        b = l2[j] if j < len(l2) else 0
        total = a + b + carry
        res.append(total % 10)
        carry = total // 10
        i += 1
        j += 1
    return res"""},
        ],
    },
    {
        "slug": "remove-nth-node", "lcId": 19, "title": "删除链表的倒数第 N 个结点",
        "difficulty": "中等", "tags": ["链表", "双指针"], "category": "链表",
        "visualizer": "sliding-window.html", "visHint": "快慢指针保持固定间隔（窗口）",
        "desc": "给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"},
            {"input": "head = [1], n = 1", "output": "[]"},
            {"input": "head = [1,2], n = 1", "output": "[1]"},
        ],
        "hints": ["快指针先走 n 步，然后快慢一起走", "用哨兵节点简化删除头节点的情况"],
        "funcName": "remove_nth_from_end",
        "testCases": [
            {"args": [[1, 2, 3, 4, 5], 2], "expect": [1, 2, 3, 5]},
            {"args": [[1], 1], "expect": []},
            {"args": [[1, 2], 1], "expect": [1]},
        ],
        "solutions": [
            {"name": "快慢双指针（一趟扫描）", "time": "O(n)", "space": "O(1)",
             "idea": "让快指针先走 n 步，两者之间就保持了 n 的间隔。然后快慢一起前进，当快指针到达末尾时，慢指针正好指向待删除节点的前一个。本题用数组模拟链表节点。",
             "code": """def remove_nth_from_end(head, n):
    # 哨兵节点放在最前面，统一处理「删除头节点」的情况
    nodes = [None] + list(head)
    fast = 0
    slow = 0
    # 快指针先走 n 步（到倒数第 n 个位置）
    for _ in range(n):
        fast += 1
    # 同步前进直到 fast 到最后一个节点
    while fast + 1 < len(nodes):
        fast += 1
        slow += 1
    # 删除 slow 的下一个节点（即倒数第 n 个）
    del nodes[slow + 1]
    return nodes[1:]"""},
            {"name": "转数组处理（直观）", "time": "O(n)", "space": "O(n)",
             "idea": "先把链表转成数组，直接按索引删除倒数第 n 个元素，再还原。逻辑最清晰，适合先求正确再优化。",
             "code": """def remove_nth_from_end(head, n):
    arr = list(head)
    idx = len(arr) - n
    arr.pop(idx)
    return arr"""},
        ],
    },
    {
        "slug": "intersection-two-lists", "lcId": 160, "title": "相交链表",
        "difficulty": "简单", "tags": ["链表", "双指针", "哈希表"], "category": "链表",
        "visualizer": "sliding-window.html", "visHint": "双指针走「对方的路」实现对齐",
        "desc": "给你两个单链表的头节点 headA 和 headB，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 null。题目数据保证整个链式结构中不存在环。",
        "examples": [
            {"input": "intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3",
             "output": "Intersected at '8'"},
            {"input": "intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2",
             "output": "No intersection"},
        ],
        "hints": ["两个指针分别走完自己的路再走对方的路，总路程相同", "相遇点就是交点"],
        "funcName": "get_intersection_node",
        "testCases": [
            {"args": [[4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3], "expect": 8},
            {"args": [[2, 6, 4], [1, 5], 3, 2], "expect": None},
            {"args": [[1], [1], 0, 0], "expect": 1},
        ],
        "solutions": [
            {"name": "双指针走对方的路", "time": "O(m+n)", "space": "O(1)",
             "idea": "把两条链表首尾相接来看：pA 走 A 再走 B，pB 走 B 再走 A，两者走过的总长度相同。逐位置比较这两个「虚拟序列」，第一次出现相同节点时即为交点。",
             "code": """def get_intersection_node(headA, headB, skipA, skipB):
    common_len = len(headA) - skipA
    if common_len <= 0 or len(headB) - skipB != common_len:
        return None
    base = 1000
    common_ids = [base + i for i in range(common_len)]
    common_vals = headA[skipA:]
    a_ids = list(range(skipA)) + common_ids
    b_ids = list(range(500, 500 + skipB)) + common_ids
    ids = {i: v for i, v in zip(common_ids, common_vals)}

    # 两条「虚拟串联序列」：A+B 与 B+A，长度相同
    seq_a = a_ids + b_ids
    seq_b = b_ids + a_ids
    for x, y in zip(seq_a, seq_b):
        if x == y and x in ids:
            return ids[x]
    return None"""},
            {"name": "哈希集合记录节点", "time": "O(m+n)", "space": "O(m)",
             "idea": "先遍历 A 把所有节点放进集合，再遍历 B，第一个出现在集合中的节点就是交点。思路最直接。",
             "code": """def get_intersection_node(headA, headB, skipA, skipB):
    common_len = len(headA) - skipA
    if common_len <= 0 or len(headB) - skipB != common_len:
        return None
    base = 1000
    common_ids = [base + i for i in range(common_len)]
    common_vals = headA[skipA:]
    a_ids = list(range(skipA)) + common_ids
    b_ids = list(range(500, 500 + skipB)) + common_ids
    ids = {i: v for i, v in zip(common_ids, common_vals)}

    seen = set(a_ids)
    for nid in b_ids:
        if nid in seen:
            return ids[nid]
    return None"""},
        ],
    },
    {
        "slug": "palindrome-linked-list", "lcId": 234, "title": "回文链表",
        "difficulty": "简单", "tags": ["链表", "双指针", "栈"], "category": "链表",
        "visualizer": "sliding-window.html", "visHint": "双指针从两端向中间比较",
        "desc": "给你一个单链表的头节点 head，请你判断该链表是否为回文链表。如果是，返回 true；否则，返回 false。",
        "examples": [
            {"input": "head = [1,2,2,1]", "output": "true"},
            {"input": "head = [1,2]", "output": "false"},
        ],
        "hints": ["转成数组后用双指针最简单", "进阶：快慢指针找中点 + 反转后半段，O(1) 空间"],
        "funcName": "is_palindrome_list",
        "testCases": [
            {"args": [[1, 2, 2, 1]], "expect": True},
            {"args": [[1, 2]], "expect": False},
            {"args": [[1]], "expect": True},
            {"args": [[]], "expect": True},
        ],
        "solutions": [
            {"name": "数组双指针", "time": "O(n)", "space": "O(n)",
             "idea": "把链表值复制到数组，用左右指针向中间比较。写法简单直观。",
             "code": """def is_palindrome_list(head):
    a = list(head)
    l, r = 0, len(a) - 1
    while l < r:
        if a[l] != a[r]:
            return False
        l += 1
        r -= 1
    return True"""},
            {"name": "快慢指针 + 反转后半段（O(1) 空间）", "time": "O(n)", "space": "O(1)",
             "idea": "快慢指针找到链表中点，反转后半段，然后与前半段逐一比较，最后可选恢复链表。这里用数组模拟该过程。",
             "code": """def is_palindrome_list(head):
    a = list(head)
    n = len(a)
    # 反转后半段
    mid = (n + 1) // 2
    second = a[mid:][::-1]
    first = a[:n // 2]
    return first == second"""},
        ],
    },
    {
        "slug": "linked-list-cycle-ii", "lcId": 142, "title": "环形链表 II",
        "difficulty": "中等", "tags": ["链表", "双指针", "哈希表"], "category": "链表",
        "visualizer": "sliding-window.html", "visHint": "快慢指针 + 数学推导找环入口",
        "desc": "给定一个链表的头节点 head，返回链表开始入环的第一个节点。如果链表无环，则返回 null。如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。不允许修改链表。",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "tail connects to node index 1"},
            {"input": "head = [1,2], pos = 0", "output": "tail connects to node index 0"},
            {"input": "head = [1], pos = -1", "output": "no cycle"},
        ],
        "hints": ["先用快慢指针判断有没有环", "相遇后，一个指针回到起点，两者同步走，再次相遇即入环点"],
        "funcName": "detect_cycle",
        "testCases": [
            {"args": [[3, 2, 0, -4], 1], "expect": 1},
            {"args": [[1, 2], 0], "expect": 0},
            {"args": [[1], -1], "expect": -1},
        ],
        "solutions": [
            {"name": "快慢指针 + 数学推导", "time": "O(n)", "space": "O(1)",
             "idea": "快慢指针相遇后，让一个指针回到 head，两指针同速前进，再次相遇的位置就是入环点。原理：设头到环入口距离为 a，入口到相遇点距离为 b，则相遇时快指针多走了一圈，可推出 a = 环长 - b。",
             "code": """def detect_cycle(head, pos):
    if not head or pos < 0:
        return -1
    n = len(head)
    nxt = list(range(1, n)) + [pos]      # 构造 next
    slow = fast = 0
    while True:
        if nxt[fast] == -1:
            return -1
        fast = nxt[fast]
        if nxt[fast] == -1:
            return -1
        fast = nxt[fast]
        slow = nxt[slow]
        if fast == slow:
            break
    # 找入环点
    p = 0
    q = slow
    while p != q:
        p = nxt[p]
        q = nxt[q]
    return p"""},
        ],
    },
]
