document.addEventListener('DOMContentLoaded', function() {
    const mesActualElement = document.querySelector('#mes-actual');
    if (mesActualElement) {
        const mesActual = mesActualElement.dataset.mesActual;
        window.history.replaceState({}, document.title, "?mes=" + mesActual);
    }
    document.querySelectorAll('.btn[data-mes]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const mes = this.getAttribute('data-mes');
            window.location.search = "?mes=" + mes;
        });
    });
});