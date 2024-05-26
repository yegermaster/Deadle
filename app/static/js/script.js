/**
 * Get elements by ID or class.
 */
const getById = id => document.getElementById(id);
const getByClass = (element, className) => element.getElementsByClassName(className)[0];

// Modals and buttons
const modals = {
    about: getById("aboutModal"),
    help: getById("helpModal"),
    stats: getById("statsModal")
};

const buttons = {
    about: getById("aboutBtn"),
    help: getById("helpBtn"),
    stats: getById("statsBtn")
};

// Close buttons
const closeButtons = {
    about: getByClass(modals.about, "close"),
    help: getByClass(modals.help, "close"),
    stats: getByClass(modals.stats, "close")
};

/**
 * Open modal.
 * @param {HTMLElement} modal - The modal element to show.
 */
const openModal = modal => modal.style.visibility = "visible";

/**
 * Close modal.
 * @param {HTMLElement} modal - The modal element to hide.
 */
const closeModal = modal => modal.style.visibility = "hidden";

// Attach event listeners to buttons
buttons.about.onclick = () => openModal(modals.about);
buttons.help.onclick = () => openModal(modals.help);
buttons.stats.onclick = () => openModal(modals.stats);

// Attach event listeners to close buttons
closeButtons.about.onclick = () => closeModal(modals.about);
closeButtons.help.onclick = () => closeModal(modals.help);
closeButtons.stats.onclick = () => closeModal(modals.stats);

// Close modals when clicking outside
window.onclick = function(event) {
    Object.values(modals).forEach(modal => {
        if (event.target === modal) {
            closeModal(modal);
        }
    });
};
