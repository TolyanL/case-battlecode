document.addEventListener("DOMContentLoaded", function () {
  function getUsernameFromH3() {
    const h3Element = document.querySelector("h3.font-bold.text-white.text-xl");
    if (!h3Element) return null;

    let username = h3Element.textContent.trim();
    username = username.replace(/\s*\(Вы\)\s*/g, "").trim();
    return username || null;
  }

  function updateButtonUI(button, newState, statusElement) {
    switch (newState) {
      case "ready":
        button.setAttribute("data-state", "ready");
        button.innerHTML =
          '<i data-feather="clock" class="w-3 h-3 inline mr-1"></i>Приготовьтесь';
        button.className =
          "action-btn w-full px-4 py-3 bg-orange-600 hover:bg-orange-800 text-white font-medium rounded-lg transition-colors duration-300 flex items-center justify-center";
        if (statusElement) {
          statusElement.innerHTML =
            '<i data-feather="clock" class="w-3 h-3 inline mr-1"></i>Ожидание';
          statusElement.className =
            "bg-amber-500/20 text-amber-400 text-xs font-semibold px-2 py-1 rounded";
        }
        break;
      case "not-ready":
        button.setAttribute("data-state", "not-ready");
        button.innerHTML =
          '<i data-feather="check" class="w-3 h-3 inline mr-1"></i>Готов';
        button.className =
          "action-btn w-full px-4 py-3 bg-green-600 hover:bg-green-800 text-white font-medium rounded-lg transition-colors duration-300 flex items-center justify-center";
        if (statusElement) {
          statusElement.innerHTML =
            '<i data-feather="check" class="w-3 h-3 inline mr-1"></i>Готов';
          statusElement.className =
            "bg-green-500/20 text-green-400 text-xs font-semibold px-2 py-1 rounded";
        }
        break;
    }
  }

  const actionBtn = document.querySelector(".action-btn");
  const statusElement = document.querySelector(
    ".bg-amber-500\\/20, .bg-green-500\\/20"
  );

  if (actionBtn) {
      actionBtn.addEventListener("click", async function (e) {
          e.preventDefault();

          const currentState = this.getAttribute("data-state");
          if (!currentState) return;

          const username = getUsernameFromH3();
          if (!username) return;

          const payload = {
              user: username,
              state: currentState,
          };

          try {
              const csrfToken =
                  document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

              const response = await fetch("/pvp/rest/battle/change-state", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": csrfToken,
                  },
                  body: JSON.stringify(payload),
              });

              if (!response.ok) return;

              const result = await response.json();

              if (result.success) {
                  if (result.message) {
                      console.log(result.message)
                      window.location.href = result.message;
                  }
                  else {
                      const nextState = currentState === "ready" ? "not-ready" : "ready";
                      updateButtonUI(this, nextState, statusElement);
                  }
              }
          } catch (error) {
              // silent fail
          }

          if (typeof feather !== "undefined") {
              feather.replace();
          }
      });
  }

  const battleButton = document.querySelector(".start-battle");
  if (battleButton) {
    battleButton.addEventListener("click", async function (e) {
      e.preventDefault();
      try {
        const opponentElement = document.querySelector(".opponent-name");
        if (!opponentElement) return;

        const opponentName = opponentElement.textContent.trim();
        if (!opponentName) return;

        const csrfToken =
          document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

        const response = await fetch("/pvp/rest/start-battle", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ opponent: opponentName }),
        });

        if (!response.ok) return;

        const result = await response.json();
        if (result.success && result.message) {
          window.location.href = result.message;
        }
      } catch (error) {
        // silent fail
      }
    });
  }

  if (typeof feather !== "undefined") {
    feather.replace();
  }
});
