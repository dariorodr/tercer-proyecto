// static/js/meses.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Meses script loaded');
    const mesActualElement = document.querySelector('#mes-actual');
    const mesInput = document.getElementById('mes-input');
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q') || '';

    if (mesActualElement && mesInput) {
        const mesActual = mesActualElement.dataset.mesActual; // e.g., "Mayo"
        const mesSeleccionado = urlParams.get('mes') || mesActual; // Fallback to current month

        // Always force URL to mesActual on page load
        const params = new URLSearchParams();
        params.set('mes', mesActual);
        if (query) params.set('q', query);
        window.history.replaceState({}, document.title, "?" + params.toString());

        // Update hidden input
        mesInput.value = mesSeleccionado;

        // Update button styles
        document.querySelectorAll('.btn[data-mes]').forEach(button => {
            const mes = button.getAttribute('data-mes');
            button.classList.remove('btn-primary', 'btn-outline-success', 'btn-outline-secondary', 'mes-actual');
            if (mes === mesSeleccionado) {
                button.classList.add('btn-primary'); // Highlight selected month
            } else {
                button.classList.add('btn-outline-secondary'); // Other months
            }
            if (mes === mesActual) {
                button.classList.add('mes-actual'); // Distinct style for current month
            }
        });

        // Handle button clicks
        document.querySelectorAll('.btn[data-mes]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const mes = this.getAttribute('data-mes');
                const params = new URLSearchParams();
                params.set('mes', mes);
                if (query) params.set('q', query);
                window.location.search = params.toString();
            });
        });

        // Handle navbar "Inicio" link
        const inicioLink = document.getElementById('inicio-link');
        if (inicioLink) {
            inicioLink.addEventListener('click', function(e) {
                e.preventDefault();
                const params = new URLSearchParams();
                params.set('mes', mesActual); // Force current month
                if (query) params.set('q', query);
                window.location.href = '{% url "inicio" %}?' + params.toString();
            });
        }
    } else {
        console.error('Elementos #mes-actual o #mes-input no encontrados');
    }
});