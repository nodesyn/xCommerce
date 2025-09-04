// xCommerce Main JavaScript
class XCommerce {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
    }

    setupEventListeners() {
        // Mobile menu toggle
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-mobile-menu-toggle]')) {
                this.toggleMobileMenu();
            }
        });

        // Cart operations
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-add-to-cart]')) {
                this.addToCart(e);
            }
            if (e.target.matches('[data-remove-from-cart]')) {
                this.removeFromCart(e);
            }
        });

        // Theme toggle
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-theme-toggle]')) {
                this.toggleTheme();
            }
        });

        // Search functionality
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
        }
    }

    initializeComponents() {
        this.initImageGallery();
        this.initQuantitySelectors();
        this.initTooltips();
    }

    // Mobile Menu
    toggleMobileMenu() {
        const menu = document.querySelector('[data-mobile-menu]');
        const overlay = document.querySelector('[data-mobile-overlay]');
        
        if (menu) {
            menu.classList.toggle('translate-x-0');
            menu.classList.toggle('-translate-x-full');
        }
        
        if (overlay) {
            overlay.classList.toggle('hidden');
        }
        
        document.body.classList.toggle('overflow-hidden');
    }

    // Cart Operations
    async addToCart(e) {
        e.preventDefault();
        const button = e.target;
        const productId = button.dataset.productId;
        const variantId = button.dataset.variantId;
        const quantity = parseInt(button.dataset.quantity) || 1;

        this.showLoading(button);

        try {
            const response = await fetch('/api/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    product_id: productId,
                    variant_id: variantId,
                    quantity: quantity
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.updateCartUI(data);
                this.showToast('Product added to cart', 'success');
                button.textContent = 'Added!';
                setTimeout(() => {
                    button.textContent = 'Add to Cart';
                }, 2000);
            } else {
                this.showToast(data.error || 'Failed to add product to cart', 'error');
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            this.showToast('Something went wrong', 'error');
        } finally {
            this.hideLoading(button);
        }
    }

    async removeFromCart(e) {
        e.preventDefault();
        const button = e.target;
        const itemId = button.dataset.itemId;

        try {
            const response = await fetch(`/api/cart/remove/${itemId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });

            if (response.ok) {
                button.closest('[data-cart-item]').remove();
                this.updateCartTotals();
                this.showToast('Item removed from cart', 'success');
            }
        } catch (error) {
            console.error('Error removing from cart:', error);
            this.showToast('Failed to remove item', 'error');
        }
    }

    // Theme Management
    toggleTheme() {
        const html = document.documentElement;
        const isDark = html.classList.contains('dark');
        
        if (isDark) {
            html.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        }
    }

    // Search
    async handleSearch(e) {
        const query = e.target.value.trim();
        const resultsContainer = document.querySelector('[data-search-results]');

        if (query.length < 2) {
            if (resultsContainer) {
                resultsContainer.innerHTML = '';
                resultsContainer.classList.add('hidden');
            }
            return;
        }

        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (resultsContainer && data.results) {
                this.renderSearchResults(data.results, resultsContainer);
                resultsContainer.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    renderSearchResults(results, container) {
        if (!results.length) {
            container.innerHTML = '<div class="p-4 text-gray-500">No results found</div>';
            return;
        }

        const html = results.map(product => `
            <a href="/products/${product.slug}/" class="block p-4 hover:bg-gray-50 dark:hover:bg-gray-800">
                <div class="flex items-center space-x-3">
                    <img src="${product.image || '/static/img/placeholder.png'}" alt="${product.name}" class="w-12 h-12 object-cover rounded">
                    <div>
                        <h4 class="font-medium text-gray-900 dark:text-gray-100">${product.name}</h4>
                        <p class="text-sm text-gray-500 dark:text-gray-400">$${product.price}</p>
                    </div>
                </div>
            </a>
        `).join('');

        container.innerHTML = html;
    }

    // Image Gallery
    initImageGallery() {
        const thumbnails = document.querySelectorAll('[data-thumbnail]');
        const mainImage = document.querySelector('[data-main-image]');

        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', (e) => {
                e.preventDefault();
                const newSrc = thumb.dataset.fullImage;
                const newAlt = thumb.dataset.alt;

                if (mainImage && newSrc) {
                    mainImage.src = newSrc;
                    mainImage.alt = newAlt;

                    // Update active thumbnail
                    thumbnails.forEach(t => t.classList.remove('ring-2', 'ring-primary-500'));
                    thumb.classList.add('ring-2', 'ring-primary-500');
                }
            });
        });
    }

    // Quantity Selectors
    initQuantitySelectors() {
        document.querySelectorAll('[data-quantity-selector]').forEach(selector => {
            const input = selector.querySelector('input');
            const decreaseBtn = selector.querySelector('[data-decrease]');
            const increaseBtn = selector.querySelector('[data-increase]');

            if (decreaseBtn) {
                decreaseBtn.addEventListener('click', () => {
                    const current = parseInt(input.value) || 1;
                    if (current > 1) {
                        input.value = current - 1;
                        this.triggerQuantityChange(input);
                    }
                });
            }

            if (increaseBtn) {
                increaseBtn.addEventListener('click', () => {
                    const current = parseInt(input.value) || 1;
                    const max = parseInt(input.getAttribute('max')) || 999;
                    if (current < max) {
                        input.value = current + 1;
                        this.triggerQuantityChange(input);
                    }
                });
            }

            if (input) {
                input.addEventListener('change', () => {
                    this.triggerQuantityChange(input);
                });
            }
        });
    }

    triggerQuantityChange(input) {
        const event = new CustomEvent('quantityChange', {
            detail: { quantity: parseInt(input.value), input: input }
        });
        input.dispatchEvent(event);
    }

    // Tooltips
    initTooltips() {
        const tooltips = document.querySelectorAll('[data-tooltip]');
        tooltips.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip.bind(this));
            element.addEventListener('mouseleave', this.hideTooltip.bind(this));
        });
    }

    showTooltip(e) {
        const text = e.target.dataset.tooltip;
        const tooltip = document.createElement('div');
        tooltip.className = 'absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg';
        tooltip.textContent = text;
        tooltip.id = 'tooltip';

        document.body.appendChild(tooltip);
        
        const rect = e.target.getBoundingClientRect();
        tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
    }

    hideTooltip() {
        const tooltip = document.getElementById('tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    // UI Updates
    updateCartUI(data) {
        const cartCount = document.querySelector('[data-cart-count]');
        if (cartCount && data.cart_count !== undefined) {
            cartCount.textContent = data.cart_count;
            cartCount.classList.toggle('hidden', data.cart_count === 0);
        }
    }

    updateCartTotals() {
        // This would be called after cart updates to refresh totals
        const cartItems = document.querySelectorAll('[data-cart-item]');
        let total = 0;

        cartItems.forEach(item => {
            const price = parseFloat(item.dataset.price) || 0;
            const quantity = parseInt(item.querySelector('[data-quantity]').value) || 0;
            total += price * quantity;
        });

        const totalElement = document.querySelector('[data-cart-total]');
        if (totalElement) {
            totalElement.textContent = `$${total.toFixed(2)}`;
        }
    }

    // Notifications
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast-notification p-4 rounded-lg shadow-lg text-white fade-in ${this.getToastColor(type)}`;
        toast.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-3 text-white hover:text-gray-200">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;

        container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    getToastColor(type) {
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        };
        return colors[type] || colors.info;
    }

    // Loading States
    showLoading(element) {
        const originalText = element.textContent;
        element.dataset.originalText = originalText;
        element.textContent = 'Loading...';
        element.disabled = true;
    }

    hideLoading(element) {
        element.textContent = element.dataset.originalText || 'Submit';
        element.disabled = false;
    }

    // Utilities
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.xcommerce = new XCommerce();
});

// Service Worker Registration (for PWA functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}