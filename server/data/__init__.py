# -*- coding: utf-8 -*-
"""题库数据层：汇总三道题单并提供查询接口。

纯数据模块，不含业务逻辑（筛选、排序等交给 service 层）。
"""
from typing import List, Dict, Any, Optional

from .problems_part1 import PART1
from .problems_part2 import PART2
from .problems_part3 import PART3
from .problems_part4 import PART4
from .problems_part5 import PART5
from .problems_part6 import PART6
from .problems_part7 import PART7

# 全部题目
PROBLEMS: List[Dict[str, Any]] = (PART1 + PART2 + PART3 + PART4
                                  + PART5 + PART6 + PART7)

# 按 slug 建索引
BY_SLUG: Dict[str, Dict[str, Any]] = {p["slug"]: p for p in PROBLEMS}

# 分类顺序（决定前端展示顺序）
CATEGORY_ORDER = [
    "数组与哈希",
    "双指针",
    "滑动窗口",
    "二分查找",
    "排序",
    "递归与回溯",
    "动态规划",
    "图与树",
    "栈与队列",
    "链表",
    "字符串",
    "贪心",
    "模拟与进阶",
]

DIFFICULTY_ORDER = ["简单", "中等", "困难"]


def all_problems() -> List[Dict[str, Any]]:
    return PROBLEMS


def get(slug: str) -> Optional[Dict[str, Any]]:
    return BY_SLUG.get(slug)


def categories() -> List[Dict[str, Any]]:
    """返回分类及其题目数量。"""
    counts: Dict[str, int] = {}
    for p in PROBLEMS:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    out = []
    for c in CATEGORY_ORDER:
        if c in counts:
            out.append({"name": c, "count": counts[c]})
    # 兜底：不在预设顺序里的分类
    for c, n in counts.items():
        if c not in CATEGORY_ORDER:
            out.append({"name": c, "count": n})
    return out


def all_tags() -> List[Dict[str, Any]]:
    """返回全部标签及使用频次（按频次降序）。"""
    counts: Dict[str, int] = {}
    for p in PROBLEMS:
        for t in p.get("tags", []):
            counts[t] = counts.get(t, 0) + 1
    items = [{"name": k, "count": v} for k, v in counts.items()]
    items.sort(key=lambda x: (-x["count"], x["name"]))
    return items


def stats() -> Dict[str, Any]:
    """题库统计信息。"""
    by_diff: Dict[str, int] = {}
    for p in PROBLEMS:
        d = p["difficulty"]
        by_diff[d] = by_diff.get(d, 0) + 1
    linked = sum(1 for p in PROBLEMS if p.get("visualizer"))
    return {
        "total": len(PROBLEMS),
        "byDifficulty": {d: by_diff.get(d, 0) for d in DIFFICULTY_ORDER},
        "byCategory": categories(),
        "withVisualizer": linked,
        "visualizerRate": round(linked / len(PROBLEMS), 3) if PROBLEMS else 0,
    }


def by_visualizer(page: str) -> List[Dict[str, Any]]:
    """反查：某个可视化页关联了哪些题目。"""
    return [p for p in PROBLEMS if p.get("visualizer") == page]


def to_summary(p: Dict[str, Any]) -> Dict[str, Any]:
    """把完整题目裁剪成列表页需要的摘要（避免传输大段代码）。"""
    return {
        "slug": p["slug"],
        "lcId": p["lcId"],
        "title": p["title"],
        "difficulty": p["difficulty"],
        "tags": p.get("tags", []),
        "category": p["category"],
        "visualizer": p.get("visualizer"),
        "visHint": p.get("visHint"),
        "solutionCount": len(p.get("solutions", [])),
        "descBrief": (p.get("desc", "")[:70] + "…") if len(p.get("desc", "")) > 70 else p.get("desc", ""),
    }
