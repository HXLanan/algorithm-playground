# -*- coding: utf-8 -*-
"""核心算法模块：KMP 字符串匹配。

朴素匹配在失配时要把主串指针回退，最坏 O(n·m)。
KMP 用模式串自身的"最长公共前后缀"信息（next 数组），
失配时只滑动模式串而不回退主串指针，做到 O(n+m)。
"""
from typing import List, Dict, Any


def build_next(pattern: str) -> List[int]:
    """构造 next 数组（前缀函数）。

    next[i] = pattern[0..i] 的最长相等前后缀长度。
    """
    n = len(pattern)
    nxt = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt


def search(text: str, pattern: str, max_steps: int = 2000) -> Dict[str, Any]:
    """KMP 匹配，返回所有出现位置与完整过程帧。"""
    if not pattern:
        return {"text": text, "pattern": pattern, "matches": [],
                "steps": [], "next": [], "explain": "模式串为空"}

    nxt = build_next(pattern)
    n, m = len(text), len(pattern)
    matches: List[int] = []
    steps: List[Dict[str, Any]] = []
    j = 0
    comparisons = 0
    fallbacks = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            fallbacks += 1
            if len(steps) < max_steps:
                steps.append({
                    "i": i, "j": j, "type": "fallback",
                    "text": text, "pattern": pattern,
                    "msg": "失配：利用 next[%d]=%d，模式串右滑到 %d（主串指针不回退）"
                           % (j - 1, nxt[j - 1], nxt[j - 1]),
                })
            j = nxt[j - 1]
        comparisons += 1
        if text[i] == pattern[j]:
            if len(steps) < max_steps:
                steps.append({
                    "i": i, "j": j, "type": "match",
                    "text": text, "pattern": pattern,
                    "msg": "字符 %r 匹配成功，继续比下一位" % text[i],
                })
            j += 1
            if j == m:
                matches.append(i - m + 1)
                if len(steps) < max_steps:
                    steps.append({
                        "i": i, "j": j - 1, "type": "found",
                        "text": text, "pattern": pattern,
                        "msg": "🎉 在位置 %d 找到一个完整匹配！" % (i - m + 1),
                    })
                j = nxt[j - 1] if j > 0 else 0
        else:
            if len(steps) < max_steps:
                steps.append({
                    "i": i, "j": j, "type": "mismatch",
                    "text": text, "pattern": pattern,
                    "msg": "首字符就不匹配，主串指针右移一位",
                })

    # 朴素算法对比
    naive_cmp = _naive_comparisons(text, pattern)

    return {
        "text": text,
        "pattern": pattern,
        "matches": matches,
        "next": nxt,
        "steps": steps,
        "comparisons": comparisons,
        "fallbacks": fallbacks,
        "naiveComparisons": naive_cmp,
        "explain": "next 数组记录了模式串的「自我重复」结构；失配时靠它一口气滑到下一个可匹配位置，主串指针永不回头——所以是线性的 O(n+m)。",
    }


def _naive_comparisons(text: str, pattern: str) -> int:
    """朴素匹配的比较次数（用于对比）。"""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return 0
    cnt = 0
    for s in range(n - m + 1):
        k = 0
        while k < m:
            cnt += 1
            if text[s + k] != pattern[k]:
                break
            k += 1
        if k == m:
            break
    return cnt


def demo_pair():
    """返回一组便于演示的默认文本/模式。"""
    return {"text": "ABABDABACDABABCABAB", "pattern": "ABABCABAB"}
