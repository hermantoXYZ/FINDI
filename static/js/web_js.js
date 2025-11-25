
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger-menu');
    const navMenu = document.querySelector('.nav-menu');

    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    // Close menu if a link is clicked (optional, good for single-page apps)
    // Exclude dropdown links to prevent menu from closing when opening dropdowns
    document.querySelectorAll('.nav-menu ul li a:not(.has-dropdown > a)').forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth <= 992) { // Only for mobile
                navMenu.classList.remove('active');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Toggle dropdown on click for mobile
    document.querySelectorAll('.nav-menu .has-dropdown > a').forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                e.stopPropagation(); // Prevent event bubbling
                const parentLi = this.parentElement;
                
                // Simple toggle - if active, close it; if not active, open it and close others
                if (parentLi.classList.contains('active')) {
                    // If already active, close it
                    parentLi.classList.remove('active');
                } else {
                    // If not active, close all others and open this one
                    document.querySelectorAll('.nav-menu .has-dropdown').forEach(function(li) {
                        li.classList.remove('active');
                    });
                    parentLi.classList.add('active');
                }
            }
        });
    });

    // Optional: Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 992) {
            // Don't close dropdowns if clicking inside the nav menu
            if (!e.target.closest('.nav-menu')) {
                document.querySelectorAll('.nav-menu .has-dropdown').forEach(function(li) {
                    li.classList.remove('active');
                });
            }
        }
    });
});

const sliderContainer = document.getElementById('sliderContainer');
const dotsContainer = document.getElementById('sliderDots');
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
let currentSlideIndex = 0;
let autoSlideInterval;

// Fungsi untuk menampilkan slide tertentu
function showSlide(index) {
// Pastikan indeks berada dalam batas yang valid
if (index >= slides.length) {
    currentSlideIndex = 0;
} else if (index < 0) {
    currentSlideIndex = slides.length - 1;
} else {
    currentSlideIndex = index;
}

// Geser container slider
sliderContainer.style.transform = `translateX(-${currentSlideIndex * 100}%)`;

// Update dot aktif
dots.forEach((dot, i) => {
    dot.classList.remove('active');
    if (i === currentSlideIndex) {
        dot.classList.add('active');
    }
});

// Re-trigger animasi konten slide
slides.forEach(slide => {
    const content = slide.querySelector('.slide-content');
    if (content) {
        content.style.animation = 'none'; // Reset animation
        void content.offsetWidth; // Trigger reflow
        content.style.animation = 'fadeInScale 1.2s ease-out forwards'; // Restart animation
    }
});
}

// Fungsi untuk slide berikutnya
function nextSlide() {
showSlide(currentSlideIndex + 1);
resetAutoSlide();
}

// Fungsi untuk slide sebelumnya
function prevSlide() {
showSlide(currentSlideIndex - 1);
resetAutoSlide();
}

// Fungsi untuk navigasi langsung melalui dot
function currentSlide(n) {
showSlide(n - 1); // n-1 karena indeks array dimulai dari 0
resetAutoSlide();
}

// Fungsi untuk memulai auto-slide
function startAutoSlide() {
autoSlideInterval = setInterval(() => {
    nextSlide();
}, 5000); // Ganti slide setiap 5 detik
}

// Fungsi untuk mereset auto-slide (saat navigasi manual)
function resetAutoSlide() {
clearInterval(autoSlideInterval);
startAutoSlide();
}

// Inisialisasi slider saat halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
showSlide(0); // Tampilkan slide pertama
startAutoSlide(); // Mulai auto-slide
});

// Optional: Pause auto-slide on hover
sliderContainer.addEventListener('mouseenter', () => {
clearInterval(autoSlideInterval);
});

sliderContainer.addEventListener('mouseleave', () => {
startAutoSlide();
});

// Basic touch/swipe functionality for mobile
let touchStartX = 0;
let touchEndX = 0;

sliderContainer.addEventListener('touchstart', (e) => {
touchStartX = e.touches[0].clientX;
});

sliderContainer.addEventListener('touchend', (e) => {
touchEndX = e.changedTouches[0].clientX;
handleSwipe();
});

function handleSwipe() {
const swipeThreshold = 50; // Minimum distance for a swipe

if (touchEndX < touchStartX - swipeThreshold) {
    nextSlide(); // Swiped left
} else if (touchEndX > touchStartX + swipeThreshold) {
    prevSlide(); // Swiped right
}
}
