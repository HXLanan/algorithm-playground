# -*- coding: utf-8 -*-
"""题库数据层（第三部分）：图与树 / 字符串 / 栈与队列 / 链表 / 贪心 / 模拟。

字段说明见 problems_part1.py 顶部注释。
"""

PART3 = [
    {
        "slug": "number-of-islands", "lcId": 200, "title": "岛屿数量",
        "difficulty": "中等", "tags": ["图", "BFS", "DFS", "并查集"], "category": "图与树",
        "visualizer": "pathfinding.html", "visHint": "与 A* 寻路同为网格上的搜索遍历",
        "desc": "给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。",
        "examples": [
            {"input": 'grid = [["1","1","0"],["1","1","0"],["0","0","1"]]', "output": "2"},
            {"input": 'grid = [["1","1","1"],["0","1","0"],["1","1","1"]]', "output": "1"},
        ],
        "hints": ["遍历网格，遇到陆地就计数并「淹没」整个岛", "DFS/BFS 都可以"],
        "funcName": "num_islands",
        "testCases": [
            {"args": [[["1","1","0"],["1","1","0"],["0","0","1"]]], "expect": 2},
            {"args": [[["1","1","1"],["0","1","0"],["1","1","1"]]], "expect": 1},
            {"args": [[["0"]]], "expect": 0},
        ],
        "solutions": [
            {"name": "DFS 淹没法", "time": "O(m×n)", "space": "O(m×n)",
             "idea": "遍历每个格子，遇到 '1' 就把岛屿计数 +1，然后用 DFS 把这个岛所有相连的 '1' 全部改成 '0'（淹没），避免重复计数。",
             "code": """def num_islands(grid):
    if not grid:
        return 0
    g = [row[:] for row in grid]     # 复制，避免修改输入
    rows, cols = len(g), len(g[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or g[r][c] != '1':
            return
        g[r][c] = '0'
        dfs(r + 1, c); dfs(r - 1, c)
        dfs(r, c + 1); dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if g[r][c] == '1':
                count += 1
                dfs(r, c)
    return count"""},
            {"name": "BFS 淹没法", "time": "O(m×n)", "space": "O(m×n)",
             "idea": "同上是淹没，但用队列做广度优先，避免深递归爆栈。",
             "code": """from collections import deque

def num_islands(grid):
    if not grid:
        return 0
    g = [row[:] for row in grid]
    rows, cols = len(g), len(g[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != '1':
                continue
            count += 1
            q = deque([(r, c)])
            g[r][c] = '0'
            while q:
                x, y = q.popleft()
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == '1':
                        g[nx][ny] = '0'
                        q.append((nx, ny))
    return count"""},
        ],
    },
    {
        "slug": "course-schedule", "lcId": 207, "title": "课程表",
        "difficulty": "中等", "tags": ["图", "拓扑排序", "BFS", "DFS"], "category": "图与树",
        "visualizer": "topo-sort.html", "visHint": "这就是拓扑排序的经典应用（检测循环依赖）",
        "desc": "你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses-1。在选修某些课程之前需要一些先修课程，先修课程按数组 prerequisites 给出，其中 prerequisites[i] = [ai, bi] 表示如果要学习课程 ai 则必须先学习课程 bi。请你判断是否可能完成所有课程的学习？如果可以，返回 true；否则返回 false。",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true"},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false",
             "explain": "课程 0 和 1 互相依赖，形成环，无法完成"},
        ],
        "hints": ["本质是判断有向图是否有环", "Kahn 算法：如果最后没能取出全部节点，就有环"],
        "funcName": "can_finish",
        "testCases": [
            {"args": [2, [[1, 0]]], "expect": True},
            {"args": [2, [[1, 0], [0, 1]]], "expect": False},
            {"args": [1, []], "expect": True},
        ],
        "solutions": [
            {"name": "Kahn 算法（BFS 拓扑排序）", "time": "O(V+E)", "space": "O(V+E)",
             "idea": "统计每门课的入度（先修数量）。把所有入度为 0 的课入队，逐个出队并让它指向的课入度减 1。若最终出队数量等于课程总数，说明无环。",
             "code": """from collections import deque

def can_finish(numCourses, prerequisites):
    indeg = [0] * numCourses
    adj = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[b].append(a)          # b 是 a 的先修
        indeg[a] += 1

    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    taken = 0
    while q:
        u = q.popleft()
        taken += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == numCourses"""},
        ],
    },
    {
        "slug": "max-depth-binary-tree", "lcId": 104, "title": "二叉树的最大深度",
        "difficulty": "简单", "tags": ["树", "DFS", "BFS"], "category": "图与树",
        "visualizer": "bst.html", "visHint": "理解二叉树的递归结构",
        "desc": "给定一个二叉树 root，返回其最大深度。二叉树的最大深度是指从根节点到最远叶子节点的最长路径上的节点数。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3"},
            {"input": "root = [1,null,2]", "output": "2"},
        ],
        "hints": ["最大深度 = 1 + max(左子树深度, 右子树深度)", "空节点深度为 0"],
        "funcName": "max_depth",
        "testCases": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expect": 3},
            {"args": [[1, None, 2]], "expect": 2},
            {"args": [[]], "expect": 0},
        ],
        "solutions": [
            {"name": "递归 DFS（层序数组表示）", "time": "O(n)", "space": "O(h)",
             "idea": "输入用层序数组表示二叉树（None 表示空节点）。先把数组还原成树，再用「最大深度 = 1 + max(左, 右)」递归求解。",
             "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root):
    if not root:
        return 0
    # 层序数组 -> 二叉树
    head = TreeNode(root[0])
    q = [head]
    i = 1
    while q and i < len(root):
        node = q.pop(0)
        if i < len(root) and root[i] is not None:
            node.left = TreeNode(root[i])
            q.append(node.left)
        i += 1
        if i < len(root) and root[i] is not None:
            node.right = TreeNode(root[i])
            q.append(node.right)
        i += 1

    def depth(node):
        if node is None:
            return 0
        return 1 + max(depth(node.left), depth(node.right))

    return depth(head)"""},
        ],
    },
    {
        "slug": "valid-parentheses", "lcId": 20, "title": "有效的括号",
        "difficulty": "简单", "tags": ["栈", "字符串"], "category": "栈与队列",
        "visualizer": None, "visHint": None,
        "desc": "给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s，判断字符串是否有效。有效字符串需满足：左括号必须用相同类型的右括号闭合；左括号必须以正确的顺序闭合；每个右括号都有一个对应的相同类型的左括号。",
        "examples": [
            {"input": 's = "()"', "output": "true"},
            {"input": 's = "()[]{}"', "output": "true"},
            {"input": 's = "(]"', "output": "false"},
        ],
        "hints": ["遇到左括号入栈", "遇到右括号检查栈顶是否匹配"],
        "funcName": "is_valid",
        "testCases": [
            {"args": ["()"], "expect": True},
            {"args": ["()[]{}"], "expect": True},
            {"args": ["(]"], "expect": False},
            {"args": ["([)]"], "expect": False},
            {"args": [""], "expect": True},
        ],
        "solutions": [
            {"name": "栈", "time": "O(n)", "space": "O(n)",
             "idea": "左括号压栈；遇到右括号时，栈顶必须是配对的左括号，否则非法。最后栈必须为空。",
             "code": """def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack"""},
        ],
    },
    {
        "slug": "reverse-linked-list", "lcId": 206, "title": "反转链表",
        "difficulty": "简单", "tags": ["链表", "递归"], "category": "链表",
        "visualizer": None, "visHint": None,
        "desc": "给你单链表的头节点 head，请你反转链表，并返回反转后的链表。",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "head = []", "output": "[]"},
        ],
        "hints": ["用 prev / cur / nxt 三个指针逐节点翻转", "注意最后返回 prev"],
        "funcName": "reverse_list",
        "testCases": [
            {"args": [[1, 2, 3, 4, 5]], "expect": [5, 4, 3, 2, 1]},
            {"args": [[]], "expect": []},
            {"args": [[1]], "expect": [1]},
        ],
        "solutions": [
            {"name": "迭代三指针", "time": "O(n)", "space": "O(1)",
             "idea": "先把数组构造成链表节点。prev 初始为 None，cur 为头节点。每步先用 nxt 记住下一个节点，再把 cur.next 指向 prev，然后整体前移。最后沿 prev 收集结果。",
             "code": """class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt


def reverse_list(head):
    # 数组 -> 链表
    dummy = ListNode(0)
    tail = dummy
    for v in head:
        tail.next = ListNode(v)
        tail = tail.next

    # 反转
    prev = None
    cur = dummy.next
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # 链表 -> 数组
    res = []
    while prev:
        res.append(prev.val)
        prev = prev.next
    return res"""},
        ],
    },
    {
        "slug": "best-time-stock", "lcId": 121, "title": "买卖股票的最佳时机",
        "difficulty": "简单", "tags": ["数组", "贪心", "动态规划"], "category": "贪心",
        "visualizer": None, "visHint": None,
        "desc": "给定一个数组 prices，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。你只能选择某一天买入这只股票，并选择在未来的某一个不同的日子卖出。设计一个算法来计算你所能获取的最大利润。返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0。",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explain": "第 2 天买(1)，第 5 天卖(6)"},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explain": "不交易"},
        ],
        "hints": ["遍历时维护「到目前为止的最低价」", "每天都假设今天卖出"],
        "funcName": "max_profit",
        "testCases": [
            {"args": [[7, 1, 5, 3, 6, 4]], "expect": 5},
            {"args": [[7, 6, 4, 3, 1]], "expect": 0},
            {"args": [[]], "expect": 0},
        ],
        "solutions": [
            {"name": "一次遍历（贪心）", "time": "O(n)", "space": "O(1)",
             "idea": "维护历史最低价 min_price。遍历每一天，先更新最低价，再用「今天价格 - 最低价」更新最大利润。",
             "code": """def max_profit(prices):
    min_price = float('inf')
    best = 0
    for p in prices:
        if p < min_price:
            min_price = p
        elif p - min_price > best:
            best = p - min_price
    return best"""},
        ],
    },
    {
        "slug": "merge-intervals", "lcId": 56, "title": "合并区间",
        "difficulty": "中等", "tags": ["数组", "排序", "贪心"], "category": "贪心",
        "visualizer": "divide-sort.html", "visHint": "排序是这类问题的第一步",
        "desc": "以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi]。请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]",
             "output": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"},
        ],
        "hints": ["按左端点排序", "若当前区间左端点 ≤ 上一个区间右端点，则合并"],
        "funcName": "merge_intervals",
        "testCases": [
            {"args": [[[1,3],[2,6],[8,10],[15,18]]], "expect": [[1,6],[8,10],[15,18]]},
            {"args": [[[1,4],[4,5]]], "expect": [[1,5]]},
            {"args": [[]], "expect": []},
        ],
        "solutions": [
            {"name": "排序 + 一次扫描", "time": "O(n log n)", "space": "O(n)",
             "idea": "按起点排序后，依次检查：若当前区间起点 ≤ 结果中最后一个区间的终点，就合并（更新终点为两者较大值）；否则直接追加。",
             "code": """def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    res = [list(intervals[0])]
    for start, end in intervals[1:]:
        if start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res"""},
        ],
    },
    {
        "slug": "jump-game", "lcId": 55, "title": "跳跃游戏",
        "difficulty": "中等", "tags": ["数组", "贪心"], "category": "贪心",
        "visualizer": None, "visHint": None,
        "desc": "给你一个非负整数数组 nums，你最初位于数组的第一个下标。数组中的每个元素代表你在该位置可以跳跃的最大长度。判断你是否能够到达最后一个下标。",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "true", "explain": "跳 1 步到下标1，再跳 3 步到末尾"},
            {"input": "nums = [3,2,1,0,4]", "output": "false"},
        ],
        "hints": ["维护「当前能到达的最远位置」", "若遍历到某处超过最远位置，说明卡住了"],
        "funcName": "can_jump",
        "testCases": [
            {"args": [[2, 3, 1, 1, 4]], "expect": True},
            {"args": [[3, 2, 1, 0, 4]], "expect": False},
            {"args": [[0]], "expect": True},
        ],
        "solutions": [
            {"name": "贪心（维护最远可达）", "time": "O(n)", "space": "O(1)",
             "idea": "边走边更新「从当前位置能跳到的最远下标」reach。如果当前位置 i 已经超过 reach，说明走不到这里，失败。",
             "code": """def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
        if reach >= len(nums) - 1:
            return True
    return True"""},
        ],
    },
    {
        "slug": "longest-common-prefix", "lcId": 14, "title": "最长公共前缀",
        "difficulty": "简单", "tags": ["字符串"], "category": "字符串",
        "visualizer": None, "visHint": None,
        "desc": "编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 \"\"。",
        "examples": [
            {"input": 'strs = ["flower","flow","flight"]', "output": '"fl"'},
            {"input": 'strs = ["dog","racecar","car"]', "output": '""'},
        ],
        "hints": ["以第一个字符串为基准，逐字符与其余字符串比较"],
        "funcName": "longest_common_prefix",
        "testCases": [
            {"args": [["flower", "flow", "flight"]], "expect": "fl"},
            {"args": [["dog", "racecar", "car"]], "expect": ""},
            {"args": [["a"]], "expect": "a"},
        ],
        "solutions": [
            {"name": "纵向扫描", "time": "O(n×m)", "space": "O(1)",
             "idea": "以第一个字符串为基准，逐列比较所有字符串的第 i 个字符。一旦某个字符串长度不够或字符不同，就返回已匹配的前缀。",
             "code": """def longest_common_prefix(strs):
    if not strs:
        return ""
    for i in range(len(strs[0])):
        ch = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]"""},
        ],
    },
    {
        "slug": "game-of-life", "lcId": 289, "title": "生命游戏",
        "difficulty": "中等", "tags": ["数组", "矩阵", "模拟"], "category": "模拟与进阶",
        "visualizer": "life.html", "visHint": "这就是该可视化页演示的原题",
        "desc": "根据百度百科，生命游戏是英国数学家约翰·何顿·康威在 1970 年发明的细胞自动机。给定一个包含 m × n 个格子的面板，每一个格子都可以看成是一个细胞。每个细胞都具有一个初始状态：1 即为活细胞，0 即为死细胞。每个细胞与其八个相邻位置（水平，垂直，对角线）的细胞都遵循四条生存定律。请你计算面板上下一个状态。",
        "examples": [
            {"input": "board = [[0,1,0],[0,1,0],[0,1,0]]",
             "output": "[[0,0,0],[1,1,1],[0,0,0]]"},
        ],
        "hints": ["四条规则：孤独死、存活、拥挤死、繁殖", "必须同时更新，不能边算边改（用副本或状态编码）"],
        "funcName": "game_of_life",
        "testCases": [
            {"args": [[[0,1,0],[0,1,0],[0,1,0]]], "expect": [[0,0,0],[1,1,1],[0,0,0]]},
            {"args": [[[1,1],[1,0]]], "expect": [[1,1],[1,1]]},
        ],
        "solutions": [
            {"name": "复制一份原状态", "time": "O(m×n)", "space": "O(m×n)",
             "idea": "因为更新时要看「原始」邻居，所以先复制一份原面板，然后基于副本计算每个格子的新状态。",
             "code": """def game_of_life(board):
    if not board:
        return board
    rows, cols = len(board), len(board[0])
    old = [row[:] for row in board]

    def neighbors(r, c):
        cnt = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    cnt += old[nr][nc]
        return cnt

    for r in range(rows):
        for c in range(cols):
            n = neighbors(r, c)
            if old[r][c] == 1:
                board[r][c] = 1 if n in (2, 3) else 0
            else:
                board[r][c] = 1 if n == 3 else 0
    return board"""},
        ],
    },
    {
        "slug": "rotate-image", "lcId": 48, "title": "旋转图像",
        "difficulty": "中等", "tags": ["数组", "矩阵", "数学"], "category": "模拟与进阶",
        "visualizer": None, "visHint": None,
        "desc": "给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。你必须在原地旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要使用另一个矩阵来旋转图像。",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]",
             "output": "[[7,4,1],[8,5,2],[9,6,3]]"},
        ],
        "hints": ["先转置（沿主对角线翻转）", "再左右翻转每一行"],
        "funcName": "rotate",
        "testCases": [
            {"args": [[[1,2,3],[4,5,6],[7,8,9]]], "expect": [[7,4,1],[8,5,2],[9,6,3]]},
            {"args": [[[1]]], "expect": [[1]]},
        ],
        "solutions": [
            {"name": "转置 + 行翻转", "time": "O(n²)", "space": "O(1)",
             "idea": "顺时针旋转 90° 等价于「先沿主对角线转置，再把每一行左右翻转」。两步都是原地操作。",
             "code": """def rotate(matrix):
    n = len(matrix)
    # 转置
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # 每行左右翻转
    for i in range(n):
        matrix[i].reverse()
    return matrix"""},
        ],
    },
]
