'use strict';


// Select all elements with data-toggle="popover"
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="popover"]'));

// Initialize Bootstrap Popover for each selected element
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

/* Enable Bootstrap Alert */

// Select all elements with the class "alert"
var alertList = document.querySelectorAll('.alert');

// Initialize Bootstrap Alert for each selected element
alertList.forEach(function (alert) {
  new bootstrap.Alert(alert);
});

/* Responsive Sidepanel */

// Elements related to the responsive sidepanel
const sidePanelToggler = document.getElementById('sidepanel-toggler');
const sidePanel = document.getElementById('app-sidepanel');
const sidePanelDrop = document.getElementById('sidepanel-drop');
const sidePanelClose = document.getElementById('sidepanel-close');

// When the window loads, call the responsiveSidePanel function
window.addEventListener('load', function () {
  responsiveSidePanel();
});

// When the window is resized, call the responsiveSidePanel function
window.addEventListener('resize', function () {
  responsiveSidePanel();
});

// Function to handle responsive behavior of the sidepanel
function responsiveSidePanel() {
  let w = window.innerWidth;
  if (w >= 1200) {
    // If the window is larger
    sidePanel.classList.remove('sidepanel-hidden');
    sidePanel.classList.add('sidepanel-visible');
  } else {
    // If the window is smaller
    sidePanel.classList.remove('sidepanel-visible');
    sidePanel.classList.add('sidepanel-hidden');
  }
}

// Toggle sidepanel visibility when the sidePanelToggler is clicked
sidePanelToggler.addEventListener('click', () => {
  if (sidePanel.classList.contains('sidepanel-visible')) {
    sidePanel.classList.remove('sidepanel-visible');
    sidePanel.classList.add('sidepanel-hidden');
  } else {
    sidePanel.classList.remove('sidepanel-hidden');
    sidePanel.classList.add('sidepanel-visible');
  }
});

// Close the sidepanel when the sidePanelClose element is clicked
sidePanelClose.addEventListener('click', (e) => {
  e.preventDefault();
  sidePanelToggler.click();
});

// Close the sidepanel when the sidePanelDrop element is clicked
sidePanelDrop.addEventListener('click', (e) => {
  sidePanelToggler.click();
});


const searchMobileTrigger = document.querySelector('.search-mobile-trigger');
const searchBox = document.querySelector('.app-search-box');

searchMobileTrigger.addEventListener('click', () => {
  searchBox.classList.toggle('is-visible');

  let searchMobileTriggerIcon = document.querySelector('.search-mobile-trigger-icon');

  if (searchMobileTriggerIcon.classList.contains('fa-search')) {
    searchMobileTriggerIcon.classList.remove('fa-search');
    searchMobileTriggerIcon.classList.add('fa-times');
  } else {
    searchMobileTriggerIcon.classList.remove('fa-times');
    searchMobileTriggerIcon.classList.add('fa-search');
  }
});
