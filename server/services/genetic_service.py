# -*- coding: utf-8 -*-
"""服务层：遗传算法业务编排。"""
from typing import Dict, Any, Optional

from ..algo import genetic
from .. import config


def evolve(population=None, pop_size: Optional[int] = None,
           generations: int = 1) -> Dict[str, Any]:
    """进化若干代。

    population 由前端回传时，表示"在现有种群上继续进化一代"，
    从而实现点击式逐代交互。
    """
    if pop_size is None:
        pop_size = 200
    try:
        pop_size = int(pop_size)
    except (TypeError, ValueError):
        pop_size = 200
    if pop_size < 10:
        pop_size = 10
    if pop_size > config.GENETIC_MAX_POP:
        pop_size = config.GENETIC_MAX_POP

    try:
        generations = int(generations)
    except (TypeError, ValueError):
        generations = 1
    if generations < 1:
        generations = 1
    if generations > 200:
        generations = 200

    clean_pop = _sanitize(population)
    return genetic.run(pop_size=pop_size, generations=generations, population=clean_pop)


def _sanitize(population):
    """校验并清洗前端回传的种群，非法时返回 None（由算法层重新随机初始化）。

    防止畸形输入触发 float() 异常导致 500。
    """
    if not population or not isinstance(population, (list, tuple)):
        return None
    cleaned = []
    for ind in population:
        try:
            x = float(ind[0])
            y = float(ind[1])
        except (TypeError, ValueError, IndexError, KeyError):
            return None                       # 有一个不合规就整体丢弃，改用随机种群
        # 夹紧到合法区间
        cleaned.append([min(0.99, max(0.01, x)), min(0.99, max(0.01, y))])
        if len(cleaned) >= config.GENETIC_MAX_POP:
            break
    return cleaned or None
