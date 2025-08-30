const themeToggle = document.getElementById('theme-toggle');

// Theme state: 'auto', 'light', or 'dark'
let currentTheme = 'auto';

// Function to apply theme
function applyTheme(theme) {
    document.body.classList.remove('light', 'dark');
    
    if (theme === 'light') {
        document.body.classList.add('light');
    } else if (theme === 'dark') {
        document.body.classList.add('dark');
    }
    // If theme is 'auto', no classes are added, so CSS media queries take effect
}

// Function to get system theme preference
function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Function to update toggle button text
function updateToggleButton() {
    const systemTheme = getSystemTheme();
    
    if (currentTheme === 'auto') {
        themeToggle.textContent = `Theme: Auto (${systemTheme === 'dark' ? 'Dark' : 'Light'})`;
    } else if (currentTheme === 'light') {
        themeToggle.textContent = 'Theme: Light';
    } else {
        themeToggle.textContent = 'Theme: Dark';
    }
}

// Initialize with auto theme (respects system preference)
applyTheme(currentTheme);
updateToggleButton();

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (currentTheme === 'auto') {
        updateToggleButton();
    }
});

// Toggle between auto -> light -> dark -> auto
themeToggle.addEventListener('click', () => {
    if (currentTheme === 'auto') {
        currentTheme = 'light';
    } else if (currentTheme === 'light') {
        currentTheme = 'dark';
    } else {
        currentTheme = 'auto';
    }
    
    applyTheme(currentTheme);
    updateToggleButton();
});
