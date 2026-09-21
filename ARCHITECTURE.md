# Algo Playground —— 软件架构设计

> 趣味算法讲解合集：把抽象算法还原成看得见、玩得起来的交互动画。

---

## 一、总体分层架构图

```
┌──────────────────────────────────────────────────────────────────────────┐
│                            用 户 浏 览 器                                  │
│                                                                            │
│   ┌────────────────────────────────────────────────────────────────┐      │
│   │                    表现层 Presentation (前端)                    │      │
│   │                                                                  │      │
│   │   index.html   sort.html   wheat.html   fibonacci.html  genetic.html
│   │       │            │           │             │              │         │
│   │       └────────────┴───────────┴─────────────┴──────────────┘         │
│   │                            │                                          │
│   │                    ┌───────▼────────┐                                 │
│   │                    │  公共资源层      │  style.css / nav.js            │
│   │                    │  Common Assets  │  algo-utils.js                 │
│   │                    └───────┬────────┘                                 │
│   │                            │                                          │
│   │              ┌─────────────▼──────────────┐                           │
│   │              │   可视化组件层 View Widgets  │                           │
│   │              │  Canvas 渲染器 / 动画调度器   │                           │
│   │              └─────────────┬──────────────┘                           │
│   └────────────────────────────┼──────────────────────────────────────────┘
│                                 │  HTTP / JSON (fetch)
└─────────────────────────────────┼──────────────────────────────────────────
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       服务端 Server (Python 3 / conda mvs_case)            │
│                                                                            │
│   ┌────────────────────────────────────────────────────────────────┐      │
│   │                     应用层 Application                           │      │
│   │   app.py —— Flask 应用工厂 (create_app)                          │      │
│   │   ├── 静态资源路由  (pages / assets)                             │      │
│   │   └── Blueprint 注册                                             │      │
│   └───────┬───────────────────────┬────────────────────┬────────────┘      │
│           │                       │                    │                   │
│   ┌───────▼────────┐   ┌──────────▼─────────┐  ┌───────▼──────────┐       │
│   │  路由层 Routes  │   │   服务层 Services   │  │  配置层 Config    │       │
│   │                │   │                     │  │                  │       │
│   │ sort_bp        │──▶│ sort_service        │  │ settings.py      │       │
│   │ wheat_bp       │──▶│ wheat_service       │  │ (端口/路径/常量)   │       │
│   │ fibonacci_bp   │──▶│ fibonacci_service   │  │                  │       │
│   │ genetic_bp     │──▶│ genetic_service     │  │                  │       │
│   └────────────────┘   └──────────┬──────────┘  └──────────────────┘       │
│                                   │                                        │
│                        ┌──────────▼──────────┐                            │
│                        │  核心算法层 Algo Core │                            │
│                        │  sorting.py          │                            │
│                        │  exponential.py      │                            │
│                        │  fib.py              │                            │
│                        │  genetic.py          │                            │
│                        └─────────────────────┘                            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 二、模块划分与职责

### 2.1 分层职责表

| 层 | 模块 | 职责 | 不做什么 |
|---|---|---|---|
| 表现层 | `pages/*.html` | 页面结构、交互控件 | 不写算法 |
| | `assets/*.css` | 视觉样式、主题 | 不含逻辑 |
| | `assets/js/*.js` | 动画渲染、请求后端、交互 | 不重复实现算法 |
| 应用层 | `server/app.py` | 创建 Flask 应用、注册蓝图、托管静态资源 | 不含业务逻辑 |
| 路由层 | `server/routes/*.py` | 定义 HTTP 接口、参数校验、组装响应 | 不写算法细节 |
| 服务层 | `server/services/*.py` | 编排业务流程、调用算法层、格式化结果 | 不做 HTTP 细节 |
| 算法层 | `server/algo/*.py` | 纯算法实现（可独立单测） | 不依赖 Flask |
| 配置层 | `server/config.py` | 端口、路径、常量、环境 | — |

### 2.2 核心设计原则

- **前后端职责分离**：前端负责"画"，后端负责"算"。前端本地也能离线跑（内嵌一份核心算法兜底），联网时优先用后端 API 拿权威结果。
- **算法层零依赖**：`server/algo/` 下的模块只用 Python 标准库，可单独测试、可复用。
- **单页单模块**：四个讲解页彼此独立，共用公共资源层，互不耦合。

---

## 三、模块关系图（依赖方向）

```
        pages/*.html
             │  引用
             ▼
      assets/js/*.js ──── fetch ────▶ server/routes/*.py
             │                              │
             │ 调用（可选兜底）               │ 调用
             ▼                              ▼
      assets/js/algo-core.js        server/services/*.py
                                            │ 调用
                                            ▼
                                     server/algo/*.py
                                    （纯算法，零依赖）
```

依赖方向始终单向向下，**不存在反向依赖**（算法层永不 import 路由/服务）。

---

## 四、数据流图（一次典型交互）

```
① 用户点击「运行」
        │
        ▼
② 前端 JS 收集参数 {array, algo, speed}
        │
        ├─── 有后端 ──▶ ③ POST /api/sort/run  ──▶ ④ sort_service 校验
        │                                              │
        │                                              ▼
        │                                     ⑤ algo.sorting 生成步骤序列
        │                                              │
        │              ◀── ⑥ 返回 JSON {steps:[...]} ──┘
        │
        └─── 无后端 ──▶ 本地 algo-core.js 直接生成步骤
        │
        ▼
⑦ 动画调度器按帧播放 steps
        │
        ▼
⑧ Canvas 渲染器逐帧绘制 → 用户看到动画
```

---

## 五、目录结构设计

```
algo-playground/
├── README.md                     # 使用说明
├── ARCHITECTURE.md               # 本架构文档
├── requirements.txt              # Python 依赖清单
├── run.py                        # 启动入口
│
├── server/                       # 服务端
│   ├── __init__.py
│   ├── app.py                    # Flask 应用工厂
│   ├── config.py                 # 配置常量
│   ├── algo/                     # 核心算法层（零依赖）
│   │   ├── __init__.py
│   │   ├── sorting.py
│   │   ├── exponential.py
│   │   ├── fib.py
│   │   └── genetic.py
│   ├── services/                 # 服务层
│   │   ├── __init__.py
│   │   ├── sort_service.py
│   │   ├── wheat_service.py
│   │   ├── fibonacci_service.py
│   │   └── genetic_service.py
│   └── routes/                   # 路由层（蓝图）
│       ├── __init__.py
│       ├── sort_routes.py
│       ├── wheat_routes.py
│       ├── fibonacci_routes.py
│       └── genetic_routes.py
│
├── pages/                        # 页面
│   ├── index.html
│   ├── sort.html
│   ├── wheat.html
│   ├── fibonacci.html
│   └── genetic.html
│
└── assets/                       # 公共资源
    ├── style.css
    └── js/
        ├── nav.js
        ├── algo-core.js          # 前端兜底算法
        └── ui.js                 # 通用 UI 工具
```

---

## 六、接口约定（API）

| 方法 | 路径 | 作用 | 请求 | 响应 |
|---|---|---|---|---|
| GET | `/api/health` | 健康检查 | — | `{status:"ok"}` |
| POST | `/api/sort/run` | 生成排序步骤 | `{array, algo}` | `{steps:[{list,a,b,desc,c,w}]}` |
| POST | `/api/sort/random` | 生成随机数组 | `{n}` | `{array:[...]}` |
| GET | `/api/wheat/board` | 麦粒棋盘数据 | `?cells=64` | `{cells:[[idx,count,unit]]}` |
| GET | `/api/fib/sequence` | 斐波那契序列 | `?n=20` | `{seq:[...],details:[{month,total,newborn}]}` |
| POST | `/api/genetic/evolve` | 进化一代/多代 | `{pop,gens,target}` | `{best,generation,samples:[...]}` |

---

## 七、健壮性设计

| 风险点 | 处理方式 | 位置 |
|---|---|---|
| 前端回传畸形种群 | `_sanitize()` 校验并夹紧，非法则整体丢弃改用随机种群 | `services/genetic_service.py` |
| 数组含非数字/过短/过长 | 捕获异常并抛 `ValueError` → 路由层返回 400（而非 500） | `services/sort_service.py` |
| 查询参数非数字 | `try/except` 回退到默认值 | 各 service |
| 朴素递归求 fib(50) 卡死服务 | 用数学公式 `2·F(n)-1` 直接算调用次数，不做真实递归 | `algo/fib.py` |
| 前端异步请求未返回时点击播放 | `loading` 标志 + 按钮禁用，防止竞态重复重置 | `pages/sort.html` |
| 前端空种群渲染崩溃 | 空数组提前返回 | `pages/genetic.html` |
| 后端不可用 | 前端 `algo-core.js` 本地兜底，页面不白屏 | `assets/js/ui.js` |

### 验证方式
`selfcheck.py` 提供 **40+ 项断言**，无需浏览器即可验证：
排序结果正确性、麦粒数量精确性、斐波那契数值、遗传收敛性、
非法参数的安全处理（应报错而不是崩溃）。

---

## 八、算法目录（catalog）

`server/catalog.py` 集中登记全部 12 个算法页的元信息（图标、标题、分类、顺序），
首页与导航都从这里取数据——**新增算法只需在此登记一处**，避免多处硬编码不同步。

| 分类 | 算法 |
|---|---|
| 经典算法 | 排序、麦粒棋盘、兔子农场、汉诺塔 |
| 搜索与寻路 | A* 寻路、N 皇后、KMP |
| 涌现与自组织 | 生命游戏、遗传算法、蚁群算法 |
| 数学之美 | 蒙特卡罗、曼德勃罗集 |

接口：`GET /api/catalog` 返回完整清单；前端离线时使用内置兜底目录（与之保持一致）。

---

## 九、实现顺序与完成情况

1. ✅ 架构设计（本文档）
2. ✅ 后端骨架：`config.py` → `app.py` → `run.py`
3. ✅ 算法层（12 个模块）：`sorting` / `exponential` / `fib` / `genetic` /
   `life` / `hanoi` / `nqueens` / `montecarlo` / `mandelbrot` / `pathfinding` / `aco` / `kmp`
4. ✅ 服务层：12 个 service（参数校验 + 业务编排）
5. ✅ 路由层：25 个 Blueprint + 健康检查 + 目录接口
6. ✅ 前端公共层：`style.css` / `nav.js` / `algo-core.js` / `algo-core-ext.js` / `ui.js`
7. ✅ 25 个页面模块 + 首页分类导航
8. ✅ 依赖清单、运行文档、自检脚本

### 扩展到 25 个算法（第三批 13 个）

在既有分层架构上**平行扩展**，未改动任何已有代码路径：

| 批次 | 算法 | 新增文件 |
|---|---|---|
| 13-15 | 快速排序/归并排序、二分查找、快速幂 | `divide_sort.py` / `binary_search.py` / `fast_power.py` |
| 16-18 | 图算法(Dijkstra/BFS/DFS)、二叉搜索树、二叉堆 | `graph_algo.py` / `bst.py` / `heap.py` |
| 19-20 | 0-1 背包、最长公共子序列 | `knapsack.py` / `lcs.py` |
| 21-22 | 埃拉托斯特尼筛法、约瑟夫环 | `prime_sieve.py` / `josephus.py` |
| 23-25 | 一致性哈希、拓扑排序、滑动窗口 | `consistent_hash.py` / `topo_sort.py` / `sliding_window.py` |

每个算法同样遵循 **算法层 → 服务层 → 路由层 → 前端页面 → 兜底库** 五处登记，
并在 `catalog.py` 中登记一条元信息。

### 验证状态
- `selfcheck.py`：**213 项断言全部 PASS**（不依赖 Flask，覆盖算法层 + 服务层 + 目录集成）
- **交叉验证**：背包 vs 暴力枚举、LCS vs 标准 DP、Dijkstra vs 堆实现、
  筛法 vs 试除法、滑动窗口 vs 暴力、约瑟夫公式 vs 模拟 —— 全部一致
- API 端到端：25 个算法各至少 1 个接口，**全部返回 200**，错误分支正确返回 400
- 前端语法：Node `--check` 全部 JS（4 个文件 + 52 段内联脚本）**零错误**
- 资源可达：26 个页面 + 5 个静态资源，**全部 200**

### 已知设计权衡
- `nqueens.solve()` 把「解总数统计」与「过程帧收集」解耦：解数始终完整
  （n=8 正确得到 92），过程帧限量 20000 以免响应过大。
- 递归版斐波那契保留在 `fib.py` 中作为教学对照，但服务接口改走数学公式
  `2·F(n)−1` 计算调用次数，避免 n 较大时服务被指数级计算拖死。
- `josephus.simulate()` 的规模上限（2000）只限制**模拟**，
  更大规模请用 `formula()` 的 O(n) 递推（已验证到 n=100000）。
- `consistent_hash.RING_SIZE` 取 100000（真实系统用 2³²），
  以减小哈希碰撞、让虚拟节点的均衡效果符合理论预期。

---

# 第二部分：LeetCode 刷题模块

把「看得懂算法」和「写得出代码」连起来——每个可视化演示都能对应到真实面试题。

## 十、题库模块架构

```
┌───────────────────────────────────────────────────────────────┐
│                    前端 (pages/)                               │
│                                                                │
│   problems.html  ──▶  题单列表页                                │
│      │                 · 按分类/难度/关键词筛选                  │
│      │                 · 显示"关联可视化"标签                    │
│      ▼                                                         │
│   problem.html   ──▶  题目详情页                                │
│      · 题目描述 / 示例 / 提示                                   │
│      · 解题思路（多种解法 + 复杂度）                             │
│      · 代码实现（Python）                                       │
│      · 关联算法讲解页链接 ──────────┐                           │
│      · 在线运行测试用例            │                            │
└────────────────────────────────────┼───────────────────────────┘
                                      │ 跳转到可视化
                                      ▼
                        pages/{sort,life,nqueens,...}.html
                                      ▲
                    （可视化页也可反查相关题目）
┌─────────────────────────────────────┼───────────────────────────┐
│                    服务端 (server/)  │                           │
│                                      │                           │
│   routes/problems_routes.py ─────────┘                          │
│      GET  /api/problems            题单（支持筛选）              │
│      GET  /api/problems/<slug>     题目详情                     │
│      GET  /api/problems/meta       分类/难度/统计元信息          │
│      POST /api/problems/<slug>/run 在线运行用户代码（沙箱受限）   │
│                          │                                      │
│   services/problem_service.py   筛选、排序、校验、编排            │
│                          │                                      │
│   data/problems.py      ← 题库数据（纯数据，无逻辑）              │
│   data/solutions.py     ← 参考解法（可执行 Python 函数）          │
│   algo/judge.py         ← 判题器（跑测试用例，对比输出）          │
└─────────────────────────────────────────────────────────────────┘
```

## 十一、题库数据模型

```python
{
  "slug": "two-sum",                    # 唯一标识（同 LeetCode）
  "lcId": 1,                            # LeetCode 题号
  "title": "两数之和",
  "difficulty": "简单",                  # 简单 / 中等 / 困难
  "tags": ["数组", "哈希表"],             # 算法标签
  "category": "哈希表",                  # 题库主分类
  "visualizer": "sort.html",            # 关联的可视化页（可为 null）
  "visualizerHint": "先用排序把范围缩小", # 关联说明
  "description": "题目描述…",
  "examples": [                          # 示例（用于判题）
     {"input": "nums = [2,7,11,15], target = 9",
      "output": "[0,1]",
      "explain": "因为 nums[0] + nums[1] == 9"}
  ],
  "hints": ["暴力是 O(n²)", "用哈希表换空间"],
  "solutions": [                         # 多种解法
     {"name": "暴力枚举", "time": "O(n²)", "space": "O(1)",
      "idea": "双重循环…", "code": "def two_sum(...)…"}
  ],
  "relatedToVisualizer": True            # 是否由可视化页反查可见
}
```

## 十二、判题器设计（algo/judge.py）

**职责**：给定用户代码 + 测试用例，运行并对比结果。

| 环节 | 做法 | 安全考虑 |
|---|---|---|
| 提取函数 | 从用户代码里 `exec` 后取指定函数名 | 限制代码长度 |
| 运行用例 | 逐个用例调用函数，捕获异常 | `try/except` 隔离 |
| 对比输出 | 与期望值做结构化比较（顺序不敏感用排序后比较） | 超时保护 |
| 结果返回 | 每个用例的通过/失败 + 实际输出 | 不泄露系统信息 |

> ⚠️ **安全声明**：本项目是**本地学习工具**，判题器使用受限的 `exec`，
> **不是生产级沙箱**。它只用于跑自己写的算法题解；不要把服务暴露到公网。
> 代码中会做基础防护（禁用部分危险内置、限制长度），但不保证恶意代码安全。

## 十三、题目 ↔ 可视化 双向联动

| 方向 | 实现 |
|---|---|
| 题目 → 可视化 | 题目详情页显示"🧩 去看可视化演示"按钮，跳到对应算法页 |
| 可视化 → 题目 | 算法页底部显示"📝 相关 LeetCode 题目"，点进去做题 |

联动关系集中在 `data/problems.py` 的 `visualizer` 字段定义，前端通过
`GET /api/problems?visualizer=sort.html` 反查。

## 十四、题库分类体系

| 分类 | 说明 | 示例题 |
|---|---|---|
| 数组与哈希 | 基础中的基础 | 1. 两数之和、49. 字母异位词分组 |
| 双指针 | 相向/同向双指针 | 15. 三数之和、11. 盛最多水容器 |
| 滑动窗口 | 定长/不定长 | 3. 无重复字符最长子串、438. 找异位词 |
| 二分查找 | 有序性利用 | 704. 二分查找、34. 查找首末位置 |
| 排序 | 各类排序实现 | 912. 排序数组、215. 第K大元素 |
| 递归与回溯 | 试探与撤销 | 46. 全排列、51. N皇后、78. 子集 |
| 动态规划 | 状态转移 | 70. 爬楼梯、198. 打家劫舍、322. 零钱兑换 |
| BFS/DFS | 图与网格遍历 | 200. 岛屿数量、994. 腐烂的橘子 |
| 字符串 | 匹配与处理 | 28. 找出第一个匹配项、459. 重复子串 |
| 栈与队列 | 线性结构 | 20. 有效括号、155. 最小栈 |
| 链表 | 指针操作 | 206. 反转链表、141. 环形链表 |
| 二叉树 | 递归遍历 | 94. 中序遍历、104. 最大深度 |
| 贪心 | 局部最优 | 121. 买卖股票、55. 跳跃游戏 |
| 模拟与进阶 | 综合 | 289. 生命游戏、478. 圆内随机点 |

## 十五、实现顺序与完成情况

1. ✅ 题库数据层：`data/problems_part1~3.py`（**71 题**，含描述/示例/思路/代码/测试用例）
2. ✅ 题库汇总层：`data/__init__.py`（索引、分类、标签、统计、反查）
3. ✅ 判题器：`algo/judge.py`（受限 exec + 模块白名单 + 异常隔离）
4. ✅ 服务层：`services/problem_service.py`（筛选/搜索/详情/判题/反查）
5. ✅ 路由层：`routes/problems_routes.py`（6 个接口）
6. ✅ 前端：`problems.html`（题单，支持多维筛选）、`problem.html`（详情 + 在线判题）
7. ✅ 双向联动：`assets/js/related.js`（25 个算法页已注入）
8. ✅ 导航与主页集成：题库入口卡片 + 实时统计
9. ✅ 自检扩充：**268 项断言**；端到端验证全部通过

### 题库模块验证结果
- **87 个参考答案全部通过自己的测试用例**（71 题，多数题含 2 种解法）
- **判题器安全防护全部生效**：拒绝 `import os/socket`、`open()`、`eval`、
  `__import__`、空代码、超长代码、未定义函数
- **允许的模块正常可用**：`heapq`、`collections` 等纯计算模块
- **异常隔离**：单用例异常不影响其余用例，且标记为失败
- **筛选全部有效**：难度 / 分类 / 标签 / 关键词 / limit / offset

## 十六、题库模块的接口清单

| 方法 | 路径 | 作用 |
|---|---|---|
| GET | `/api/problems/list` | 题目列表（支持 category/difficulty/tag/keyword/visualizer/limit/offset） |
| GET | `/api/problems/meta` | 分类、标签、难度、统计 |
| GET | `/api/problems/related` | 反查某可视化页关联的题目 |
| GET | `/api/problems/hint` | 搜索联想 |
| GET | `/api/problems/<slug>` | 题目详情（含解法与测试用例） |
| POST | `/api/problems/<slug>/run` | 判题（`{code}` 或 `{useReference:true}`） |

### 判题器安全边界（重要）

判题器使用**受限 `exec`**，属于本地学习工具，**不是生产级沙箱**：

| 防护 | 实现 |
|---|---|
| 模块白名单 | 只允许 `collections/heapq/math/bisect/itertools/functools/re/copy/string` |
| 内置函数白名单 | 剔除 `open/eval/exec/compile/file` 等 |
| 危险写法拦截 | 检测 `__import__`、`import os`、`open(` 等关键字 |
| 长度限制 | 提交代码 ≤ 8000 字符 |
| 时间限制 | 单用例 ≤ 3 秒（POSIX 用 SIGALRM，Windows 降级为事后检查） |
| 异常隔离 | 单用例异常不影响其余，且不泄露系统信息 |

> ⚠️ 请勿将服务暴露到公网。这是为「自己练习算法题」设计的工具。
