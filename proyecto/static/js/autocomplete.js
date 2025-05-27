document.addEventListener('DOMContentLoaded', () => {
    console.log('Autocomplete script loaded');
    const searchInput = document.getElementById('search-input');
    const suggestionsContainer = document.getElementById('suggestions');
    const mesInput = document.getElementById('mes-input');
    const searchForm = document.getElementById('search-form');

    if (!searchInput || !suggestionsContainer || !mesInput || !searchForm) {
        console.error('Required elements not found');
        return;
    }

    // Limpiar input y parámetro q al recargar
    window.addEventListener('load', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const mes = urlParams.get('mes') || mesInput.value;
        searchInput.value = ''; // Limpiar el input
        const newParams = new URLSearchParams();
        if (mes) newParams.set('mes', mes); // Mantener solo mes
        const newUrl = window.location.pathname + (newParams.toString() ? `?${newParams.toString()}` : '');
        window.history.replaceState({}, document.title, newUrl);
    });

    let timeoutId = null;

    // Función para obtener sugerencias
    const fetchSuggestions = async (query) => {
        const url = `/buscar-productos/?q=${encodeURIComponent(query)}`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Network error');
            const data = await response.json();
            return data.resultados;
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            return [];
        }
    };

    // Mostrar sugerencias
    const showSuggestions = (suggestions) => {
        suggestionsContainer.innerHTML = '';
        if (suggestions.length === 0) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        suggestions.forEach(suggestion => {
            const item = document.createElement('a');
            item.href = '#';
            item.className = 'list-group-item list-group-item-action';
            item.textContent = suggestion.nombre;
            item.addEventListener('click', (e) => {
                e.preventDefault();
                searchInput.value = suggestion.nombre;
                suggestionsContainer.style.display = 'none';
                searchForm.submit();
            });
            suggestionsContainer.appendChild(item);
        });
        suggestionsContainer.style.display = 'block';
    };

    // Manejar entrada del usuario
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        if (timeoutId) clearTimeout(timeoutId);

        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        timeoutId = setTimeout(async () => {
            const suggestions = await fetchSuggestions(query);
            showSuggestions(suggestions);
        }, 300);
    });

    // Ocultar sugerencias al perder foco
    searchInput.addEventListener('blur', () => {
        setTimeout(() => {
            suggestionsContainer.style.display = 'none';
        }, 200);
    });

    // Mostrar sugerencias al enfocar si hay texto
    searchInput.addEventListener('focus', () => {
        if (searchInput.value.trim().length >= 2) {
            fetchSuggestions(searchInput.value.trim()).then(showSuggestions);
        }
    });

    // Manejar teclas
    searchInput.addEventListener('keydown', (e) => {
        const items = suggestionsContainer.querySelectorAll('.list-group-item');
        if (!items.length) return;

        let index = Array.from(items).findIndex(item => item.classList.contains('active'));

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (index < items.length - 1) {
                if (index >= 0) items[index].classList.remove('active');
                index++;
                items[index].classList.add('active');
                items[index].scrollIntoView({ block: 'nearest' });
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (index > 0) {
                items[index].classList.remove('active');
                index--;
                items[index].classList.add('active');
                items[index].scrollIntoView({ block: 'nearest' });
            }
        } else if (e.key === 'Enter' && index >= 0) {
            e.preventDefault();
            searchInput.value = items[index].textContent;
            suggestionsContainer.style.display = 'none';
            searchForm.submit();
        } else if (e.key === 'Escape') {
            suggestionsContainer.style.display = 'none';
        }
    });
});