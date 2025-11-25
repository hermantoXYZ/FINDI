// Reusable Slider Class
class PartnersSlider {
    constructor(sliderId, prevBtnId, nextBtnId, dotsId) {
        this.slider = document.getElementById(sliderId);
        this.cards = this.slider.children;
        this.prevBtn = document.getElementById(prevBtnId);
        this.nextBtn = document.getElementById(nextBtnId);
        this.dotsContainer = document.getElementById(dotsId);

        this.currentIndex = 0;
        this.isDragging = false;
        this.startPos = 0;
        this.currentTranslate = 0;
        this.prevTranslate = 0;
        this.isAnimating = false;

        this.recalculateDimensions();
        this.init();
    }

    getCardWidth() {
        const screenWidth = window.innerWidth;
        if (screenWidth <= 480) return 280 + 16; // Mobile
        if (screenWidth <= 768) return 320 + 16; // Tablet
        return 350 + 16; // Desktop
    }

    getVisibleCards() {
        const containerWidth = this.slider.parentElement.offsetWidth;
        const cardWidth = this.getCardWidth();
        return Math.max(1, Math.floor(containerWidth / cardWidth));
    }

    recalculateDimensions() {
        this.cardWidth = this.getCardWidth();
        this.visibleCards = this.getVisibleCards();
        this.maxIndex = Math.max(0, this.cards.length - this.visibleCards);
        this.currentIndex = Math.min(this.currentIndex, this.maxIndex);

        this.createDots();
        this.updateButtons();
        this.goToSlide(this.currentIndex);
    }

    createDots() {
        this.dotsContainer.innerHTML = '';
        for (let i = 0; i <= this.maxIndex; i++) {
            const dot = document.createElement('div');
            dot.className = `dot ${i === this.currentIndex ? 'active' : ''}`;
            dot.addEventListener('click', () => this.goToSlide(i));
            this.dotsContainer.appendChild(dot);
        }
    }

    updateDots() {
        Array.from(this.dotsContainer.children).forEach((dot, i) => {
            dot.classList.toggle('active', i === this.currentIndex);
        });
    }

    goToSlide(index) {
        this.currentIndex = Math.max(0, Math.min(index, this.maxIndex));
        const translateX = -this.currentIndex * this.cardWidth;
        this.slider.style.transform = `translateX(${translateX}px)`;
        this.updateDots();
        this.updateButtons();
    }

    updateButtons() {
        this.prevBtn.disabled = this.currentIndex === 0;
        this.nextBtn.disabled = this.currentIndex === this.maxIndex;
    }

    nextSlide() {
        if (this.currentIndex < this.maxIndex) this.goToSlide(this.currentIndex + 1);
    }

    prevSlide() {
        if (this.currentIndex > 0) this.goToSlide(this.currentIndex - 1);
    }

    touchStart(e) {
        if (this.isAnimating) return;
        this.isDragging = true;
        this.startPos = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        this.prevTranslate = -this.currentIndex * this.cardWidth;
        this.slider.style.cursor = 'grabbing';
    }

    touchMove(e) {
        if (!this.isDragging || this.isAnimating) return;
        e.preventDefault();
        const currentPosition = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        this.currentTranslate = this.prevTranslate + currentPosition - this.startPos;

        // Resistance at edges
        if (this.currentTranslate > 0) this.currentTranslate *= 0.3;
        else if (this.currentTranslate < -this.maxIndex * this.cardWidth) {
            const overDrag = this.currentTranslate + this.maxIndex * this.cardWidth;
            this.currentTranslate = -this.maxIndex * this.cardWidth + overDrag * 0.3;
        }

        this.slider.style.transform = `translateX(${this.currentTranslate}px)`;
    }

    touchEnd() {
        if (!this.isDragging) return;
        this.isDragging = false;
        this.slider.style.cursor = 'grab';

        const movedBy = this.currentTranslate - this.prevTranslate;
        const threshold = this.cardWidth * 0.2;

        if (movedBy < -threshold && this.currentIndex < this.maxIndex) this.currentIndex++;
        else if (movedBy > threshold && this.currentIndex > 0) this.currentIndex--;

        this.isAnimating = true;
        this.slider.style.transition = 'transform 0.3s ease';
        this.goToSlide(this.currentIndex);

        setTimeout(() => {
            this.slider.style.transition = '';
            this.isAnimating = false;
        }, 300);
    }

    init() {
        this.createDots();
        this.updateButtons();
        this.addEventListeners();
    }

    addEventListeners() {
        this.prevBtn.addEventListener('click', () => this.prevSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());

        this.slider.addEventListener('touchstart', (e) => this.touchStart(e), { passive: false });
        this.slider.addEventListener('touchmove', (e) => this.touchMove(e), { passive: false });
        this.slider.addEventListener('touchend', () => this.touchEnd());

        this.slider.addEventListener('mousedown', (e) => this.touchStart(e));
        this.slider.addEventListener('mousemove', (e) => this.touchMove(e));
        this.slider.addEventListener('mouseup', () => this.touchEnd());
        this.slider.addEventListener('mouseleave', () => this.touchEnd());
        this.slider.addEventListener('contextmenu', (e) => e.preventDefault());
    }
}

// Initialize Partners Slider
document.addEventListener('DOMContentLoaded', () => {
    const partners = new PartnersSlider('partnersSlider', 'partnersPrevBtn', 'partnersNextBtn', 'partnersSliderDots');

    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            partners.recalculateDimensions();
        }, 250);
    });

    window.addEventListener('orientationchange', () => {
        setTimeout(() => partners.recalculateDimensions(), 500);
    });
});
