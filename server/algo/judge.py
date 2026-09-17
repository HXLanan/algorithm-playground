# -*- coding: utf-8 -*-
"""核心算法模块：判题器。

给定用户提交的 Python 代码与测试用例，运行并对比结果。

⚠️ 安全声明
    本项目是**本地学习工具**。判题器使用受限的 `exec` 执行用户代码，
    **不是生产级沙箱**，仅用于运行自己写的算法题解。
    请勿把服务暴露到公网。

已有的基础防护：
    · 限制代码长度与执行时间（用例级别）
    · 清理危险的内置函数（open/exec/eval/__import__ 等）
    · 异常捕获与隔离，单个用例失败不影响其余用例
    · 不返回系统级的错误细节
"""
import time
import signal
from typing import List, Dict, Any, Optional, Callable

MAX_CODE_LEN = 8000          # 提交代码长度上限
MAX_CASE_SECONDS = 3.0       # 单个用例执行时间上限

# 允许导入的模块（白名单：纯计算类，无 IO/系统能力）
import collections as _collections
import heapq as _heapq
import math as _math
import bisect as _bisect
import itertools as _itertools
import functools as _functools
import re as _re
import copy as _copy
import string as _string

SAFE_MODULES = {
    "collections": _collections,
    "heapq": _heapq,
    "math": _math,
    "bisect": _bisect,
    "itertools": _itertools,
    "functools": _functools,
    "re": _re,
    "copy": _copy,
    "string": _string,
}


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    """受控的 __import__：只允许白名单内的模块。"""
    root = name.split(".")[0]
    if root in SAFE_MODULES:
        return SAFE_MODULES[root]
    raise ImportError("模块 `%s` 不被允许导入（仅支持：%s）"
                      % (name, ", ".join(sorted(SAFE_MODULES))))


# 允许使用的内置函数（白名单，最小化风险）
SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any, "bool": bool, "chr": chr,
    "dict": dict, "divmod": divmod, "enumerate": enumerate, "filter": filter,
    "float": float, "format": format, "frozenset": frozenset, "getattr": getattr,
    "hasattr": hasattr, "hash": hash, "hex": hex, "int": int, "isinstance": isinstance,
    "issubclass": issubclass, "iter": iter, "len": len, "list": list, "map": map,
    "max": max, "min": min, "next": next, "oct": oct, "ord": ord, "pow": pow,
    "range": range, "repr": repr, "reversed": reversed, "round": round,
    "set": set, "setattr": setattr, "slice": slice, "sorted": sorted,
    "str": str, "sum": sum, "tuple": tuple, "type": type, "zip": zip,
    "True": True, "False": False, "None": None,
    "Exception": Exception, "ValueError": ValueError, "TypeError": TypeError,
    "IndexError": IndexError, "KeyError": KeyError, "StopIteration": StopIteration,
    "__build_class__": __build_class__, "__name__": "__main__",
    "__import__": _safe_import,        # 受控导入，支持 import heapq 等写法
}


class _Timeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise _Timeout()


def _can_set_alarm() -> bool:
    """Windows 上 signal.SIGALRM 不可用，需降级处理。"""
    return hasattr(signal, "SIGALRM") and hasattr(signal, "setitimer")


