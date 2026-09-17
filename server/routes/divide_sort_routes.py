# -*- coding: utf-8 -*-
"""路由层：分治排序（快速/归并）。"""
from flask import Blueprint, request, jsonify

from ..services import divide_sort_service

divide_sort_bp = Blueprint("divide_sort", __name__)


@divide_sort_bp.post("/random")
def random_array():
    body = request.get_json(silent=True) or {}
    return jsonify(divide_sort_service.make_random(body.get("n")))


@divide_sort_bp.post("/run")
def run():
    body = request.get_json(silent=True) or {}
    try:
        return jsonify(divide_sort_service.run(body.get("array"), body.get("algo", "quick")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
