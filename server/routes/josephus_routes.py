# -*- coding: utf-8 -*-
"""路由层：约瑟夫环。"""
from flask import Blueprint, request, jsonify

from ..services import josephus_service

josephus_bp = Blueprint("josephus", __name__)


@josephus_bp.get("/simulate")
def simulate():
    return jsonify(josephus_service.simulate(
        request.args.get("n", type=int), request.args.get("k", type=int)))


@josephus_bp.get("/formula")
def formula():
    return jsonify(josephus_service.formula(
        request.args.get("n", type=int), request.args.get("k", type=int)))


@josephus_bp.get("/default")
def default_case():
    return jsonify(josephus_service.default_case())
