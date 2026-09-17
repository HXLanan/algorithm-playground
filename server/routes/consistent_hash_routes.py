# -*- coding: utf-8 -*-
"""路由层：一致性哈希。"""
from flask import Blueprint, request, jsonify

from ..services import consistent_hash_service

consistent_hash_bp = Blueprint("consistent_hash", __name__)


@consistent_hash_bp.post("/distribute")
def distribute():
    b = request.get_json(silent=True) or {}
    return jsonify(consistent_hash_service.distribute(
        b.get("servers"), b.get("keys"), b.get("vnodes"), b.get("key_count")))


@consistent_hash_bp.post("/compare_removal")
def compare_removal():
    b = request.get_json(silent=True) or {}
    return jsonify(consistent_hash_service.compare_removal(
        b.get("servers"), b.get("keys"), b.get("vnodes"), b.get("key_count")))


@consistent_hash_bp.get("/default")
def default_case():
    return jsonify(consistent_hash_service.default_case())
