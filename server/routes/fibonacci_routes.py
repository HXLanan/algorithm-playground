# -*- coding: utf-8 -*-
"""路由层：斐波那契（兔子农场）相关接口。"""
from flask import Blueprint, request, jsonify

from ..services import fibonacci_service

fibonacci_bp = Blueprint("fibonacci", __name__)


@fibonacci_bp.get("/sequence")
def sequence():
    """斐波那契序列。query: ?months=20"""
    months = request.args.get("months", default=None, type=int)
    return jsonify(fibonacci_service.get_sequence(months))


@fibonacci_bp.get("/cost")
def cost():
    """递归 vs 迭代调用次数对比。query: ?n=25"""
    n = request.args.get("n", default=None, type=int)
    return jsonify(fibonacci_service.compare_cost(n))
