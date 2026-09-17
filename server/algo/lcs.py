# -*- coding: utf-8 -*-
"""核心算法模块：动态规划（最长公共子序列 LCS）。

给定两个字符串，求它们最长的公共子序列长度（子序列不要求连续）。

DP 定义：dp[i][j] = A 前 i 个字符 与 B 前 j 个字符 的 LCS 长度
转移：
  · 若 A[i-1] == B[j-1]：dp[i][j] = dp[i-1][j-1] + 1
  · 否则：dp[i][j] = max(dp[i-1][j], dp[i][j-1])

应用：git diff、DNA 序列比对、拼写纠错等。
"""
from typing import List, Dict, Any


def solve(a: str, b: str) -> Dict[str, Any]:
    """求解 LCS，返回 DP 表、具体子序列与推导过程。"""
    a = str(a)
    b = str(b)
    n, m = len(a), len(b)
    if n > 60 or m > 60:
        a, b = a[:60], b[:60]
        n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    trace: List[Dict[str, Any]] = []

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                trace.append({
                    "i": i, "j": j, "type": "match",
                    "char": a[i - 1], "value": dp[i][j],
                    "msg": "字符 %r 相同 → dp[%d][%d] = dp[%d][%d] + 1 = %d"
                           % (a[i - 1], i, j, i - 1, j - 1, dp[i][j]),
                })
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                    trace.append({
                        "i": i, "j": j, "type": "up",
                        "char": None, "value": dp[i][j],
                        "msg": "字符不同 → 取上方较大值 %d" % dp[i][j],
                    })
                else:
                    dp[i][j] = dp[i][j - 1]
                    trace.append({
                        "i": i, "j": j, "type": "left",
                        "char": None, "value": dp[i][j],
                        "msg": "字符不同 → 取左方较大值 %d" % dp[i][j],
                    })

    # 回溯构造子序列
    seq = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            seq.append(a[i - 1])
            i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    seq.reverse()

    return {
        "a": a,
        "b": b,
        "length": dp[n][m],
        "subsequence": "".join(seq),
        "table": dp,
        "steps": trace,
        "explain": "LCS 是「二维 DP」的典范：状态由两个下标共同决定。"
                   "字符相同就斜着 +1（继承左上角），不同就取上方或左方的较大者。"
                   "git diff、DNA 比对都建立在这个思想上。",
    }


def default_case() -> Dict[str, Any]:
    return {"a": "ABCBDAB", "b": "BDCABA"}
