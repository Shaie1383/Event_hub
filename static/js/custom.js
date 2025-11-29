/* ============================================================
   SHAISTA — ADVANCED UI LOGIC (AMOGHA STYLE)
   Applies to: events page, resources page, home page
   ============================================================ */

/* ========== AOS Animation Init ========== */
document.addEventListener("DOMContentLoaded", () => {
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 900,
            once: false,
            easing: "ease-in-out"
        });
    }
});

/* ============================================================
   SEARCH BAR — LIVE FILTERING (EVENTS + RESOURCES)
   ============================================================ */
function setupLiveSearch(searchInputId, cardSelector) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;

    searchInput.addEventListener("input", () => {
        let term = searchInput.value.toLowerCase();
        document.querySelectorAll(cardSelector).forEach(card => {
            let text = card.innerText.toLowerCase();
            card.style.display = text.includes(term) ? "block" : "none";
        });
    });
}

// Events page search
setupLiveSearch("event-search", ".event-card");

// Resource page search
setupLiveSearch("resource-search", ".resource-card");

/* ============================================================
   CATEGORY SELECT FILTER
   ============================================================ */
function setupCategoryFilter(selectId, cardSelector, categoryAttr) {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.addEventListener("change", () => {
        let value = select.value.toLowerCase();
        document.querySelectorAll(cardSelector).forEach(card => {
            let cat = card.getAttribute(categoryAttr)?.toLowerCase() || "";
            card.style.display = (value === "all" || cat === value) ? "block" : "none";
        });
    });
}

// Event category filter
setupCategoryFilter("category-select", ".event-card", "data-category");

// Resource category filter
setupCategoryFilter("resource-category", ".resource-card", "data-category");

/* ============================================================
   SORTING — A–Z, Z–A, DATE
   ============================================================ */
function setupSort(selectId, containerSelector, cardSelector) {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.addEventListener("change", () => {
        const sortType = select.value;
        const container = document.querySelector(containerSelector);
        const cards = [...document.querySelectorAll(cardSelector)];

        if (sortType === "az") {
            cards.sort((a, b) =>
                a.querySelector(".event-title").innerText.localeCompare(
                    b.querySelector(".event-title").innerText
                )
            );
        }

        if (sortType === "za") {
            cards.sort((a, b) =>
                b.querySelector(".event-title").innerText.localeCompare(
                    a.querySelector(".event-title").innerText
                )
            );
        }

        if (sortType === "date") {
            cards.sort((a, b) =>
                new Date(a.getAttribute("data-date")) -
                new Date(b.getAttribute("data-date"))
            );
        }

        // Re-attach in sorted order
        cards.forEach(card => container.appendChild(card));
    });
}

// Event sorting
setupSort("sort-select", "#event-list", ".event-card");

/* ============================================================
   MODALS — FILL EVENT NAME AUTOMATICALLY
   ============================================================ */

document.addEventListener("click", e => {
    if (e.target.classList.contains("open-register-modal")) {
        const eventName = e.target.getAttribute("data-event");
        const hiddenInput = document.getElementById("modal-event-name");
        const titleSpan = document.getElementById("register-event-title");

        if (hiddenInput) hiddenInput.value = eventName;
        if (titleSpan) titleSpan.textContent = eventName;
    }
});

/* ============================================================
   RESOURCE CART HANDLER (FRONTEND LOGIC)
   ============================================================ */

let cart = [];

function updateCartUI() {
    const list = document.getElementById("cart-items");
    const count = document.getElementById("cart-count");

    if (!list) return;

    list.innerHTML = "";

    cart.forEach(item => {
        let li = document.createElement("li");
        li.className = "cart-list-item";

        li.innerHTML = `
            <span>${item}</span>
            <button class="btn btn-sm btn-danger remove-item" data-item="${item}">×</button>
        `;

        list.appendChild(li);
    });

    if (count) count.textContent = cart.length;
}

// Handle Add-to-Cart buttons
document.addEventListener("click", e => {
    if (e.target.classList.contains("add-to-cart")) {
        let resource = e.target.getAttribute("data-name");

        if (!cart.includes(resource)) {
            cart.push(resource);
            updateCartUI();
        }
    }
});

// Remove items from cart
document.addEventListener("click", e => {
    if (e.target.classList.contains("remove-item")) {
        let name = e.target.getAttribute("data-item");
        cart = cart.filter(r => r !== name);
        updateCartUI();
    }
});

/* ============================================================
   DARK / LIGHT MODE TOGGLE
   ============================================================ */
const toggle = document.getElementById("theme-toggle");

if (toggle) {
    toggle.addEventListener("click", () => {
        document.body.classList.toggle("light-mode");

        // Optional: store in local storage
        const mode = document.body.classList.contains("light-mode") ? "light" : "dark";
        localStorage.setItem("theme", mode);
    });

    // Load saved mode
    const saved = localStorage.getItem("theme");
    if (saved === "light") {
        document.body.classList.add("light-mode");
    }
}

/* ============================================================
   SMOOTH PAGE FADE-IN
   ============================================================ */

document.body.style.opacity = 0;
window.onload = () => {
    document.body.style.transition = "opacity .8s ease-in-out";
    document.body.style.opacity = 1;
};

/* ============================================================
   CARD HOVER — ELEGANT SCALE + GLOW
   ============================================================ */

document.querySelectorAll(".event-card, .resource-card").forEach(card => {
    card.addEventListener("mousemove", e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        card.style.transform = `translateY(-8px) rotateX(${(-y / 40)}deg) rotateY(${x / 40}deg)`;
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0px) rotateX(0deg) rotateY(0deg)";
    });
});
