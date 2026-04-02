/**
 * Card / table rendering helpers (DOM or canvas extension point).
 */
(function () {
  /**
   * @param {string[]} cardCodes e.g. ["AH", "10S"]
   * @param {HTMLElement | null} container
   */
  window.renderCardCodes = function (cardCodes, container) {
    if (!container) return;
    container.innerHTML = "";
    cardCodes.forEach((code) => {
      const div = document.createElement("div");
      div.className = "card-face";
      div.textContent = code;
      div.style.cssText =
        "display:inline-block;margin:4px;padding:8px 12px;background:#fff;color:#111;border-radius:6px;font-weight:600;";
      container.appendChild(div);
    });
  };
})();
