# -*- coding: utf-8 -*-
"""路由层：素数筛。"""
from flask import Blueprint, request, jsonify

from ..services import prime_sieve_service

prime_sieve_bp = Blueprint("prime_sieve", __name__)


@prime_sieve_bp.get("/sieve")
def sieve():
    n = request.args.get("n", default=None, type=int)
    return jsonify(prime_sieve_service.sieve(n))


@prime_sieve_bp.get("/density")
def density():
    n = request.args.get("n", default=None, type=int)
    return jsonify(prime_sieve_service.density(n))
