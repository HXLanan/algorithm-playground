# -*- coding: utf-8 -*-
"""路由层：曼德勃罗集分形。"""
from flask import Blueprint, request, jsonify

from ..services import mandelbrot_service

mandelbrot_bp = Blueprint("mandelbrot", __name__)


@mandelbrot_bp.get("/render")
def render():
    """渲染。query: ?width=120&height=80&cx=-0.5&cy=0&zoom=1&max_iter=60"""
    a = request.args
    return jsonify(mandelbrot_service.render(
        a.get("width", type=int), a.get("height", type=int),
        a.get("cx", type=float), a.get("cy", type=float),
        a.get("zoom", type=float), a.get("max_iter", type=int)))


@mandelbrot_bp.get("/views")
def views():
    return jsonify(mandelbrot_service.preset_views())


@mandelbrot_bp.get("/orbit")
def orbit():
    a = request.args
    return jsonify(mandelbrot_service.orbit(
        a.get("cx", type=float), a.get("cy", type=float), a.get("steps", type=int)))
