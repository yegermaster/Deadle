/**
 * Get elements by ID or class.
 */
const getById = id => document.getElementById(id);
const getByClass = (element, className) => element.getElementsByClassName(className)[0];

// Modals and buttons
const modals = {
    about: getById("aboutModal"),
    help: getById("helpModal"),
    stats: getById("statsModal"),
    login: getById("loginModal")
};

const buttons = {
    about: getById("aboutBtn"),
    help: getById("helpBtn"),
    stats: getById("statsBtn")
};

// Open and close modal functions
const openModal = modal => {
    console.log(`Opening modal: ${modal.id}`);
    modal.style.display = "block";
};

const closeModal = modal => {
    console.log(`Closing modal: ${modal.id}`);
    modal.style.display = "none";
};

// Ensure modals are initially hidden
Object.values(modals).forEach(modal => {
    if (modal) {
        modal.style.display = "none";
    }
});

// Close modals when clicking outside
window.onclick = function(event) {
    Object.values(modals).forEach(modal => {
        if (modal && event.target === modal && modal !== modals.login) { // Prevent closing login modal
            closeModal(modal);
        }
    });
};

// Attach event listeners to buttons
Object.keys(buttons).forEach(key => {
    const button = buttons[key];
    if (button) {
        button.onclick = () => {
            console.log(`Button clicked: ${key}`);
            openModal(modals[key]);
        };
    }
});

// Close modal when close button is clicked
document.querySelectorAll('.close').forEach(btn => {
    btn.onclick = function() {
        const modalId = this.dataset.modal + "Modal";
        console.log(`Close button clicked, closing modal: ${modalId}`);
        closeModal(getById(modalId));
    };
});

window.onload = function() {
    fetch('/check-auth')
        .then(response => response.json())
        .then(data => {
            if (!data.is_authenticated) {
                openModal(modals.login);
            }
        })
        .catch(error => console.error('Error checking authentication:', error));
};


// Test function to verify modal functionality
const testModals = () => {
    console.log("Testing modals:");
    Object.keys(buttons).forEach(key => {
        buttons[key].click();
        console.log(`${key} modal should be visible.`);
        setTimeout(() => {
            console.log(`${key} modal should be hidden.`);
            closeModal(modals[key]);
        }, 2000); // Hide after 2 seconds
    });
};

// Uncomment to test modals
// testModals();
