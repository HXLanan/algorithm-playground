# -*- coding: utf-8 -*-
"""路由层：排序相关接口。"""
from flask import Blueprint, request, jsonify

from ..services import sort_service

sort_bp = Blueprint("sort", __name__)


@sort_bp.get("/algorithms")
def algorithms():
    """列出支持的排序算法。"""
    return jsonify(sort_service.list_algorithms())


@sort_bp.post("/random")
def random_array():
    """生成随机数组。body: {n}"""
    body = request.get_json(silent=True) or {}
    return jsonify(sort_service.make_random(body.get("n")))


@sort_bp.post("/run")
def run():
    """生成排序步骤序列。body: {array, algo}"""
    body = request.get_json(silent=True) or {}
    try:
        result = sort_service.run_sort(body.get("array"), body.get("algo", "bubble"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(result)
