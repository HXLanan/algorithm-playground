# -*- coding: utf-8 -*-
"""路由层：N 皇后。"""
from flask import Blueprint, request, jsonify

from ..services import nqueens_service

nqueens_bp = Blueprint("nqueens", __name__)


@nqueens_bp.get("/solve")
def solve():
    """求解。query: ?n=6&max_solutions=3"""
    n = request.args.get("n", default=None, type=int)
    ms = request.args.get("max_solutions", default=5, type=int)
    return jsonify(nqueens_service.solve(n, max_solutions=ms))


@nqueens_bp.get("/counts")
def counts():
    return jsonify(nqueens_service.counts())
