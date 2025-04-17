document.addEventListener('DOMContentLoaded', function() {
    // Obtener el mes actual desde un elemento data en el HTML
    const mesActual = document.querySelector('#mes-actual').dataset.mesActual;
    
    // Forzar el mes actual en la URL al cargar la página
    window.history.replaceState({}, document.title, "?mes=" + mesActual);
    
    // Manejar clics en los botones de meses
    document.querySelectorAll('.btn[data-mes]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const mes = this.getAttribute('data-mes');
            window.location.search = "?mes=" + mes;
        });
    });
});