def run_code(code: str, func_name: str, cases: List[Dict[str, Any]],
             compare: Optional[Callable] = None) -> Dict[str, Any]:
    """执行用户代码并逐用例判题。

    参数：
        code       用户提交的 Python 源码（需定义名为 func_name 的函数）
        func_name  要调用的函数名
        cases      测试用例 [{"args": [...], "expect": ...}, ...]
        compare    自定义比较函数 (actual, expect) -> bool，默认深度比较

    返回：
        {"ok": bool, "passed": int, "total": int, "results": [...], "error": str|None}
    """
    if not code or not code.strip():
        return _fail("代码为空")
    if len(code) > MAX_CODE_LEN:
        return _fail("代码过长（上限 %d 字符）" % MAX_CODE_LEN)

    # 危险关键字粗筛（不是完备防护，但能挡掉明显的越界尝试）
    banned = ("__import__", "import os", "import sys", "import subprocess",
              "import shutil", "open(", "eval(", "exec(", "compile(")
    for b in banned:
        if b in code:
            return _fail("代码中包含不被允许的写法：%s" % b)

    # 在受限命名空间中执行用户代码
    sandbox: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    try:
        compiled = compile(code, "<submission>", "exec")
        exec(compiled, sandbox)          # noqa: S102 —— 本地学习工具，见模块文档
    except Exception as e:
        return _fail("代码编译/执行失败：%s: %s" % (type(e).__name__, e))

    fn = sandbox.get(func_name)
    if not callable(fn):
        return _fail("未找到函数 `%s`。请确保代码中定义了它。" % func_name)

    results = []
    passed = 0
    t0 = time.time()

    for idx, case in enumerate(cases):
        args = case.get("args", [])
        expect = case.get("expect")
        # 深拷贝参数，避免用例之间互相污染
        import copy
        try:
            call_args = copy.deepcopy(args)
        except Exception:
            call_args = args

        case_start = time.time()
        try:
            if _can_set_alarm():
                old = signal.signal(signal.SIGALRM, _timeout_handler)
                signal.setitimer(signal.ITIMER_REAL, MAX_CASE_SECONDS)
            try:
                actual = fn(*call_args)
            finally:
                if _can_set_alarm():
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old)

            elapsed = time.time() - case_start
            if elapsed > MAX_CASE_SECONDS:
                raise _Timeout()

            # 输出比较（可能需要排序以忽略顺序差异）
            norm_expect = _normalize(expect)
            norm_actual = _normalize(actual)
            if compare is not None:
                ok = compare(actual, expect)
            else:
                ok = _deep_equal(norm_actual, norm_expect)

            if ok:
                passed += 1
            results.append({
                "index": idx + 1,
                "args": _safe_repr(args),
                "expect": _safe_repr(expect),
                "actual": _safe_repr(actual),
                "passed": bool(ok),
                "timeMs": round(elapsed * 1000, 2),
            })
        except _Timeout:
            results.append({
                "index": idx + 1,
                "args": _safe_repr(args),
                "expect": _safe_repr(expect),
                "actual": None,
                "passed": False,
                "error": "超时（超过 %.1f 秒）" % MAX_CASE_SECONDS,
                "timeMs": round(MAX_CASE_SECONDS * 1000, 2),
            })
        except Exception as e:
            results.append({
                "index": idx + 1,
                "args": _safe_repr(args),
                "expect": _safe_repr(expect),
                "actual": None,
                "passed": False,
                "error": "%s: %s" % (type(e).__name__, e),
                "timeMs": round((time.time() - case_start) * 1000, 2),
            })

    total_time = round((time.time() - t0) * 1000, 2)
    return {
        "ok": passed == len(cases),
        "passed": passed,
        "total": len(cases),
        "results": results,
        "timeMs": total_time,
        "error": None,
    }


def _normalize(v):
    """把结果归一化，便于比较。

    · 子集/全排列类题目顺序不固定 → 对顶层列表做排序后比较
    · [[1,2],[3]] 这种嵌套结构也排序内部
    """
    if isinstance(v, (list, tuple)):
        items = [_normalize(x) for x in v]
        try:
            # 尝试按字符串键排序（元素类型混合时也能工作）
            items_sorted = sorted(items, key=lambda x: repr(x))
        except Exception:
            items_sorted = items
        return items_sorted
    return v


def _deep_equal(a, b) -> bool:
    """深度比较，容忍 int/float 的等价（如 2 与 2.0）。"""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 1e-9
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(_deep_equal(x, y) for x, y in zip(a, b))
    return a == b


def _safe_repr(v, limit: int = 200) -> str:
    try:
        s = repr(v)
    except Exception:
        s = "<不可表示>"
    if len(s) > limit:
        s = s[:limit] + "…"
    return s


def _fail(msg: str) -> Dict[str, Any]:
    return {"ok": False, "passed": 0, "total": 0, "results": [],
            "error": msg, "timeMs": 0}


def self_test() -> Dict[str, Any]:
    """判题器自测：验证自身工作正常。"""
    code = """def add(a, b):
    return a + b
"""
    r = run_code(code, "add", [
        {"args": [1, 2], "expect": 3},
        {"args": [0, 0], "expect": 0},
    ])
    return {"selfTest": r, "ok": r["ok"] and r["passed"] == 2}
