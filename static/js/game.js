/**
 * UI updates and API / Socket.IO wiring.
 */
(function () {
  const statusEl = document.getElementById("status");
  const playerCardsEl = document.getElementById("player-cards");
  const dealerCardsEl = document.getElementById("dealer-cards");
  const socket =
    typeof io !== "undefined"
      ? io({ transports: ["websocket", "polling"] })
      : null;

  function renderState(data) {
    if (typeof window.renderCardCodes === "function") {
      window.renderCardCodes(data.player_cards || [], playerCardsEl);
      window.renderCardCodes(data.dealer_cards || [], dealerCardsEl);
    }
    if (!statusEl) return;
    const parts = [
      `Phase: ${data.phase}`,
      `You: (${data.player_total})`,
      `Dealer: (${data.dealer_total})`,
    ];
    statusEl.textContent = parts.join(" · ");
  }

  if (socket) {
    socket.on("connect", () => {
      if (statusEl) statusEl.textContent = "Connected.";
    });
    socket.on("state", renderState);
  }

  window.fetchState = async function () {
    const r = await fetch("/api/state");
    const data = await r.json();
    renderState(data);
  };

  window.emitGame = function (event) {
    if (socket) socket.emit(event);
  };
})();
