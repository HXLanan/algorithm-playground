# -*- coding: utf-8 -*-
"""服务层：LeetCode 题库。

职责：筛选、搜索、排序、判题编排。数据来自 `server.data`。
"""
from typing import Dict, Any, List, Optional

from ..data import (PROBLEMS, BY_SLUG, all_problems, get, categories,
                    all_tags, stats, by_visualizer, to_summary)
from ..algo import judge


def list_problems(category: Optional[str] = None,
                  difficulty: Optional[str] = None,
                  tag: Optional[str] = None,
                  keyword: Optional[str] = None,
                  visualizer: Optional[str] = None,
                  limit: Optional[int] = None,
                  offset: int = 0,
                  with_detail: bool = False) -> Dict[str, Any]:
    """按条件筛选题目列表。

    返回摘要列表（不含大段代码），便于前端渲染。
    """
    items = list(all_problems())

    if category:
        items = [p for p in items if p["category"] == category]
    if difficulty:
        items = [p for p in items if p["difficulty"] == difficulty]
    if tag:
        items = [p for p in items if tag in p.get("tags", [])]
    if visualizer:
        items = [p for p in items if p.get("visualizer") == visualizer]
    if keyword:
        kw = keyword.strip().lower()
        if kw:
            def match(p):
                hay = (p["title"] + " " + p.get("desc", "") + " " +
                       " ".join(p.get("tags", [])) + " " + str(p.get("lcId", "")))
                return kw in hay.lower()
            items = [p for p in items if match(p)]

    total = len(items)
    start = max(0, int(offset or 0))
    if limit is not None:
        items = items[start:start + max(1, int(limit))]
    elif start:
        items = items[start:]

    return {
        "items": [to_summary(p) for p in items],
        "total": total,
        "returned": len(items),
        "filters": {"category": category, "difficulty": difficulty,
                    "tag": tag, "keyword": keyword, "visualizer": visualizer},
    }


def get_problem(slug: str) -> Dict[str, Any]:
    """获取题目详情（含描述、示例、解法）。"""
    p = get(slug)
    if not p:
        raise ValueError("题目不存在：%s" % slug)
    # 不直接回传内部测试用例的答案细节没关系（本地学习工具），但摘要一下
    return {
        "slug": p["slug"],
        "lcId": p["lcId"],
        "title": p["title"],
        "difficulty": p["difficulty"],
        "tags": p.get("tags", []),
        "category": p["category"],
        "visualizer": p.get("visualizer"),
        "visHint": p.get("visHint"),
        "desc": p.get("desc", ""),
        "examples": p.get("examples", []),
        "hints": p.get("hints", []),
        "funcName": p["funcName"],
        "solutions": p.get("solutions", []),
        "testCases": p.get("testCases", []),
        "relatedVisualizer": _visualizer_info(p.get("visualizer")),
    }


def _visualizer_info(page: Optional[str]) -> Optional[Dict[str, Any]]:
    """把可视化页文件名转成可展示的信息。"""
    if not page:
        return None
    from ..catalog import CATALOG
    for item in CATALOG:
        if item["page"] == page:
            return {"page": page, "title": item["title"],
                    "icon": item.get("icon", ""), "subtitle": item.get("subtitle", "")}
    return {"page": page, "title": page, "icon": "🧩", "subtitle": ""}


def meta() -> Dict[str, Any]:
    """题库元信息：分类、标签、难度、统计。"""
    return {
        "categories": categories(),
        "tags": all_tags(),
        "difficulties": ["简单", "中等", "困难"],
        "stats": stats(),
    }


def run_solution(slug: str, code: str, use_reference: bool = False) -> Dict[str, Any]:
    """判题：运行用户提交的代码。

    use_reference=True 时改为运行参考答案（用于"一键看答案通过"演示）。
    """
    p = get(slug)
    if not p:
        raise ValueError("题目不存在：%s" % slug)

    if use_reference:
        if not p.get("solutions"):
            raise ValueError("该题没有参考答案")
        code = p["solutions"][0]["code"]

    res = judge.run_code(code, p["funcName"], p.get("testCases", []))
    res["slug"] = slug
    res["title"] = p["title"]
    return res


def related_problems(visualizer: str, limit: int = 8) -> Dict[str, Any]:
    """反查：某个可视化页关联的题目。"""
    items = by_visualizer(visualizer)
    return {
        "visualizer": visualizer,
        "items": [to_summary(p) for p in items[:limit]],
        "total": len(items),
    }


def search_hint(keyword: str, limit: int = 6) -> Dict[str, Any]:
    """给搜索框用的轻量联想（匹配标题、题号、slug、标签）。"""
    kw = (keyword or "").strip().lower()
    if not kw:
        return {"items": [], "keyword": keyword}
    out = []
    for p in PROBLEMS:
        hay = " ".join([p["title"], str(p["lcId"]), p["slug"],
                        " ".join(p.get("tags", []))]).lower()
        if kw in hay:
            out.append({"slug": p["slug"], "lcId": p["lcId"],
                        "title": p["title"], "difficulty": p["difficulty"]})
        if len(out) >= limit:
            break
    return {"items": out, "keyword": keyword}
