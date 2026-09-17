# -*- coding: utf-8 -*-
"""路由层：遗传算法相关接口。"""
from flask import Blueprint, request, jsonify

from ..services import genetic_service

genetic_bp = Blueprint("genetic", __name__)


@genetic_bp.post("/evolve")
def evolve():
    """进化若干代。body: {population, pop_size, generations}"""
    body = request.get_json(silent=True) or {}
    return jsonify(genetic_service.evolve(
        population=body.get("population"),
        pop_size=body.get("pop_size"),
        generations=body.get("generations", 1),
    ))
