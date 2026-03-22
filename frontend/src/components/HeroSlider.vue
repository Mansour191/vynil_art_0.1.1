<template>
  <section class="hero-slider">
    <div class="slider-container">
      <!-- Slides -->
      <div
        v-for="(slide, index) in slides"
        :key="index"
        class="slide"
        :class="{ active: currentSlide === index }"
      >
        <div class="slide-bg" :style="{ backgroundImage: `url(${slide.image})` }"></div>
        <div class="overlay"></div>
        <div class="slide-content">
          <span class="slide-category">
            <i :class="slide.icon"></i>
            <span>{{ $t(slide.categoryKey) }}</span>
          </span>
          <h2 class="slide-title">{{ $t(slide.titleKey) }}</h2>
          <p class="slide-description">{{ $t(slide.descKey) }}</p>
          <div class="slide-buttons">
            <!-- استخدام router-link للمسارات الداخلية -->
            <router-link
              v-if="!isExternalLink(slide.btn1Link)"
              :to="slide.btn1Link"
              class="btn-primary"
            >
              <i :class="slide.btn1Icon"></i>
              <span>{{ $t(slide.btn1Key) }}</span>
            </router-link>
            <!-- استخدام a للروابط الخارجية -->
            <a
              v-else
              :href="slide.btn1Link"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-primary"
            >
              <i :class="slide.btn1Icon"></i>
              <span>{{ $t(slide.btn1Key) }}</span>
            </a>

            <router-link
              v-if="!isExternalLink(slide.btn2Link)"
              :to="slide.btn2Link"
              class="btn-secondary"
            >
              <i :class="slide.btn2Icon"></i>
              <span>{{ $t(slide.btn2Key) }}</span>
            </router-link>
            <a
              v-else
              :href="slide.btn2Link"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-secondary"
            >
              <i :class="slide.btn2Icon"></i>
              <span>{{ $t(slide.btn2Key) }}</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Slider Controls -->
      <button aria-label="السابق" class="slider-control prev" @click="prevSlide">
        <i class="fa-solid fa-chevron-left"></i>
      </button>
      <button aria-label="التالي" class="slider-control next" @click="nextSlide">
        <i class="fa-solid fa-chevron-right"></i>
      </button>

      <!-- Indicators -->
      <div class="slider-indicators">
        <div class="progress-container">
          <div class="progress-bar" :style="{ width: progressWidth + '%' }"></div>
        </div>
        <div class="dots-container">
          <span
            v-for="(slide, index) in slides"
            :key="index"
            class="dot"
            :class="{ active: currentSlide === index }"
            @click="goToSlide(index)"
          ></span>
        </div>
        <div class="slide-counter">
          <span class="current">{{ formatNumber(currentSlide + 1) }}</span>
          <span class="separator">/</span>
          <span class="total">{{ formatNumber(slides.length) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSlider',
  data() {
    return {
      currentSlide: 0,
      interval: null,
      slides: [
        {
          image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
          icon: 'fa-solid fa-couch',
          categoryKey: 'slide1Category',
          titleKey: 'slide1Title',
          descKey: 'slide1Desc',
          btn1Key: 'slide1Btn1',
          btn1Icon: 'fa-solid fa-search',
          btn1Link: '/gallery',
          btn2Key: 'slide1Btn2',
          btn2Icon: 'fa-solid fa-phone-alt',
          btn2Link: '/contact',
        },
        {
          image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
          icon: 'fa-solid fa-paint-roller',
          categoryKey: 'slide2Category',
          titleKey: 'slide2Title',
          descKey: 'slide2Desc',
          btn1Key: 'slide2Btn1',
          btn1Icon: 'fa-solid fa-images',
          btn1Link: '/gallery?category=walls',
          btn2Key: 'slide2Btn2',
          btn2Icon: 'fa-solid fa-info-circle',
          btn2Link: '/about',
        },
        {
          image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
          icon: 'fa-solid fa-utensils',
          categoryKey: 'slide3Category',
          titleKey: 'slide3Title',
          descKey: 'slide3Desc',
          btn1Key: 'slide3Btn1',
          btn1Icon: 'fa-solid fa-utensils',
          btn1Link: '/gallery?category=kitchens',
          btn2Key: 'slide3Btn2',
          btn2Icon: 'fab fa-whatsapp',
          btn2Link: 'https://wa.me/213663140341',
        },
        {
          image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
          icon: 'fa-solid fa-door-open',
          categoryKey: 'slide4Category',
          titleKey: 'slide4Title',
          descKey: 'slide4Desc',
          btn1Key: 'slide4Btn1',
          btn1Icon: 'fa-solid fa-door-open',
          btn1Link: '/gallery?category=doors',
          btn2Key: 'slide4Btn2',
          btn2Icon: 'fa-solid fa-envelope',
          btn2Link: '/contact',
        },
        {
          image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
          icon: 'fa-solid fa-border-all',
          categoryKey: 'slide5Category',
          titleKey: 'slide5Title',
          descKey: 'slide5Desc',
          btn1Key: 'slide5Btn1',
          btn1Icon: 'fa-solid fa-border-all',
          btn1Link: '/gallery?category=tiles',
          btn2Key: 'slide5Btn2',
          btn2Icon: 'fa-solid fa-images',
          btn2Link: '/gallery',
        },
      ],
    };
  },
  computed: {
    progressWidth() {
      return ((this.currentSlide + 1) / this.slides.length) * 100;
    },
  },
  mounted() {
    this.startAutoPlay();
    // التحقق من وجود Font Awesome
    this.checkFontAwesome();
  },
  beforeDestroy() {
    this.stopAutoPlay();
  },
  methods: {
    startAutoPlay() {
      this.interval = setInterval(() => {
        this.nextSlide();
      }, 15000);
    },
    stopAutoPlay() {
      clearInterval(this.interval);
    },
    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.slides.length;
      this.resetInterval();
    },
    prevSlide() {
      this.currentSlide = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
      this.resetInterval();
    },
    goToSlide(index) {
      this.currentSlide = index;
      this.resetInterval();
    },
    resetInterval() {
      this.stopAutoPlay();
      this.startAutoPlay();
    },
    formatNumber(num) {
      return num < 10 ? `0${num}` : `${num}`;
    },
    isExternalLink(link) {
      return link.startsWith('http') || link.startsWith('https') || link.startsWith('www');
    },
    checkFontAwesome() {
      // التحقق من تحميل Font Awesome
      if (typeof window !== 'undefined') {
        const hasFontAwesome =
          document.querySelector('link[href*="font-awesome"]') ||
          document.querySelector('link[href*="fontawesome"]');
        if (!hasFontAwesome) {
          console.warn('Font Awesome may not be loaded. Please check your index.html');
        }
      }
    },
  },
};
</script>

