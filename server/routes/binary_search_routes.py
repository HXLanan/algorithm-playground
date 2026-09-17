# -*- coding: utf-8 -*-
"""路由层：二分查找。"""
from flask import Blueprint, request, jsonify

from ..services import binary_search_service

binary_search_bp = Blueprint("binary_search", __name__)


@binary_search_bp.post("/search")
def search():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(binary_search_service.search(
            b.get("nums"), b.get("target"), b.get("size"), b.get("seed")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@binary_search_bp.post("/lower_bound")
def lower_bound():
    b = request.get_json(silent=True) or {}
    return jsonify(binary_search_service.lower_bound(b.get("nums"), b.get("target")))
