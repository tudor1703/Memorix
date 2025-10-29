document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('send-email-form');
    const messageBox = document.getElementById('email-message');

    if (!form) return; // dacă nu există formularul, nu continuăm

    form.addEventListener('submit', async function(e) {
        e.preventDefault(); // prevenim trimiterea normală

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            const data = await response.json();

            const isSuccess = data.message.toLowerCase().includes('success');
            messageBox.textContent = isSuccess
                ? 'Emails sent successfully!'
                : 'Failed to send emails.';
            messageBox.className = 'email-message ' + (isSuccess ? 'success' : 'error');

            messageBox.style.display = 'block';
            setTimeout(() => messageBox.style.opacity = '1', 10);

            setTimeout(() => {
                messageBox.style.opacity = '0';
                setTimeout(() => messageBox.style.display = 'none', 500);
            }, 2000);
        } catch (error) {
            messageBox.textContent = 'An error occurred.';
            messageBox.className = 'email-message error';
            messageBox.style.display = 'block';
            messageBox.style.opacity = '1';

            setTimeout(() => {
                messageBox.style.opacity = '0';
                setTimeout(() => messageBox.style.display = 'none', 500);
            }, 2000);
        }
    });
});
