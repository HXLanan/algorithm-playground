# -*- coding: utf-8 -*-
"""服务层：最长公共子序列（动态规划）。"""
from typing import Dict, Any

from ..algo import lcs
from .. import config


def solve(a=None, b=None) -> Dict[str, Any]:
    s1 = str(a) if a is not None else "ABCBDAB"
    s2 = str(b) if b is not None else "BDCABA"
    if len(s1) > config.LCS_MAX_LEN:
        s1 = s1[:config.LCS_MAX_LEN]
    if len(s2) > config.LCS_MAX_LEN:
        s2 = s2[:config.LCS_MAX_LEN]
    if not s1 or not s2:
        raise ValueError("两个字符串都不能为空")
    return lcs.solve(s1, s2)


def default_case() -> Dict[str, Any]:
    return lcs.default_case()
