/**
 * Get elements by ID or class.
 */
const getById = id => document.getElementById(id); // A function that takes 'id' and retunres the element with that ID
const getByClass = (element, className) => element.getElementsByClassName(className)[0]; // A function that take element and className and returns the first element with that class name 

// Modals and buttons
const modals = { // An object that stores refrences to the modal elements by thier IDs.
    about: getById("aboutModal"),
    help: getById("helpModal"),
    stats: getById("statsModal")
};

const buttons = { // An object that stores references to the button elements by their IDs.
    about: getById("aboutBtn"),
    help: getById("helpBtn"),
    stats: getById("statsBtn")
};

// Close buttons
const closeButtons = { // An object that stores references to the close button elements inside each modal by their class name "close".
    about: getByClass(modals.about, "close"),
    help: getByClass(modals.help, "close"),
    stats: getByClass(modals.stats, "close")
};

/**
 * Open modal.
 * @param {HTMLElement} modal - The modal element to show.
 */
const openModal = modal => modal.style.visibility = "visible"; // A function that takes a modal element and sets its visibility to "visible" to show it.

/**
 * Close modal.
 * @param {HTMLElement} modal - The modal element to hide.
 */
const closeModal = modal => modal.style.visibility = "hidden"; // A function that takes a modal element and sets its visibility to "hidden".

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
