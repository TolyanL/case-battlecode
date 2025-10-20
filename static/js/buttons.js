document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".action-btn").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            const slug = this.dataset.slug;
            const btnAction = this.dataset.action;

            const originalText = this.textContent;
            const originalClassName = this.className;

            const actions = {
                "accept": {
                    url: "/quests/rest/accept",
                    successMsg: "💀 Сдаться",
                    newAction: "give-up",
                    oldColor: "cyan",
                    newColor: "gray",
                    data: ""
                },
                "give-up": {
                    url: "/quests/rest/give-up",
                    successMsg: "🕒 Квест заблокирован, возвращайтесь через 3 дня",
                    newAction: "accept",
                    oldColor: "gray",
                    newColor: "cyan",
                    data: ""
                },
                "complete": {
                    url: "/quests/rest/complete",
                    successMsg: "⚔️ Start Code Battle",
                    newAction: "-",
                    oldColor: "gray",
                    newColor: "cyan",
                    data: window.codeEditor ? window.codeEditor.getValue() : ""
                },
                // Courses
                "enroll": {
                    url: "/courses/rest/enroll",
                    successMsg: "💀 Отписаться от курса",
                    newAction: "unenroll",
                    oldColor: "cyan",
                    newColor: "gray",
                    data: ""
                },
                "unenroll": {
                    url: "/courses/rest/unenroll",
                    successMsg: "🚀 Начать курс",
                    newAction: "enroll",
                    oldColor: "gray",
                    newColor: "cyan",
                    data: ""
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
                    slug: slug,
                    data: actionConfig.data
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

                    if (btnAction == "complete") {
                        window.location.href = `/quests/reviews/${slug}`;
                    } else if (btnAction == "give-up") {
                        window.location.href = `/quests/details/${slug}`;
                    } else if (btnAction == "accept") {
                        window.location.href = `/quests/work/${slug}`;
                    }
                } else {
                    this.textContent = originalText;
                }
            })
            .catch(err => {
                this.textContent = originalText;
                this.className = originalClassName;
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });
});