let deleted = [];

// Listen for clicks on grid entries
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('div.entry-absolute-box').forEach(entry => {
        entry.addEventListener('click', event => {
            const div = event.currentTarget;

            deleted.push(div);
            div.style.display = 'none';
        });
    });
});

// Listen for Ctrl+Z (Undo)
document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 'z') {
        event.preventDefault();

        const div = deleted.pop();

        if (div) {
            div.style.display = '';
        }
    }
});
