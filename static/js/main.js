// static/js/main.js

// Initialize AOS (Animate on Scroll)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
        navbar.style.backgroundColor = '#1a1a1a';
    } else {
        navbar.classList.remove('navbar-scrolled');
        navbar.style.backgroundColor = '#212529';
    }
});

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                }
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Tour audio player controls
const audioPlayers = document.querySelectorAll('audio');
audioPlayers.forEach(player => {
    player.addEventListener('play', function() {
        // Pause other players when this one starts
        audioPlayers.forEach(p => {
            if (p !== this && !p.paused) {
                p.pause();
            }
        });
    });

    // Save playback position
    player.addEventListener('timeupdate', function() {
        localStorage.setItem('audioPosition_' + this.src, this.currentTime);
    });

    // Resume from saved position
    const savedPosition = localStorage.getItem('audioPosition_' + player.src);
    if (savedPosition) {
        player.currentTime = parseFloat(savedPosition);
    }
});

// Loading spinner for async operations
function showSpinner(show = true) {
    let spinner = document.querySelector('.loading-spinner');

    if (show) {
        if (!spinner) {
            spinner = document.createElement('div');
            spinner.className = 'loading-spinner spinner';
            spinner.style.position = 'fixed';
            spinner.style.top = '50%';
            spinner.style.left = '50%';
            spinner.style.transform = 'translate(-50%, -50%)';
            spinner.style.zIndex = '9999';
            document.body.appendChild(spinner);
        }
    } else {
        if (spinner) {
            spinner.remove();
        }
    }
}

// Copy link functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = 'Link copied to clipboard!';
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Debounce function for search
function debounce(func, wait) {
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

// Handle escape key for modals
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Initialize toastr options
if (typeof toastr !== 'undefined') {
    toastr.options = {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-top-right",
        timeOut: 3000
    };
}

// ============================================
// NEW: DARK MODE TOGGLE
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');

    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        if (darkModeIcon) {
            darkModeIcon.classList.remove('fa-moon');
            darkModeIcon.classList.add('fa-sun');
        }
    }

    // Toggle dark mode
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');

            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
                if (darkModeIcon) {
                    darkModeIcon.classList.remove('fa-moon');
                    darkModeIcon.classList.add('fa-sun');
                }
                if (typeof toastr !== 'undefined') {
                    toastr.success('Dark mode enabled');
                }
            } else {
                localStorage.setItem('darkMode', 'disabled');
                if (darkModeIcon) {
                    darkModeIcon.classList.remove('fa-sun');
                    darkModeIcon.classList.add('fa-moon');
                }
                if (typeof toastr !== 'undefined') {
                    toastr.info('Light mode enabled');
                }
            }
        });
    }
});

// ============================================
// NEW: SKELETON LOADING
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const skeletonLoader = document.getElementById('skeletonLoader');
    const monumentsContainer = document.getElementById('monumentsContainer');

    if (skeletonLoader && monumentsContainer) {
        // Simulate loading delay (remove this in production)
        setTimeout(function() {
            skeletonLoader.style.display = 'none';
            monumentsContainer.style.display = 'flex';
        }, 800);
    }
});

// ============================================
// NEW: IMAGE ZOOM ON HOVER
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const zoomContainers = document.querySelectorAll('.zoom-container');

    zoomContainers.forEach(container => {
        const img = container.querySelector('.zoom-image');
        const lens = container.querySelector('.zoom-lens');

        if (!img || !lens) return;

        container.addEventListener('mousemove', function(e) {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Calculate lens position
            let lensX = x - lens.offsetWidth / 2;
            let lensY = y - lens.offsetHeight / 2;

            // Constrain lens within container
            lensX = Math.max(0, Math.min(lensX, rect.width - lens.offsetWidth));
            lensY = Math.max(0, Math.min(lensY, rect.height - lens.offsetHeight));

            lens.style.left = lensX + 'px';
            lens.style.top = lensY + 'px';

            // Calculate zoom position
            const imgWidth = img.naturalWidth;
            const imgHeight = img.naturalHeight;

            const zoomX = (lensX / rect.width) * imgWidth;
            const zoomY = (lensY / rect.height) * imgHeight;

            // Apply zoom transform
            img.style.transformOrigin = `${zoomX}px ${zoomY}px`;
            img.classList.add('zoomed');
        });

        container.addEventListener('mouseleave', function() {
            img.classList.remove('zoomed');
            img.style.transformOrigin = 'center center';
        });

        // Double-click for full zoom
        img.addEventListener('dblclick', function(e) {
            e.preventDefault();
            this.classList.toggle('full-zoom');
            if (this.classList.contains('full-zoom')) {
                this.style.transform = 'scale(2.5)';
                this.style.cursor = 'zoom-out';
            } else {
                this.style.transform = 'scale(1)';
                this.style.cursor = 'zoom-in';
            }
        });
    });
});

// ============================================
// NEW: FULL SCREEN FOR VIRTUAL TOURS
// ============================================
function toggleFullScreen() {
    const panorama = document.getElementById('panorama');
    if (!panorama) return;

    if (!document.fullscreenElement) {
        // Enter full screen
        if (panorama.requestFullscreen) {
            panorama.requestFullscreen();
        } else if (panorama.webkitRequestFullscreen) { /* Safari */
            panorama.webkitRequestFullscreen();
        } else if (panorama.msRequestFullscreen) { /* IE11 */
            panorama.msRequestFullscreen();
        }

        // Change button icon
        const btn = document.querySelector('.fullscreen-btn');
        if (btn) {
            btn.innerHTML = '<i class="fas fa-compress"></i> Exit Full Screen';
        }
    } else {
        // Exit full screen
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) { /* Safari */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE11 */
            document.msExitFullscreen();
        }

        // Change button icon
        const btn = document.querySelector('.fullscreen-btn');
        if (btn) {
            btn.innerHTML = '<i class="fas fa-expand"></i> Full Screen';
        }
    }
}

// Listen for full screen change events
document.addEventListener('fullscreenchange', updateFullScreenButton);
document.addEventListener('webkitfullscreenchange', updateFullScreenButton);
document.addEventListener('msfullscreenchange', updateFullScreenButton);

function updateFullScreenButton() {
    const btn = document.querySelector('.fullscreen-btn');
    if (!btn) return;

    if (document.fullscreenElement) {
        btn.innerHTML = '<i class="fas fa-compress"></i> Exit Full Screen';
    } else {
        btn.innerHTML = '<i class="fas fa-expand"></i> Full Screen';
    }
}

// ============================================
// NEW: ENHANCED BREADCRUMB
// ============================================
function generateBreadcrumb() {
    // This is handled by Django template
    // Just add active class to current page
    const path = window.location.pathname;
    const breadcrumbItems = document.querySelectorAll('.breadcrumb-item a');

    breadcrumbItems.forEach(item => {
        if (item.getAttribute('href') === path) {
            item.classList.add('active');
        }
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', generateBreadcrumb);