<style scoped>
.hero-slider {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
  margin: 10px 0;
  box-shadow: var(--shadow-soft);
}

.slider-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.8s ease, visibility 0.8s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 5;
}

.slide-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: transform 15s ease;
}

.slide.active .slide-bg {
  transform: scale(1.1);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2;
}

.slide-content {
  position: relative;
  z-index: 10;
  max-width: 100%;
  padding: 20px;
  text-align: center;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  animation: slideContentIn 1s ease forwards;
  transform: translateY(30px);
  opacity: 0;
}

.slide.active .slide-content {
  animation: slideContentIn 0.8s 0.3s ease forwards;
}

@keyframes slideContentIn {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-category {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 15px;
  background: var(--gold-gradient);
  color: #000000;
  border-radius: 25px;
  font-size: 0.85rem;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: var(--shadow-gold);
}

.slide-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #fff 0%, #ffd700 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.slide-description {
  font-size: 0.95rem;
  margin-bottom: 20px;
  color: white;
  line-height: 1.6;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}

.slide-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 30px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(212, 175, 55, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(212, 175, 55, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: var(--gold-primary);
  color: var(--bg-deep);
  transform: translateY(-3px);
}

.slider-control {
  display: none;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 45px;
  height: 45px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 50%;
  color: white;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 20;
  transition: all 0.3s;
  font-size: 1.1rem;
}

.slider-control:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.slider-control.prev {
  left: 20px;
}

.slider-control.next {
  right: 20px;
}

.slider-indicators {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  padding: 8px 15px;
  border-radius: 30px;
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.progress-container {
  width: 60px;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--gold-gradient);
  transition: width 0.3s linear;
}

.dots-container {
  display: flex;
  gap: 5px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.dot.active {
  background: var(--gold-gradient);
  transform: scale(1.3);
  width: 16px;
  border-radius: 8px;
}

.slide-counter {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 600;
}

.slide-counter .current {
  color: var(--gold-primary);
}

/* RTL Support */
[dir='rtl'] .slider-control.prev {
  left: auto;
  right: 20px;
}

[dir='rtl'] .slider-control.next {
  right: auto;
  left: 20px;
}

[dir='rtl'] .slider-control.prev i {
  transform: rotate(180deg);
}

[dir='rtl'] .slider-control.next i {
  transform: rotate(180deg);
}

/* Media Queries */
@media (min-width: 480px) {
  .slide-buttons {
    flex-direction: row;
    justify-content: center;
  }

  .btn-primary,
  .btn-secondary {
    min-width: 160px;
  }
}

@media (min-width: 768px) {
  .hero-slider {
    height: 500px;
    margin: 20px 0;
    border-radius: 20px;
  }

  .slide-content {
    max-width: 600px;
    padding: 30px;
  }

  .slide-title {
    font-size: 2rem;
  }

  .slide-description {
    font-size: 1rem;
  }

  .slider-control {
    display: flex;
  }

  .slider-indicators {
    bottom: 20px;
    padding: 8px 20px;
    gap: 15px;
  }

  .progress-container {
    width: 80px;
  }

  .dots-container {
    gap: 8px;
  }

  .dot {
    width: 10px;
    height: 10px;
  }

  .dot.active {
    width: 18px;
  }

  .slide-counter {
    font-size: 0.85rem;
  }
}

@media (min-width: 1024px) {
  .hero-slider {
    height: 600px;
  }

  .slide-content {
    max-width: 700px;
  }

  .slide-title {
    font-size: 2.5rem;
  }

  .slide-description {
    font-size: 1.1rem;
  }

  .slider-control {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }

  .slider-control.prev {
    left: 30px;
  }

  .slider-control.next {
    right: 30px;
  }

  [dir='rtl'] .slider-control.prev {
    left: auto;
    right: 30px;
  }

  [dir='rtl'] .slider-control.next {
    right: auto;
    left: 30px;
  }
}

@media (min-width: 1400px) {
  .hero-slider {
    height: 700px;
  }

  .slide-title {
    font-size: 3rem;
  }
}

@media (max-width: 480px) {
  .slide-title {
    font-size: 1.3rem;
  }

  .slide-description {
    font-size: 0.9rem;
  }
}
</style>
