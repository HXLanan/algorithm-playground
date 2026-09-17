# -*- coding: utf-8 -*-
"""路由层：0-1 背包。"""
from flask import Blueprint, request, jsonify

from ..services import knapsack_service

knapsack_bp = Blueprint("knapsack", __name__)


@knapsack_bp.post("/solve")
def solve():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(knapsack_service.solve(
            b.get("weights"), b.get("values"), b.get("capacity")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@knapsack_bp.get("/random")
def random_case():
    from flask import request as rq
    return jsonify(knapsack_service.random_case(
        rq.args.get("n", type=int), rq.args.get("seed", type=int)))


@knapsack_bp.get("/default")
def default_case():
    return jsonify(knapsack_service.default_case())
