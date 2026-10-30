
/*
 * MiniDash - Frontend Application
 *
 * Handles restaurant browsing, menu selection, shopping cart,
 * order creation, and live delivery tracking.
 */

// ============================================================
// 1. HTML ELEMENTS AND APPLICATION STATE
// ============================================================

const restaurantGrid = document.getElementById("restaurantGrid");
const menuSection = document.getElementById("menuSection");
const menuGrid = document.getElementById("menuGrid");
const menuTitle = document.getElementById("menuTitle");
const searchInput = document.getElementById("searchInput");
const cartPanel = document.getElementById("cartPanel");
const cartItems = document.getElementById("cartItems");
const cartCount = document.getElementById("cartCount");
const cartTotal = document.getElementById("cartTotal");
const trackingContent = document.getElementById("trackingContent");
const checkoutButton = document.getElementById("checkoutButton");

let restaurants = [];
let selectedRestaurantId = null;
let cart = [];
let activeOrderId = null;
let trackingTimer = null;

const statusSteps = [
    "PLACED",
    "PREPARING",
    "READY",
    "PICKED_UP",
    "DELIVERED"
];

// ============================================================
// 2. API AND HTML HELPER FUNCTIONS
// ============================================================

// Sends requests to the MiniDash FastAPI backend.
async function request(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        const message = typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data);

        throw new Error(message || `Request failed: ${response.status}`);
    }

    return data;
}

// Creates HTML elements safely without using innerHTML.
function createElement(tag, className = "", text) {
    const element = document.createElement(tag);

    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;

    return element;
}

// Converts backend prices into dollars.
// MiniDash may return price_cents instead of price.
function getItemPrice(item) {
    if (item.price_cents !== undefined && item.price_cents !== null) {
        const cents = Number(item.price_cents);
        return Number.isFinite(cents) ? cents / 100 : null;
    }

    if (item.price !== undefined && item.price !== null) {
        const dollars = Number(item.price);
        return Number.isFinite(dollars) ? dollars : null;
    }

    return null;
}

// Formats a valid dollar amount with two decimal places.
function formatPrice(amount) {
    return Number.isFinite(amount)
        ? `$${amount.toFixed(2)}`
        : "Price unavailable";
}

// ============================================================
// 3. RESTAURANT EMOJIS
// ============================================================

// Selects a restaurant emoji based on its name and cuisine.
function getRestaurantVisual(restaurant) {
    const text = `${restaurant.name || ""} ${restaurant.cuisine || ""}`
        .toLowerCase();

    if (text.includes("pizza")) return "🍕";
    if (text.includes("italian") || text.includes("napoli")) return "🍝";
    if (text.includes("sushi") || text.includes("japanese")) return "🍣";
    if (text.includes("mexican") || text.includes("taco")) return "🌮";
    if (text.includes("burger") || text.includes("american")) return "🍔";
    if (/(salad|healthy|green|vegan|vegetarian)/.test(text)) return "🥗";
    if (text.includes("greek") || text.includes("mediterranean")) return "🥙";
    if (text.includes("chinese")) return "🥡";
    if (text.includes("thai")) return "🍜";
    if (text.includes("indian")) return "🍛";
    if (text.includes("korean")) return "🍚";
    if (text.includes("seafood")) return "🦐";
    if (text.includes("breakfast") || text.includes("brunch")) return "🥞";
    if (text.includes("bakery")) return "🥐";
    if (text.includes("coffee") || text.includes("cafe")) return "☕";

    return "🍽️";
}

// ============================================================
// 4. MENU ITEM EMOJIS
// ============================================================

// Uses the dish name to select a more accurate food emoji.
function getMenuItemVisual(item) {
    const name = (item.name || "").toLowerCase();

    // Italian food
    if (/(pizza|margherita)/.test(name)) return "🍕";
    if (/(pasta|spaghetti|penne|alfredo|lasagna|ravioli|linguine|fettuccine)/.test(name)) {
        return "🍝";
    }

    // Burgers and sandwiches
    if (/(burger|cheeseburger)/.test(name)) return "🍔";
    if (name.includes("fries")) return "🍟";
    if (name.includes("hot dog")) return "🌭";
    if (/(sandwich|panini|sub)/.test(name)) return "🥪";

    // Mexican food
    if (name.includes("taco")) return "🌮";
    if (/(burrito|wrap|quesadilla)/.test(name)) return "🌯";
    if (name.includes("nacho")) return "🧀";

    // Asian food
    if (/(sushi|maki|california roll|dragon roll)/.test(name)) return "🍣";
    if (/(ramen|noodle|pho)/.test(name)) return "🍜";
    if (/(dumpling|gyoza)/.test(name)) return "🥟";

    // Salads and bowls
    if (/(salad|caesar|poke|grain bowl|quinoa bowl)/.test(name)) return "🥗";
    if (/(rice|risotto)/.test(name)) return "🍚";

    // Protein dishes
    if (/(chicken|wings)/.test(name)) return "🍗";
    if (/(steak|beef)/.test(name)) return "🥩";
    if (/(shrimp|prawn)/.test(name)) return "🍤";
    if (/(fish|salmon|tuna)/.test(name)) return "🐟";

    // Other meals
    if (/(soup|chowder|stew)/.test(name)) return "🍲";
    if (name.includes("egg")) return "🍳";
    if (name.includes("pancake")) return "🥞";
    if (name.includes("waffle")) return "🧇";
    if (name.includes("croissant")) return "🥐";
    if (name.includes("avocado")) return "🥑";

    // Desserts
    if (name.includes("cake")) return "🍰";
    if (name.includes("cookie")) return "🍪";
    if (/(ice cream|gelato)/.test(name)) return "🍨";
    if (/(donut|doughnut)/.test(name)) return "🍩";
    if (name.includes("brownie")) return "🍫";

    // Drinks
    if (/(coffee|latte|cappuccino)/.test(name)) return "☕";
    if (/(smoothie|juice|soda)/.test(name)) return "🥤";

    return "🍽️";
}

