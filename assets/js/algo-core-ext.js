/* =========================================================
 * algo-core-ext.js —— 前端兜底算法库（扩充版）
 * ---------------------------------------------------------
 * 为新增的 8 个算法提供离线兜底实现，结构与后端保持一致。
 * 挂载到 window.AlgoExt
 * ========================================================= */
(function (global) {
  "use strict";

  /* ================= 1. 康威生命游戏 ================= */
  function lifeEmpty(rows, cols) {
    var g = [];
    for (var r = 0; r < rows; r++) { var row = []; for (var c = 0; c < cols; c++) row.push(0); g.push(row); }
    return g;
  }
  function lifeRandom(rows, cols, density) {
    density = density === undefined ? 0.28 : density;
    var g = [];
    for (var r = 0; r < rows; r++) {
      var row = [];
      for (var c = 0; c < cols; c++) row.push(Math.random() < density ? 1 : 0);
      g.push(row);
    }
    return g;
  }
  function lifeNeighbors(g, r, c) {
    var rows = g.length, cols = g[0].length, n = 0;
    for (var dr = -1; dr <= 1; dr++) {
      for (var dc = -1; dc <= 1; dc++) {
        if (dr === 0 && dc === 0) continue;
        n += g[(r + dr + rows) % rows][(c + dc + cols) % cols];
      }
    }
    return n;
  }
  function lifeStep(g) {
    var rows = g.length, cols = g[0].length, out = lifeEmpty(rows, cols);
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var n = lifeNeighbors(g, r, c);
        out[r][c] = g[r][c] ? ((n === 2 || n === 3) ? 1 : 0) : (n === 3 ? 1 : 0);
      }
    }
    return out;
  }
  function lifePopulation(g) {
    var s = 0;
    for (var r = 0; r < g.length; r++) for (var c = 0; c < g[r].length; c++) s += g[r][c];
    return s;
  }
  function lifeRun(g, generations) {
    generations = generations || 1;
    var cur = g.map(function (row) { return row.slice(); });
    var pop = [lifePopulation(cur)];
    for (var i = 0; i < generations; i++) { cur = lifeStep(cur); pop.push(lifePopulation(cur)); }
    return { grid: cur, population: pop, generations: generations, alive: pop[pop.length - 1] };
  }
  var LIFE_PATTERNS = {
    glider: [[1, 0], [2, 1], [0, 2], [1, 2], [2, 2]],
    blinker: [[1, 0], [1, 1], [1, 2]],
    block: [[0, 0], [1, 0], [0, 1], [1, 1]],
    toad: [[1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1]],
    beacon: [[0, 0], [1, 0], [0, 1], [3, 2], [2, 3], [3, 3]]
  };
  function lifePlace(g, pattern, top, left) {
    var cells = LIFE_PATTERNS[pattern];
    if (!cells) return g;
    for (var i = 0; i < cells.length; i++) {
      var r = top + cells[i][0], c = left + cells[i][1];
      if (g[r] && g[r][c] !== undefined) g[r][c] = 1;
    }
    return g;
  }

  /* ================= 2. 汉诺塔 ================= */
  function hanoiSolve(n) {
    var steps = [];
    function move(k, f, t, a) {
      if (k === 0) return;
      move(k - 1, f, a, t);
      steps.push({ disk: k, from: f, to: t });
      move(k - 1, a, t, f);
    }
    move(n, "A", "C", "B");
    return steps;
  }
  function hanoiSimulate(n) {
    var steps = hanoiSolve(n);
    var pegs = { A: [], B: [], C: [] };
    for (var i = n; i >= 1; i--) pegs.A.push(i);
    var snaps = [{ pegs: clonePegs(pegs), move: null, index: 0 }];
    for (var k = 0; k < steps.length; k++) {
      var mv = steps[k];
      var d = pegs[mv.from].pop();
      pegs[mv.to].push(d);
      snaps.push({ pegs: clonePegs(pegs), move: mv, index: k + 1 });
    }
    return {
      disks: n, totalMoves: Math.pow(2, n) - 1, steps: steps,
      snapshots: snaps, solved: steps.length === Math.pow(2, n) - 1
    };
  }
  function clonePegs(p) {
    return { A: p.A.slice(), B: p.B.slice(), C: p.C.slice() };
  }

  /* ================= 3. N 皇后 ================= */
  function nqueensSolve(n, maxSolutions) {
    maxSolutions = maxSolutions || 5;
    var sols = [], steps = [], queens = [];
    for (var i = 0; i < n; i++) queens.push(-1);
    var cols = {}, d1 = {}, d2 = {}, conflicts = 0;

    function bt(row) {
      if (sols.length >= maxSolutions || steps.length > 20000) return;
      if (row === n) {
        sols.push(queens.slice());
        steps.push({ type: "solution", board: queens.slice(), msg: "找到一个解！" });
        return;
      }
      for (var col = 0; col < n; col++) {
        if (steps.length > 20000) return;
        if (cols[col] || d1[row - col] || d2[row + col]) {
          conflicts++;
          steps.push({ type: "conflict", row: row, col: col, board: queens.slice(),
                       msg: "第 " + row + " 行第 " + col + " 列被攻击，换一列" });
          continue;
        }
        queens[row] = col; cols[col] = 1; d1[row - col] = 1; d2[row + col] = 1;
        steps.push({ type: "place", row: row, col: col, board: queens.slice(),
                     msg: "在第 " + row + " 行第 " + col + " 列放置皇后" });
        bt(row + 1);
        queens[row] = -1; delete cols[col]; delete d1[row - col]; delete d2[row + col];
        if (steps.length < 20000) {
          steps.push({ type: "backtrack", row: row, col: col, board: queens.slice(),
                       msg: "第 " + row + " 行此路不通，撤回" });
        }
      }
    }
    bt(0);
    return { n: n, solutions: sols, solutionCount: sols.length, steps: steps, conflicts: conflicts };
  }

  /* ================= 4. 蒙特卡罗 ================= */
  function monteCarlo(total, keepPoints) {
    total = total || 3000;
    keepPoints = keepPoints || 1500;
    var inside = 0, pts = [], every = Math.max(1, Math.floor(total / keepPoints));
    for (var i = 0; i < total; i++) {
      var x = Math.random(), y = Math.random();
      var hit = (x - 0.5) * (x - 0.5) + (y - 0.5) * (y - 0.5) <= 0.25;
      if (hit) inside++;
      if (i % every === 0 && pts.length < keepPoints) pts.push([+x.toFixed(4), +y.toFixed(4), hit ? 1 : 0]);
    }
    var pi = 4 * inside / total;
    return {
      total: total, inside: inside, ratio: inside / total, pi: pi,
      error: Math.abs(pi - Math.PI), points: pts
    };
  }

  /* ================= 5. 曼德勃罗集 ================= */
  function mandelbrotRender(width, height, cx, cy, zoom, maxIter) {
    width = width || 120; height = height || 80;
    cx = cx === undefined ? -0.5 : cx; cy = cy === undefined ? 0 : cy;
    zoom = zoom || 1; maxIter = maxIter || 60;
    var span = 3.0 / zoom, aspect = width / height;
    var x0 = cx - span / 2, y0 = cy - (span / aspect) / 2;
    var dx = span / width, dy = (span / aspect) / height;
    var grid = [], insideCount = 0;
    for (var j = 0; j < height; j++) {
      var row = [], py = y0 + j * dy;
      for (var i = 0; i < width; i++) {
        var px = x0 + i * dx, zx = 0, zy = 0, it = 0;
        while (it < maxIter) {
          var zx2 = zx * zx, zy2 = zy * zy;
          if (zx2 + zy2 > 4) break;
          zy = 2 * zx * zy + py; zx = zx2 - zy2 + px; it++;
        }
        if (it >= maxIter) insideCount++;
        row.push(it);
      }
      grid.push(row);
    }
    return { width: width, height: height, grid: grid, insideCount: insideCount,
             center: [cx, cy], zoom: zoom, maxIter: maxIter };
  }

  /* ================= 6. A* 寻路 ================= */
  function makeMaze(rows, cols) {
    var g = [];
    for (var r = 0; r < rows; r++) { var row = []; for (var c = 0; c < cols; c++) row.push(0); g.push(row); }
    var walls = Math.floor(rows * cols / 5);
    for (var k = 0; k < walls; k++) {
      g[Math.floor(Math.random() * rows)][Math.floor(Math.random() * cols)] = 1;
    }
    g[0][0] = 0; g[rows - 1][cols - 1] = 0;
    return g;
  }
  function pathSearch(grid, start, goal, algo) {
    algo = algo || "astar";
    var rows = grid.length, cols = grid[0].length;
    var dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];
    var visited = [], came = {}, found = false;
    function key(r, c) { return r + "," + c; }
    function ok(r, c) { return r >= 0 && r < rows && c >= 0 && c < cols && grid[r][c] === 0; }
    if (!ok(start[0], start[1]) || !ok(goal[0], goal[1])) {
      return { visited: [], path: [], found: false, visitedCount: 0, pathLength: 0, algo: algo };
    }
    if (algo === "bfs") {
      var q = [start], seen = {}; seen[key(start[0], start[1])] = 1;
      while (q.length) {
        var cur = q.shift();
        visited.push(cur);
        if (cur[0] === goal[0] && cur[1] === goal[1]) { found = true; break; }
        for (var i = 0; i < dirs.length; i++) {
          var nr = cur[0] + dirs[i][0], nc = cur[1] + dirs[i][1];
          if (ok(nr, nc) && !seen[key(nr, nc)]) {
            seen[key(nr, nc)] = 1; came[key(nr, nc)] = cur; q.push([nr, nc]);
          }
        }
      }
    } else if (algo === "dfs") {
      var st = [start], seen2 = {}; seen2[key(start[0], start[1])] = 1;
      while (st.length) {
        var cur2 = st.pop();
        visited.push(cur2);
        if (cur2[0] === goal[0] && cur2[1] === goal[1]) { found = true; break; }
        for (var j = dirs.length - 1; j >= 0; j--) {
          var nr2 = cur2[0] + dirs[j][0], nc2 = cur2[1] + dirs[j][1];
          if (ok(nr2, nc2) && !seen2[key(nr2, nc2)]) {
            seen2[key(nr2, nc2)] = 1; came[key(nr2, nc2)] = cur2; st.push([nr2, nc2]);
          }
        }
      }
    } else {
      // A* / Dijkstra 简化版：用优先队列模拟（数组排序，规模小够用）
      var dist = {}, open = [start]; dist[key(start[0], start[1])] = 0;
      var closed = {};
      function h(a) { return algo === "astar" ? Math.abs(a[0] - goal[0]) + Math.abs(a[1] - goal[1]) : 0; }
      while (open.length) {
        open.sort(function (p, q2) {
          return (dist[key(p[0], p[1])] + h(p)) - (dist[key(q2[0], q2[1])] + h(q2));
        });
        var cur3 = open.shift();
        if (closed[key(cur3[0], cur3[1])]) continue;
        closed[key(cur3[0], cur3[1])] = 1;
        visited.push(cur3);
        if (cur3[0] === goal[0] && cur3[1] === goal[1]) { found = true; break; }
        for (var m = 0; m < dirs.length; m++) {
          var nr3 = cur3[0] + dirs[m][0], nc3 = cur3[1] + dirs[m][1];
          if (!ok(nr3, nc3)) continue;
          var nd = dist[key(cur3[0], cur3[1])] + 1;
          var k3 = key(nr3, nc3);
          if (dist[k3] === undefined || nd < dist[k3]) {
            dist[k3] = nd; came[k3] = cur3; open.push([nr3, nc3]);
          }
        }
      }
    }
    var path = [];
    if (found) {
      var node = goal;
      while (node) { path.push(node); node = came[key(node[0], node[1])]; }
      path.reverse();
    }
    return { visited: visited, path: path, found: found,
             visitedCount: visited.length, pathLength: path.length, algo: algo };
  }

  /* ================= 7. 蚁群算法 ================= */
  function acoRandomCities(n) {
    var a = [];
    for (var i = 0; i < n; i++) a.push([+(0.05 + Math.random() * 0.9).toFixed(4), +(0.05 + Math.random() * 0.9).toFixed(4)]);
    return a;
  }
  function acoDist(a, b) { return Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])); }
  function acoTourLength(cities, tour) {
    var t = 0;
    for (var i = 0; i < tour.length; i++) t += acoDist(cities[tour[i]], cities[tour[(i + 1) % tour.length]]);
    return t;
  }
  function acoRun(cities, ants, iterations) {
    ants = ants || 20; iterations = iterations || 30;
    var n = cities.length;
    var pher = [], dist = [];
    for (var i = 0; i < n; i++) {
      pher.push([]); dist.push([]);
      for (var j = 0; j < n; j++) { pher[i].push(1.0); dist[i].push(acoDist(cities[i], cities[j])); }
    }
    var best = null, bestLen = Infinity, history = [];
    for (var it = 0; it < iterations; it++) {
      var tours = [], lens = [];
      for (var a = 0; a < ants; a++) {
        var start = Math.floor(Math.random() * n), tour = [start], unv = {};
        for (var u = 0; u < n; u++) if (u !== start) unv[u] = 1;
        var cur = start;
        while (Object.keys(unv).length) {
          var cand = Object.keys(unv).map(Number), ws = [], tot = 0;
          for (var ci = 0; ci < cand.length; ci++) {
            var nx = cand[ci], d = dist[cur][nx];
            var w = pher[cur][nx] * Math.pow(1 / (d > 1e-9 ? d : 1e9), 3);
            ws.push([nx, w]); tot += w;
          }
          var r = Math.random() * tot, pick = cand[cand.length - 1], acc = 0;
          for (var wi = 0; wi < ws.length; wi++) { acc += ws[wi][1]; if (acc >= r) { pick = ws[wi][0]; break; } }
          tour.push(pick); delete unv[pick]; cur = pick;
        }
        var len = acoTourLength(cities, tour);
        tours.push(tour); lens.push(len);
        if (len < bestLen) { bestLen = len; best = tour.slice(); }
      }
      for (var p = 0; p < n; p++) for (var q = 0; q < n; q++) pher[p][q] *= 0.6;
      for (var ti = 0; ti < tours.length; ti++) {
        var add = 100 / (lens[ti] || 1);
        for (var k = 0; k < n; k++) {
          var x = tours[ti][k], y = tours[ti][(k + 1) % n];
          pher[x][y] += add; pher[y][x] += add;
        }
      }
      history.push(+bestLen.toFixed(4));
    }
    return { cities: cities, bestTour: best, bestLength: +bestLen.toFixed(4),
             history: history, iterations: iterations, ants: ants };
  }

  /* ================= 8. KMP ================= */
  function kmpNext(pattern) {
    var n = pattern.length, nxt = [];
    for (var i = 0; i < n; i++) nxt.push(0);
    var j = 0;
    for (var i2 = 1; i2 < n; i2++) {
      while (j > 0 && pattern[i2] !== pattern[j]) j = nxt[j - 1];
      if (pattern[i2] === pattern[j]) j++;
      nxt[i2] = j;
    }
    return nxt;
  }
  function kmpSearch(text, pattern) {
    var nxt = kmpNext(pattern), matches = [], steps = [], j = 0, cmp = 0;
    for (var i = 0; i < text.length; i++) {
      while (j > 0 && text[i] !== pattern[j]) {
        steps.push({ i: i, j: j, type: "fallback", msg: "失配：靠 next 右滑" });
        j = nxt[j - 1];
      }
      cmp++;
      if (text[i] === pattern[j]) {
        steps.push({ i: i, j: j, type: "match", msg: "匹配成功" });
        j++;
        if (j === pattern.length) {
          matches.push(i - pattern.length + 1);
          steps.push({ i: i, j: j - 1, type: "found", msg: "找到匹配！" });
          j = j > 0 ? nxt[j - 1] : 0;
        }
      } else {
        steps.push({ i: i, j: j, type: "mismatch", msg: "首字符不匹配" });
      }
    }
    return { text: text, pattern: pattern, matches: matches, next: nxt,
             steps: steps, comparisons: cmp };
  }

  /* ================= 9. 分治排序（快排/归并） ================= */
  function divideSortSteps(input, algo) {
    var a = input.slice(), steps = [], c = 0, w = 0;
    function rec(desc, ai, bi, mark, lo, hi) {
      steps.push({ list: a.slice(), desc: desc,
        a: ai === undefined ? -1 : ai, b: bi === undefined ? -1 : bi,
        mark: mark === undefined ? -1 : mark,
        lo: lo === undefined ? -1 : lo, hi: hi === undefined ? -1 : hi,
        c: c, w: w });
    }
    function quick(lo, hi) {
      if (lo >= hi) { if (lo === hi) rec('区间只剩 1 个元素', -1, -1, lo, lo, hi); return; }
      var pivot = a[hi];
      rec('选定基准值 ' + pivot, -1, -1, hi, lo, hi);
      var i = lo;
      for (var j = lo; j < hi; j++) {
        c++;
        rec('比较 ' + a[j] + ' 与基准 ' + pivot, j, hi, -1, lo, hi);
        if (a[j] < pivot) {
          if (i !== j) { var t = a[i]; a[i] = a[j]; a[j] = t; w++;
            rec(a[i] + ' < ' + pivot + '，换到左区', i, j, -1, lo, hi); }
          i++;
        }
      }
      var t2 = a[i]; a[i] = a[hi]; a[hi] = t2; w++;
      rec('基准 ' + pivot + ' 归位到索引 ' + i, -1, -1, i, lo, hi);
      quick(lo, i - 1); quick(i + 1, hi);
    }
    function mergeSort(lo, hi) {
      if (lo >= hi) return;
      var mid = (lo + hi) >> 1;
      rec('把区间 [' + lo + ', ' + hi + '] 对半切', -1, -1, -1, lo, hi);
      mergeSort(lo, mid); mergeSort(mid + 1, hi);
      var left = a.slice(lo, mid + 1), right = a.slice(mid + 1, hi + 1);
      var i = 0, j = 0, k = lo;
      while (i < left.length && j < right.length) {
        c++;
        if (left[i] <= right[j]) { a[k] = left[i]; rec('取较小的 ' + left[i], -1, -1, k, lo, hi); i++; }
        else { a[k] = right[j]; rec('取较小的 ' + right[j], -1, -1, k, lo, hi); j++; }
        w++; k++;
      }
      while (i < left.length) { a[k] = left[i]; w++; rec('填入剩余 ' + left[i], -1, -1, k, lo, hi); i++; k++; }
      while (j < right.length) { a[k] = right[j]; w++; rec('填入剩余 ' + right[j], -1, -1, k, lo, hi); j++; k++; }
      rec('区间 [' + lo + ', ' + hi + '] 合并完成', -1, -1, -1, lo, hi);
    }
    if (algo === 'merge') mergeSort(0, a.length - 1); else quick(0, a.length - 1);
    return { algo: algo, sorted: a.slice(), steps: steps, totalCompares: c, totalWrites: w };
  }

  /* ================= 10. 二分查找 ================= */
  function binarySearch(arr, target) {
    var a = arr.slice().sort(function (x, y) { return x - y; });
    var lo = 0, hi = a.length - 1, steps = [], cmp = 0, found = -1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1; cmp++;
      steps.push({ lo: lo, hi: hi, mid: mid, arr: a.slice(), type: 'probe',
        msg: '范围 [' + lo + ', ' + hi + ']，中点 ' + mid + '（值 ' + a[mid] + '）', comparisons: cmp });
      if (a[mid] === target) { found = mid;
        steps.push({ lo: lo, hi: hi, mid: mid, arr: a.slice(), type: 'found',
          msg: '命中！在索引 ' + mid, comparisons: cmp }); break; }
      else if (a[mid] < target) { steps.push({ lo: lo, hi: hi, mid: mid, arr: a.slice(),
        type: 'right', msg: a[mid] + ' < ' + target + '，丢弃左半', comparisons: cmp }); lo = mid + 1; }
      else { steps.push({ lo: lo, hi: hi, mid: mid, arr: a.slice(),
        type: 'left', msg: a[mid] + ' > ' + target + '，丢弃右半', comparisons: cmp }); hi = mid - 1; }
    }
    return { target: target, array: a, found: found, steps: steps, comparisons: cmp,
             maxPossible: Math.ceil(Math.log2(a.length)) + 1, linearWorst: a.length };
  }

  /* ================= 11. 快速幂 ================= */
  function fastPower(base, exp, mod) {
    mod = mod || 0;
    var result = 1, b = base, e = exp, steps = [], bitIndex = 0;
    while (e > 0) {
      var bit = e & 1;
      steps.push({ bitIndex: bitIndex, bit: bit, base: b, exp: e, result: result,
        msg: '指数 ' + e + ' 最低位 ' + bit + (bit ? ' → 乘进结果' : ' → 跳过') });
      if (bit) { result = result * b; if (mod) result %= mod; }
      b = b * b; if (mod) b %= mod;
      e >>= 1; bitIndex++;
    }
    steps.push({ bitIndex: bitIndex, bit: -1, base: b, exp: 0, result: result,
      msg: '计算结束，结果 = ' + result });
    return { base: base, exp: exp, mod: mod, result: result, steps: steps,
             naiveOps: exp, fastOps: exp > 0 ? exp.toString(2).length : 0,
             binaryExp: exp > 0 ? exp.toString(2) : '0' };
  }

  /* ================= 12. 图算法 ================= */
  function randomGraphJS(n, extra, seed) {
    n = n || 8;
    var pos = [], edges = [], seen = {};
    for (var i = 0; i < n; i++) {
      var ang = 2 * Math.PI * i / n;
      pos.push([+(0.5 + 0.38 * Math.cos(ang)).toFixed(4), +(0.5 + 0.38 * Math.sin(ang)).toFixed(4)]);
    }
    function add(u, v) {
      var key = Math.min(u, v) + '-' + Math.max(u, v);
      if (seen[key] || u === v) return;
      seen[key] = 1;
      edges.push({ u: u, v: v, w: 1 + Math.floor(Math.random() * 20) });
    }
    for (var k = 0; k < n - 1; k++) add(k, k + 1);
    for (var e2 = 0; e2 < (extra || 6); e2++) add(Math.floor(Math.random() * n), Math.floor(Math.random() * n));
    return { n: n, pos: pos, edges: edges, weighted: true };
  }
  function graphRun(graph, start, algo) {
    var n = graph.n, adj = [], i;
    for (i = 0; i < n; i++) adj.push([]);
    for (var ei = 0; ei < graph.edges.length; ei++) {
      var e = graph.edges[ei];
      adj[e.u].push([e.v, e.w]); adj[e.v].push([e.u, e.w]);
    }
    var order = [], dist = {}, parent = {}, steps = [];
    dist[start] = 0; parent[start] = null;
    if (algo === 'bfs') {
      var q = [start], seen = {}; seen[start] = 1;
      while (q.length) {
        var u = q.shift(); order.push(u);
        steps.push({ visit: u, dist: dist[u], order: order.slice(), msg: '出队 ' + u });
        for (var a1 = 0; a1 < adj[u].length; a1++) {
          var v1 = adj[u][a1][0];
          if (!seen[v1]) { seen[v1] = 1; parent[v1] = u; dist[v1] = dist[u] + 1;
            q.push(v1); steps.push({ visit: v1, order: order.slice(), msg: '发现 ' + v1 + ' 入队' }); }
        }
      }
    } else if (algo === 'dfs') {
      var st = [start], seen2 = {};
      while (st.length) {
        var u2 = st.pop();
        if (seen2[u2]) continue;
        seen2[u2] = 1; order.push(u2);
        steps.push({ visit: u2, order: order.slice(), msg: '访问 ' + u2 });
        for (var a2 = adj[u2].length - 1; a2 >= 0; a2--) {
          var v2 = adj[u2][a2][0];
          if (!seen2[v2]) { if (parent[v2] === undefined) parent[v2] = u2; st.push(v2); }
        }
      }
    } else {
      var done = {}, pq = [[0, start]];
      while (pq.length) {
        pq.sort(function (x, y) { return x[0] - y[0]; });
        var top = pq.shift(), d = top[0], u3 = top[1];
        if (done[u3]) continue;
        done[u3] = 1; order.push(u3);
        steps.push({ visit: u3, dist: d, order: order.slice(), msg: '取出最近的 ' + u3 + '（距离 ' + d + '）' });
        for (var a3 = 0; a3 < adj[u3].length; a3++) {
          var v3 = adj[u3][a3][0], w3 = adj[u3][a3][1], nd = d + w3;
          if (dist[v3] === undefined || nd < dist[v3]) {
            dist[v3] = nd; parent[v3] = u3; pq.push([nd, v3]);
          }
        }
      }
    }
    var tree = [];
    for (var key in parent) { if (parent[key] !== null && parent[key] !== undefined) tree.push([+parent[key], +key]); }
    return { algo: algo, graph: graph, start: start, order: order, dist: dist,
             tree: tree, steps: steps, visitedCount: order.length };
  }

  /* ================= 13. 二叉搜索树 ================= */
  function bstBuild(values) {
    var root = null, steps = [];
    function insert(node, v, path) {
      if (!node) { steps.push({ type: 'insert', val: v, path: path.slice(), msg: v + ' 放入空位' }); return { val: v, left: null, right: null }; }
      path.push(node.val);
      if (v < node.val) { steps.push({ type: 'compare', val: v, at: node.val, path: path.slice(), msg: v + ' < ' + node.val + '，往左' }); node.left = insert(node.left, v, path); }
      else if (v > node.val) { steps.push({ type: 'compare', val: v, at: node.val, path: path.slice(), msg: v + ' > ' + node.val + '，往右' }); node.right = insert(node.right, v, path); }
      else steps.push({ type: 'duplicate', val: v, path: path.slice(), msg: v + ' 已存在' });
      return node;
    }
    for (var i = 0; i < values.length; i++) root = insert(root, values[i], []);
    function inorder(nd) { return nd ? inorder(nd.left).concat([nd.val], inorder(nd.right)) : []; }
    function height(nd) { return nd ? 1 + Math.max(height(nd.left), height(nd.right)) : 0; }
    function count(nd) { return nd ? 1 + count(nd.left) + count(nd.right) : 0; }
    return { root: root, values: values, steps: steps, inorder: inorder(root),
             height: height(root), count: count(root) };
  }

  /* ================= 14. 堆 ================= */
  function heapDemo(values, pops) {
    var a = [], steps = [];
    function push(v) {
      a.push(v); var i = a.length - 1;
      steps.push({ type: 'push', heap: a.slice(), i: i, msg: '插入 ' + v });
      while (i > 0) {
        var p = (i - 1) >> 1;
        if (a[i] < a[p]) {
          var t = a[i]; a[i] = a[p]; a[p] = t;
          steps.push({ type: 'swap', heap: a.slice(), i: i, j: p, msg: '上浮交换' });
          i = p;
        } else { steps.push({ type: 'stable', heap: a.slice(), i: i, msg: '堆序满足，停止' }); break; }
      }
    }
    function pop() {
      if (!a.length) return null;
      var top = a[0], last = a.pop();
      steps.push({ type: 'pop', heap: a.slice(), i: 0, msg: '取出堆顶 ' + top });
      if (a.length) {
        a[0] = last;
        var i = 0;
        while (true) {
          var l = 2 * i + 1, r = 2 * i + 2, sm = i;
          if (l < a.length && a[l] < a[sm]) sm = l;
          if (r < a.length && a[r] < a[sm]) sm = r;
          if (sm === i) { steps.push({ type: 'stable', heap: a.slice(), i: i, msg: '停止下沉' }); break; }
          var t = a[i]; a[i] = a[sm]; a[sm] = t;
          steps.push({ type: 'swap', heap: a.slice(), i: i, j: sm, msg: '下沉交换' });
          i = sm;
        }
      }
      return top;
    }
    for (var i = 0; i < values.length; i++) push(values[i]);
    var afterPush = a.slice(), popped = [];
    for (var p = 0; p < (pops || 3) && a.length; p++) popped.push(pop());
    return { input: values, heapAfterPush: afterPush, popped: popped,
             heapAfterPop: a.slice(), steps: steps };
  }

  /* ================= 15. 0-1 背包 ================= */
  function knapsackSolve(weights, values, capacity) {
    var n = weights.length;
    var dp = [], i, j;
    for (i = 0; i <= n; i++) { dp.push([]); for (j = 0; j <= capacity; j++) dp[i].push(0); }
    for (i = 1; i <= n; i++) {
      for (j = 0; j <= capacity; j++) {
        var skip = dp[i - 1][j], w = weights[i - 1], v = values[i - 1];
        if (w <= j) dp[i][j] = Math.max(skip, dp[i - 1][j - w] + v);
        else dp[i][j] = skip;
      }
    }
    var picked = [], jj = capacity;
    for (i = n; i > 0; i--) {
      if (dp[i][jj] !== dp[i - 1][jj]) { picked.unshift(i); jj -= weights[i - 1]; }
    }
    return { weights: weights, values: values, capacity: capacity,
             maxValue: dp[n][capacity], table: dp, picked: picked };
  }

  /* ================= 16. LCS ================= */
  function lcsSolve(a, b) {
    var n = a.length, m = b.length, dp = [], i, j;
    for (i = 0; i <= n; i++) { dp.push([]); for (j = 0; j <= m; j++) dp[i].push(0); }
    for (i = 1; i <= n; i++) {
      for (j = 1; j <= m; j++) {
        if (a[i - 1] === b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
        else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
    var seq = [], ii = n, jjj = m;
    while (ii > 0 && jjj > 0) {
      if (a[ii - 1] === b[jjj - 1]) { seq.unshift(a[ii - 1]); ii--; jjj--; }
      else if (dp[ii - 1][jjj] >= dp[ii][jjj - 1]) ii--; else jjj--;
    }
    return { a: a, b: b, length: dp[n][m], subsequence: seq.join(''), table: dp };
  }

  /* ================= 17. 素数筛 ================= */
  function primeSieve(n) {
    var isP = [], i, j;
    for (i = 0; i <= n; i++) isP.push(true);
    isP[0] = isP[1] = false;
    var steps = [];
    for (i = 2; i * i <= n; i++) {
      if (isP[i]) {
        var removed = [];
        for (j = i * i; j <= n; j += i) { if (isP[j]) { isP[j] = false; removed.push(j); } }
        if (steps.length < 100) steps.push({ prime: i, removed: removed.slice(0, 100),
          msg: '以 ' + i + ' 为筛，划掉 ' + removed.length + ' 个倍数' });
      }
    }
    var primes = [];
    for (i = 2; i <= n; i++) if (isP[i]) primes.push(i);
    return { n: n, primes: primes, primeCount: primes.length, steps: steps, isPrime: isP };
  }

  /* ================= 18. 约瑟夫环 ================= */
  function josephusSimulate(n, k) {
    var p = [], i;
    for (i = 1; i <= n; i++) p.push(i);
    var order = [], frames = [], idx = 0;
    while (p.length) {
      idx = (idx + k - 1) % p.length;
      var out = p.splice(idx, 1)[0];
      order.push(out);
      if (frames.length < 300) frames.push({ out: out, remaining: p.slice(), round: order.length });
    }
    return { n: n, k: k, order: order, last: order[order.length - 1], frames: frames };
  }
  function josephusFormula(n, k) {
    var f = 0;
    for (var i = 2; i <= n; i++) f = (f + k) % i;
    return { n: n, k: k, survivor: f + 1 };
  }

  /* ================= 19. 一致性哈希 ================= */
  var RING = 100000;
  function chHash(s) {
    // FNV-1a 变体：比简单的移位叠加分布更均匀（模拟后端的 MD5 效果）
    var h = 2166136261 >>> 0;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = (h * 16777619) >>> 0;
    }
    // 再做一次混合，减少低位规律性
    h ^= h >>> 15;
    h = (h * 2246822507) >>> 0;
    h ^= h >>> 13;
    return h % RING;
  }
  function chBuildRing(servers, vnodes) {
    var ring = [];
    for (var i = 0; i < servers.length; i++) {
      for (var v = 0; v < (vnodes || 1); v++) {
        var name = (vnodes || 1) === 1 ? servers[i] : servers[i] + '#' + v;
        var pos = chHash(name);
        ring.push({ pos: pos, angle360: Math.floor(pos * 360 / RING) % 360, server: servers[i], vnode: name });
      }
    }
    ring.sort(function (a, b) { return a.pos - b.pos; });
    return ring;
  }
  function chLocate(ring, key) {
    if (!ring.length) return { key: key, server: null };
    var pos = chHash(key), ans = 0;
    for (var i = 0; i < ring.length; i++) { if (ring[i].pos >= pos) { ans = i; break; } }
    if (ring[ring.length - 1].pos < pos) ans = 0;
    return { key: key, pos: pos, server: ring[ans].server };
  }
  function chDistribute(keys, servers, vnodes) {
    var ring = chBuildRing(servers, vnodes), counts = {}, details = [];
    for (var i = 0; i < servers.length; i++) counts[servers[i]] = 0;
    for (var k = 0; k < keys.length; k++) {
      var loc = chLocate(ring, keys[k]);
      if (loc.server) counts[loc.server]++;
      details.push(loc);
    }
    return { servers: servers, vnodes: vnodes, ring: ring, counts: counts, details: details, keyCount: keys.length };
  }

  /* ================= 20. 拓扑排序 ================= */
  function randomDagJS(n) {
    n = n || 7;
    var pos = [], edges = [], seen = {};
    for (var i = 0; i < n; i++) {
      pos.push([+(0.08 + 0.84 * i / Math.max(1, n - 1)).toFixed(4),
                +(0.15 + 0.7 * ((i * 7) % 5) / 4).toFixed(4)]);
    }
    function add(u, v) {
      if (u >= v) return;
      var key = u + '-' + v;
      if (seen[key]) return;
      seen[key] = 1; edges.push({ u: u, v: v });
    }
    for (var j = 0; j < n - 1; j++) add(j, j + 1);
    for (var e = 0; e < 4; e++) { var a = Math.floor(Math.random() * n), b = Math.floor(Math.random() * n); add(Math.min(a, b), Math.max(a, b)); }
    return { n: n, pos: pos, edges: edges };
  }
  function topoKahn(graph) {
    var n = graph.n, indeg = [], adj = [], i;
    for (i = 0; i < n; i++) { indeg.push(0); adj.push([]); }
    for (i = 0; i < graph.edges.length; i++) { adj[graph.edges[i].u].push(graph.edges[i].v); indeg[graph.edges[i].v]++; }
    var q = [], order = [], steps = [];
    for (i = 0; i < n; i++) if (indeg[i] === 0) q.push(i);
    steps.push({ type: 'init', indeg: indeg.slice(), queue: q.slice(), order: [], msg: '入度为0的节点：' + q });
    while (q.length) {
      var u = q.shift(); order.push(u);
      for (var a = 0; a < adj[u].length; a++) {
        var v = adj[u][a]; indeg[v]--;
        if (indeg[v] === 0) q.push(v);
      }
      steps.push({ type: 'process', node: u, indeg: indeg.slice(), queue: q.slice(), order: order.slice(), msg: '取出 ' + u });
    }
    return { algorithm: 'kahn', graph: graph, order: order, steps: steps, hasCycle: order.length !== n };
  }

  /* ================= 21. 滑动窗口 ================= */
  function swFixed(nums, k) {
    var n = nums.length, s = 0, i;
    for (i = 0; i < k; i++) s += nums[i];
    var best = s, bestI = 0, steps = [];
    steps.push({ lo: 0, hi: k - 1, sum: s, best: best, bestRange: [0, k - 1], msg: '初始窗口和 ' + s });
    for (i = k; i < n; i++) {
      s += nums[i] - nums[i - k];
      var lo = i - k + 1;
      if (s > best) { best = s; bestI = lo; }
      steps.push({ lo: lo, hi: i, sum: s, best: best, bestRange: [bestI, bestI + k - 1],
        msg: '窗口 [' + lo + ', ' + i + '] 和 = ' + s });
    }
    return { nums: nums, k: k, maxSum: best, bestRange: [bestI, bestI + k - 1], steps: steps };
  }
  function swMin(nums, target) {
    var lo = 0, s = 0, best = nums.length + 1, bestRange = null, steps = [];
    for (var hi = 0; hi < nums.length; hi++) {
      s += nums[hi];
      while (s >= target && lo <= hi) {
        if (hi - lo + 1 < best) { best = hi - lo + 1; bestRange = [lo, hi]; }
        s -= nums[lo]; lo++;
      }
      steps.push({ lo: lo, hi: hi, sum: s, best: best <= nums.length ? best : null, msg: 'hi=' + hi + ' lo=' + lo });
    }
    return { nums: nums, target: target, minLength: best <= nums.length ? best : 0, bestRange: bestRange, steps: steps };
  }
  function swLongest(text) {
    var last = {}, lo = 0, best = 0, bestRange = null, steps = [];
    for (var hi = 0; hi < text.length; hi++) {
      var ch = text[hi];
      if (last[ch] !== undefined && last[ch] >= lo) lo = last[ch] + 1;
      last[ch] = hi;
      if (hi - lo + 1 > best) { best = hi - lo + 1; bestRange = [lo, hi]; }
      steps.push({ lo: lo, hi: hi, ch: ch, best: best, msg: '窗口 [' + lo + ', ' + hi + '] 长度 ' + (hi - lo + 1) });
    }
    return { text: text, length: best,
             substring: bestRange ? text.substring(bestRange[0], bestRange[1] + 1) : '',
             bestRange: bestRange, steps: steps };
  }

  /* ================= 导出 ================= */
  global.AlgoExt = {
    // 生命游戏
    lifeEmpty: lifeEmpty, lifeRandom: lifeRandom, lifeStep: lifeStep,
    lifeRun: lifeRun, lifePlace: lifePlace, LIFE_PATTERNS: LIFE_PATTERNS,
    // 汉诺塔
    hanoiSolve: hanoiSolve, hanoiSimulate: hanoiSimulate,
    // N 皇后
    nqueensSolve: nqueensSolve,
    // 蒙特卡罗
    monteCarlo: monteCarlo,
    // 曼德勃罗
    mandelbrotRender: mandelbrotRender,
    // 寻路
    makeMaze: makeMaze, pathSearch: pathSearch,
    // 蚁群
    acoRandomCities: acoRandomCities, acoRun: acoRun, acoTourLength: acoTourLength,
    // KMP
    kmpNext: kmpNext, kmpSearch: kmpSearch,
    // 第三批
    divideSortSteps: divideSortSteps,
    binarySearch: binarySearch,
    fastPower: fastPower,
    randomGraphJS: randomGraphJS, graphRun: graphRun,
    bstBuild: bstBuild,
    heapDemo: heapDemo,
    knapsackSolve: knapsackSolve,
    lcsSolve: lcsSolve,
    primeSieve: primeSieve,
    josephusSimulate: josephusSimulate, josephusFormula: josephusFormula,
    chBuildRing: chBuildRing, chLocate: chLocate, chDistribute: chDistribute, chHash: chHash,
    randomDagJS: randomDagJS, topoKahn: topoKahn,
    swFixed: swFixed, swMin: swMin, swLongest: swLongest
  };
})(window);
