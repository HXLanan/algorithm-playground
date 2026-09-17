/* =========================================================
 * ui.js —— 通用 UI 工具 & 后端调用封装
 * ========================================================= */
(function (global) {
  "use strict";

  var API_BASE = "";   // 同源部署时留空即可

  /** 简易 DOM 查询 */
  function $(sel) { return document.querySelector(sel); }
  function $all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }

  /**
   * 调用后端 API；若后端不可用则返回 null，由调用方走本地兜底。
   * 这样页面在"有后端"和"双击打开"两种情况下都不会白屏。
   */
  function api(path, options) {
    options = options || {};
    var opts = {
      method: options.method || "GET",
      headers: { "Content-Type": "application/json" }
    };
    if (options.body) opts.body = JSON.stringify(options.body);

    return fetch(API_BASE + path, opts)
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .catch(function () {
        return null;   // 静默降级到本地算法
      });
  }

  /** 状态提示条 */
  function setStatus(el, text, type) {
    if (!el) return;
    el.textContent = text;
    el.style.color = type === "err" ? "#fb7185"
                   : type === "ok" ? "#34d399"
                   : "#9aa3c0";
  }

  /** 数字格式化：大数用 1.23eX */
  function shortNum(v) {
    var s = String(v);
    if (s.length <= 8) return s;
    return s[0] + "." + s.slice(1, 3) + "e" + (s.length - 1);
  }

  /** 数值千分位 */
  function comma(v) {
    return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  /** 请求动画帧循环封装 */
  function rafLoop(fn) {
    var stopped = false;
    function loop() {
      if (stopped) return;
      fn();
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
    return function stop() { stopped = true; };
  }

  global.UI = {
    $: $,
    $all: $all,
    api: api,
    setStatus: setStatus,
    shortNum: shortNum,
    comma: comma,
    rafLoop: rafLoop,
    API_BASE: API_BASE
  };
})(window);
