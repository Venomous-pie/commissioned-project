/* static/js/main.js */

document.addEventListener('DOMContentLoaded', function() {
    // Add to cart AJAX functionality
    const addToCartLinks = document.querySelectorAll('a[href^="/cart/add/"]');
    addToCartLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create a form to submit the data
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = this.href;
            
            // Add CSRF token
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = document.querySelector('#csrf-form input[name="csrfmiddlewaretoken"]').value;
            form.appendChild(csrfInput);
            
            // Add quantity
            const quantityInput = document.createElement('input');
            quantityInput.type = 'hidden';
            quantityInput.name = 'quantity';
            quantityInput.value = '1';
            form.appendChild(quantityInput);
            
            // Submit the form with AJAX
            const formData = new FormData(form);
            fetch(this.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update cart badge
                const cartBadge = document.querySelector('.navbar .fa-shopping-cart').nextElementSibling;
                if (data.cart_count > 0) {
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                    } else {
                        const newBadge = document.createElement('span');
                        newBadge.className = 'badge rounded-pill bg-danger';
                        newBadge.textContent = data.cart_count;
                        document.querySelector('.navbar .fa-shopping-cart').after(newBadge);
                    }
                }
                
                // Show success message
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-success alert-dismissible fade show';
                alertDiv.innerHTML = '<strong>Success!</strong> Item added to your cart.' +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
                document.querySelector('main').prepend(alertDiv);
                
                // Update button text to "Add More"
                this.textContent = 'Add More';
                
                // Automatically close the alert after 3 seconds
                setTimeout(() => {
                    const alert = document.querySelector('.alert');
                    if (alert) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 3000);
            })
            .catch(error => {
                console.error('Error adding to cart:', error);
            });
        });
    });

    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Add slide-in-up animation to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('slide-in-up');
        }, index * 100); // Stagger the animations
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const productCard = this.closest('.product-card');
            if (productCard) {
                productCard.classList.add('animate__animated', 'animate__pulse');
                setTimeout(() => {
                    productCard.classList.remove('animate__animated', 'animate__pulse');
                }, 1000);
            }
        });
    });
    
    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) {
                this.value = 1;
            }
        });
    });
    
    // Wishlist toggle with AJAX
    const wishlistForms = document.querySelectorAll('form[action^="/add-to-wishlist/"]');
    wishlistForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Only handle if the user is logged in (form exists)
            e.preventDefault();
            
            // Get the button and icon
            const button = this.querySelector('button');
            const icon = button.querySelector('i');
            
            // Create form data for submission
            const formData = new FormData(this);
            
            // Submit the form with AJAX
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update UI based on response
                if (data.in_wishlist) {
                    // Item added to wishlist
                    if (icon) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        icon.classList.add('text-danger');
                    }
                    // If we have text in the button, update it
                    if (button.textContent.trim().length > 0) {
                        button.classList.remove('btn-outline-danger');
                        button.classList.add('btn-danger');
                        // Find text node and update it
                        for (let node of button.childNodes) {
                            if (node.nodeType === 3) { // Text node
                                node.textContent = ' In Wishlist';
                                break;
                            }
                        }
                    }
                } else {
                    // Item removed from wishlist
                    if (icon) {
                        icon.classList.remove('fas');
                        icon.classList.remove('text-danger');
                        icon.classList.add('far');
                    }
                    // If we have text in the button, update it
                    if (button.textContent.trim().length > 0) {
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-danger');
                        // Find text node and update it
                        for (let node of button.childNodes) {
                            if (node.nodeType === 3) { // Text node
                                node.textContent = ' Add to Wishlist';
                                break;
                            }
                        }
                    }
                }
                
                // Show success message
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-success alert-dismissible fade show';
                alertDiv.innerHTML = '<strong>Success!</strong> ' + data.message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
                document.querySelector('main').prepend(alertDiv);
                
                // Automatically close the alert after 3 seconds
                setTimeout(() => {
                    const alert = document.querySelector('.alert');
                    if (alert) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 3000);
            })
            .catch(error => {
                console.error('Error updating wishlist:', error);
            });
        });
    });
    
    // Wishlist toggle animation (for non-AJAX fallback)
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't apply this if we're already handling with AJAX
            if (button.closest('form[action^="/add-to-wishlist/"]')) {
                // Don't toggle the icon here since the AJAX response will handle it
                return;
            }
            
            // For non-AJAX fallback - this code should rarely execute
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.classList.add('text-danger');
            } else {
                icon.classList.remove('fas');
                icon.classList.remove('text-danger');
                icon.classList.add('far');
            }
        });
    });

    // Search Suggestions
    const searchInput = document.querySelector('.search-input');
    const suggestionsContainer = document.querySelector('.search-suggestions');
    let debounceTimer;

    // Show suggestions container when input is focused
    searchInput.addEventListener('focus', function() {
        if (this.value.length >= 2) {
            suggestionsContainer.style.display = 'block';
        }
    });

    // Hide suggestions container when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            suggestionsContainer.style.display = 'none';
        }
    });

    // Handle input changes
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        // Debounce the API call
        debounceTimer = setTimeout(() => {
            fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.suggestions.length > 0) {
                        suggestionsContainer.innerHTML = data.suggestions.map(product => `
                            <a href="${product.url}" class="suggestion-item text-decoration-none">
                                <img src="${product.image_url}" alt="${product.name}" class="suggestion-img">
                                <div class="suggestion-content">
                                    <div class="suggestion-title">${product.name}</div>
                                    <div class="suggestion-category">${product.category}</div>
                                </div>
                                <div class="suggestion-price">$${product.price}</div>
                            </a>
                        `).join('');
                        suggestionsContainer.style.display = 'block';
                    } else {
                        suggestionsContainer.innerHTML = `
                            <div class="suggestion-item">
                                <div class="suggestion-content">
                                    <div class="suggestion-title text-muted">No products found</div>
                                </div>
                            </div>
                        `;
                        suggestionsContainer.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error fetching suggestions:', error);
                });
        }, 300); // Wait 300ms after user stops typing
    });
});