# -*- coding: utf-8 -*-
"""题库数据层（第六部分）：图与树 / 动态规划 / 回溯 / 贪心 补强。"""

PART6 = [
    {
        "slug": "rotting-oranges", "lcId": 994, "title": "腐烂的橘子",
        "difficulty": "中等", "tags": ["图", "BFS", "矩阵"], "category": "图与树",
        "visualizer": "pathfinding.html", "visHint": "多源 BFS：从一个集合同时向外扩散",
        "desc": "在给定的 m x n 网格 grid 中，每个单元格可以有以下三个值之一：值 0 代表空单元格；值 1 代表新鲜橘子；值 2 代表腐烂的橘子。每分钟，腐烂的橘子会使其上、下、左、右四个方向上的新鲜橘子腐烂。返回直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 -1。",
        "examples": [
            {"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4"},
            {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1"},
        ],
        "hints": ["把所有腐烂橘子同时放入队列（多源 BFS）", "答案是最后一层扩散的层数"],
        "funcName": "oranges_rotting",
        "testCases": [
            {"args": [[[2,1,1],[1,1,0],[0,1,1]]], "expect": 4},
            {"args": [[[2,1,1],[0,1,1],[1,0,1]]], "expect": -1},
            {"args": [[[0,2]]], "expect": 0},
        ],
        "solutions": [
            {"name": "多源 BFS", "time": "O(m×n)", "space": "O(m×n)",
             "idea": "先统计新鲜橘子数，并把所有腐烂橘子的位置放进队列。然后做 BFS，每层代表一分钟。BFS 结束后若还有新鲜橘子则返回 -1，否则返回层数。",
             "code": """from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    while q:
        minutes += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        if fresh == 0:
            return minutes
    return -1"""},
        ],
    },
    {
        "slug": "invert-binary-tree", "lcId": 226, "title": "翻转二叉树",
        "difficulty": "简单", "tags": ["树", "递归", "DFS"], "category": "图与树",
        "visualizer": "bst.html", "visHint": "二叉树的递归结构操作",
        "desc": "给你一棵二叉树的根节点 root，翻转这棵二叉树，并返回其根节点。",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"},
            {"input": "root = [2,1,3]", "output": "[2,3,1]"},
        ],
        "hints": ["交换左右孩子，然后递归翻转子树"],
        "funcName": "invert_tree",
        "testCases": [
            {"args": [[4, 2, 7, 1, 3, 6, 9]], "expect": [4, 7, 2, 9, 6, 3, 1]},
            {"args": [[2, 1, 3]], "expect": [2, 3, 1]},
            {"args": [[]], "expect": []},
        ],
        "solutions": [
            {"name": "递归交换（层序数组表示）", "time": "O(n)", "space": "O(h)",
             "idea": "用层序数组表示树。递归地交换每个节点的左右孩子，再分别翻转两棵子树。",
             "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root):
    if not root:
        return []
    # 数组 -> 树
    head = TreeNode(root[0])
    q = [head]
    i = 1
    while q and i < len(root):
        node = q.pop(0)
        if i < len(root) and root[i] is not None:
            node.left = TreeNode(root[i]); q.append(node.left)
        i += 1
        if i < len(root) and root[i] is not None:
            node.right = TreeNode(root[i]); q.append(node.right)
        i += 1

    def invert(node):
        if node is None:
            return
        node.left, node.right = node.right, node.left
        invert(node.left)
        invert(node.right)

    invert(head)

    # 树 -> 数组（层序，去掉尾部 None）
    res = []
    q2 = [head]
    while q2:
        node = q2.pop(0)
        if node is None:
            res.append(None)
        else:
            res.append(node.val)
            q2.append(node.left)
            q2.append(node.right)
    while res and res[-1] is None:
        res.pop()
    return res"""},
        ],
    },
    {
        "slug": "level-order", "lcId": 102, "title": "二叉树的层序遍历",
        "difficulty": "中等", "tags": ["树", "BFS"], "category": "图与树",
        "visualizer": "graph.html", "visHint": "BFS 在树结构上的应用",
        "desc": "给你二叉树的根节点 root，返回其节点值的层序遍历。（即逐层地，从左到右访问所有节点）。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
        ],
        "hints": ["用队列，每次处理「当前层的所有节点」"],
        "funcName": "level_order",
        "testCases": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expect": [[3], [9, 20], [15, 7]]},
            {"args": [[1]], "expect": [[1]]},
            {"args": [[]], "expect": []},
        ],
        "solutions": [
            {"name": "BFS 分层处理", "time": "O(n)", "space": "O(n)",
             "idea": "用队列做 BFS。关键在于每轮先记录队列当前长度 size，这一轮就只处理这 size 个节点——它们正好是同一层。",
             "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    if not root:
        return []
    head = TreeNode(root[0])
    q = [head]
    i = 1
    while q and i < len(root):
        node = q.pop(0)
        if i < len(root) and root[i] is not None:
            node.left = TreeNode(root[i]); q.append(node.left)
        i += 1
        if i < len(root) and root[i] is not None:
            node.right = TreeNode(root[i]); q.append(node.right)
        i += 1

    res = []
    q2 = [head]
    while q2:
        level = []
        for _ in range(len(q2)):
            node = q2.pop(0)
            level.append(node.val)
            if node.left:
                q2.append(node.left)
            if node.right:
                q2.append(node.right)
        res.append(level)
    return res"""},
        ],
    },
    {
        "slug": "edit-distance", "lcId": 72, "title": "编辑距离",
        "difficulty": "困难", "tags": ["动态规划", "字符串"], "category": "动态规划",
        "visualizer": "lcs.html", "visHint": "与 LCS 同为二维 DP 的经典",
        "desc": "给你两个单词 word1 和 word2，请返回将 word1 转换成 word2 所使用的最少操作数。你可以对一个单词进行如下三种操作：插入一个字符、删除一个字符、替换一个字符。",
        "examples": [
            {"input": 'word1 = "horse", word2 = "ros"', "output": "3",
             "explain": "horse -> rorse (替换) -> rose (删除) -> ros (删除)"},
            {"input": 'word1 = "intention", word2 = "execution"', "output": "5"},
        ],
        "hints": ["dp[i][j] = word1 前 i 个字符转成 word2 前 j 个字符的最少操作数", "字符相同则继承 dp[i-1][j-1]"],
        "funcName": "min_distance",
        "testCases": [
            {"args": ["horse", "ros"], "expect": 3},
            {"args": ["intention", "execution"], "expect": 5},
            {"args": ["", ""], "expect": 0},
            {"args": ["abc", ""], "expect": 3},
        ],
        "solutions": [
            {"name": "二维动态规划", "time": "O(m×n)", "space": "O(m×n)",
             "idea": "dp[i][j] 表示 word1 前 i 个字符转成 word2 前 j 个字符的最少操作数。字符相同时沿用 dp[i-1][j-1]；不同时取「删除/插入/替换」三种操作的最小值 +1。",
             "code": """def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],       # 删除
                                   dp[i][j - 1],       # 插入
                                   dp[i - 1][j - 1])   # 替换
    return dp[m][n]"""},
        ],
    },
    {
        "slug": "partition-equal-subset", "lcId": 416, "title": "分割等和子集",
        "difficulty": "中等", "tags": ["动态规划", "数组", "背包"], "category": "动态规划",
        "visualizer": "knapsack.html", "visHint": "0-1 背包的变体：能否恰好装满容量 sum/2",
        "desc": "给你一个只包含正整数的非空数组 nums。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。",
        "examples": [
            {"input": "nums = [1,5,11,5]", "output": "true", "explain": "数组可以分割成 [1,5,5] 和 [11]"},
            {"input": "nums = [1,2,3,5]", "output": "false"},
        ],
        "hints": ["总和必须是偶数", "转化为：能否选出一些数使和为 sum/2（0-1 背包）"],
        "funcName": "can_partition",
        "testCases": [
            {"args": [[1, 5, 11, 5]], "expect": True},
            {"args": [[1, 2, 3, 5]], "expect": False},
            {"args": [[1, 1]], "expect": True},
            {"args": [[1]], "expect": False},
        ],
        "solutions": [
            {"name": "0-1 背包（一维滚动数组）", "time": "O(n×sum)", "space": "O(sum)",
             "idea": "若总和为奇数直接 false。目标变成「能否用 nums 中的数凑出 sum/2」。用一维 dp 数组，dp[j] 表示能否凑出和 j，从大到小遍历容量避免重复使用元素。",
             "code": """def can_partition(nums):
    total = sum(nums)
    if total % 2 == 1:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for j in range(target, x - 1, -1):   # 倒序：每个数只用一次
            dp[j] = dp[j] or dp[j - x]
    return dp[target]"""},
        ],
    },
    {
        "slug": "word-search", "lcId": 79, "title": "单词搜索",
        "difficulty": "中等", "tags": ["回溯", "矩阵", "DFS"], "category": "递归与回溯",
        "visualizer": "nqueens.html", "visHint": "回溯法在二维网格上的应用",
        "desc": "给定一个 m x n 二维字符网格 board 和一个字符串单词 word。如果 word 存在于网格中，返回 true；否则，返回 false。单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中「相邻」单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。",
        "examples": [
            {"input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"',
             "output": "true"},
        ],
        "hints": ["从每个格子出发尝试 DFS", "访问过的格子要标记，回溯时恢复"],
        "funcName": "exist",
        "testCases": [
            {"args": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"], "expect": True},
            {"args": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"], "expect": True},
            {"args": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"], "expect": False},
        ],
        "solutions": [
            {"name": "DFS 回溯", "time": "O(m×n×3^k)", "space": "O(k)",
             "idea": "枚举每个起点做 DFS。每走一步就把当前格子临时标记为已访问（改成特殊字符），四个方向继续匹配；匹配失败则恢复现场（回溯）。",
             "code": """def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        tmp = board[r][c]
        board[r][c] = '#'          # 标记已访问
        found = (dfs(r + 1, c, idx + 1) or dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or dfs(r, c - 1, idx + 1))
        board[r][c] = tmp          # 回溯恢复
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False"""},
        ],
    },
    {
        "slug": "generate-parentheses", "lcId": 22, "title": "括号生成",
        "difficulty": "中等", "tags": ["回溯", "字符串", "动态规划"], "category": "递归与回溯",
        "visualizer": "nqueens.html", "visHint": "回溯：每步做合法选择",
        "desc": "数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且有效的括号组合。",
        "examples": [
            {"input": "n = 3", "output": '["((()))","(()())","(())()","()(())","()()()"]'},
            {"input": "n = 1", "output": '["()"]'},
        ],
        "hints": ["左括号数 < n 时可以加左括号", "右括号数 < 左括号数时可以加右括号"],
        "funcName": "generate_parenthesis",
        "testCases": [
            {"args": [3], "expect": ["((()))","(()())","(())()","()(())","()()()"]},
            {"args": [1], "expect": ["()"]},
            {"args": [2], "expect": ["(())","()()"]},
        ],
        "solutions": [
            {"name": "回溯（记录已用括号数）", "time": "O(4ⁿ/√n)", "space": "O(n)",
             "idea": "维护已用的左括号数 left 和右括号数 right。只要 left < n 就能加左括号；只要 right < left 就能加右括号。凑满 2n 个字符即为一个合法组合。",
             "code": """def generate_parenthesis(n):
    res = []
    path = []

    def backtrack(left, right):
        if len(path) == 2 * n:
            res.append(''.join(path))
            return
        if left < n:
            path.append('(')
            backtrack(left + 1, right)
            path.pop()
        if right < left:
            path.append(')')
            backtrack(left, right + 1)
            path.pop()

    backtrack(0, 0)
    return res"""},
        ],
    },
    {
        "slug": "partition-labels", "lcId": 763, "title": "划分字母区间",
        "difficulty": "中等", "tags": ["贪心", "字符串", "哈希表"], "category": "贪心",
        "visualizer": None, "visHint": None,
        "desc": "给你一个字符串 s。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是 s。返回一个表示每个字符串片段的长度的列表。",
        "examples": [
            {"input": 's = "ababcbacadefegdehijhklij"', "output": "[9,7,8]",
             "explain": "划分结果为 \"ababcbaca\"、\"defegde\"、\"hijhklij\""},
            {"input": 's = "eccbbbbdec"', "output": "[10]"},
        ],
        "hints": ["先记录每个字母最后出现的位置", "贪心地扩展到「当前片段内所有字母的最远位置」"],
        "funcName": "partition_labels",
        "testCases": [
            {"args": ["ababcbacadefegdehijhklij"], "expect": [9, 7, 8]},
            {"args": ["eccbbbbdec"], "expect": [10]},
        ],
        "solutions": [
            {"name": "贪心 + 最远边界", "time": "O(n)", "space": "O(1)",
             "idea": "先扫一遍记录每个字母最后出现的下标。再扫一遍，维护当前片段的「最远边界」end = max(end, last[s[i]])。当 i == end 时说明当前片段可以切分了，记录长度并开始新片段。",
             "code": """def partition_labels(s):
    last = {}
    for i, ch in enumerate(s):
        last[ch] = i
    res = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res"""},
        ],
    },
]