// ============================================================
// 5. RESTAURANT BROWSING
// ============================================================

// Retrieves restaurant data from FastAPI.
async function loadRestaurants() {
    try {
        const data = await request("/restaurants");

        restaurants = Array.isArray(data)
            ? data
            : data.restaurants || [];

        renderRestaurants(restaurants);
    } catch (error) {
        restaurantGrid.textContent =
            `Unable to load restaurants: ${error.message}`;
    }
}

// Creates restaurant cards dynamically using backend data.
function renderRestaurants(items) {
    restaurantGrid.replaceChildren();

    if (!items.length) {
        restaurantGrid.textContent = "No restaurants found.";
        return;
    }

    items.forEach(restaurant => {
        const card = createElement("article", "restaurant-card");

        const image = createElement(
            "div",
            "restaurant-image",
            getRestaurantVisual(restaurant)
        );

        const name = createElement("h3", "", restaurant.name);

        const description = createElement(
            "p",
            "",
            restaurant.cuisine ||
            restaurant.description ||
            "Fresh, delicious food"
        );

        card.append(image, name, description);

        // Clicking a card opens its restaurant menu.
        card.addEventListener("click", () => openMenu(restaurant));

        restaurantGrid.appendChild(card);
    });
}

// ============================================================
// 6. RESTAURANT MENUS
// ============================================================

// Retrieves menu items for the selected restaurant.
async function openMenu(restaurant) {
    try {
        const restaurantId = restaurant.id;

        const data = await request(
            `/restaurants/${restaurantId}/menu`
        );

        const items = Array.isArray(data)
            ? data
            : data.items || data.menu || [];

        // An order may contain food from only one restaurant.
        if (selectedRestaurantId !== restaurantId) {
            cart = [];
            updateCart();
        }

        selectedRestaurantId = restaurantId;
        menuTitle.textContent = `${restaurant.name} Menu`;
        menuGrid.replaceChildren();

        items.forEach(item => {
            const card = createElement("article", "menu-card");

            const image = createElement(
                "div",
                "food-image",
                getMenuItemVisual(item)
            );

            const name = createElement("h3", "", item.name);

            const itemPrice = getItemPrice(item);

            const price = createElement(
                "p",
                "",
                formatPrice(itemPrice)
            );

            const button = createElement(
                "button",
                "",
                "Add to Cart"
            );

            // Prevent ordering items without a valid price.
            if (itemPrice === null || itemPrice < 0) {
                button.disabled = true;
                button.title = "Price information is unavailable";
            } else {
                button.addEventListener("click", () => addToCart(item));
            }

            card.append(image, name, price, button);
            menuGrid.appendChild(card);
        });

        if (!items.length) {
            menuGrid.textContent = "No menu items available.";
        }

        menuSection.classList.remove("hidden");

        menuSection.scrollIntoView({
            behavior: "smooth"
        });
    } catch (error) {
        alert(`Could not open menu: ${error.message}`);
    }
}

// ============================================================
// 7. SHOPPING CART
// ============================================================

// Adds a selected menu item or increases its quantity.
function addToCart(item) {
    const itemPrice = getItemPrice(item);

    if (itemPrice === null || itemPrice < 0) {
        alert("This item's price is unavailable.");
        return;
    }

    const existing = cart.find(entry => entry.id === item.id);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: item.id,
            name: item.name,
            price: itemPrice,
            quantity: 1
        });
    }

    updateCart();
    cartPanel.classList.remove("hidden");
}

