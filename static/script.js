// script.js - JavaScript for Crop Recommendation System

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Input range sliders - update value display
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    rangeInputs.forEach(input => {
        const valueDisplay = document.getElementById(`${input.id}-value`);
        if (valueDisplay) {
            valueDisplay.textContent = input.value;
            
            input.addEventListener('input', () => {
                valueDisplay.textContent = input.value;
            });
        }
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach(message => {
        setTimeout(() => {
            const closeButton = message.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000); // Auto-dismiss after 5 seconds
    });

    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // File input validation - check file type
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', () => {
            const filePath = fileInput.value;
            const allowedExtensions = /(\.csv)$/i;
            
            if (!allowedExtensions.exec(filePath)) {
                alert('Please upload a CSV file only');
                fileInput.value = '';
                return false;
            }
        });
    }

    // Input validation for number inputs
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', () => {
            const min = parseFloat(input.getAttribute('min'));
            const max = parseFloat(input.getAttribute('max'));
            const value = parseFloat(input.value);
            
            if (value < min) {
                input.setCustomValidity(`Value should be at least ${min}`);
            } else if (value > max) {
                input.setCustomValidity(`Value should be at most ${max}`);
            } else {
                input.setCustomValidity('');
            }
        });
    });

    // Dynamic form field - Show/hide additional fields based on selection
    const cropTypeSelect = document.getElementById('crop-type');
    const additionalFields = document.getElementById('additional-fields');
    
    if (cropTypeSelect && additionalFields) {
        cropTypeSelect.addEventListener('change', () => {
            if (cropTypeSelect.value !== '') {
                additionalFields.classList.remove('d-none');
            } else {
                additionalFields.classList.add('d-none');
            }
        });
    }
});