# -*- coding: utf-8 -*-
"""服务层：图算法（Dijkstra / BFS / DFS）。"""
from typing import Dict, Any, Optional

from ..algo import graph_algo


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_graph(graph):
    """校验并清洗前端传来的图结构。"""
    if not graph or not isinstance(graph, dict):
        return None
    try:
        n = int(graph.get("n", 0))
    except (TypeError, ValueError):
        return None
    if n < 3 or n > 20:
        return None
    edges = []
    for e in graph.get("edges") or []:
        try:
            u, v, w = int(e["u"]), int(e["v"]), int(e.get("w", 1))
        except (TypeError, ValueError, KeyError):
            return None
        if 0 <= u < n and 0 <= v < n and u != v and w > 0:
            edges.append({"u": u, "v": v, "w": w})
    if not edges:
        return None
    pos = graph.get("pos")
    if not pos or len(pos) != n:
        import math
        pos = []
        for i in range(n):
            a = 2 * math.pi * i / n
            pos.append([round(0.5 + 0.38 * math.cos(a), 4),
                        round(0.5 + 0.38 * math.sin(a), 4)])
    return {"n": n, "nodes": list(range(n)), "pos": pos, "edges": edges,
            "weighted": bool(graph.get("weighted", True))}


def run(graph=None, start=None, algo="dijkstra", new_graph=False,
        n=None, seed=None) -> Dict[str, Any]:
    g = _clean_graph(graph)
    if g is None or new_graph:
        size = min(20, max(3, _to_int(n, 8)))
        g = graph_algo.random_graph(size, size, _to_int(seed, None))
    s = _to_int(start, 0)
    if s < 0 or s >= g["n"]:
        s = 0
    return graph_algo.run(g, s, algo)


def compare(graph=None, start=None) -> Dict[str, Any]:
    g = _clean_graph(graph) or graph_algo.sample_graph()
    return graph_algo.compare(g, _to_int(start, 0))
