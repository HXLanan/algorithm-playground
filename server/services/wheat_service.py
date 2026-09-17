# -*- coding: utf-8 -*-
"""服务层：麦粒棋盘（指数爆炸）业务编排。"""
from typing import Dict, Any, Optional

from ..algo import exponential
from .. import config


def get_board(cells: Optional[int] = None) -> Dict[str, Any]:
    """返回棋盘数据（含每格粒数与类比换算）。"""
    if cells is None:
        cells = config.WHEAT_CELLS
    try:
        cells = int(cells)
    except (TypeError, ValueError):
        cells = config.WHEAT_CELLS
    if cells < 1:
        cells = 1
    if cells > config.WHEAT_CELLS:
        cells = config.WHEAT_CELLS
    board = exponential.build_board(cells)
    # 用配置里的常量覆盖，保持单一数据源
    g = board["total_grain"]
    grams = g * config.WHEAT_GRAIN_GRAM
    tons = grams / 1_000_000.0
    board["total_tons"] = tons
    board["total_tons_str"] = exponential._short(int(tons))
    board["world_years"] = tons / config.WORLD_WHEAT_TON_PER_YEAR
    board["grain_gram"] = config.WHEAT_GRAIN_GRAM
    board["world_wheat_tons_per_year"] = config.WORLD_WHEAT_TON_PER_YEAR
    return board


def get_complexity() -> Dict[str, Any]:
    """返回复杂度对比表（线性 / 平方 / 指数）。"""
    return {"table": exponential.complexity_table()}
