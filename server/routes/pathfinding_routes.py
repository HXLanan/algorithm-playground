# -*- coding: utf-8 -*-
"""路由层：A* 寻路。"""
from flask import Blueprint, request, jsonify

from ..services import pathfinding_service

pathfinding_bp = Blueprint("pathfinding", __name__)


@pathfinding_bp.post("/search")
def search():
    """搜索。body: {grid, start, goal, algo, diagonal, rows, cols, seed}"""
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(pathfinding_service.search(
            b.get("grid"), b.get("start"), b.get("goal"),
            b.get("algo", "astar"), b.get("diagonal", False),
            b.get("rows"), b.get("cols"), b.get("seed")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@pathfinding_bp.post("/compare")
def compare():
    """四算法对比。body: {grid, start, goal, rows, cols}"""
    b = request.get_json(silent=True) or {}
    return jsonify(pathfinding_service.compare(
        b.get("grid"), b.get("start"), b.get("goal"), b.get("rows"), b.get("cols")))
