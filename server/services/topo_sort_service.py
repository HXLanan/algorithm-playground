# -*- coding: utf-8 -*-
"""服务层：拓扑排序。"""
from typing import Dict, Any

from ..algo import topo_sort


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_graph(graph):
    if not graph or not isinstance(graph, dict):
        return None
    try:
        n = int(graph.get("n", 0))
    except (TypeError, ValueError):
        return None
    if n < 3 or n > 16:
        return None
    edges = []
    for e in graph.get("edges") or []:
        try:
            u, v = int(e["u"]), int(e["v"])
        except (TypeError, ValueError, KeyError):
            return None
        if 0 <= u < n and 0 <= v < n and u != v:
            edges.append({"u": u, "v": v})
    if not edges:
        return None
    pos = graph.get("pos")
    if not pos or len(pos) != n:
        pos = [[round(0.08 + 0.84 * i / max(1, n - 1), 4),
                round(0.15 + 0.7 * ((i * 7) % 5) / 4.0, 4)] for i in range(n)]
    return {"n": n, "pos": pos, "edges": edges}


def run(graph=None, algo="kahn", new_graph=False, n=None, seed=None):
    g = _clean_graph(graph)
    if g is None or new_graph:
        size = min(16, max(3, _to_int(n, 7)))
        g = topo_sort.random_dag(size, 4, _to_int(seed, None))
    return topo_sort.run(g, algo)


def cyclic() -> Dict[str, Any]:
    return topo_sort.cyclic_example()
