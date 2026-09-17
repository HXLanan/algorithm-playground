# -*- coding: utf-8 -*-
"""路由层：图算法。"""
from flask import Blueprint, request, jsonify

from ..services import graph_service

graph_bp = Blueprint("graph", __name__)


@graph_bp.post("/run")
def run():
    b = request.get_json(silent=True) or {}
    return jsonify(graph_service.run(
        b.get("graph"), b.get("start"), b.get("algo", "dijkstra"),
        b.get("new_graph", False), b.get("n"), b.get("seed")))


@graph_bp.post("/compare")
def compare():
    b = request.get_json(silent=True) or {}
    return jsonify(graph_service.compare(b.get("graph"), b.get("start")))
