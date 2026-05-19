document.addEventListener('DOMContentLoaded', () => {
    // --- Dark Mode Logic ---
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateToggleIcon('dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                updateToggleIcon('light');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateToggleIcon('dark');
            }
        });
    }

    function updateToggleIcon(theme) {
        if (!themeToggle) return;
        if (theme === 'dark') {
            themeToggle.innerHTML = '☀️ Light Mode';
        } else {
            themeToggle.innerHTML = '🌙 Dark Mode';
        }
    }

    // --- Search / Filter Logic ---
    const searchInput = document.getElementById('search-input');
    const tableBody = document.querySelector('tbody');
    
    if (searchInput && tableBody) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const rows = tableBody.querySelectorAll('tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.classList.remove('hidden');
                } else {
                    row.classList.add('hidden');
                }
            });
        });
    }

    // --- FAB Back to Top ---
    const fab = document.getElementById('fab');
    if (fab) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                fab.classList.add('visible');
            } else {
                fab.classList.remove('visible');
            }
        });

        fab.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Animate elements on load
    document.body.classList.add('animate-fade-in');
});

// --- Table Sorting Logic ---
// We attach this globally so the onclick="sortTable(x)" in HTML works
window.sortTable = function(columnIndex) {
    const table = document.getElementById("questionsTable");
    if (!table) return;
    
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.querySelectorAll('tr:not(.hidden)')); // Only sort visible
    const hiddenRows = Array.from(tbody.querySelectorAll('tr.hidden')); // keep hidden separately
    
    const header = table.tHead.rows[0].cells[columnIndex];
    const isAsc = !header.classList.contains('sort-asc');

    // Reset all headers
    table.tHead.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Set new sort direction
    header.classList.toggle('sort-asc', isAsc);
    header.classList.toggle('sort-desc', !isAsc);

    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();

        // Check if values are numeric
        const aNum = parseInt(aText);
        const bNum = parseInt(bText);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAsc ? (aNum - bNum) : (bNum - aNum);
        }

        // Fallback to string comparison
        return isAsc ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });

    // Clear and re-append
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
    hiddenRows.forEach(row => tbody.appendChild(row));
};
