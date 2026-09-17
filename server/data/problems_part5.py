# -*- coding: utf-8 -*-
"""题库数据层（第五部分）：栈与队列 / 链表 / 字符串 补强。"""

PART5 = [
    {
        "slug": "min-stack", "lcId": 155, "title": "最小栈",
        "difficulty": "中等", "tags": ["栈", "设计"], "category": "栈与队列",
        "visualizer": None, "visHint": None,
        "desc": "设计一个支持 push，pop，top 操作，并能在常数时间内检索到最小元素的栈。实现 MinStack 类：MinStack() 初始化堆栈对象；void push(int val) 将元素 val 推入堆栈；void pop() 删除堆栈顶部的元素；int top() 获取堆栈顶部的元素；int getMin() 获取堆栈中的最小元素。",
        "examples": [
            {"input": '["MinStack","push","push","push","getMin","pop","top","getMin"]\n[[],[-2],[0],[-3],[],[],[],[]]',
             "output": "[null,null,null,null,-3,null,0,-2]"},
        ],
        "hints": ["用一个辅助栈同步记录「当前最小值」", "每次 push 都把新的最小值压入辅助栈"],
        "funcName": "min_stack_ops",
        "testCases": [
            {"args": [["MinStack","push","push","push","getMin","pop","top","getMin"],
                      [[],[-2],[0],[-3],[],[],[],[]]],
             "expect": [None,None,None,None,-3,None,0,-2]},
            {"args": [["MinStack","push","push","getMin","pop","getMin"],
                      [[],[5],[3],[],[],[]]],
             "expect": [None,None,None,3,None,5]},
        ],
        "solutions": [
            {"name": "辅助栈同步最小值", "time": "O(1) 每次操作", "space": "O(n)",
             "idea": "主栈存数据，辅助栈存「到这里为止的最小值」。push 时辅助栈压入 min(新值, 辅助栈顶)；pop 时两个栈一起弹。",
             "code": """class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []

    def push(self, val):
        self.data.append(val)
        self.mins.append(val if not self.mins else min(val, self.mins[-1]))

    def pop(self):
        self.data.pop()
        self.mins.pop()

    def top(self):
        return self.data[-1]

    def getMin(self):
        return self.mins[-1]


def min_stack_ops(ops, args):
    st = None
    out = []
    for op, arg in zip(ops, args):
        if op == "MinStack":
            st = MinStack()
            out.append(None)
        elif op == "push":
            st.push(arg[0]); out.append(None)
        elif op == "pop":
            st.pop(); out.append(None)
        elif op == "top":
            out.append(st.top())
        elif op == "getMin":
            out.append(st.getMin())
    return out"""},
        ],
    },
    {
        "slug": "daily-temperatures", "lcId": 739, "title": "每日温度",
        "difficulty": "中等", "tags": ["栈", "单调栈", "数组"], "category": "栈与队列",
        "visualizer": None, "visHint": None,
        "desc": "给定一个整数数组 temperatures，表示每天的温度，返回一个数组 answer，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。",
        "examples": [
            {"input": "temperatures = [73,74,75,71,69,72,76,73]",
             "output": "[1,1,4,2,1,1,0,0]"},
            {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]"},
        ],
        "hints": ["从右往左看，用单调栈存「还没找到更高温的天」", "栈里存下标，保持温度递减"],
        "funcName": "daily_temperatures",
        "testCases": [
            {"args": [[73, 74, 75, 71, 69, 72, 76, 73]], "expect": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"args": [[30, 40, 50, 60]], "expect": [1, 1, 1, 0]},
            {"args": [[30, 60, 90]], "expect": [1, 1, 0]},
        ],
        "solutions": [
            {"name": "单调栈（存下标）", "time": "O(n)", "space": "O(n)",
             "idea": "从左到右遍历，维护一个「温度递减」的下标栈。当前温度比栈顶温度高时，说明栈顶那天找到了答案，弹出并记录天数差；否则当前天下标入栈。",
             "code": """def daily_temperatures(temperatures):
    n = len(temperatures)
    ans = [0] * n
    stack = []            # 存下标，温度递减
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans"""},
        ],
    },
    {
        "slug": "largest-rectangle", "lcId": 84, "title": "柱状图中最大的矩形",
        "difficulty": "困难", "tags": ["栈", "单调栈", "数组"], "category": "栈与队列",
        "visualizer": None, "visHint": None,
        "desc": "给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1。求在该柱状图中，能够勾勒出来的矩形的最大面积。",
        "examples": [
            {"input": "heights = [2,1,5,6,2,3]", "output": "10"},
            {"input": "heights = [2,4]", "output": "4"},
        ],
        "hints": ["对每根柱子，找出它能向左右延伸的边界", "单调递增栈可以一次求出左右边界"],
        "funcName": "largest_rectangle_area",
        "testCases": [
            {"args": [[2, 1, 5, 6, 2, 3]], "expect": 10},
            {"args": [[2, 4]], "expect": 4},
            {"args": [[1]], "expect": 1},
            {"args": [[0]], "expect": 0},
        ],
        "solutions": [
            {"name": "单调递增栈", "time": "O(n)", "space": "O(n)",
             "idea": "维护「高度递增」的下标栈，并在数组首尾各加一个高度 0 的哨兵。当遇到比栈顶矮的柱子时，说明栈顶柱子的右边界确定，弹出并计算以它为高的最大矩形（宽度 = 当前下标 - 新栈顶下标 - 1）。",
             "code": """def largest_rectangle_area(heights):
    h = [0] + list(heights) + [0]        # 首尾加哨兵，简化边界处理
    stack = []
    best = 0
    for i, x in enumerate(h):
        while stack and h[stack[-1]] > x:
            j = stack.pop()
            height = h[j]
            width = i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best"""},
        ],
    },
    {
        "slug": "merge-two-lists", "lcId": 21, "title": "合并两个有序链表",
        "difficulty": "简单", "tags": ["链表", "递归"], "category": "链表",
        "visualizer": None, "visHint": None,
        "desc": "将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。",
        "examples": [
            {"input": "l1 = [1,2,4], l2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "l1 = [], l2 = []", "output": "[]"},
        ],
        "hints": ["用哨兵节点简化头节点处理", "每次取两个链表头部较小的那个"],
        "funcName": "merge_two_lists",
        "testCases": [
            {"args": [[1, 2, 4], [1, 3, 4]], "expect": [1, 1, 2, 3, 4, 4]},
            {"args": [[], []], "expect": []},
            {"args": [[], [0]], "expect": [0]},
        ],
        "solutions": [
            {"name": "迭代 + 哨兵节点", "time": "O(m+n)", "space": "O(1)",
             "idea": "建一个哨兵头节点，用 tail 指针串接。每次比较两个链表的当前节点，把较小的接上并前移。最后把非空的那条直接接上。",
             "code": """def merge_two_lists(l1, l2):
    res = []
    i = j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            res.append(l1[i]); i += 1
        else:
            res.append(l2[j]); j += 1
    res.extend(l1[i:])
    res.extend(l2[j:])
    return res"""},
        ],
    },
    {
        "slug": "linked-list-cycle", "lcId": 141, "title": "环形链表",
        "difficulty": "简单", "tags": ["链表", "双指针", "哈希表"], "category": "链表",
        "visualizer": "sliding-window.html", "visHint": "快慢指针（龟兔赛跑）的经典应用",
        "desc": "给你一个链表的头节点 head，判断链表中是否有环。如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true"},
            {"input": "head = [1,2], pos = -1", "output": "false"},
        ],
        "hints": ["快指针每次走两步，慢指针走一步", "如果有环，快指针一定会追上慢指针"],
        "funcName": "has_cycle",
        "testCases": [
            {"args": [[3, 2, 0, -4], 1], "expect": True},
            {"args": [[1, 2], -1], "expect": False},
            {"args": [[1], -1], "expect": False},
        ],
        "solutions": [
            {"name": "快慢指针（O(1) 空间）", "time": "O(n)", "space": "O(1)",
             "idea": "慢指针每次走 1 步，快指针每次走 2 步。若存在环，快指针必然在环内追上慢指针；若无环，快指针先到达终点。",
             "code": """def has_cycle(head, pos):
    # 用数组+pos 模拟链表，返回是否存在环
    if not head:
        return False
    n = len(head)
    nxt = list(range(1, n)) + [pos]      # 构造 next 指针
    if pos < 0:
        nxt[-1] = -1
    slow, fast = 0, 0
    while True:
        if fast == -1 or nxt[fast] == -1:
            return False
        fast = nxt[fast]
        if fast == -1 or nxt[fast] == -1:
            return False
        fast = nxt[fast]
        slow = nxt[slow]
        if fast == slow:
            return True"""},
        ],
    },
    {
        "slug": "reverse-words", "lcId": 151, "title": "反转字符串中的单词",
        "difficulty": "中等", "tags": ["字符串", "双指针"], "category": "字符串",
        "visualizer": None, "visHint": None,
        "desc": "给你一个字符串 s，请你反转字符串中单词的顺序。单词是由非空格字符组成的字符串。s 中使用至少一个空格将字符串中的单词分隔开。返回单词顺序颠倒且单词之间用单个空格连接的结果字符串。",
        "examples": [
            {"input": 's = "the sky is blue"', "output": '"blue is sky the"'},
            {"input": 's = "  hello world  "', "output": '"world hello"'},
        ],
        "hints": ["先 split 再反转再 join", "注意处理多余空格"],
        "funcName": "reverse_words",
        "testCases": [
            {"args": ["the sky is blue"], "expect": "blue is sky the"},
            {"args": ["  hello world  "], "expect": "world hello"},
            {"args": ["a good   example"], "expect": "example good a"},
        ],
        "solutions": [
            {"name": "split + reverse", "time": "O(n)", "space": "O(n)",
             "idea": "Python 的 split() 无参调用会自动处理连续空格和首尾空格，然后反转列表再用单空格连接。",
             "code": """def reverse_words(s):
    return ' '.join(reversed(s.split()))"""},
        ],
    },
    {
        "slug": "longest-palindrome-substr", "lcId": 5, "title": "最长回文子串",
        "difficulty": "中等", "tags": ["字符串", "动态规划", "双指针"], "category": "字符串",
        "visualizer": None, "visHint": None,
        "desc": "给你一个字符串 s，找到 s 中最长的回文子串。回文是指正序和倒序读都一样的字符串。",
        "examples": [
            {"input": 's = "babad"', "output": '"bab"', "explain": '"aba" 同样是符合题意的答案'},
            {"input": 's = "cbbd"', "output": '"bb"'},
        ],
        "hints": ["回文可以从中心向两边扩展", "中心可能是一个字符，也可能是两个字符之间"],
        "funcName": "longest_palindrome",
        "testCases": [
            {"args": ["babad"], "expect": "bab"},
            {"args": ["cbbd"], "expect": "bb"},
            {"args": ["a"], "expect": "a"},
            {"args": ["ac"], "expect": "a"},
        ],
        "solutions": [
            {"name": "中心扩展（直观高效）", "time": "O(n²)", "space": "O(1)",
             "idea": "枚举每个可能的回文中心（2n-1 个：n 个字符中心 + n-1 个间隙中心），从中心向两边扩展，记录最长的那个。",
             "code": """def longest_palindrome(s):
    if not s:
        return ""
    start, end = 0, 0

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1        # 返回有效区间

    for i in range(len(s)):
        l1, r1 = expand(i, i)          # 奇数长度
        l2, r2 = expand(i, i + 1)      # 偶数长度
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start:end + 1]"""},
        ],
    },
]
