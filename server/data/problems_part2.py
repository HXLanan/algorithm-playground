# -*- coding: utf-8 -*-
"""题库数据层（第二部分）：排序 / 递归与回溯 / 动态规划。

字段说明见 problems_part1.py 顶部注释。
"""

PART2 = [
    {
        "slug": "sort-an-array", "lcId": 912, "title": "排序数组",
        "difficulty": "中等", "tags": ["数组", "排序", "分治"], "category": "排序",
        "visualizer": "divide-sort.html", "visHint": "快排 / 归并排序的实战题目",
        "desc": "给你一个整数数组 nums，请你将该数组升序排列。请在不使用内置排序函数的情况下实现，时间复杂度尽量做到 O(n log n)。",
        "examples": [
            {"input": "nums = [5,2,3,1]", "output": "[1,2,3,5]"},
            {"input": "nums = [5,1,1,2,0,0]", "output": "[0,0,1,1,2,5]"},
        ],
        "hints": ["快排：选基准分区后递归", "归并：对半切分再合并有序段"],
        "funcName": "sort_array",
        "testCases": [
            {"args": [[5, 2, 3, 1]], "expect": [1, 2, 3, 5]},
            {"args": [[5, 1, 1, 2, 0, 0]], "expect": [0, 0, 1, 1, 2, 5]},
            {"args": [[]], "expect": []},
        ],
        "solutions": [
            {"name": "归并排序（稳定 O(n log n)）", "time": "O(n log n)", "space": "O(n)",
             "idea": "对半切分到单元素，再自底向上合并两个有序段。复杂度稳定，且是稳定排序。",
             "code": """def sort_array(nums):
    def merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = merge_sort(a[:mid])
        right = merge_sort(a[mid:])
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res
    return merge_sort(nums)"""},
            {"name": "快速排序", "time": "平均 O(n log n)", "space": "O(log n)",
             "idea": "选最右元素为基准，把小的放左边、大的放右边，基准归位后递归处理左右两段。",
             "code": """def sort_array(nums):
    a = list(nums)
    def quick(lo, hi):
        if lo >= hi:
            return
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        quick(lo, i - 1)
        quick(i + 1, hi)
    quick(0, len(a) - 1)
    return a"""},
        ],
    },
    {
        "slug": "kth-largest", "lcId": 215, "title": "数组中的第K个最大元素",
        "difficulty": "中等", "tags": ["数组", "堆", "快速选择"], "category": "排序",
        "visualizer": "heap.html", "visHint": "用「大小为 K 的小根堆」解决 Top-K 问题",
        "desc": "给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4"},
        ],
        "hints": ["维护大小为 k 的小根堆，堆顶就是第 k 大", "或用快速选择做到平均 O(n)"],
        "funcName": "find_kth_largest",
        "testCases": [
            {"args": [[3, 2, 1, 5, 6, 4], 2], "expect": 5},
            {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expect": 4},
            {"args": [[1], 1], "expect": 1},
        ],
        "solutions": [
            {"name": "小根堆（Top-K 标准解法）", "time": "O(n log k)", "space": "O(k)",
             "idea": "遍历数组，把元素压入大小为 k 的小根堆；堆满后若新元素比堆顶大，就弹出堆顶再压入。最后堆顶就是第 k 大。",
             "code": """import heapq

def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]"""},
            {"name": "排序后取下标", "time": "O(n log n)", "space": "O(1)",
             "idea": "排序后，第 k 大的元素位于下标 n-k。最简单直接。",
             "code": """def find_kth_largest(nums, k):
    a = sorted(nums)
    return a[len(a) - k]"""},
        ],
    },
    {
        "slug": "permutations", "lcId": 46, "title": "全排列",
        "difficulty": "中等", "tags": ["回溯", "数组"], "category": "递归与回溯",
        "visualizer": "nqueens.html", "visHint": "与 N 皇后同属回溯法家族",
        "desc": "给定一个不含重复数字的数组 nums，返回其所有可能的全排列。你可以按任意顺序返回答案。",
        "examples": [
            {"input": "nums = [1,2,3]",
             "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]"},
        ],
        "hints": ["回溯三步：做选择 → 递归 → 撤销选择", "用 used 数组标记已用元素"],
        "funcName": "permute",
        "testCases": [
            {"args": [[1, 2, 3]], "expect": [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]},
            {"args": [[0, 1]], "expect": [[0,1],[1,0]]},
            {"args": [[1]], "expect": [[1]]},
        ],
        "solutions": [
            {"name": "回溯法", "time": "O(n·n!)", "space": "O(n)",
             "idea": "维护当前路径 path 和已用标记 used。每层尝试所有未使用的数，加入路径后递归，返回时撤销。",
             "code": """def permute(nums):
    res = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res"""},
        ],
    },
    {
        "slug": "subsets", "lcId": 78, "title": "子集",
        "difficulty": "中等", "tags": ["回溯", "位运算"], "category": "递归与回溯",
        "visualizer": "nqueens.html", "visHint": "回溯法中「每个元素选或不选」的模型",
        "desc": "给你一个整数数组 nums，数组中的元素互不相同。返回该数组所有可能的子集（幂集）。解集不能包含重复的子集。",
        "examples": [
            {"input": "nums = [1,2,3]",
             "output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"},
            {"input": "nums = [0]", "output": "[[],[0]]"},
        ],
        "hints": ["每个元素都有「选」和「不选」两种决策", "共 2ⁿ 个子集"],
        "funcName": "subsets",
        "testCases": [
            {"args": [[1, 2, 3]],
             "expect": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]},
            {"args": [[0]], "expect": [[], [0]]},
        ],
        "solutions": [
            {"name": "回溯（选/不选）", "time": "O(n·2ⁿ)", "space": "O(n)",
             "idea": "对每个位置，先尝试「不选」再尝试「选」，走到末尾时记录当前子集。",
             "code": """def subsets(nums):
    res = []
    path = []

    def backtrack(i):
        if i == len(nums):
            res.append(path[:])
            return
        backtrack(i + 1)              # 不选 nums[i]
        path.append(nums[i])          # 选 nums[i]
        backtrack(i + 1)
        path.pop()

    backtrack(0)
    return res"""},
            {"name": "位运算枚举", "time": "O(n·2ⁿ)", "space": "O(1)",
             "idea": "n 个元素共有 2ⁿ 种选法，用一个整数的二进制位表示「第 i 个元素选不选」。",
             "code": """def subsets(nums):
    n = len(nums)
    res = []
    for mask in range(1 << n):
        cur = []
        for i in range(n):
            if mask & (1 << i):
                cur.append(nums[i])
        res.append(cur)
    return res"""},
        ],
    },
    {
        "slug": "n-queens", "lcId": 51, "title": "N 皇后",
        "difficulty": "困难", "tags": ["回溯", "数组"], "category": "递归与回溯",
        "visualizer": "nqueens.html", "visHint": "这就是该可视化页演示的原题",
        "desc": "按照国际象棋的规则，皇后可以攻击与之处在同一行、同一列或同一斜线上的棋子。n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。给你一个整数 n，返回所有不同的 n 皇后问题的解决方案。",
        "examples": [
            {"input": "n = 4", "output": "[[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]"},
        ],
        "hints": ["逐行放置，每行只放一个", "用三个集合记录被占用的列和两条对角线"],
        "funcName": "solve_n_queens",
        "testCases": [
            {"args": [4], "expect": [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]},
            {"args": [1], "expect": [["Q"]]},
        ],
        "solutions": [
            {"name": "回溯 + 集合剪枝", "time": "O(n!)", "space": "O(n)",
             "idea": "逐行放皇后。用 cols / diag1(row-col) / diag2(row+col) 三个集合快速判断某位置是否被攻击，放置后递归下一行，返回时撤销。",
             "code": """def solve_n_queens(n):
    res = []
    board = [['.'] * n for _ in range(n)]
    cols, d1, d2 = set(), set(), set()

    def backtrack(row):
        if row == n:
            res.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in d1 or (row + col) in d2:
                continue
            board[row][col] = 'Q'
            cols.add(col); d1.add(row - col); d2.add(row + col)
            backtrack(row + 1)
            board[row][col] = '.'
            cols.discard(col); d1.discard(row - col); d2.discard(row + col)

    backtrack(0)
    return res"""},
        ],
    },
    {
        "slug": "climbing-stairs", "lcId": 70, "title": "爬楼梯",
        "difficulty": "简单", "tags": ["动态规划", "记忆化"], "category": "动态规划",
        "visualizer": "fibonacci.html", "visHint": "本质就是斐波那契数列",
        "desc": "假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？",
        "examples": [
            {"input": "n = 2", "output": "2", "explain": "1+1 或 2"},
            {"input": "n = 3", "output": "3", "explain": "1+1+1、1+2、2+1"},
        ],
        "hints": ["到达第 n 阶的方法数 = 到达 n-1 阶 + 到达 n-2 阶", "正是斐波那契数列"],
        "funcName": "climb_stairs",
        "testCases": [
            {"args": [1], "expect": 1},
            {"args": [2], "expect": 2},
            {"args": [3], "expect": 3},
            {"args": [10], "expect": 89},
        ],
        "solutions": [
            {"name": "动态规划（滚动变量）", "time": "O(n)", "space": "O(1)",
             "idea": "设 f(n) 为到达第 n 阶的方法数。最后一步要么走 1 阶（来自 n-1），要么走 2 阶（来自 n-2），所以 f(n)=f(n-1)+f(n-2)。用两个变量滚动即可。",
             "code": """def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b"""},
            {"name": "记忆化递归", "time": "O(n)", "space": "O(n)",
             "idea": "朴素递归会重复计算，用字典缓存已算过的结果。",
             "code": """def climb_stairs(n):
    memo = {}
    def f(k):
        if k <= 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = f(k - 1) + f(k - 2)
        return memo[k]
    return f(n)"""},
        ],
    },
    {
        "slug": "house-robber", "lcId": 198, "title": "打家劫舍",
        "difficulty": "中等", "tags": ["动态规划"], "category": "动态规划",
        "visualizer": "knapsack.html", "visHint": "与 0-1 背包同为「选或不选」的 DP 模型",
        "desc": "你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。给定一个代表每个房屋存放金额的非负整数数组，计算你不触动警报装置的情况下，一夜之内能够偷窃到的最高金额。",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explain": "偷 1 号房(1) 和 3 号房(3)"},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explain": "偷 1、3、5 号房"},
        ],
        "hints": ["每间房：偷（则前一间不能偷）或不偷", "dp[i] = max(dp[i-1], dp[i-2]+nums[i])"],
        "funcName": "rob",
        "testCases": [
            {"args": [[1, 2, 3, 1]], "expect": 4},
            {"args": [[2, 7, 9, 3, 1]], "expect": 12},
            {"args": [[5]], "expect": 5},
            {"args": [[]], "expect": 0},
        ],
        "solutions": [
            {"name": "动态规划（滚动变量）", "time": "O(n)", "space": "O(1)",
             "idea": "prev2 表示「不偷当前这间」的最优（即前一间的最优），prev1 表示「考虑当前及之前」的最优。每步取 max(prev1, prev2+nums[i])。",
             "code": """def rob(nums):
    prev2 = 0      # dp[i-2]
    prev1 = 0      # dp[i-1]
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1"""},
        ],
    },
    {
        "slug": "coin-change", "lcId": 322, "title": "零钱兑换",
        "difficulty": "中等", "tags": ["动态规划", "完全背包"], "category": "动态规划",
        "visualizer": "knapsack.html", "visHint": "完全背包问题（物品可重复选）",
        "desc": "给你一个整数数组 coins，表示不同面额的硬币；以及一个整数 amount，表示总金额。计算并返回可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。你可以认为每种硬币的数量是无限的。",
        "examples": [
            {"input": "coins = [1,2,5], amount = 11", "output": "3", "explain": "11 = 5 + 5 + 1"},
            {"input": "coins = [2], amount = 3", "output": "-1"},
        ],
        "hints": ["dp[i] 表示凑出金额 i 的最少硬币数", "dp[i] = min(dp[i-coin] + 1)"],
        "funcName": "coin_change",
        "testCases": [
            {"args": [[1, 2, 5], 11], "expect": 3},
            {"args": [[2], 3], "expect": -1},
            {"args": [[1], 0], "expect": 0},
        ],
        "solutions": [
            {"name": "完全背包 DP", "time": "O(amount × n)", "space": "O(amount)",
             "idea": "dp[i] = 凑出金额 i 的最少硬币数，初始为无穷大。对每个金额 i，尝试每一种硬币，取 dp[i-coin]+1 的最小值。",
             "code": """def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
    return dp[amount] if dp[amount] != INF else -1"""},
        ],
    },
    {
        "slug": "lcs", "lcId": 1143, "title": "最长公共子序列",
        "difficulty": "中等", "tags": ["动态规划", "字符串"], "category": "动态规划",
        "visualizer": "lcs.html", "visHint": "这就是该可视化页演示的原题",
        "desc": "给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。如果不存在公共子序列，返回 0。子序列是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符后组成的新字符串。",
        "examples": [
            {"input": 'text1 = "abcde", text2 = "ace"', "output": "3", "explain": "最长公共子序列是 \"ace\""},
            {"input": 'text1 = "abc", text2 = "abc"', "output": "3"},
            {"input": 'text1 = "abc", text2 = "def"', "output": "0"},
        ],
        "hints": ["二维 DP", "字符相同就斜着 +1，不同就取上/左较大值"],
        "funcName": "longest_common_subsequence",
        "testCases": [
            {"args": ["abcde", "ace"], "expect": 3},
            {"args": ["abc", "abc"], "expect": 3},
            {"args": ["abc", "def"], "expect": 0},
            {"args": ["", "abc"], "expect": 0},
        ],
        "solutions": [
            {"name": "二维动态规划", "time": "O(n×m)", "space": "O(n×m)",
             "idea": "dp[i][j] 表示 text1 前 i 个字符与 text2 前 j 个字符的 LCS 长度。字符相同时 dp[i][j]=dp[i-1][j-1]+1；否则取 max(dp[i-1][j], dp[i][j-1])。",
             "code": """def longest_common_subsequence(text1, text2):
    n, m = len(text1), len(text2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]"""},
        ],
    },
    {
        "slug": "max-subarray", "lcId": 53, "title": "最大子数组和",
        "difficulty": "中等", "tags": ["数组", "动态规划", "分治"], "category": "动态规划",
        "visualizer": "sliding-window.html", "visHint": "理解「连续子区间」的处理方式",
        "desc": "给你一个整数数组 nums，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6",
             "explain": "连续子数组 [4,-1,2,1] 的和最大，为 6"},
            {"input": "nums = [1]", "output": "1"},
        ],
        "hints": ["Kadane 算法：cur = max(x, cur+x)", "若前面的累加和变成负数就丢掉重来"],
        "funcName": "max_sub_array",
        "testCases": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expect": 6},
            {"args": [[1]], "expect": 1},
            {"args": [[-1]], "expect": -1},
            {"args": [[-2, -1]], "expect": -1},
        ],
        "solutions": [
            {"name": "Kadane 算法（贪心/DP）", "time": "O(n)", "space": "O(1)",
             "idea": "维护「以当前位置结尾的最大子数组和」cur。每步 cur = max(x, cur + x)：要么从当前数重新开始，要么接上前面的。全程记录最大值。",
             "code": """def max_sub_array(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best"""},
        ],
    },
]
