document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.action-btn');
    buttons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();

            const action = button.dataset.action;
            const code = button.dataset.code;

            const endpoint = action === 'complete' 
                ? '/pvp/rest/battle/complete' 
                : '/pvp/rest/battle/fail';

            try {
                const csrfToken = getCsrfToken();

                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        action: action,
                        code: code
                    })
                });

                const result = await response.json();

                if (result.success) {
                    const redirectUrl = `/pvp/battle/${code}/results`;
                    window.location.href = redirectUrl;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});

function getCsrfToken() {
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfElement) return csrfElement.value;

    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();

    return '';
}