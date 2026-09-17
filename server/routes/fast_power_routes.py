# -*- coding: utf-8 -*-
"""路由层：快速幂。"""
from flask import Blueprint, request, jsonify

from ..services import fast_power_service

fast_power_bp = Blueprint("fast_power", __name__)


@fast_power_bp.post("/power")
def power():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(fast_power_service.power(b.get("base"), b.get("exp"), b.get("mod")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@fast_power_bp.get("/compare")
def compare():
    return jsonify(fast_power_service.compare())
