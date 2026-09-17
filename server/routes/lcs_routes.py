# -*- coding: utf-8 -*-
"""路由层：最长公共子序列。"""
from flask import Blueprint, request, jsonify

from ..services import lcs_service

lcs_bp = Blueprint("lcs", __name__)


@lcs_bp.post("/solve")
def solve():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(lcs_service.solve(b.get("a"), b.get("b")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@lcs_bp.get("/default")
def default_case():
    return jsonify(lcs_service.default_case())
