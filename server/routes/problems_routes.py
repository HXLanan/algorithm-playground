# -*- coding: utf-8 -*-
"""路由层：LeetCode 题库。"""
from flask import Blueprint, request, jsonify

from ..services import problem_service

problems_bp = Blueprint("problems", __name__)


@problems_bp.get("/list")
def list_problems():
    """题目列表（支持筛选）。

    query: ?category=&difficulty=&tag=&keyword=&visualizer=&limit=&offset=
    """
    a = request.args
    return jsonify(problem_service.list_problems(
        category=a.get("category") or None,
        difficulty=a.get("difficulty") or None,
        tag=a.get("tag") or None,
        keyword=a.get("keyword") or None,
        visualizer=a.get("visualizer") or None,
        limit=a.get("limit", type=int),
        offset=a.get("offset", type=int) or 0,
    ))


@problems_bp.get("/meta")
def meta():
    """题库元信息：分类、标签、难度、统计。"""
    return jsonify(problem_service.meta())


@problems_bp.get("/related")
def related():
    """反查某个可视化页关联的题目。query: ?visualizer=sort.html"""
    page = request.args.get("visualizer", "")
    limit = request.args.get("limit", default=8, type=int)
    if not page:
        return jsonify({"error": "缺少 visualizer 参数"}), 400
    return jsonify(problem_service.related_problems(page, limit))


@problems_bp.get("/hint")
def hint():
    """搜索联想。query: ?q=two"""
    return jsonify(problem_service.search_hint(request.args.get("q", "")))


@problems_bp.get("/<slug>")
def detail(slug):
    """题目详情。"""
    try:
        return jsonify(problem_service.get_problem(slug))
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@problems_bp.post("/<slug>/run")
def run(slug):
    """判题。body: {code, useReference}"""
    body = request.get_json(silent=True) or {}
    try:
        return jsonify(problem_service.run_solution(
            slug, body.get("code", ""), bool(body.get("useReference"))))
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
