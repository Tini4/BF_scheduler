let deleted = [];

// Listen for clicks on entries
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('div.entry-absolute-box').forEach((entry) => {
        entry.addEventListener('click', (event) => {
            const div = event.currentTarget;

            deleted.push(div);
            div.style.display = 'none';
        });
    });
});

// Listen for Ctrl+Z (Undo)
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'z') {
        event.preventDefault();

        const div = deleted.pop();

        if (div) {
            div.style.display = '';
        }
    }
});

// Listen for Ctrl+O (Order)
document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 'o') {
        event.preventDefault();

        document.querySelectorAll('div.entry-absolute-box').forEach(entry => {
            entry.classList.add('leftmost', 'rightmost');
            entry.style.left = Math.floor(parseFloat(entry.style.left) / 20) * 20 + '%';
            entry.style.width = '20%';
        });
    }
});
