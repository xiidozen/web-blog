const themeToggle = document.getElementById('theme-toggle');

// Set default theme to light without persisting
document.body.classList.add('light');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light');
    document.body.classList.toggle('dark');
});
