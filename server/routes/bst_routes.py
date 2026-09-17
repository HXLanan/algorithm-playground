# -*- coding: utf-8 -*-
"""路由层：二叉搜索树。"""
from flask import Blueprint, request, jsonify

from ..services import bst_service

bst_bp = Blueprint("bst", __name__)


@bst_bp.post("/build")
def build():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(bst_service.build(b.get("values")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bst_bp.post("/search")
def search():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(bst_service.search(b.get("values"), b.get("target")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bst_bp.post("/balanced")
def balanced():
    b = request.get_json(silent=True) or {}
    try:
        return jsonify(bst_service.balanced(b.get("values")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
