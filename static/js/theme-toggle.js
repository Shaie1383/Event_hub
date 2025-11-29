/* ============================================================
   Theme Toggle (Light / Dark Mode)
   ------------------------------------------------------------
   - Saves preference in localStorage
   - Detects system preference on first load
   - Adds smooth transitions
   - Works across all pages
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("themeToggle");
    const body = document.body;

    // Enable smooth transition after first paint
    setTimeout(() => body.classList.add("theme-transition"), 100);

    // Load user preference
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        body.classList.toggle("dark-mode", savedTheme === "dark");
    } else {
        // Auto-detect OS theme on first load
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        body.classList.toggle("dark-mode", prefersDark);
    }

    // Toggle function
    const updateTheme = () => {
        body.classList.toggle("dark-mode");
        const newTheme = body.classList.contains("dark-mode") ? "dark" : "light";
        localStorage.setItem("theme", newTheme);
        toggleBtn.innerText = newTheme === "dark" ? "☀ Light Mode" : "🌙 Dark Mode";
    };

    // Update button text on load
    toggleBtn.innerText = body.classList.contains("dark-mode")
        ? "☀ Light Mode"
        : "🌙 Dark Mode";

    // Listen for toggle click
    toggleBtn.addEventListener("click", updateTheme);
});
