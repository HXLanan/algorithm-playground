# -*- coding: utf-8 -*-
"""自检脚本：不依赖 Flask，直接验证算法层与服务层的正确性。

用法（在 algo-playground/ 目录下）：
    python selfcheck.py

它会跑一组断言，全部通过则打印 "ALL PASS"。
这能在没有浏览器/前端环境时，快速确认核心逻辑无误。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.algo import sorting, exponential, fib, genetic          # noqa: E402
from server.algo import life, hanoi, nqueens, montecarlo            # noqa: E402
from server.algo import mandelbrot, pathfinding, aco, kmp           # noqa: E402
from server.algo import (divide_sort, binary_search, fast_power,    # noqa: E402
                         graph_algo, bst, heap, knapsack, lcs,
                         prime_sieve, josephus, consistent_hash,
                         topo_sort, sliding_window)
from server.services import (sort_service, wheat_service,           # noqa: E402
                             fibonacci_service, genetic_service,
                             life_service, hanoi_service,
                             nqueens_service, montecarlo_service,
                             mandelbrot_service, pathfinding_service,
                             aco_service, kmp_service,
                             divide_sort_service, binary_search_service,
                             fast_power_service, graph_service,
                             bst_service, heap_service, knapsack_service,
                             lcs_service, prime_sieve_service,
                             josephus_service, consistent_hash_service,
                             topo_sort_service, sliding_window_service)
from server.catalog import CATALOG                                  # noqa: E402

PASSED = []


def check(name, cond):
    if cond:
        PASSED.append(name)
        print("  [PASS] %s" % name)
    else:
        print("  [FAIL] %s" % name)
        raise AssertionError(name)


def test_sorting():
    print("\n[1/4] 排序算法层")
    for algo in sorting.SUPPORTED:
        data = [5, 3, 8, 1, 9, 2]
        r = sorting.build_steps(data, algo)
        check("%s 结果已排序" % algo, r["sorted"] == sorted(data))
        check("%s 原数组未被修改" % algo, data == [5, 3, 8, 1, 9, 2])
        check("%s 生成了步骤" % algo, len(r["steps"]) > 0)
        # 每帧快照长度一致
        ok_len = all(len(s["list"]) == len(data) for s in r["steps"])
        check("%s 每帧快照长度一致" % algo, ok_len)
        # 最后一帧应等于有序结果
        check("%s 末帧等于有序结果" % algo, r["steps"][-1]["list"] == sorted(data))

    # 边界：已有序数组（冒泡应提前结束）
    r = sorting.build_steps([1, 2, 3, 4], "bubble")
    check("冒泡对已有序数组提前结束", r["totalWrites"] == 0)

    # 边界：含重复元素
    r = sorting.build_steps([3, 1, 3, 2, 1], "insertion")
    check("插入排序处理重复元素", r["sorted"] == [1, 1, 2, 3, 3])

    # 非法算法
    try:
        sorting.build_steps([1, 2], "nope")
        check("非法算法应报错", False)
    except ValueError:
        check("非法算法应报错", True)


def test_exponential():
    print("\n[2/4] 麦粒棋盘（指数）算法层")
    b = exponential.build_board(64)
    check("第 1 格 = 1 粒", b["rows"][0]["grain"] == 1)
    check("第 2 格 = 2 粒", b["rows"][1]["grain"] == 2)
    check("第 64 格 = 2^63", b["rows"][63]["grain"] == (1 << 63))
    check("总数 = 2^64 - 1", b["total_grain"] == (1 << 64) - 1)
    check("累计值随格数递增", b["rows"][10]["cumulative"] > b["rows"][9]["cumulative"])
    tbl = exponential.complexity_table([10, 20])
    check("复杂度表长度正确", len(tbl) == 2)
    check("指数列计算正确", tbl[1]["O_2n"] == (1 << 20))


def test_fib():
    print("\n[3/4] 斐波那契算法层")
    check("F(0)=0", fib.fib_iterative(0) == 0)
    check("F(1)=1", fib.fib_iterative(1) == 1)
    check("F(2)=1", fib.fib_iterative(2) == 1)
    check("F(10)=55", fib.fib_iterative(10) == 55)
    check("F(20)=6765", fib.fib_iterative(20) == 6765)

    seq = fib.build_sequence(10)
    check("序列首项为 0", seq["seq"][0] == 0)
    check("第 1 月 1 对", seq["details"][1]["total"] == 1)
    check("第 7 月 13 对", seq["details"][7]["total"] == 13)
    check("第 2 月无新生", seq["details"][2]["newborn"] == 0)

    # 调用次数公式 2*F(n)-1 与真实递归结果核对
    counter = {"calls": 0}
    fib.fib_recursive(10, counter)
    check("递归调用次数 = 2*F(n)-1", counter["calls"] == 2 * fib.fib_iterative(10) - 1)
    check("count_recursive_calls 与真实一致",
          fib.count_recursive_calls(10) == counter["calls"])


def test_genetic():
    print("\n[4/4] 遗传算法层")
    # 适应度：金峰处最大
    gx, gy = genetic.GOLD
    check("金峰处适应度 = 1", abs(genetic.fitness(gx, gy) - 1.0) < 1e-9)
    check("远离金峰适应度更小", genetic.fitness(0.0, 0.0) < genetic.fitness(gx, gy))

    import random
    rng = random.Random(42)
    pop = genetic.random_population(200, rng)
    check("种群大小正确", len(pop) == 200)
    check("初始个体都在 [0,1] 内",
          all(0.0 <= x <= 1.0 and 0.0 <= y <= 1.0 for x, y in pop))

    before = max(genetic.fitness(x, y) for x, y in pop)
    res = genetic.run(pop_size=200, generations=60, seed=42)
    after = res["best"]["fitness"]
    check("进化后最优不低于初始", after >= before)
    check("进化后最优接近金峰（>0.9）", after > 0.9)
    check("返回种群数量一致", len(res["population"]) == 200)
    check("坐标已四舍五入到 4 位",
          all(len(str(v).split(".")[-1]) <= 4 for ind in res["population"] for v in ind))


def test_services():
    print("\n[5/5] 服务层（含参数校验）")
    r = sort_service.make_random(12)
    check("生成 12 元素数组", r["count"] == 12 and len(r["array"]) == 12)

    check("make_random 容忍非法输入", sort_service.make_random("abc")["count"] == 10)

    check("run_sort 返回步骤", len(sort_service.run_sort([3, 1, 2], "bubble")["steps"]) > 0)

    try:
        sort_service.run_sort([1], "bubble")
        check("元素过少应报错", False)
    except ValueError:
        check("元素过少应报错", True)

    try:
        sort_service.run_sort(["a", "b"], "bubble")
        check("非数字元素应报错", False)
    except ValueError:
        check("非数字元素应报错", True)

    check("棋盘服务格子数", len(wheat_service.get_board(64)["rows"]) == 64)
    check("棋盘服务容忍非法输入", len(wheat_service.get_board("x")["rows"]) == 64)

    check("fib 服务返回明细", len(fibonacci_service.get_sequence(10)["details"]) == 11)
    check("fib 成本对比", fibonacci_service.compare_cost(20)["recursive_calls"] == 2 * 6765 - 1)

    # 遗传服务：畸形种群应被清洗为 None → 重新随机
    res = genetic_service.evolve(population=[["bad", "data"]], pop_size=50)
    check("畸形种群被安全处理", res["size"] == 50)

    res2 = genetic_service.evolve(population=[[0.5, 0.5], [0.6, 0.7]], pop_size=50)
    check("合法种群被接受", res2["size"] == 2)


def test_life():
    print("\n[6/9] 康威生命游戏")
    # 滑翔机：周期 4 的移动体，人口恒为 5
    g = life.empty_grid(12, 12)
    life.place_pattern(g, "glider", 1, 1)
    check("滑翔机初始人口 = 5", life._population(g) == 5)
    r = life.run(g, 4)
    check("滑翔机 4 代后人口仍为 5", r["alive"] == 5)
    # 方块是静物，永不变化
    g2 = life.empty_grid(8, 8)
    life.place_pattern(g2, "block", 2, 2)
    r2 = life.run(g2, 5)
    check("方块（静物）不变", r2["alive"] == 4)
    # 闪烁器周期 2
    g3 = life.empty_grid(7, 7)
    life.place_pattern(g3, "blinker", 3, 2)
    a3 = life.run(g3, 1)["grid"]
    b3 = life.run(a3, 1)["grid"]
    check("闪烁器周期为 2", b3 == life.run(g3, 2)["grid"])
    check("空网格保持为空", life.run(life.empty_grid(5, 5), 3)["alive"] == 0)
    # 服务层
    r4 = life_service.new_grid(20, 30, pattern="glider")
    check("服务层可摆放图案", r4["alive"] == 5)
    try:
        life_service.evolve([[0, 1], [1, 0]][0:1])
        check("服务层拒绝过小网格", False)
    except ValueError:
        check("服务层拒绝过小网格", True)
    check("服务层列出图案", len(life_service.patterns()["patterns"]) >= 5)


def test_hanoi():
    print("\n[7/9] 汉诺塔")
    for n in (1, 2, 3, 4, 5):
        r = hanoi.simulate(n)
        check("n=%d 步数 = 2^n-1" % n, len(r["steps"]) == (1 << n) - 1)
        check("n=%d 求解完成" % n, r["solved"])
        # 最终所有盘都在 C
        check("n=%d 全部移到 C" % n, r["snapshots"][-1]["pegs"]["C"] == list(range(n, 0, -1)))
        check("n=%d 起始都在 A" % n, r["snapshots"][0]["pegs"]["A"] == list(range(n, 0, -1)))
    # 校验每一步都合法（不能大盘压小盘）
    r = hanoi.simulate(5)
    ok = True
    for snap in r["snapshots"]:
        for peg, stack in snap["pegs"].items():
            for i in range(len(stack) - 1):
                if stack[i] < stack[i + 1]:
                    ok = False
    check("每一步都满足大盘在下", ok)
    check("服务层限额生效", hanoi_service.simulate(99)["disks"] == 12)
    check("移动次数表正确", hanoi_service.move_counts()["table"][0]["moves"] == 1)


def test_nqueens():
    print("\n[8/9] N 皇后")
    # 已知解数（solutionCount 是完整统计，不受过程帧上限影响）
    known = {4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    for n, expect in known.items():
        r = nqueens.solve(n, max_solutions=200)
        check("n=%d 解数 = %d" % (n, expect), r["solutionCount"] == expect)
    check("n=2 无解", nqueens.solve(2)["solutionCount"] == 0)
    check("n=3 无解", nqueens.solve(3)["solutionCount"] == 0)

    # 校验解确实合法（互不攻击）
    r = nqueens.solve(8, max_solutions=200)
    valid = True
    for sol in r["solutions"]:
        for i in range(len(sol)):
            for j in range(i + 1, len(sol)):
                if sol[i] == sol[j]:
                    valid = False
                if abs(sol[i] - sol[j]) == abs(i - j):
                    valid = False
    check("8 皇后所有解都合法", valid)
    check("过程帧包含放置与回溯", len(r["steps"]) > 0)
    check("服务层返回解数表", len(nqueens_service.counts()["table"]) >= 5)


def test_montecarlo():
    print("\n[9/9] 蒙特卡罗 + 曼德勃罗 + 寻路 + 蚁群 + KMP")
    # 蒙特卡罗：点数越多误差越小（统计意义上）
    import math
    r_big = montecarlo.estimate(100000, seed=42, keep_points=100)
    check("10 万点误差 < 0.02", r_big["error"] < 0.02)
    check("命中率 ≈ π/4", abs(r_big["ratio"] - math.pi / 4) < 0.01)
    check("返回点数受限", len(r_big["points"]) <= 100)

    # 曼德勃罗：原点属于集合（迭代不逃逸）
    r = mandelbrot.render(40, 30, max_iter=50)
    check("渲染尺寸正确", r["width"] == 40 and r["height"] == 30)
    check("存在集合内部点", r["insideCount"] > 0)
    o = mandelbrot.orbit(0.0, 0.0, 20)
    check("原点不逃逸", o["escaped"] is False)
    o2 = mandelbrot.orbit(2.0, 2.0, 20)
    check("(2,2) 会逃逸", o2["escaped"] is True)

    # 寻路：无墙直线地图
    g = pathfinding.make_grid(8, 12)
    r = pathfinding.search(g, (0, 0), (7, 11), "astar")
    check("A* 能找到路径", r["found"])
    check("无墙时路径长 = 行+列+1", r["pathLength"] == 7 + 11 + 1)
    r_b = pathfinding.search(g, (0, 0), (7, 11), "bfs")
    check("BFS 也能找到", r_b["found"])
    check("A* 访问不多于 BFS", r["visitedCount"] <= r_b["visitedCount"])
    # 完全封死
    blocked = [[1] * 12 for _ in range(8)]
    blocked[0][0] = 0
    blocked[7][11] = 0
    check("封死时报告无路径", not pathfinding.search(blocked, (0, 0), (7, 11), "astar")["found"])

    # 蚁群：应能找到比随机更短的路径
    r = aco.run(cities=aco.random_cities(10, 1), ants=25, iterations=40, seed=1)
    check("蚁群城市数正确", len(r["cities"]) == 10)
    check("最优路径含全部城市", len(r["bestTour"]) == 10)
    check("历史曲线非空", len(r["history"]) == 40)
    check("长度逐步不增（记录的是历史最优）",
          all(r["history"][i] >= r["history"][i + 1] - 1e-9 for i in range(len(r["history"]) - 1)))
    check("环游长度计算正确",
          abs(aco.tour_length([[0, 0], [1, 0], [1, 1], [0, 1]], [0, 1, 2, 3]) - 4.0) < 1e-9)

    # KMP
    r = kmp.search("ABABDABACDABABCABAB", "ABABCABAB")
    check("KMP 匹配位置正确", r["matches"] == [10])
    check("next 数组长度正确", len(r["next"]) == 9)
    check("KMP 比较次数少于朴素", r["comparisons"] < r["naiveComparisons"])
    check("next[0] = 0", kmp.build_next("ABABCABAB")[0] == 0)
    # 校验 next 数组正确性（前缀函数定义）
    pat = "aabaaab"
    nxt = kmp.build_next(pat)
    ok = True
    for i in range(len(pat)):
        sub = pat[:i + 1]
        best = 0
        for L in range(1, len(sub)):
            if sub[:L] == sub[-L:]:
                best = L
        if nxt[i] != best:
            ok = False
    check("next 数组符合前缀函数定义", ok)
    check("无匹配时返回空", kmp.search("abcdef", "xyz")["matches"] == [])
    check("多处匹配", kmp.search("aaaa", "aa")["matches"] == [0, 1, 2])
    check("服务层拒绝空模式串", _raises(lambda: kmp_service.search("abc", "")))


def test_divide_sort():
    print("\n[11/15] 分治排序（快排 / 归并）")
    for algo in divide_sort.SUPPORTED:
        for data in ([5, 3, 8, 1, 9, 2], [1], [2, 2, 2], list(range(10, 0, -1))):
            r = divide_sort.build_steps(data, algo)
            check("%s 结果正确 (%d 元素)" % (algo, len(data)), r["sorted"] == sorted(data))
    r = divide_sort.build_steps([5, 3, 8, 1, 9, 2], "quick")
    check("快排生成步骤", len(r["steps"]) > 0)
    check("快排末帧有序", r["steps"][-1]["list"] == sorted([5, 3, 8, 1, 9, 2]))
    r2 = divide_sort.build_steps([5, 3, 8, 1, 9, 2], "merge")
    check("归并末帧有序", r2["steps"][-1]["list"] == sorted([5, 3, 8, 1, 9, 2]))
    check("非法算法报错", _raises(lambda: divide_sort.build_steps([1, 2], "bad")))
    # 随机大数组
    import random
    rng = random.Random(7)
    big = [rng.randint(1, 100) for _ in range(60)]
    check("快排处理 60 元素", divide_sort.build_steps(big, "quick")["sorted"] == sorted(big))
    check("归并处理 60 元素", divide_sort.build_steps(big, "merge")["sorted"] == sorted(big))


def test_binary_search():
    print("\n[12/15] 二分查找 + 快速幂")
    arr = [1, 3, 5, 7, 9, 11, 13]
    for t in arr:
        r = binary_search.search(arr, t)
        check("找到 %d" % t, r["found"] == arr.index(t))
    r = binary_search.search(arr, 4)
    check("找不到时返回 -1", r["found"] == -1)
    check("比较次数不超过 log2(n)+1", r["comparisons"] <= 4)
    # 大数组边界
    big = list(range(1, 10001))
    r = binary_search.search(big, 10000)
    check("1 万元素找到末位", r["found"] == 9999)
    check("1 万元素比较次数 ≤ 15", r["comparisons"] <= 15)

    # 快速幂
    check("2^10 = 1024", fast_power.power(2, 10)["result"] == 1024)
    check("3^0 = 1", fast_power.power(3, 0)["result"] == 1)
    check("2^0 = 1", fast_power.power(2, 0)["result"] == 1)
    check("快速幂与内置一致", fast_power.power(7, 23)["result"] == 7 ** 23)
    check("模幂正确", fast_power.power(3, 100, 1000000007)["result"] == pow(3, 100, 1000000007))
    check("快速幂次数 = 二进制位数", fast_power.power(2, 1000)["fastOps"] == 10)
    check("负指数报错", _raises(lambda: fast_power.power(2, -1)))


def test_graph_bst_heap():
    print("\n[13/15] 图算法 + BST + 堆")
    g = graph_algo.sample_graph()
    for algo in graph_algo.SUPPORTED:
        r = graph_algo.run(g, 0, algo)
        check("%s 访问全部节点" % algo, r["visitedCount"] == g["n"])
        check("%s 起点第一个被访问" % algo, r["order"][0] == 0)
    # Dijkstra 最短距离正确性（对比 Floyd 暴力）
    r = graph_algo.run(g, 0, "dijkstra")
    import heapq
    INF = float("inf")
    dist = {i: INF for i in range(g["n"])}
    dist[0] = 0
    adj = {}
    for e in g["edges"]:
        adj.setdefault(e["u"], []).append((e["v"], e["w"]))
        adj.setdefault(e["v"], []).append((e["u"], e["w"]))
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    ok = all(int(r["dist"][str(k)]) == dist[k] for k in range(g["n"]) if dist[k] < INF)
    check("Dijkstra 距离与标准实现一致", ok)

    # BST
    r = bst.build([50, 30, 70, 20, 40, 60, 80])
    check("BST 中序遍历升序", r["inorder"] == sorted([50, 30, 70, 20, 40, 60, 80]))
    check("BST 节点数正确", r["count"] == 7)
    check("BST 高度合理", r["height"] == 3)
    s = bst.search([50, 30, 70, 20, 40], 40)
    check("BST 能找到存在的值", s["found"])
    s2 = bst.search([50, 30, 70], 99)
    check("BST 找不到不存在的值", not s2["found"])
    bal = bst.balanced_check(list(range(1, 16)))
    check("有序插入高度 = 15（退化）", bal["sortedInsert"]["height"] == 15)
    check("随机插入高度明显更小", bal["randomInsert"]["height"] < 10)
    # 中序必然有序（更大规模）
    rng_vals = [12, 4, 88, 31, 7, 55, 2, 99, 41]
    check("BST 中序始终升序", bst.build(rng_vals)["inorder"] == sorted(rng_vals))

    # 堆
    h = heap.demo([5, 2, 8, 1, 9, 3, 7], 3)
    check("堆顶是最小值", h["heapAfterPush"][0] == 1)
    check("弹出顺序升序", h["popped"] == [1, 2, 3])
    # 验证堆序性质
    def is_min_heap(arr):
        for i in range(len(arr)):
            l, r = 2 * i + 1, 2 * i + 2
            if l < len(arr) and arr[i] > arr[l]:
                return False
            if r < len(arr) and arr[i] > arr[r]:
                return False
        return True
    check("堆满足堆序性质", is_min_heap(h["heapAfterPush"]))
    check("堆排序结果正确", heap.heap_sort([5, 2, 8, 1, 9, 3])["sorted"] == [1, 2, 3, 5, 8, 9])
    import random as _r
    rr = _r.Random(3)
    vals = [_r.randint(1, 50) for _ in range(20)]
    check("堆排序 20 元素正确", heap.heap_sort(vals)["sorted"] == sorted(vals))


def test_dp():
    print("\n[14/15] 动态规划（背包 / LCS）")
    r = knapsack.solve([2, 3, 4, 5], [3, 4, 5, 6], 8)
    check("背包样例最大价值 = 10", r["maxValue"] == 10)
    # 与暴力枚举对比
    import itertools
    def brute(w, v, cap):
        best = 0
        n = len(w)
        for mask in range(1 << n):
            tw = tv = 0
            for i in range(n):
                if mask & (1 << i):
                    tw += w[i]; tv += v[i]
            if tw <= cap:
                best = max(best, tv)
        return best
    import random as _r2
    rr = _r2.Random(11)
    ok = True
    for _ in range(15):
        n = rr.randint(1, 6)
        w = [rr.randint(1, 6) for _ in range(n)]
        v = [rr.randint(1, 15) for _ in range(n)]
        cap = rr.randint(1, 15)
        if knapsack.solve(w, v, cap)["maxValue"] != brute(w, v, cap):
            ok = False
    check("背包与暴力枚举 15 组随机数据一致", ok)
    check("容量为 0 返回 0", knapsack.solve([1], [5], 0)["maxValue"] == 0)

    # LCS
    r = lcs.solve("ABCBDAB", "BDCABA")
    check("LCS 长度 = 4", r["length"] == 4)
    check("LCS 是公共子序列", _is_subseq(r["subsequence"], "ABCBDAB") and
          _is_subseq(r["subsequence"], "BDCABA"))
    check("LCS 相同串", lcs.solve("abc", "abc")["length"] == 3)
    check("LCS 无公共字符", lcs.solve("abc", "xyz")["length"] == 0)
    check("LCS 空串", lcs.solve("", "abc")["length"] == 0)
    # 与暴力 DP 对比
    def lcs_brute(a, b):
        n, m = len(a), len(b)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dp[i][j] = dp[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(dp[i-1][j], dp[i][j-1])
        return dp[n][m]
    rr3 = _r2.Random(5)
    ok2 = True
    for _ in range(10):
        a = "".join(rr3.choice("abc") for _ in range(rr3.randint(1, 8)))
        b = "".join(rr3.choice("abc") for _ in range(rr3.randint(1, 8)))
        if lcs.solve(a, b)["length"] != lcs_brute(a, b):
            ok2 = False
    check("LCS 与标准 DP 10 组数据一致", ok2)


def _is_subseq(sub, s):
    it = iter(s)
    return all(ch in it for ch in sub)


def test_number_theory():
    print("\n[15/15] 数论 + 工程算法 + 拓扑 + 滑窗")
    # 素数筛
    r = prime_sieve.sieve(100)
    check("100 内素数 25 个", r["primeCount"] == 25)
    check("素数列表前几项正确", r["primes"][:5] == [2, 3, 5, 7, 11])
    check("100 内无合数误判", not any(p in r["primes"] for p in (1, 4, 9, 25, 49, 91)))
    # 与暴力判定对比
    def is_prime(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True
    check("筛法与试除法结果一致", r["primes"] == [n for n in range(2, 101) if is_prime(n)])
    check("1000 内 168 个素数", prime_sieve.sieve(1000)["primeCount"] == 168)

    # 约瑟夫环：公式与模拟必须一致
    ok = True
    for n in (5, 10, 17, 50, 200, 500, 2000):
        for k in (2, 3, 7, 11):
            a = josephus.formula(n, k)["survivor"]
            b = josephus.simulate(n, k, collect_frames=False)["last"]
            if a != b:
                ok = False
    check("约瑟夫环：公式与模拟全部一致", ok)
    check("n=10,k=3 最后幸存者 = 4", josephus.formula(10, 3)["survivor"] == 4)
    check("出列顺序人数正确", len(josephus.simulate(10, 3)["order"]) == 10)
    check("n=100000 公式法可算", josephus.formula(100000, 3)["survivor"] > 0)

    # 一致性哈希
    keys = ["user:%d" % i for i in range(1, 41)]
    r = consistent_hash.distribute(keys, ["S1", "S2", "S3", "S4"], 3)
    check("所有 key 都被分配", sum(r["counts"].values()) == 40)
    check("环上有节点", len(r["ring"]) == 12)
    cmp = consistent_hash.compare_removal(keys, ["S1", "S2", "S3", "S4"], 3)
    check("一致性哈希迁移量 < 取模哈希",
          cmp["consistentHashing"]["moved"] < cmp["moduloHashing"]["moved"])
    check("一致性哈希迁移比例 < 50%", cmp["consistentHashing"]["ratio"] < 0.5)
    vc = consistent_hash.vnode_comparison(["S1", "S2", "S3", "S4"], keys)
    sds = [x["stddev"] for x in vc["table"]]
    check("虚拟节点越多越均衡", sds[0] >= sds[-1])

    # 拓扑排序
    dag = topo_sort.random_dag(7, 4, seed=1)
    r = topo_sort.kahn(dag)
    check("DAG 无环", not r["hasCycle"])
    check("拓扑序含全部节点", len(r["order"]) == 7)
    # 验证拓扑序合法性：每条边的 u 都在 v 之前
    pos = {node: i for i, node in enumerate(r["order"])}
    ok_topo = all(pos[e["u"]] < pos[e["v"]] for e in dag["edges"])
    check("拓扑序满足所有依赖关系", ok_topo)
    cyc = topo_sort.cyclic_example()
    check("有环图被正确检测", cyc["result"]["hasCycle"])
    r2 = topo_sort.dfs_topo(dag)
    pos2 = {node: i for i, node in enumerate(r2["order"])}
    check("DFS 拓扑序也合法",
          all(pos2[e["u"]] < pos2[e["v"]] for e in dag["edges"]))

    # 滑动窗口
    r = sliding_window.fixed_window([2, 1, 5, 1, 3, 2], 3)
    check("定长窗口最大和 = 9", r["maxSum"] == 9)
    r = sliding_window.min_length_window([2, 3, 1, 2, 4, 3], 7)
    check("最短子数组长度 = 2", r["minLength"] == 2)
    r = sliding_window.longest_unique_substring("abcabcbb")
    check("最长无重复子串 = 'abc'", r["substring"] == "abc" and r["length"] == 3)
    check("全相同字符串", sliding_window.longest_unique_substring("bbbbb")["length"] == 1)
    check("全不同字符串", sliding_window.longest_unique_substring("abcdef")["length"] == 6)
    # 定长窗口与暴力对比
    import random as _r3
    rr = _r3.Random(9)
    okf = True
    for _ in range(10):
        n = rr.randint(3, 15)
        arr = [rr.randint(1, 20) for _ in range(n)]
        k = rr.randint(1, n)
        bf = max(sum(arr[i:i+k]) for i in range(n - k + 1))
        if sliding_window.fixed_window(arr, k)["maxSum"] != bf:
            okf = False
    check("定长窗口与暴力 10 组一致", okf)


def _raises(fn):
    try:
        fn()
        return False
    except Exception:
        return True


def test_catalog():
    print("\n[16/16] 目录与集成")
    check("算法目录共 25 项", len(CATALOG) == 25)
    pages = set(x["page"] for x in CATALOG)
    check("目录中页面名唯一", len(pages) == len(CATALOG))
    # 每个目录项对应的页面文件应存在
    import os
    pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
    missing = [x["page"] for x in CATALOG
               if not os.path.isfile(os.path.join(pages_dir, x["page"]))]
    check("所有目录项都有对应页面文件: %s" % (missing or "无缺失"), not missing)
    # 每项必备字段
    need = ("id", "page", "title", "desc", "category", "order")
    bad = [x.get("id") for x in CATALOG if any(k not in x for k in need)]
    check("目录项字段完整: %s" % (bad or "全部完整"), not bad)
    cats = set(x["category"] for x in CATALOG)
    check("分类数量 ≥ 6 个", len(cats) >= 6)
    orders = [x["order"] for x in CATALOG]
    check("order 序号唯一", len(set(orders)) == len(orders))


def test_problems():
    print("\n[17/18] LeetCode 题库数据层")
    from server.data import (PROBLEMS, BY_SLUG, categories, all_tags,
                             stats, by_visualizer, to_summary, get)
    from server.services import problem_service

    check("题库至少 60 题", len(PROBLEMS) >= 60)
    check("slug 唯一", len(BY_SLUG) == len(PROBLEMS))
    check("LeetCode 题号唯一", len(set(p["lcId"] for p in PROBLEMS)) == len(PROBLEMS))
    check("题目都有标题", all(p["title"] for p in PROBLEMS))
    check("题目都有描述", all(p.get("desc") for p in PROBLEMS))
    check("题目都有示例", all(p.get("examples") for p in PROBLEMS))
    check("题目都有解法", all(p.get("solutions") for p in PROBLEMS))
    check("题目都有测试用例", all(p.get("testCases") for p in PROBLEMS))
    check("题目都有函数名", all(p.get("funcName") for p in PROBLEMS))

    # 每道题至少 1 个测试用例，且用例含 args/expect
    case_bad = []
    for p in PROBLEMS:
        if not p["testCases"]:
            case_bad.append(p["slug"])
            continue
        for c in p["testCases"]:
            if "args" not in c or "expect" not in c:
                case_bad.append(p["slug"])
    check("测试用例格式完整: %s" % (case_bad[:3] or "全部完整"), not case_bad)

    # 每个分类至少 2 道题（避免分类过碎）
    from server.data import categories as _cats
    thin = [c["name"] for c in _cats() if c["count"] < 2]
    check("没有过于单薄的分类: %s" % (thin or "无"), not thin)

    # 难度分布合理：三种难度都有
    diffs_present = set(p["difficulty"] for p in PROBLEMS)
    check("三种难度都有题目", diffs_present == {"简单", "中等", "困难"})

    # 字段完整性
    need = ("slug", "lcId", "title", "difficulty", "tags", "category",
            "desc", "solutions", "funcName", "testCases")
    bad = [p.get("slug") for p in PROBLEMS if any(k not in p for k in need)]
    check("题目字段完整: %s" % (bad or "全部完整"), not bad)

    # 难度取值合法
    diffs = set(p["difficulty"] for p in PROBLEMS)
    check("难度取值合法", diffs <= {"简单", "中等", "困难"})

    # 解法字段完整
    sol_bad = []
    for p in PROBLEMS:
        for s in p["solutions"]:
            if not all(k in s for k in ("name", "time", "space", "idea", "code")):
                sol_bad.append(p["slug"])
    check("解法字段完整: %s" % (sol_bad or "全部完整"), not sol_bad)

    # 关联可视化页必须真实存在
    import os
    pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
    vis_bad = []
    for p in PROBLEMS:
        v = p.get("visualizer")
        if v and not os.path.isfile(os.path.join(pages_dir, v)):
            vis_bad.append("%s -> %s" % (p["slug"], v))
    check("关联的可视化页都存在: %s" % (vis_bad or "全部存在"), not vis_bad)

    st = stats()
    check("统计：总数一致", st["total"] == len(PROBLEMS))
    check("统计：难度之和 = 总数",
          sum(st["byDifficulty"].values()) == len(PROBLEMS))
    check("统计：分类之和 = 总数",
          sum(c["count"] for c in st["byCategory"]) == len(PROBLEMS))
    check("有题目关联了可视化", st["withVisualizer"] > 0)

    check("分类列表非空", len(categories()) > 0)
    check("标签列表非空", len(all_tags()) > 0)
    check("按可视化页反查可用", len(by_visualizer("nqueens.html")) >= 1)
    check("摘要不含完整解法代码", "solutions" not in to_summary(PROBLEMS[0]))

    # 服务层筛选
    r = problem_service.list_problems()
    check("服务层返回全部题目", r["total"] == len(PROBLEMS))
    r = problem_service.list_problems(difficulty="简单")
    check("按难度筛选有效", all(i["difficulty"] == "简单" for i in r["items"]))
    r = problem_service.list_problems(category="动态规划")
    check("按分类筛选有效", r["total"] > 0 and
          all(i["category"] == "动态规划" for i in r["items"]))
    r = problem_service.list_problems(tag="双指针")
    check("按标签筛选有效", r["total"] > 0 and
          all("双指针" in i["tags"] for i in r["items"]))
    r = problem_service.list_problems(keyword="两数之和")
    check("关键词搜索有效", r["total"] >= 1)
    r = problem_service.list_problems(limit=5)
    check("limit 生效", len(r["items"]) == 5 and r["total"] == len(PROBLEMS))
    r = problem_service.list_problems(offset=5, limit=3)
    check("offset 生效", len(r["items"]) == 3)

    # 详情
    d = problem_service.get_problem("two-sum")
    check("详情含完整字段", d["slug"] == "two-sum" and d["solutions"])
    check("详情含关联可视化信息", d["relatedVisualizer"] is not None)
    check("不存在的题目报错", _raises(lambda: problem_service.get_problem("no-such")))

    # 反查
    r = problem_service.related_problems("nqueens.html")
    check("反查关联题目有效", r["total"] >= 1)
    hint = problem_service.search_hint("two")
    check("搜索联想有效（匹配 slug）", len(hint["items"]) >= 1)


def test_judge():
    print("\n[18/18] 判题器")
    from server.algo import judge
    from server.data import PROBLEMS, BY_SLUG
    from server.services import problem_service

    # 自测
    st = judge.self_test()
    check("判题器自测通过", st["ok"])

    # 关键：所有参考答案都必须通过自己的测试用例
    total_sol = 0
    failed = []
    for p in PROBLEMS:
        for s in p["solutions"]:
            total_sol += 1
            res = judge.run_code(s["code"], p["funcName"], p["testCases"])
            if not res["ok"]:
                failed.append("%s/%s" % (p["slug"], s["name"]))
    check("全部 %d 个参考答案都通过测试: %s" % (total_sol, failed[:3] or "无失败"),
          not failed)

    # 判题正确性
    bad = judge.run_code("def two_sum(nums, target):\n    return [9, 9]\n",
                         "two_sum", BY_SLUG["two-sum"]["testCases"])
    check("错误答案被判为不通过", not bad["ok"] and bad["passed"] == 0)

    good = judge.run_code(BY_SLUG["two-sum"]["solutions"][0]["code"],
                          "two_sum", BY_SLUG["two-sum"]["testCases"])
    check("正确答案被判为通过", good["ok"] and good["passed"] == good["total"])

    # 安全防护
    check("空代码被拒绝", judge.run_code("", "f", [])["error"] is not None)
    check("超长代码被拒绝",
          judge.run_code("x=1\n" * 5000, "f", [])["error"] is not None)
    check("未定义函数被拒绝", judge.run_code("x = 1\n", "f", [])["error"] is not None)
    check("import os 被拒绝",
          judge.run_code("import os\ndef f():\n    return 1\n", "f", [])["error"] is not None)
    check("import socket 被拒绝",
          judge.run_code("import socket\ndef f():\n    return 1\n", "f", [])["error"] is not None)
    check("open() 被拒绝",
          judge.run_code('def f():\n    return open("x").read()\n', "f", [])["error"] is not None)
    check("eval 被拒绝",
          judge.run_code('def f():\n    return eval("1")\n', "f", [])["error"] is not None)
    check("危险 import 写法被拒绝",
          judge.run_code('def f():\n    return __import__("os")\n', "f", [])["error"] is not None)

    # 允许的模块应可用
    ok_mod = judge.run_code(
        "import heapq\ndef f(a):\n    heapq.heapify(a)\n    return a[0]\n",
        "f", [{"args": [[3, 1, 2]], "expect": 1}])
    check("允许的模块 heapq 可用", ok_mod["ok"])
    ok_mod2 = judge.run_code(
        "from collections import deque\ndef f(a):\n    q = deque(a)\n    return q.popleft()\n",
        "f", [{"args": [[5, 6]], "expect": 5}])
    check("允许的模块 collections 可用", ok_mod2["ok"])

    # 异常隔离
    ex = judge.run_code("def f(a):\n    return a[0]\n", "f",
                        [{"args": [[]], "expect": 1}])
    check("运行时异常被捕获并标记失败",
          not ex["ok"] and ex["results"][0]["passed"] is False)
    check("异常用例含错误信息", "error" in ex["results"][0])

    # 部分通过
    part = judge.run_code("def f(a):\n    return a[0]\n", "f", [
        {"args": [[7]], "expect": 7},
        {"args": [[8]], "expect": 9},
    ])
    check("部分通过判定正确", part["passed"] == 1 and part["total"] == 2)

    # 服务层一键参考答案
    r = problem_service.run_solution("n-queens", "", use_reference=True)
    check("一键运行参考答案通过", r["ok"])
    check("不存在的题目判题报错",
          _raises(lambda: problem_service.run_solution("no-such", "x = 1")))


if __name__ == "__main__":
    print("=" * 60)
    print("  Algo Playground 自检")
    print("=" * 60)
    try:
        test_sorting()
        test_exponential()
        test_fib()
        test_genetic()
        test_services()
        test_life()
        test_hanoi()
        test_nqueens()
        test_montecarlo()
        test_divide_sort()
        test_binary_search()
        test_graph_bst_heap()
        test_dp()
        test_number_theory()
        test_catalog()
        test_problems()
        test_judge()
    except AssertionError as e:
        print("\n❌ 自检失败：%s" % e)
        sys.exit(1)
    except Exception as e:
        print("\n❌ 自检异常：%r" % e)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  ALL PASS ✅  共 %d 项检查全部通过" % len(PASSED))
    print("=" * 60)
