document.addEventListener('DOMContentLoaded', function () {
    console.log('Alertas script loaded'); // Para depuración
    const alerts = document.querySelectorAll('.alert');
    console.log('Found alerts:', alerts.length); // Para depuración
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150); // Elimina del DOM tras la transición
        }, 3000); // 3 segundos
    });
});