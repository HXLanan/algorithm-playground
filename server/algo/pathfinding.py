# -*- coding: utf-8 -*-
"""核心算法模块：A* 寻路。

在网格地图上从起点走到终点，A* 用启发式函数（到终点的估计距离）
引导搜索方向，比 BFS/Dijkstra 探索更少的格子。

支持对比 A* / Dijkstra / BFS / DFS 四种策略的搜索过程。
"""
import heapq
from collections import deque
from typing import List, Dict, Any, Optional, Tuple

SUPPORTED = ("astar", "dijkstra", "bfs", "dfs")
ALGO_NAMES = {
    "astar": "A* 启发式搜索",
    "dijkstra": "Dijkstra 最短路",
    "bfs": "广度优先 BFS",
    "dfs": "深度优先 DFS",
}
MAX_DIM = 60


def make_grid(rows: int = 20, cols: int = 30, walls: Optional[List[List[int]]] = None,
              seed: Optional[int] = None, wall_ratio: float = 0.0) -> List[List[int]]:
    """生成网格。0=通路，1=墙。"""
    if walls is not None:
        return [[1 if v else 0 for v in row] for row in walls]
    import random
    rng = random.Random(seed)
    return [[1 if rng.random() < wall_ratio else 0 for _ in range(cols)]
            for _ in range(rows)]


def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """曼哈顿距离（四方向移动时是可采纳的启发式）。"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int],
           algo: str = "astar", allow_diagonal: bool = False,
           max_visited: int = 4000) -> Dict[str, Any]:
    """执行搜索，返回访问顺序与最终路径。"""
    if algo not in SUPPORTED:
        algo = "astar"
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if not rows or not cols:
        return _empty_result(algo)

    if allow_diagonal:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def ok(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0

    if not ok(*start) or not ok(*goal):
        return _empty_result(algo, "起点或终点不可通行")

    visited_order: List[List[int]] = []
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    found = False

    if algo in ("astar", "dijkstra"):
        dist = {start: 0.0}
        pq = [(0.0, start)]
        closed = set()
        while pq and len(visited_order) < max_visited:
            _, cur = heapq.heappop(pq)
            if cur in closed:
                continue
            closed.add(cur)
            visited_order.append([cur[0], cur[1]])
            if cur == goal:
                found = True
                break
            for dr, dc in dirs:
                nr, nc = cur[0] + dr, cur[1] + dc
                if not ok(nr, nc):
                    continue
                step = 1.4142 if (dr and dc) else 1.0
                nd = dist[cur] + step
                nxt = (nr, nc)
                if nd < dist.get(nxt, float("inf")):
                    dist[nxt] = nd
                    came_from[nxt] = cur
                    h = _heuristic(nxt, goal) if algo == "astar" else 0.0
                    heapq.heappush(pq, (nd + h, nxt))

    elif algo == "bfs":
        q = deque([start])
        seen = {start}
        while q and len(visited_order) < max_visited:
            cur = q.popleft()
            visited_order.append([cur[0], cur[1]])
            if cur == goal:
                found = True
                break
            for dr, dc in dirs:
                nr, nc = cur[0] + dr, cur[1] + dc
                nxt = (nr, nc)
                if ok(nr, nc) and nxt not in seen:
                    seen.add(nxt)
                    came_from[nxt] = cur
                    q.append(nxt)

    else:  # dfs
        st = [start]
        seen = {start}
        while st and len(visited_order) < max_visited:
            cur = st.pop()
            visited_order.append([cur[0], cur[1]])
            if cur == goal:
                found = True
                break
            for dr, dc in reversed(dirs):
                nr, nc = cur[0] + dr, cur[1] + dc
                nxt = (nr, nc)
                if ok(nr, nc) and nxt not in seen:
                    seen.add(nxt)
                    came_from[nxt] = cur
                    st.append(nxt)

    path: List[List[int]] = []
    if found:
        node: Optional[Tuple[int, int]] = goal
        while node is not None:
            path.append([node[0], node[1]])
            node = came_from.get(node)
        path.reverse()

    return {
        "algo": algo,
        "algoName": ALGO_NAMES[algo],
        "start": list(start),
        "goal": list(goal),
        "visited": visited_order,
        "path": path,
        "visitedCount": len(visited_order),
        "pathLength": len(path),
        "found": found,
        "wallCount": sum(sum(row) for row in grid),
        "gridSize": [rows, cols],
    }


def _empty_result(algo: str, msg: str = "无可行路径") -> Dict[str, Any]:
    return {
        "algo": algo,
        "algoName": ALGO_NAMES.get(algo, algo),
        "visited": [], "path": [], "visitedCount": 0,
        "pathLength": 0, "found": False, "message": msg,
    }


def compare(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Dict[str, Any]:
    """对比四种算法在同一张地图上的表现。"""
    out = {}
    for a in SUPPORTED:
        r = search(grid, start, goal, a)
        out[a] = {
            "name": ALGO_NAMES[a],
            "visitedCount": r["visitedCount"],
            "pathLength": r["pathLength"],
            "found": r["found"],
        }
    return {
        "comparison": out,
        "explain": "A* 靠启发式「盯着终点」搜，访问格子通常最少；Dijkstra 均匀外扩（圆形）；BFS 保证无权图最短但范围大；DFS 一头扎到底、路径往往不是最短。",
    }
