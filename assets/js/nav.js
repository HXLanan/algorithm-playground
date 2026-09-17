/* =========================================================
 * nav.js —— 顶部导航（25 个算法页，按分类分组）
 * ========================================================= */
(function () {
  "use strict";
  var groups = [
    {
      label: "排序",
      pages: [
        { href: 'sort.html', label: '简单排序' },
        { href: 'divide-sort.html', label: '快排/归并' },
        { href: 'heap.html', label: '堆与优先队列' }
      ]
    },
    {
      label: "查找",
      pages: [
        { href: 'binary-search.html', label: '二分查找' },
        { href: 'sliding-window.html', label: '滑动窗口' },
        { href: 'kmp.html', label: 'KMP 匹配' },
        { href: 'fast-power.html', label: '快速幂' }
      ]
    },
    {
      label: "图与树",
      pages: [
        { href: 'graph.html', label: '图算法' },
        { href: 'pathfinding.html', label: 'A* 寻路' },
        { href: 'topo-sort.html', label: '拓扑排序' },
        { href: 'bst.html', label: '二叉搜索树' }
      ]
    },
    {
      label: "回溯与DP",
      pages: [
        { href: 'nqueens.html', label: 'N 皇后' },
        { href: 'knapsack.html', label: '0-1 背包' },
        { href: 'lcs.html', label: '最长公共子序列' }
      ]
    },
    {
      label: "数学",
      pages: [
        { href: 'wheat.html', label: '麦粒棋盘' },
        { href: 'fibonacci.html', label: '兔子农场' },
        { href: 'hanoi.html', label: '汉诺塔' },
        { href: 'prime-sieve.html', label: '素数筛' },
        { href: 'josephus.html', label: '约瑟夫环' },
        { href: 'montecarlo.html', label: '蒙特卡罗' },
        { href: 'mandelbrot.html', label: '曼德勃罗集' }
      ]
    },
    {
      label: "智能与涌现",
      pages: [
        { href: 'genetic.html', label: '遗传算法' },
        { href: 'aco.html', label: '蚁群算法' },
        { href: 'life.html', label: '生命游戏' }
      ]
    },
    {
      label: "工程",
      pages: [
        { href: 'consistent-hash.html', label: '一致性哈希' }
      ]
    }
  ];

  var active = window.__ALGO_ACTIVE__ || 'index.html';
  var bar = document.createElement('nav');
  bar.className = 'topbar';

  var brand = document.createElement('a');
  brand.className = 'brand';
  brand.href = 'index.html';
  brand.textContent = '🧮 Algo Playground';
  bar.appendChild(brand);

  // 题库入口（放在最前面，方便快速进入）
  var libGroup = document.createElement('span');
  libGroup.className = 'navgroup';
  libGroup.textContent = '刷题';
  bar.appendChild(libGroup);

  var libLink = document.createElement('a');
  libLink.className = 'navlink' + (active === 'problems.html' ? ' active' : '');
  libLink.href = 'problems.html';
  libLink.textContent = '📝 LeetCode 题库';
  bar.appendChild(libLink);

  groups.forEach(function (g) {
    var label = document.createElement('span');
    label.className = 'navgroup';
    label.textContent = g.label;
    bar.appendChild(label);

    g.pages.forEach(function (p) {
      var link = document.createElement('a');
      link.className = 'navlink' + (p.href === active ? ' active' : '');
      link.href = p.href;
      link.textContent = p.label;
      bar.appendChild(link);
    });
  });

  document.body.insertBefore(bar, document.body.firstChild);
})();
