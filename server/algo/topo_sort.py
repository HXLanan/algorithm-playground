# -*- coding: utf-8 -*-
"""核心算法模块：拓扑排序（有向无环图 DAG）。

用途：给有依赖关系的任务排出执行顺序。
例：课程先修关系、构建系统的编译顺序、包管理器依赖解析。

两种经典实现：
  · Kahn 算法：不断取"入度为 0"的节点（BFS 思想）
  · DFS 后序逆序：深度优先，完成顺序的逆序即为拓扑序

若图中存在环，则无拓扑序（报错）。
"""
from collections import deque
from typing import List, Dict, Any, Optional


def random_dag(n: int = 7, extra: int = 4, seed: Optional[int] = None) -> Dict[str, Any]:
    """生成随机 DAG：只在小编号指向大编号之间连边，天然无环。"""
    import random
    rng = random.Random(seed)
    if n < 3:
        n = 3
    if n > 16:
        n = 16

    pos = []
    for i in range(n):
        pos.append([round(0.08 + 0.84 * i / max(1, n - 1), 4),
                    round(0.15 + 0.7 * ((i * 7) % 5) / 4.0, 4)])

    edges = []
    seen = set()

    def add(u, v):
        if u >= v or (u, v) in seen:
            return
        seen.add((u, v))
        edges.append({"u": u, "v": v})

    for i in range(n - 1):
        add(i, i + 1)
    for _ in range(extra):
        a = rng.randrange(n)
        b = rng.randrange(n)
        add(min(a, b), max(a, b))

    return {"n": n, "pos": pos, "edges": edges}


def kahn(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Kahn 算法：基于入度的拓扑排序。"""
    n = graph["n"]
    indeg = [0] * n
    adj = [[] for _ in range(n)]
    for e in graph["edges"]:
        adj[e["u"]].append(e["v"])
        indeg[e["v"]] += 1

    steps: List[Dict[str, Any]] = []
    q = deque([i for i in range(n) if indeg[i] == 0])
    steps.append({
        "type": "init", "indeg": list(indeg), "queue": list(q), "order": [],
        "msg": "初始入度为 0 的节点入队：%s" % (list(q) or "无"),
    })

    order: List[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        removed = []
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
                removed.append(v)
        steps.append({
            "type": "process", "node": u, "indeg": list(indeg),
            "queue": list(q), "order": list(order), "newZero": removed,
            "msg": "取出 %d 加入拓扑序；其邻居入度 -1%s" % (
                u, ("，%s 入度归零入队" % removed) if removed else ""),
        })

    ok = len(order) == n
    return {
        "algorithm": "kahn",
        "algorithmName": "Kahn 算法（入度法）",
        "graph": graph,
        "order": order,
        "steps": steps,
        "hasCycle": not ok,
        "explain": "反复取出入度为 0 的节点，并把它指向的节点入度减 1。"
                   "如果最后没能取出全部节点，说明图里有环（任务互相依赖，无法排序）。",
    }


def dfs_topo(graph: Dict[str, Any]) -> Dict[str, Any]:
    """DFS 后序逆序求拓扑序。"""
    n = graph["n"]
    adj = [[] for _ in range(n)]
    for e in graph["edges"]:
        adj[e["u"]].append(e["v"])

    visited = [0] * n        # 0 未访问 1 访问中 2 已完成
    order: List[int] = []
    steps: List[Dict[str, Any]] = []
    has_cycle = {"v": False}

    def dfs(u: int) -> None:
        visited[u] = 1
        steps.append({"type": "enter", "node": u, "order": list(order),
                      "msg": "进入节点 %d" % u})
        for v in adj[u]:
            if visited[v] == 1:
                has_cycle["v"] = True
                steps.append({"type": "cycle", "node": v, "order": list(order),
                              "msg": "⚠️ 节点 %d 正在访问中又被遇到 → 存在环" % v})
            elif visited[v] == 0:
                dfs(v)
        visited[u] = 2
        order.append(u)
        steps.append({"type": "finish", "node": u, "order": list(order),
                      "msg": "节点 %d 完成，加入序列尾部" % u})

    for i in range(n):
        if visited[i] == 0:
            dfs(i)

    order.reverse()
    return {
        "algorithm": "dfs",
        "algorithmName": "DFS 后序逆序",
        "graph": graph,
        "order": order,
        "steps": steps,
        "hasCycle": has_cycle["v"],
        "explain": "深度优先遍历，节点「完成」时压入序列，最后整体反转。"
                   "直觉：一个任务必须等它依赖的所有任务都完成，才能排到前面。",
    }


def run(graph: Optional[Dict[str, Any]] = None, algo: str = "kahn") -> Dict[str, Any]:
    if not graph:
        graph = random_dag(7, 4, seed=2024)
    if algo == "dfs":
        return dfs_topo(graph)
    return kahn(graph)


def cyclic_example() -> Dict[str, Any]:
    """构造一个带环的图，用来说明"无解"的情况。"""
    g = {"n": 5, "pos": [[0.1, 0.5], [0.3, 0.2], [0.5, 0.7], [0.7, 0.3], [0.9, 0.5]],
         "edges": [{"u": 0, "v": 1}, {"u": 1, "v": 2}, {"u": 2, "v": 3},
                   {"u": 3, "v": 1}, {"u": 2, "v": 4}]}
    r = kahn(g)
    return {"graph": g, "result": r,
            "explain": "1→2→3→1 形成了环，这三个节点永远不会入度归零，"
                       "所以拓扑排序无法完成——这就是「循环依赖」检测。"}
