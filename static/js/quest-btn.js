document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".quest-btn").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            const questSlug = this.dataset.questSlug;
            const btnAction = this.dataset.action;

            const originalText = this.textContent;
            const originalClassName = this.className;
            this.disabled = true;

            const actions = {
                "accept": {
                    url: "/quests/accept",
                    successMsg: "💀 Сдаться",
                    newAction: "give-up",
                    oldColor: "cyan",
                    newColor: "gray"
                },
                "give-up": {
                    url: "/quests/give-up",
                    successMsg: "🕒 Квест заблокирован, возвращайтесь через 3 дня",
                    newAction: "accept",
                    oldColor: "gray",
                    newColor: "cyan"
                },
                "complete": {
                    url: "/quests/complete",
                    successMsg: "⚔️ Start Code Battle",
                    newAction: "-",
                    oldColor: "gray",
                    newColor: "cyan"
                }
            };

            const actionConfig = actions[btnAction];

            if (!actionConfig) {
                this.disabled = false;
                return;
            }

            fetch(actionConfig.url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    quest_slug: questSlug
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    this.textContent = actionConfig.successMsg;
                    this.className = originalClassName.replace(actionConfig.oldColor, actionConfig.newColor);
                    this.dataset.action = actionConfig.newAction;
                    showMessage(data.message, "success");
                    
                    if (btnAction == "complete") {
                        window.location.href = `/quests/reviews/${questSlug}`;
                    } else if (btnAction == "give-up") {
                        window.location.href = `/quests/details/${questSlug}`;
                    } else {
                        window.location.href = `/quests/work/${questSlug}`;
                    }
                } else {
                    this.textContent = originalText;
                    showMessage(`Ошибка: ${data.message}`, "error");
                }
            })
            .catch(err => {
                this.textContent = originalText;
                this.className = originalClassName;
                showMessage(`Произошла ошибка: ${err.message}`, "error");
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });

    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-600' : 'bg-red-600';

        alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${bgColor} text-white max-w-md`;
        alertDiv.textContent = message;

        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});