# -*- coding: utf-8 -*-
"""路由层：麦粒棋盘（指数爆炸）相关接口。"""
from flask import Blueprint, request, jsonify

from ..services import wheat_service

wheat_bp = Blueprint("wheat", __name__)


@wheat_bp.get("/board")
def board():
    """棋盘数据。query: ?cells=64"""
    cells = request.args.get("cells", default=None, type=int)
    return jsonify(wheat_service.get_board(cells))


@wheat_bp.get("/complexity")
def complexity():
    """复杂度对比表。"""
    return jsonify(wheat_service.get_complexity())