// Updates cart items, quantity, and total price.
function updateCart() {
    cartItems.replaceChildren();

    let total = 0;
    let count = 0;

    cart.forEach(item => {
        total += item.price * item.quantity;
        count += item.quantity;

        const row = createElement(
            "div",
            "cart-item",
            `${item.name} × ${item.quantity} — ${formatPrice(
                item.price * item.quantity
            )}`
        );

        cartItems.appendChild(row);
    });

    if (!cart.length) {
        cartItems.textContent = "Your cart is empty.";
    }

    cartCount.textContent = count;
    cartTotal.textContent = `Total: ${formatPrice(total)}`;

    checkoutButton.disabled = cart.length === 0;
}

// ============================================================
// 8. CHECKOUT AND ORDER CREATION
// ============================================================

// Sends the selected restaurant and cart items to the API.
async function checkout() {
    if (!selectedRestaurantId || !cart.length) {
        alert("Add something to your cart first.");
        return;
    }

    // Ask the customer for their delivery address.
const address = prompt("Enter your delivery address:");

if (address === null) {
    return; // Customer cancelled checkout.
}

if (!address.trim()) {
    alert("Please enter a delivery address.");
    return;
}

// Send the restaurant, delivery address, and items to FastAPI.
const payload = {
    restaurant_id: selectedRestaurantId,
    address: address.trim(),
    items: cart.map(item => ({
        menu_item_id: item.id,
        quantity: item.quantity
    }))
};

    checkoutButton.disabled = true;

    try {
        const order = await request("/orders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const newOrderId = order.id ?? order.order_id;

        if (newOrderId === undefined || newOrderId === null) {
            throw new Error(
                "Order created, but the server did not return an order ID."
            );
        }

        activeOrderId = newOrderId;

        cart = [];
        updateCart();
        cartPanel.classList.add("hidden");

        // Display the status immediately after checkout.
        await refreshTracking();

        document.getElementById("tracking").scrollIntoView({
            behavior: "smooth"
        });

        // Poll the API every five seconds for status updates.
        if (trackingTimer !== null) {
            clearInterval(trackingTimer);
        }

        trackingTimer = setInterval(refreshTracking, 5000);

    } catch (error) {
        alert(`Checkout failed: ${error.message}`);
    } finally {
        checkoutButton.disabled = cart.length === 0;
    }
}

// ============================================================
// 9. LIVE ORDER TRACKING
// ============================================================

// Retrieves the most recent status and estimated delivery time.
async function refreshTracking() {
    if (activeOrderId === null) return;

    try {
       // GET retrieves the latest tracking information without changing the order.
const data = await request(
    `/orders/${activeOrderId}/tracking`
);

        const status = data.status || data.state;
        const currentIndex = statusSteps.indexOf(status);

        trackingContent.replaceChildren();

        trackingContent.appendChild(
            createElement("h3", "", `Order #${activeOrderId}`)
        );

        trackingContent.appendChild(
            createElement(
                "p",
                "",
                `Current status: ${status || "Unknown"}`
            )
        );

        // Display the progress indicator.
        const steps = createElement("div", "tracking-steps");

        statusSteps.forEach((step, index) => {
            const completed =
                currentIndex >= 0 && index <= currentIndex;

            const node = createElement(
                "div",
                `tracking-step ${completed ? "completed" : ""}`,
                step.replaceAll("_", " ")
            );

            steps.appendChild(node);
        });

        trackingContent.appendChild(steps);

        if (status === "CANCELLED") {
            trackingContent.appendChild(
                createElement("p", "", "This order was cancelled.")
            );
        }

        // Display the ETA when the backend provides it.
        if (
            data.eta_minutes !== undefined &&
            data.eta_minutes !== null
        ) {
            trackingContent.appendChild(
                createElement(
                    "p",
                    "",
                    `Estimated time: ${data.eta_minutes} minutes`
                )
            );
        }

        // Stop polling completed or cancelled orders.
        if (status === "DELIVERED" || status === "CANCELLED") {
            if (trackingTimer !== null) {
                clearInterval(trackingTimer);
                trackingTimer = null;
            }
        }

    } catch (error) {
        trackingContent.textContent =
            `Tracking error: ${error.message}`;
    }
}

// ============================================================
// 10. SEARCH AND BUTTON EVENTS
// ============================================================

// Filters the restaurant cards as the user types.
searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();

    renderRestaurants(
        restaurants.filter(restaurant =>
            restaurant.name.toLowerCase().includes(query) ||
            (restaurant.cuisine || "").toLowerCase().includes(query)
        )
    );
});

// Opens the shopping cart.
document.getElementById("cartButton").addEventListener(
    "click",
    () => cartPanel.classList.remove("hidden")
);

// Closes the shopping cart.
document.getElementById("closeCart").addEventListener(
    "click",
    () => cartPanel.classList.add("hidden")
);

// Creates an order when checkout is clicked.
checkoutButton.addEventListener("click", checkout);

// ============================================================
// 11. INITIALIZE THE WEBSITE
// ============================================================

// Display the empty cart and retrieve restaurant information.
updateCart();
loadRestaurants();
