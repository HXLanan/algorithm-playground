# -*- coding: utf-8 -*-
"""核心算法模块：快速幂。

计算 x^n 时，朴素做法要乘 n 次；快速幂利用 n 的二进制分解，
每次把指数减半、底数平方，只需 O(log n) 次乘法。

例：2^10 = (2^5)^2 = ((2^2)^2 · 2)^2 —— 只需 4 次乘法而非 10 次。
"""
from typing import Dict, Any, List


def power(base: int, exp: int, mod: int = 0) -> Dict[str, Any]:
    """快速幂，支持取模（模幂运算）。"""
    if exp < 0:
        raise ValueError("本演示仅支持非负指数")
    steps: List[Dict[str, Any]] = []
    result = 1
    b = base
    e = exp
    bit_index = 0

    while e > 0:
        bit = e & 1
        steps.append({
            "bitIndex": bit_index,
            "bit": bit,
            "base": b,
            "exp": e,
            "result": result,
            "msg": "指数 %d 的二进制最低位是 %d → %s" % (
                e, bit, "该位为 1，把当前底数乘进结果" if bit else "该位为 0，跳过"),
        })
        if bit:
            result = result * b
            if mod:
                result %= mod
        b = b * b
        if mod:
            b %= mod
        e >>= 1
        bit_index += 1

    steps.append({
        "bitIndex": bit_index, "bit": -1, "base": b, "exp": 0,
        "result": result, "msg": "指数已归零，计算结束，结果 = %s" % _short(result),
    })

    naive_ops = exp
    fast_ops = exp.bit_length() if exp > 0 else 0
    return {
        "base": base,
        "exp": exp,
        "mod": mod,
        "result": result,
        "resultStr": _short(result),
        "steps": steps,
        "naiveOps": naive_ops,          # 朴素需要乘多少次
        "fastOps": fast_ops,            # 快速幂需要乘多少次（约）
        "binaryExp": bin(exp)[2:] if exp > 0 else "0",
        "explain": "把指数看成二进制，每一位决定「要不要乘上当前的底数」，"
                   "而底数不断自乘平方。乘法次数从 n 次降到约 log₂n 次。",
    }


def _short(v: int) -> str:
    s = str(v)
    if len(s) <= 20:
        return s
    return "%s.%se%d（共 %d 位）" % (s[0], s[1:3], len(s) - 1, len(s))


def compare_table() -> List[Dict[str, Any]]:
    """对比朴素幂与快速幂的乘法次数。"""
    out = []
    for n in [8, 16, 32, 64, 128, 256, 1024, 1000000]:
        out.append({
            "exp": n,
            "naive": n,
            "fast": n.bit_length(),
        })
    return out
