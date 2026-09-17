# -*- coding: utf-8 -*-
"""配置层：集中管理路径、端口与业务常量。"""
import os

# ---------- 路径 ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ---------- 服务 ----------
HOST = "127.0.0.1"
PORT = int(os.environ.get("ALGO_PORT", "8080"))
DEBUG = os.environ.get("ALGO_DEBUG", "1") == "1"

# ---------- 业务常量 ----------
MAX_ARRAY_SIZE = 60          # 排序演示允许的最大元素数
MAX_FIB_MONTH = 40           # 斐波那契最大月数
WHEAT_CELLS = 64             # 棋盘格数
WHEAT_GRAIN_GRAM = 0.03      # 每粒小麦约 0.03 克
WORLD_WHEAT_TON_PER_YEAR = 780_000_000   # 全球年产小麦（吨）近似
GENETIC_GOLD = (0.72, 0.66)  # 遗传算法"金峰"位置
GENETIC_MAX_POP = 500

# ---------- 新增算法模块的限额 ----------
LIFE_MAX_DIM = 120           # 生命游戏网格上限
HANOI_MAX_DISKS = 12         # 汉诺塔最多圆盘数
NQUEENS_MAX_N = 10           # N 皇后最大规模
MONTE_CARLO_MAX = 200000     # 蒙特卡罗最多撒点数
MANDEL_MAX_W = 300           # 曼德勃罗渲染最大宽度
MANDEL_MAX_H = 200           # 曼德勃罗渲染最大高度
PATH_MAX_DIM = 60            # 寻路地图最大边长
ACO_MAX_CITIES = 20          # 蚁群最多城市数
KMP_MAX_TEXT = 300           # KMP 主串最大长度
KMP_MAX_PATTERN = 60         # KMP 模式串最大长度

# ---------- 第三批算法模块的限额 ----------
LCS_MAX_LEN = 60             # LCS 输入串最大长度
BST_MAX_NODES = 30           # BST 最多节点数
HEAP_MAX_SIZE = 40           # 堆最多元素数
GRAPH_MAX_NODES = 20         # 图最多节点数
