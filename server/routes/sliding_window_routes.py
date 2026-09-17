# -*- coding: utf-8 -*-
"""路由层：滑动窗口。"""
from flask import Blueprint, request, jsonify

from ..services import sliding_window_service

sliding_window_bp = Blueprint("sliding_window", __name__)


@sliding_window_bp.post("/fixed")
def fixed():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(sliding_window_service.fixed(b.get("nums"), b.get("k")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@sliding_window_bp.post("/min")
def min_window():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(sliding_window_service.min_window(b.get("nums"), b.get("target")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@sliding_window_bp.post("/longest")
def longest():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(sliding_window_service.longest(b.get("text")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@sliding_window_bp.get("/default")
def default_case():
    return jsonify(sliding_window_service.default_case())
