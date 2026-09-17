# -*- coding: utf-8 -*-
"""核心算法模块：图的最短路径与遍历。

· Dijkstra：带权图的单源最短路径（非负权），用优先队列每次取最近的未访问节点。
· BFS：无权图的最短路径（层序扩散）。
· DFS：深度优先遍历，一条路走到黑。

三者都在同一张图上演示，方便对比「扩散形状」的差异。
"""
import heapq
from collections import deque
from typing import List, Dict, Any, Optional, Tuple

SUPPORTED = ("dijkstra", "bfs", "dfs")
NAMES = {
    "dijkstra": "Dijkstra 最短路",
    "bfs": "广度优先 BFS",
    "dfs": "深度优先 DFS",
}


def random_graph(n: int = 8, extra_edges: int = 6,
                 seed: Optional[int] = None,
                 weighted: bool = True) -> Dict[str, Any]:
    """生成一个随机连通图。

    先用链保证连通，再随机加边。
    """
    import random
    rng = random.Random(seed)
    if n < 3:
        n = 3
    if n > 20:
        n = 20

    pos = []
    for i in range(n):
        angle = 2 * 3.141592653589793 * i / n
        pos.append([round(0.5 + 0.38 * _cos(angle), 4),
                    round(0.5 + 0.38 * _sin(angle), 4)])

    edges = []
    seen = set()

    def add(u, v):
        key = (min(u, v), max(u, v))
        if key in seen or u == v:
            return
        seen.add(key)
        w = rng.randint(1, 20) if weighted else 1
        edges.append({"u": u, "v": v, "w": w})

    for i in range(n - 1):
        add(i, i + 1)
    for _ in range(extra_edges):
        add(rng.randrange(n), rng.randrange(n))

    return {"n": n, "nodes": list(range(n)), "pos": pos, "edges": edges,
            "weighted": weighted}


def _cos(x):
    import math
    return math.cos(x)


def _sin(x):
    import math
    return math.sin(x)


def _adj(graph) -> List[List[Tuple[int, int]]]:
    """构造邻接表。"""
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(graph["n"])]
    for e in graph["edges"]:
        adj[e["u"]].append((e["v"], e["w"]))
        adj[e["v"]].append((e["u"], e["w"]))
    return adj


def run(graph: Dict[str, Any], start: int = 0, algo: str = "dijkstra") -> Dict[str, Any]:
    """在图上运行指定算法。"""
    if algo not in SUPPORTED:
        algo = "dijkstra"
    n = graph["n"]
    if start < 0 or start >= n:
        start = 0
    adj = _adj(graph)

    order: List[int] = []          # 访问顺序
    parent: Dict[int, Optional[int]] = {start: None}
    dist: Dict[int, float] = {start: 0}
    steps: List[Dict[str, Any]] = []

    if algo == "dijkstra":
        pq = [(0, start)]
        done = set()
        while pq:
            d, u = heapq.heappop(pq)
            if u in done:
                continue
            done.add(u)
            order.append(u)
            steps.append({
                "visit": u, "dist": d, "order": list(order),
                "msg": "取出距起点最近的节点 %d（距离 %d）" % (u, d),
            })
            for v, w in adj[u]:
                nd = d + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))
                    steps.append({
                        "visit": v, "dist": nd, "order": list(order),
                        "relax": [u, v],
                        "msg": "松弛边 %d→%d：找到更短距离 %d" % (u, v, nd),
                    })

    elif algo == "bfs":
        q = deque([start])
        seen = {start}
        dist[start] = 0
        while q:
            u = q.popleft()
            order.append(u)
            steps.append({
                "visit": u, "dist": dist.get(u, 0), "order": list(order),
                "msg": "出队节点 %d（第 %d 个访问）" % (u, len(order)),
            })
            for v, _w in adj[u]:
                if v not in seen:
                    seen.add(v)
                    parent[v] = u
                    dist[v] = dist[u] + 1
                    q.append(v)
                    steps.append({
                        "visit": v, "dist": dist[v], "order": list(order),
                        "relax": [u, v],
                        "msg": "发现新节点 %d，入队" % v,
                    })

    else:  # dfs
        st = [start]
        seen = set()
        while st:
            u = st.pop()
            if u in seen:
                continue
            seen.add(u)
            order.append(u)
            steps.append({
                "visit": u, "dist": len(order), "order": list(order),
                "msg": "访问节点 %d（第 %d 个）" % (u, len(order)),
            })
            for v, _w in adj[u]:
                if v not in seen:
                    parent.setdefault(v, u)
                    st.append(v)

    # 构造生成树（用于可视化高亮）
    tree = []
    for v, p in parent.items():
        if p is not None:
            tree.append([p, v])

    return {
        "algo": algo,
        "algoName": NAMES[algo],
        "graph": graph,
        "start": start,
        "order": order,
        "dist": {str(k): v for k, v in dist.items()},
        "parent": {str(k): v for k, v in parent.items()},
        "tree": tree,
        "steps": steps,
        "visitedCount": len(order),
        "explain": {
            "dijkstra": "每次取出「当前距离最小」的节点并松弛其邻居，保证非负权图上的最短路径。",
            "bfs": "按层扩散，无权图上第一次到达某点即为最短路径。",
            "dfs": "一路深入到底再回溯，不保证最短，但能快速遍历全图。",
        }[algo],
    }


def sample_graph() -> Dict[str, Any]:
    """返回一张固定的示例图，便于多次对比同一算法效果。"""
    return random_graph(8, 6, seed=2024)


def compare(graph: Optional[Dict[str, Any]] = None, start: int = 0) -> Dict[str, Any]:
    """在同一张图上对比三种算法。"""
    if not graph:
        graph = sample_graph()
    out = {}
    for a in SUPPORTED:
        r = run(graph, start, a)
        out[a] = {"name": r["algoName"], "visited": r["visitedCount"],
                  "order": r["order"]}
    return {"comparison": out, "graph": graph,
            "explain": "同一张图上：Dijkstra 按距离扩散、BFS 按层扩散、DFS 一条道走到黑。"}
