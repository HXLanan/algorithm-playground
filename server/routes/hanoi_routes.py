# -*- coding: utf-8 -*-
"""路由层：汉诺塔。"""
from flask import Blueprint, request, jsonify

from ..services import hanoi_service

hanoi_bp = Blueprint("hanoi", __name__)


@hanoi_bp.get("/simulate")
def simulate():
    """模拟搬运。query: ?disks=4&up_to=20"""
    disks = request.args.get("disks", default=None, type=int)
    up_to = request.args.get("up_to", default=None, type=int)
    return jsonify(hanoi_service.simulate(disks, up_to))


@hanoi_bp.get("/counts")
def counts():
    return jsonify(hanoi_service.move_counts())
