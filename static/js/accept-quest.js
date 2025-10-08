document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".accept-quest-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();

            const questSlug = this.dataset.questSlug;
            const originalText = this.textContent;

            const resp = fetch(`/quests/accept`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    quest_slug: questSlug
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.textContent = "Квест взят";
                    this.className = "w-full bg-gray-700 text-gray-400 font-bold py-2 px-4 rounded-lg cursor-not-allowed opacity-75";
                    this.disabled = true;

                    showMessage(data.message, "success");
                } else {
                    this.textContent = originalText;
                    this.disabled = false;
                    showMessage(`Error ${data.message}`, "error");
                }
            })
            .catch(err => {
                this.textContent = originalText;
                this.disabled = false;
                showMessage(`Error: ${err}`, "error");
            })
        });
    })

    function showMessage(message, type) {
        const alertDiv = document.createElement('div');

        alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-600' : 'bg-red-600'
        } text-white max-w-md`;
        alertDiv.textContent = message;

        document.body.appendChild(alertDiv);
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});