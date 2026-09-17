# -*- coding: utf-8 -*-
"""路由层：拓扑排序。"""
from flask import Blueprint, request, jsonify

from ..services import topo_sort_service

topo_sort_bp = Blueprint("topo_sort", __name__)


@topo_sort_bp.post("/run")
def run():
    b = request.get_json(silent=True) or {}
    return jsonify(topo_sort_service.run(
        b.get("graph"), b.get("algo", "kahn"),
        b.get("new_graph", False), b.get("n"), b.get("seed")))


@topo_sort_bp.get("/cyclic")
def cyclic():
    return jsonify(topo_sort_service.cyclic())
