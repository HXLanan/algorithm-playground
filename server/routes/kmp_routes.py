# -*- coding: utf-8 -*-
"""路由层：KMP 字符串匹配。"""
from flask import Blueprint, request, jsonify

from ..services import kmp_service

kmp_bp = Blueprint("kmp", __name__)


@kmp_bp.get("/demo")
def demo():
    return jsonify(kmp_service.demo())


@kmp_bp.post("/search")
def search():
    """匹配。body: {text, pattern}"""
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(kmp_service.search(b.get("text"), b.get("pattern")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
