# -*- coding: utf-8 -*-
"""路由层：康威生命游戏。"""
from flask import Blueprint, request, jsonify

from ..services import life_service

life_bp = Blueprint("life", __name__)


@life_bp.get("/patterns")
def patterns():
    return jsonify(life_service.patterns())


@life_bp.post("/new")
def new_grid():
    """创建初始网格。body: {rows, cols, density, seed, pattern}"""
    b = request.get_json(silent=True) or {}
    return jsonify(life_service.new_grid(
        b.get("rows"), b.get("cols"), b.get("density"), b.get("seed"), b.get("pattern")))


@life_bp.post("/evolve")
def evolve():
    """演化。body: {grid, generations}"""
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(life_service.evolve(b.get("grid"), b.get("generations", 1)))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
