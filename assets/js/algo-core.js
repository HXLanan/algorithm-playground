/* =========================================================
 * algo-core.js —— 前端兜底算法库
 * ---------------------------------------------------------
 * 作用：当后端不可用（离线打开 HTML）时，前端用本文件在本地
 *       生成与后端一致的数据结构，保证页面永远能演示。
 * 设计：与 server/algo/*.py 的返回结构保持一致。
 * ========================================================= */
(function (global) {
  "use strict";

  /* ---------------- 排序 ---------------- */
  var SORT_SUPPORTED = ["bubble", "selection", "insertion"];
  var SORT_NAMES = { bubble: "冒泡排序", selection: "选择排序", insertion: "插入排序" };

  function randomArray(n) {
    var a = [];
    for (var i = 1; i <= n; i++) a.push(i);
    for (var k = a.length - 1; k > 0; k--) {
      var j = Math.floor(Math.random() * (k + 1));
      var t = a[k]; a[k] = a[j]; a[j] = t;
    }
    return a;
  }

  function buildSortSteps(input, algo) {
    algo = algo || "bubble";
    if (SORT_SUPPORTED.indexOf(algo) < 0) throw new Error("不支持的算法: " + algo);
    var a = input.slice();
    var n = a.length;
    var steps = [];
    var c = 0, w = 0;

    function rec(desc, ai, bi, mark) {
      steps.push({
        list: a.slice(),
        desc: desc,
        a: ai === undefined ? -1 : ai,
        b: bi === undefined ? -1 : bi,
        mark: mark === undefined ? -1 : mark,
        c: c, w: w
      });
    }

    var i, j, t;
    if (algo === "bubble") {
      for (i = 0; i < n - 1; i++) {
        var swapped = false;
        for (j = 0; j < n - 1 - i; j++) {
          c++;
          rec("比较位置 " + j + " 与 " + (j + 1) + "（" + a[j] + " / " + a[j + 1] + "）", j, j + 1);
          if (a[j] > a[j + 1]) {
            t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
            w++; swapped = true;
            rec("交换：较大的 " + a[j + 1] + " 泡到右边", j, j + 1);
          }
        }
        rec("第 " + (i + 1) + " 轮结束，最右 " + (i + 1) + " 位已确定", -1, -1, n - i - 1);
        if (!swapped) {
          rec("本轮未发生交换 → 已经有序，提前结束（冒泡的优化点）");
          break;
        }
      }
    } else if (algo === "selection") {
      for (i = 0; i < n - 1; i++) {
        var minIdx = i;
        rec("本轮从位置 " + i + " 开始找最小值", i, -1, i);
        for (j = i + 1; j < n; j++) {
          c++;
          rec("比较候选最小 " + a[minIdx] + " 与 " + a[j], minIdx, j);
          if (a[j] < a[minIdx]) {
            minIdx = j;
            rec("发现更小值 " + a[j] + "，更新最小位置为 " + j, -1, -1, j);
          }
        }
        if (minIdx !== i) {
          t = a[i]; a[i] = a[minIdx]; a[minIdx] = t;
          w++;
          rec("把最小值 " + a[i] + " 放到位置 " + i, i, minIdx);
        }
      }
    } else {
      for (i = 1; i < n; i++) {
        var key = a[i];
        rec("取出位置 " + i + " 的 " + key + " 作为“新牌”", -1, -1, i);
        j = i - 1;
        while (j >= 0) {
          c++;
          rec("比较：" + a[j] + " 与手上的 " + key, j, i);
          if (a[j] <= key) break;
          a[j + 1] = a[j];
          w++;
          rec("把较大的 " + a[j + 1] + " 右移一位", -1, -1, j + 1);
          j--;
        }
        if (a[j + 1] !== key) {
          a[j + 1] = key;
          w++;
          rec("把新牌 " + key + " 插入到位置 " + (j + 1), -1, -1, j + 1);
        }
      }
    }

    return {
      algo: algo,
      algoName: SORT_NAMES[algo],
      input: input.slice(),
      sorted: a.slice(),
      steps: steps,
      totalCompares: c,
      totalWrites: w,
      count: n
    };
  }

  /* ---------------- 麦粒棋盘（BigInt） ---------------- */
  function buildWheatBoard(cells) {
    cells = cells || 64;
    var rows = [];
    var total = BigInt(0);
    for (var i = 1; i <= cells; i++) {
      var g = BigInt(1) << BigInt(i - 1);
      total += g;
      rows.push({
        cell: i,
        grain: g.toString(),
        grain_str: shortBig(g),
        cumulative: total.toString(),
        cumulative_str: shortBig(total)
      });
    }
    var GRAIN_GRAM = 0.03;
    var tons = Number(total) * GRAIN_GRAM / 1000000;
    return {
      cells: cells,
      rows: rows,
      total_grain: total.toString(),
      total_grain_str: shortBig(total),
      total_tons: tons,
      total_tons_str: shortBig(BigInt(Math.floor(tons))),
      world_years: tons / 780000000
    };
  }

  function shortBig(v) {
    var s = v.toString();
    if (s.length <= 8) return s;
    return s[0] + "." + s.slice(1, 3) + "e" + (s.length - 1);
  }

  /* ---------------- 斐波那契 ---------------- */
  function fibIter(n) {
    if (n <= 0) return 0;
    if (n <= 2) return 1;
    var a = 1, b = 1, c;
    for (var i = 3; i <= n; i++) { c = a + b; a = b; b = c; }
    return b;
  }

  function buildFibSequence(months) {
    months = months === undefined ? 20 : months;
    var details = [];
    for (var m = 0; m <= months; m++) {
      var total = fibIter(m);
      var newborn = (m < 2) ? total : (fibIter(m) - fibIter(m - 1));
      details.push({
        month: m,
        total: total,
        newborn: newborn,
        formula: m >= 2
          ? ("F(" + m + ") = F(" + (m - 1) + ") + F(" + (m - 2) + ") = " +
             fibIter(m - 1) + " + " + fibIter(m - 2))
          : "起始条件"
      });
    }
    return {
      months: months,
      seq: details.map(function (d) { return d.total; }),
      details: details
    };
  }

  /* ---------------- 遗传算法 ---------------- */
  var GOLD = [0.72, 0.66];

  function gFitness(x, y) {
    var d = Math.sqrt((x - GOLD[0]) * (x - GOLD[0]) + (y - GOLD[1]) * (y - GOLD[1]));
    return 1 / (1 + d * d);
  }

  function gRandomPopulation(size) {
    var pop = [];
    for (var i = 0; i < size; i++) {
      pop.push([0.02 + Math.random() * 0.96, 0.02 + Math.random() * 0.96]);
    }
    return pop;
  }

  function gEvolve(pop) {
    var scored = pop.slice().sort(function (p, q) {
      return gFitness(q[0], q[1]) - gFitness(p[0], p[1]);
    });
    var weights = scored.map(function (p) { return gFitness(p[0], p[1]); });
    var total = weights.reduce(function (s, v) { return s + v; }, 0);

    function pick() {
      if (total <= 0) return scored[Math.floor(Math.random() * scored.length)];
      var r = Math.random() * total, acc = 0;
      for (var i = 0; i < scored.length; i++) {
        acc += weights[i];
        if (acc >= r) return scored[i];
      }
      return scored[scored.length - 1];
    }

    var next = [scored[0].slice()];   // 精英保留
    while (next.length < pop.length) {
      var pa = pick(), pb = pick();
      var cx = Math.random() < 0.5 ? pa[0] : pb[0];
      var cy = Math.random() < 0.5 ? pa[1] : pb[1];
      if (Math.random() < 0.15) {
        cx += (Math.random() * 2 - 1) * 0.03;
        cy += (Math.random() * 2 - 1) * 0.03;
      }
      next.push([Math.min(0.99, Math.max(0.01, cx)), Math.min(0.99, Math.max(0.01, cy))]);
    }
    return next;
  }

  function gRun(pop, generations) {
    generations = generations || 1;
    for (var i = 0; i < generations; i++) pop = gEvolve(pop);
    var best = pop[0], bf = gFitness(best[0], best[1]);
    for (var k = 1; k < pop.length; k++) {
      var f = gFitness(pop[k][0], pop[k][1]);
      if (f > bf) { bf = f; best = pop[k]; }
    }
    var avg = pop.reduce(function (s, p) { return s + gFitness(p[0], p[1]); }, 0) / pop.length;
    return {
      gold: GOLD.slice(),
      population: pop,
      size: pop.length,
      best: { x: best[0], y: best[1], fitness: bf },
      average_fitness: avg,
      generations: generations
    };
  }

  /* ---------------- 导出 ---------------- */
  global.AlgoCore = {
    SORT_SUPPORTED: SORT_SUPPORTED,
    SORT_NAMES: SORT_NAMES,
    randomArray: randomArray,
    buildSortSteps: buildSortSteps,
    buildWheatBoard: buildWheatBoard,
    shortBig: shortBig,
    fibIter: fibIter,
    buildFibSequence: buildFibSequence,
    gFitness: gFitness,
    gRandomPopulation: gRandomPopulation,
    gRun: gRun,
    GOLD: GOLD
  };
})(window);
