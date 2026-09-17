# -*- coding: utf-8 -*-
"""路由层：蚁群算法。"""
from flask import Blueprint, request, jsonify

from ..services import aco_service

aco_bp = Blueprint("aco", __name__)


@aco_bp.post("/run")
def run():
    """运行。body: {cities, ants, iterations, seed, new_cities, count}"""
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(aco_service.run(
            b.get("cities"), b.get("ants"), b.get("iterations"),
            b.get("seed"), b.get("new_cities"), b.get("count")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
