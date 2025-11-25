document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector(".hamburger");
    const closeIcon = document.querySelector(".close-icon");
    const navMenuContainer = document.querySelector(".nav-menu-container");

    // Desktop & Mobile elements
    const productLink = document.querySelector('#product-nav-item .product-link');
    const megaMenu = document.getElementById('product-mega-menu');
    const simpleDropdowns = document.querySelectorAll('.dropdown:not(#product-nav-item)');

    function isMobile() {
        return getComputedStyle(hamburger).display !== 'none';
    }

    // --- Mobile Menu Toggle --- //
    if (hamburger && closeIcon && navMenuContainer) {
        hamburger.addEventListener("click", () => {
            navMenuContainer.classList.add("active");
        });

        closeIcon.addEventListener("click", () => {
            navMenuContainer.classList.remove("active");
        });
    }

    // --- Desktop Mega Menu Toggle (Click) ---
    productLink.addEventListener('click', function(e) {
        e.preventDefault();
        if (isMobile()) return; // This logic is for desktop only

        const isActive = this.classList.contains('active');
        
        // Close everything first
        closeAllDesktopMenus();

        // If it wasn't active, open it
        if (!isActive) {
            this.classList.add('active');
            megaMenu.classList.add('active');
        }
    });

    // --- Desktop Simple Dropdowns (Hover) ---
    simpleDropdowns.forEach(dropdown => {
        let timeoutId;
        dropdown.addEventListener('mouseenter', () => {
            if (!isMobile()) {
                closeAllDesktopMenus(); // Close mega menu if open
                clearTimeout(timeoutId);
                dropdown.classList.add('active');
            }
        });

        dropdown.addEventListener('mouseleave', () => {
            if (!isMobile()) {
                timeoutId = setTimeout(() => {
                    dropdown.classList.remove('active');
                }, 200);
            }
        });
    });
    
    // --- Mobile Accordion Logic ---
    const allMobileDropdownLinks = document.querySelectorAll('.nav-menu .nav-link');
    allMobileDropdownLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!isMobile()) return;
            e.preventDefault();

            const dropdown = this.parentElement;
            const wasActive = dropdown.classList.contains('active');

            // Optional: Close others
            // document.querySelectorAll('.nav-menu .dropdown').forEach(d => {
            //     if (d !== dropdown) d.classList.remove('active');
            // });

            dropdown.classList.toggle('active');
        });
    });

    // --- Helper function to close all menus on desktop ---
    function closeAllDesktopMenus() {
        productLink.classList.remove('active');
        megaMenu.classList.remove('active');
        simpleDropdowns.forEach(d => d.classList.remove('active'));
    }

    // --- Close all menus when clicking outside ---
    document.addEventListener('click', function(e) {
        if (isMobile()) return;

        const isClickInsideHeader = document.querySelector('.site-header').contains(e.target);
        const isClickInsideMegaMenu = megaMenu.contains(e.target);

        if (!isClickInsideHeader && !isClickInsideMegaMenu) {
            closeAllDesktopMenus();
        }
    });
});



function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('show');
}

document.addEventListener('DOMContentLoaded', () => {
    const discoverGrids = document.querySelectorAll('.discover-grid');

    discoverGrids.forEach(discoverGrid => {
        let isDown = false;
        let startX;
        let scrollLeft;

        discoverGrid.addEventListener('mousedown', (e) => {
            isDown = true;
            discoverGrid.classList.add('active');
            startX = e.pageX - discoverGrid.offsetLeft;
            scrollLeft = discoverGrid.scrollLeft;
        });

        discoverGrid.addEventListener('mouseleave', () => {
            isDown = false;
            discoverGrid.classList.remove('active');
        });

        discoverGrid.addEventListener('mouseup', () => {
            isDown = false;
            discoverGrid.classList.remove('active');
        });

        discoverGrid.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - discoverGrid.offsetLeft;
            const walk = (x - startX) * 3; //scroll-fast
            discoverGrid.scrollLeft = scrollLeft - walk;
        });

        const scrollContainer = discoverGrid.parentElement;
        const leftButton = scrollContainer.querySelector('.scroll-button.left');
        const rightButton = scrollContainer.querySelector('.scroll-button.right');

        if(leftButton && rightButton) {
            leftButton.addEventListener('click', () => {
                discoverGrid.scrollBy({
                    left: -240,
                    behavior: 'smooth'
                });
            });

            rightButton.addEventListener('click', () => {
                discoverGrid.scrollBy({
                    left: 240,
                    behavior: 'smooth'
                });
            });
        }
    });
});