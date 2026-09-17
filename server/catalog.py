# -*- coding: utf-8 -*-
"""算法目录：集中管理所有算法讲解页的元信息。

首页、导航栏都从这里取数据，新增算法只需在此登记一处。
"""

CATALOG = [
    # ---------- 原有 4 个 ----------
    {
        "id": "sort", "page": "sort.html", "icon": "🧱",
        "title": "排序算法可视化",
        "subtitle": "冒泡 / 选择 / 插入",
        "desc": "柱条像气泡一样上浮归位，可调速、可单步、可对比三种写法。",
        "category": "排序与基础", "order": 1,
    },
    {
        "id": "wheat", "page": "wheat.html", "icon": "🌾",
        "title": "麦粒棋盘 · 指数爆炸",
        "subtitle": "时间复杂度 O(2ⁿ)",
        "desc": "一格翻一倍的麦粒，第 64 格就能让整个王国破产。",
        "category": "排序与基础", "order": 2,
    },
    {
        "id": "fibonacci", "page": "fibonacci.html", "icon": "🐰",
        "title": "兔子农场 · 斐波那契",
        "subtitle": "递归与数列增长",
        "desc": "每对兔子每月生一对，长出 1、1、2、3、5、8…… 向日葵也长这样。",
        "category": "排序与基础", "order": 3,
    },
    {
        "id": "genetic", "page": "genetic.html", "icon": "🧬",
        "title": "遗传算法 · 小世界",
        "subtitle": "选择-交叉-变异",
        "desc": "一群随机小点靠进化自发聚集到金峰，算法自己找出答案。",
        "category": "智能与涌现", "order": 4,
    },

    # ---------- 新增 8 个 ----------
    {
        "id": "life", "page": "life.html", "icon": "🦠",
        "title": "康威生命游戏",
        "subtitle": "元胞自动机 · 涌现",
        "desc": "三条规则就能涌现出滑翔机、脉冲星——最简单的规则，最复杂的生命。",
        "category": "智能与涌现", "order": 5,
    },
    {
        "id": "pathfinding", "page": "pathfinding.html", "icon": "🗺️",
        "title": "A* 寻路可视化",
        "subtitle": "A* / Dijkstra / BFS / DFS",
        "desc": "鼠标画墙，看搜索如何扩散并找到路径；四种算法同台对比搜索范围。",
        "category": "图与树", "order": 6,
    },
    {
        "id": "hanoi", "page": "hanoi.html", "icon": "🗼",
        "title": "汉诺塔",
        "subtitle": "递归 · 又是 2ⁿ−1",
        "desc": "三根柱子搬圆盘，n 个盘要 2ⁿ−1 步——和麦粒棋盘遥相呼应的指数爆炸。",
        "category": "排序与基础", "order": 7,
    },
    {
        "id": "nqueens", "page": "nqueens.html", "icon": "♛",
        "title": "N 皇后 · 回溯法",
        "subtitle": "试探 → 冲突 → 撤回",
        "desc": "皇后逐个放置，走不通就撤回换位，回溯法的经典教具。",
        "category": "图与树", "order": 8,
    },
    {
        "id": "montecarlo", "page": "montecarlo.html", "icon": "🎲",
        "title": "蒙特卡罗求 π",
        "subtitle": "概率算法",
        "desc": "随机撒点估算圆周率，撒得越多越准——精度只按 1/√N 提升。",
        "category": "数学之美", "order": 9,
    },
    {
        "id": "mandelbrot", "page": "mandelbrot.html", "icon": "🌀",
        "title": "曼德勃罗集",
        "subtitle": "分形 · 无限细节",
        "desc": "z←z²+c 的简单迭代，画出无限自相似的边界；可无限放大探索。",
        "category": "数学之美", "order": 10,
    },
    {
        "id": "aco", "page": "aco.html", "icon": "🐜",
        "title": "蚁群算法",
        "subtitle": "信息素 · 正反馈",
        "desc": "蚂蚁边走边留信息素，短路径越走越浓，群体自发找出最优路线。",
        "category": "智能与涌现", "order": 11,
    },
    {
        "id": "kmp", "page": "kmp.html", "icon": "🔤",
        "title": "KMP 字符串匹配",
        "subtitle": "next 数组的魔法",
        "desc": "失配时主串指针永不回头，靠 next 数组一口气滑到下一个可匹配位。",
        "category": "查找与字符串", "order": 12,
    },

    # ---------- 第三批：扩展到 25 个 ----------
    {
        "id": "divide-sort", "page": "divide-sort.html", "icon": "⚡",
        "title": "快速排序 / 归并排序",
        "subtitle": "分治思想 · O(n log n)",
        "desc": "快排选基准分区、归并对半合并——分治让排序从 O(n²) 跃升到 O(n log n)。",
        "category": "排序与基础", "order": 13,
    },
    {
        "id": "binary-search", "page": "binary-search.html", "icon": "🎯",
        "title": "二分查找",
        "subtitle": "每次砍掉一半",
        "desc": "有序数组中每次比较排除一半候选，100 万个数也只要约 20 次比较。",
        "category": "查找与字符串", "order": 14,
    },
    {
        "id": "fast-power", "page": "fast-power.html", "icon": "🚀",
        "title": "快速幂",
        "subtitle": "O(log n) 的魔法",
        "desc": "把指数拆成二进制，乘法次数从 n 次降到 log₂n 次——加密算法的基石。",
        "category": "查找与字符串", "order": 15,
    },
    {
        "id": "graph", "page": "graph.html", "icon": "🕸️",
        "title": "图算法 · 最短路与遍历",
        "subtitle": "Dijkstra / BFS / DFS",
        "desc": "同一张图上三种算法扩散形态截然不同：按距离、按层、一路深入。",
        "category": "图与树", "order": 16,
    },
    {
        "id": "bst", "page": "bst.html", "icon": "🌳",
        "title": "二叉搜索树",
        "subtitle": "中序遍历即升序",
        "desc": "左小右大的结构让查找 O(log n)——但插入顺序不对就会退化成链表。",
        "category": "图与树", "order": 17,
    },
    {
        "id": "heap", "page": "heap.html", "icon": "⛰️",
        "title": "二叉堆与优先队列",
        "subtitle": "上浮 / 下沉 O(log n)",
        "desc": "用数组就能实现的完全二叉树，取最小值 O(1)，是 Top-K 问题的利器。",
        "category": "图与树", "order": 18,
    },
    {
        "id": "knapsack", "page": "knapsack.html", "icon": "🎒",
        "title": "0-1 背包问题",
        "subtitle": "动态规划入门",
        "desc": "容量有限、每件物品只能选一次，看 DP 表如何逐格填出最优解。",
        "category": "回溯与动态规划", "order": 19,
    },
    {
        "id": "lcs", "page": "lcs.html", "icon": "🧬",
        "title": "最长公共子序列",
        "subtitle": "二维动态规划",
        "desc": "两行两列填表格，相同字符斜着 +1——git diff 和 DNA 比对的底层算法。",
        "category": "回溯与动态规划", "order": 20,
    },
    {
        "id": "prime-sieve", "page": "prime-sieve.html", "icon": "🔢",
        "title": "埃拉托斯特尼筛法",
        "subtitle": "O(n log log n)",
        "desc": "从最小素数开始划掉它的所有倍数，剩下的就是素数——快得惊人。",
        "category": "数学之美", "order": 21,
    },
    {
        "id": "josephus", "page": "josephus.html", "icon": "⭕",
        "title": "约瑟夫环",
        "subtitle": "从模拟到递推",
        "desc": "围成一圈报数出列，看着像要模拟 O(n·k)，其实一行递推就能 O(n) 算完。",
        "category": "数学之美", "order": 22,
    },
    {
        "id": "consistent-hash", "page": "consistent-hash.html", "icon": "💠",
        "title": "一致性哈希",
        "subtitle": "分布式系统的基石",
        "desc": "把哈希空间弯成环，增删服务器只迁移一小段数据——Redis Cluster 的核心。",
        "category": "工程与分布式", "order": 23,
    },
    {
        "id": "topo-sort", "page": "topo-sort.html", "icon": "🔗",
        "title": "拓扑排序",
        "subtitle": "Kahn 入度法 / DFS",
        "desc": "给有依赖的任务排出执行顺序；顺带检测「循环依赖」这种致命问题。",
        "category": "图与树", "order": 24,
    },
    {
        "id": "sliding-window", "page": "sliding-window.html", "icon": "🪟",
        "title": "滑动窗口",
        "subtitle": "双指针 · O(n)",
        "desc": "两个指针维护一个区间，把「枚举所有子区间」的 O(n²) 压缩成 O(n)。",
        "category": "查找与字符串", "order": 25,
    },
]


def by_category():
    """按分类分组，供首页展示。"""
    groups = {}
    for item in sorted(CATALOG, key=lambda x: x["order"]):
        groups.setdefault(item["category"], []).append(item)
    return groups
