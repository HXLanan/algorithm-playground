# -*- coding: utf-8 -*-
"""服务层：一致性哈希。"""
from typing import Dict, Any

from ..algo import consistent_hash


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clean_servers(servers):
    if not servers or not isinstance(servers, (list, tuple)):
        return ["S1", "S2", "S3", "S4"]
    out = [str(s)[:16] for s in servers[:12]]
    return out or ["S1", "S2", "S3", "S4"]


def distribute(servers=None, keys=None, vnodes=None, key_count=None) -> Dict[str, Any]:
    srv = _clean_servers(servers)
    vn = min(200, max(1, _to_int(vnodes, 3)))

    if not keys:
        cnt = min(200, max(5, _to_int(key_count, 40)))
        keys = ["user:%d" % i for i in range(1, cnt + 1)]
    else:
        keys = [str(k)[:32] for k in keys[:200]]

    res = consistent_hash.distribute(keys, srv, vn)
    res["vnodeComparison"] = consistent_hash.vnode_comparison(srv, keys)
    return res


def compare_removal(servers=None, keys=None, vnodes=None, key_count=None) -> Dict[str, Any]:
    srv = _clean_servers(servers)
    vn = min(200, max(1, _to_int(vnodes, 3)))
    if not keys:
        cnt = min(200, max(5, _to_int(key_count, 40)))
        keys = ["user:%d" % i for i in range(1, cnt + 1)]
    else:
        keys = [str(k)[:32] for k in keys[:200]]
    return consistent_hash.compare_removal(keys, srv, vn)


def default_case() -> Dict[str, Any]:
    return consistent_hash.default_case()
