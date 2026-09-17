# -*- coding: utf-8 -*-
"""路由层：堆与优先队列。"""
from flask import Blueprint, request, jsonify

from ..services import heap_service

heap_bp = Blueprint("heap", __name__)


@heap_bp.post("/demo")
def demo():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(heap_service.demo(b.get("values"), b.get("pops")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@heap_bp.post("/sort")
def sort():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(heap_service.sort(b.get("values")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
