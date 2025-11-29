/* ============================================================
   AOS (Animate On Scroll) — Initialization Script
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 900,          // Animation speed
            easing: "ease-in-out", // Smooth transition
            once: false,           // Animate every time in view
            mirror: false,         // No reverse animation
            offset: 120            // Trigger position
        });
    } else {
        console.warn("AOS library not loaded.");
    }
});
