# -*- coding: utf-8 -*-
"""核心算法模块：一致性哈希（Consistent Hashing）。

问题：把数据分散到 N 台服务器上，普通做法是 hash(key) % N。
但一旦增删服务器，N 变化 → **几乎所有 key 的归属都要重新分配**（缓存雪崩）。

一致性哈希的解法：把哈希空间想象成一个**环**（0 ~ 2³²-1）。
  · 每台服务器按 hash(server) 放到环上
  · 每个 key 顺时针找到的第一台服务器就是它的归属
这样增删一台服务器，只影响环上相邻的一小段区间——大部分 key 不受影响。

再加"虚拟节点"：每台物理机映射成多个虚拟节点散布在环上，让负载更均匀。
"""
import hashlib
from typing import List, Dict, Any, Optional

RING_SIZE = 100000       # 哈希环大小（真实系统用 2³²，这里取 10 万以减少碰撞）


def _h(s: str) -> int:
    """把字符串哈希到环上的一个位置（0 ~ RING_SIZE-1）。"""
    digest = hashlib.md5(s.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % RING_SIZE


def _h_visual(s: str) -> int:
    """把哈希值映射到 0~359 的可视化角度上。"""
    return int(_h(s) * 360 / RING_SIZE) % 360


def build_ring(servers: List[str], vnodes: int = 1) -> List[Dict[str, Any]]:
    """把服务器（含虚拟节点）放到环上，按位置排序。"""
    ring = []
    for s in servers:
        for v in range(max(1, vnodes)):
            name = s if vnodes == 1 else "%s#%d" % (s, v)
            pos = _h(name)
            ring.append({"pos": pos, "angle360": int(pos * 360 / RING_SIZE) % 360,
                         "server": s, "vnode": name})
    ring.sort(key=lambda x: x["pos"])
    return ring


def locate(ring: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    """为 key 找到顺时针方向的第一台服务器。"""
    if not ring:
        return {"key": key, "pos": 0, "server": None}
    pos = _h(key)
    # 二分找第一个 >= pos 的节点（环形回绕）
    lo, hi = 0, len(ring) - 1
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if ring[mid]["pos"] >= pos:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    if lo > len(ring) - 1 and ring[-1]["pos"] < pos:
        ans = 0            # 回绕到环的起点
    node = ring[ans]
    return {"key": key, "pos": pos, "angle360": int(pos * 360 / RING_SIZE) % 360,
            "server": node["server"], "nodePos": node["pos"]}


def distribute(keys: List[str], servers: List[str],
               vnodes: int = 1) -> Dict[str, Any]:
    """把一批 key 分配到服务器上。"""
    ring = build_ring(servers, vnodes)
    assign: Dict[str, List[str]] = {s: [] for s in servers}
    details = []
    for k in keys:
        loc = locate(ring, k)
        if loc["server"]:
            assign[loc["server"]].append(k)
        details.append({"key": k, "pos": loc["pos"],
                        "server": loc["server"], "nodePos": loc.get("nodePos")})

    counts = {s: len(v) for s, v in assign.items()}
    return {
        "servers": servers,
        "vnodes": vnodes,
        "ring": ring,
        "assign": assign,
        "counts": counts,
        "details": details,
        "keyCount": len(keys),
        "explain": "每个 key 沿着环顺时针找第一台服务器。",
    }


def compare_removal(keys: List[str], servers: List[str],
                    vnodes: int = 1) -> Dict[str, Any]:
    """对比「移除一台服务器」时，一致性哈希 vs 取模哈希 的迁移量。"""
    srv = list(servers)
    before = distribute(keys, srv, vnodes)

    removed = srv[-1] if len(srv) > 1 else srv[0]
    after_servers = [s for s in srv if s != removed]
    after = distribute(keys, after_servers, vnodes)

    # 一致性哈希：统计归属发生变化的 key
    moved_ch = 0
    for k in keys:
        if before["details"][keys.index(k)]["server"] != \
           after["details"][keys.index(k)]["server"]:
            moved_ch += 1

    # 取模哈希：hash(key) % N
    def mod_assign(ss):
        m = {}
        for k in keys:
            m[k] = ss[_h(k) % len(ss)] if ss else None
        return m
    mod_before = mod_assign(srv)
    mod_after = mod_assign(after_servers)
    moved_mod = sum(1 for k in keys if mod_before[k] != mod_after[k])

    total = len(keys) or 1
    return {
        "removedServer": removed,
        "totalKeys": len(keys),
        "consistentHashing": {
            "moved": moved_ch,
            "ratio": round(moved_ch / total, 4),
        },
        "moduloHashing": {
            "moved": moved_mod,
            "ratio": round(moved_mod / total, 4),
        },
        "before": before,
        "after": after,
        "explain": "理想情况下，移除 1 台服务器应只影响 1/N 的数据。"
                   "一致性哈希接近这个理想值（只迁移相邻区间），"
                   "而取模哈希几乎会打乱全部数据——这就是它被广泛用于"
                   "分布式缓存（如 Redis Cluster）的原因。",
    }


def default_case() -> Dict[str, Any]:
    """默认演示数据。"""
    servers = ["S1", "S2", "S3", "S4"]
    keys = ["user:%d" % i for i in range(1, 41)]
    return {"servers": servers, "keys": keys, "vnodes": 3}


def vnode_comparison(servers: List[str], keys: List[str]) -> Dict[str, Any]:
    """对比虚拟节点数量对负载均衡的影响。"""
    out = []
    for vn in (1, 3, 10):
        r = distribute(keys, servers, vn)
        counts = list(r["counts"].values())
        if not counts:
            continue
        avg = sum(counts) / len(counts)
        mx, mn = max(counts), min(counts)
        # 标准差衡量均衡度
        var = sum((c - avg) ** 2 for c in counts) / len(counts)
        out.append({
            "vnodes": vn,
            "counts": r["counts"],
            "max": mx, "min": mn,
            "stddev": round(var ** 0.5, 2),
        })
    return {
        "table": out,
        "explain": "虚拟节点越多，服务器在环上分布越均匀，负载越平衡。"
                   "但节点太多也会增加查找开销，实际系统通常取 100~200 个虚拟节点。",
    }
