# -*- coding: utf-8 -*-
"""路由层：蒙特卡罗估算 π。"""
from flask import Blueprint, request, jsonify

from ..services import montecarlo_service

montecarlo_bp = Blueprint("montecarlo", __name__)


@montecarlo_bp.get("/estimate")
def estimate():
    """撒点估算。query: ?total=3000&seed=1"""
    total = request.args.get("total", default=None, type=int)
    seed = request.args.get("seed", default=None, type=int)
    return jsonify(montecarlo_service.estimate(total, seed))


@montecarlo_bp.get("/convergence")
def convergence():
    seed = request.args.get("seed", default=None, type=int)
    return jsonify(montecarlo_service.convergence(seed))
