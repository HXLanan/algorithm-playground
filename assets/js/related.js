/* =========================================================
 * related.js —— 自动为算法可视化页注入「相关 LeetCode 题目」
 * ---------------------------------------------------------
 * 用法：在算法页底部加一行
 *     <script src="../assets/js/related.js"></script>
 * 它会读取 window.__ALGO_ACTIVE__（当前页文件名），
 * 向后端反查关联题目，并在页面末尾渲染一张卡片。
 * 后端不可用时静默跳过，不影响页面本身。
 * ========================================================= */
(function () {
  "use strict";

  var page = window.__ALGO_ACTIVE__;
  if (!page || page === 'index.html' || page === 'problems.html' || page === 'problem.html') {
    return;   // 首页与题库页不需要
  }

  var DIFF_COLOR = { '简单': '#34d399', '中等': '#fbbf24', '困难': '#fb7185' };

  function esc(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function render(items) {
    if (!items || !items.length) return;

    var host = document.querySelector('main.wrap');
    if (!host) return;

    var card = document.createElement('section');
    card.className = 'card';

    var h = '<h2>📝 相关 LeetCode 题目</h2>';
    h += '<p class="info-line">看完动画，试着亲手写一遍——这是检验有没有真正理解的最好方式。</p>';
    h += '<div style="display:flex;flex-direction:column;gap:8px;margin-top:12px;">';

    items.forEach(function (it) {
      var dc = DIFF_COLOR[it.difficulty] || '#9aa3c0';
      h += '<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;'
         + 'background:#161b2e;border:1px solid #2e3654;border-radius:11px;flex-wrap:wrap;">';
      h += '<div style="flex:1 1 220px;min-width:170px;">';
      h += '<a href="problem.html?slug=' + it.slug + '" style="color:#e6e9f5;text-decoration:none;'
         + 'font-weight:600;font-size:14.5px;">' + it.lcId + '. ' + esc(it.title) + '</a>';
      h += '<div style="margin-top:6px;">';
      h += '<span style="font-size:11px;padding:2px 8px;border-radius:20px;background:' + dc
         + ';color:#0b0e1a;font-weight:700;">' + it.difficulty + '</span>';
      (it.tags || []).slice(0, 3).forEach(function (t) {
        h += '<span style="font-size:11px;padding:2px 8px;border-radius:20px;background:#232a45;'
           + 'color:#9aa3c0;margin-left:5px;">' + esc(t) + '</span>';
      });
      h += '</div></div>';
      h += '<a href="problem.html?slug=' + it.slug + '" style="padding:6px 14px;border-radius:8px;'
         + 'background:#5eead4;color:#0b0e1a;text-decoration:none;font-weight:600;font-size:13px;'
         + 'white-space:nowrap;">去做题 →</a>';
      h += '</div>';
    });

    h += '</div>';
    h += '<p class="info-line" style="margin-top:14px;">' +
         '<a href="problems.html" style="color:#5eead4;text-decoration:none;">查看完整题库 →</a></p>';

    card.innerHTML = h;
    host.appendChild(card);
  }

  // 等 DOM 就绪后请求
  function boot() {
    if (typeof UI === 'undefined' || !UI.api) return;
    UI.api('/api/problems/related?visualizer=' + encodeURIComponent(page) + '&limit=6')
      .then(function (res) {
        if (res && res.items && res.items.length) {
          render(res.items);
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
