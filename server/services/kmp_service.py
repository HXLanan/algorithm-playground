# -*- coding: utf-8 -*-
"""服务层：KMP 字符串匹配。"""
from typing import Dict, Any, Optional

from ..algo import kmp
from .. import config


def search(text=None, pattern=None) -> Dict[str, Any]:
    """执行 KMP 匹配。"""
    demo = kmp.demo_pair()
    if text is None:
        text = demo["text"]
    if pattern is None:
        pattern = demo["pattern"]

    text = str(text)[:config.KMP_MAX_TEXT]
    pattern = str(pattern)[:config.KMP_MAX_PATTERN]
    if not pattern:
        raise ValueError("模式串不能为空")

    res = kmp.search(text, pattern)
    res["naiveComparisons"] = kmp._naive_comparisons(text, pattern)
    res["speedup"] = (round(res["naiveComparisons"] / res["comparisons"], 2)
                      if res["comparisons"] > 0 else 0)
    return res


def demo() -> Dict[str, Any]:
    """返回默认演示数据。"""
    return kmp.demo_pair()
