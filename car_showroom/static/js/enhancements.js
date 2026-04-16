// Luxury Car Showroom - JavaScript Enhancements

class UIEnhancer {
    constructor() {
        this.initializeEnhancements();
    }
    
    initializeEnhancements() {
        this.enhanceCarCards();
        this.enhanceForms();
        this.addPriceFormatters();
        this.addImageLazyLoading();
        this.addSmoothAnimations();
        this.addCounterAnimations();
        this.enhanceNavigation();
    }
    
    enhanceCarCards() {
        // Add hover delay for better UX
        const carCards = document.querySelectorAll('.car-card');
        carCards.forEach(card => {
            card.style.transitionDelay = '0.1s';
            
            // Add touch feedback for mobile
            card.addEventListener('touchstart', () => {
                card.classList.add('active');
            });
            
            card.addEventListener('touchend', () => {
                setTimeout(() => card.classList.remove('active'), 150);
            });
        });
    }
    
    enhanceForms() {
        // Add floating label effect
        const formInputs = document.querySelectorAll('.form-input');
        formInputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    input.parentElement.classList.remove('focused');
                }
            });
            
            // Initialize
            if (input.value) {
                input.parentElement.classList.add('focused');
            }
        });
    }
    
    addPriceFormatters() {
        // Format all prices on the page
        const priceElements = document.querySelectorAll('[data-price]');
        priceElements.forEach(element => {
            const price = parseFloat(element.dataset.price);
            if (!isNaN(price)) {
                element.textContent = this.formatPrice(price);
            }
        });
        
        // Also format any element with class "price"
        document.querySelectorAll('.price').forEach(element => {
            const priceText = element.textContent.replace(/[^0-9.]/g, '');
            const price = parseFloat(priceText);
            if (!isNaN(price)) {
                element.textContent = this.formatPrice(price);
            }
        });
    }
    
    formatPrice(price) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(price);
    }
    
    addImageLazyLoading() {
        // Lazy load images with Intersection Observer
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                        
                        // Add fade-in effect
                        img.style.opacity = '0';
                        img.style.transition = 'opacity 0.5s ease';
                        setTimeout(() => {
                            img.style.opacity = '1';
                        }, 10);
                    }
                });
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for older browsers
            lazyImages.forEach(img => {
                img.src = img.dataset.src;
            });
        }
    }
    
    addSmoothAnimations() {
        // Add staggered animation to grid items
        const staggerItems = document.querySelectorAll('.stagger-item');
        staggerItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
        });
        
        // Add scroll animations
        this.addScrollAnimations();
    }
    
    addScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements with data-animate attribute
        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });
    }
    
    addCounterAnimations() {
        // Animate statistics counters
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = 2000; // 2 seconds
            const step = target / (duration / 16); // 60fps
            
            let current = 0;
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.floor(current).toLocaleString();
            }, 16);
        });
    }
    
    enhanceNavigation() {
        // Add active state to current page in navigation
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('nav a');
        
        navLinks.forEach(link => {
            const linkPath = link.getAttribute('href');
            if (linkPath === currentPath || 
                (linkPath !== '/' && currentPath.startsWith(linkPath))) {
                link.classList.add('active');
            }
        });
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href');
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
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.uiEnhancer = new UIEnhancer();
    
    // Additional enhancement: Add keyboard navigation to car filters
    enhanceFiltersWithKeyboard();
    
    // Add loading states for forms
    enhanceFormsWithLoading();
});

function enhanceFiltersWithKeyboard() {
    const filterInputs = document.querySelectorAll('input[type="range"], select');
    filterInputs.forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.target.closest('form').submit();
            }
        });
    });
}

function enhanceFormsWithLoading() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = `
                    <svg class="animate-spin h-5 w-5 mr-2 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                `;
                submitBtn.disabled = true;
            }
        });
    });
}

// Price animation for featured cars
function animatePriceChange(element, newPrice) {
    const currentPrice = parseFloat(element.textContent.replace(/[^0-9.]/g, ''));
    if (isNaN(currentPrice)) return;
    
    const difference = newPrice - currentPrice;
    const steps = 30;
    const stepTime = 20;
    
    for (let i = 1; i <= steps; i++) {
        setTimeout(() => {
            const current = currentPrice + (difference * (i / steps));
            element.textContent = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0
            }).format(current);
        }, i * stepTime);
    }
}

// Export for use in templates
window.formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(price);
};