# -*- coding: utf-8 -*-
"""应用层：Flask 应用工厂。

职责：创建应用、注册蓝图、托管静态页面资源。不含业务逻辑。
"""
from flask import Flask, redirect, send_from_directory
from flask_cors import CORS

from . import config


def create_app():
    """创建并配置 Flask 应用。"""
    app = Flask(__name__, static_folder=None)
    CORS(app)  # 允许前端（含 file:// 场景）跨域调用 API

    # ---------- 蓝图注册 ----------
    from .routes.sort_routes import sort_bp
    from .routes.wheat_routes import wheat_bp
    from .routes.fibonacci_routes import fibonacci_bp
    from .routes.genetic_routes import genetic_bp
    from .routes.life_routes import life_bp
    from .routes.hanoi_routes import hanoi_bp
    from .routes.nqueens_routes import nqueens_bp
    from .routes.montecarlo_routes import montecarlo_bp
    from .routes.mandelbrot_routes import mandelbrot_bp
    from .routes.pathfinding_routes import pathfinding_bp
    from .routes.aco_routes import aco_bp
    from .routes.kmp_routes import kmp_bp
    # 第三批（算法 13-25）
    from .routes.divide_sort_routes import divide_sort_bp
    from .routes.binary_search_routes import binary_search_bp
    from .routes.fast_power_routes import fast_power_bp
    from .routes.graph_routes import graph_bp
    from .routes.bst_routes import bst_bp
    from .routes.heap_routes import heap_bp
    from .routes.knapsack_routes import knapsack_bp
    from .routes.lcs_routes import lcs_bp
    from .routes.prime_sieve_routes import prime_sieve_bp
    from .routes.josephus_routes import josephus_bp
    from .routes.consistent_hash_routes import consistent_hash_bp
    from .routes.topo_sort_routes import topo_sort_bp
    from .routes.sliding_window_routes import sliding_window_bp

    app.register_blueprint(sort_bp, url_prefix="/api/sort")
    app.register_blueprint(wheat_bp, url_prefix="/api/wheat")
    app.register_blueprint(fibonacci_bp, url_prefix="/api/fib")
    app.register_blueprint(genetic_bp, url_prefix="/api/genetic")
    app.register_blueprint(life_bp, url_prefix="/api/life")
    app.register_blueprint(hanoi_bp, url_prefix="/api/hanoi")
    app.register_blueprint(nqueens_bp, url_prefix="/api/nqueens")
    app.register_blueprint(montecarlo_bp, url_prefix="/api/montecarlo")
    app.register_blueprint(mandelbrot_bp, url_prefix="/api/mandelbrot")
    app.register_blueprint(pathfinding_bp, url_prefix="/api/pathfinding")
    app.register_blueprint(aco_bp, url_prefix="/api/aco")
    app.register_blueprint(kmp_bp, url_prefix="/api/kmp")
    # 第三批
    app.register_blueprint(divide_sort_bp, url_prefix="/api/divide-sort")
    app.register_blueprint(binary_search_bp, url_prefix="/api/binary-search")
    app.register_blueprint(fast_power_bp, url_prefix="/api/fast-power")
    app.register_blueprint(graph_bp, url_prefix="/api/graph")
    app.register_blueprint(bst_bp, url_prefix="/api/bst")
    app.register_blueprint(heap_bp, url_prefix="/api/heap")
    app.register_blueprint(knapsack_bp, url_prefix="/api/knapsack")
    app.register_blueprint(lcs_bp, url_prefix="/api/lcs")
    app.register_blueprint(prime_sieve_bp, url_prefix="/api/prime-sieve")
    app.register_blueprint(josephus_bp, url_prefix="/api/josephus")
    app.register_blueprint(consistent_hash_bp, url_prefix="/api/consistent-hash")
    app.register_blueprint(topo_sort_bp, url_prefix="/api/topo-sort")
    app.register_blueprint(sliding_window_bp, url_prefix="/api/sliding-window")
    # LeetCode 题库模块
    from .routes.problems_routes import problems_bp
    app.register_blueprint(problems_bp, url_prefix="/api/problems")

    # ---------- 算法清单（供首页动态渲染） ----------
    @app.get("/api/catalog")
    def catalog():
        from .catalog import CATALOG
        return {"items": CATALOG}

    # ---------- 健康检查 ----------
    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "algo-playground"}

    # ---------- 静态资源 ----------
    @app.get("/")
    def index():
        return redirect("/pages/index.html")

    @app.get("/pages/<path:filename>")
    def pages(filename):
        return send_from_directory(config.PAGES_DIR, filename)

    @app.get("/assets/<path:filename>")
    def assets(filename):
        return send_from_directory(config.ASSETS_DIR, filename)

    # 快捷路由： /sort -> /pages/sort.html
    @app.get("/<page>")
    def shortcut(page):
        import os
        target = os.path.join(config.PAGES_DIR, page + ".html")
        if os.path.isfile(target):
            return redirect("/pages/%s.html" % page)
        return {"error": "not found", "page": page}, 404

    return app
