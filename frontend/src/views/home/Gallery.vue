<template>
  <div class="gallery-page">
    <!-- Hero Section -->
    <section class="gallery-hero">
      <div class="container">
        <h1 class="page-title">{{ $t('gallery') }}</h1>
        <div class="title-decoration">
          <span class="gold-bar"></span>
          <i class="fa-solid fa-images"></i>
          <span class="gold-bar"></span>
        </div>
        <!-- مقدمة الصفحة -->
        <p class="gallery-intro">{{ $t('galleryIntro') }}</p>
      </div>
    </section>

    <!-- Filter Tabs -->
    <section class="filter-section">
      <div class="container">
        <div class="filter-tabs">
          <button
            v-for="(category, index) in categories"
            :key="index"
            :class="['filter-btn', { active: activeCategory === category.value }]"
            @click="activeCategory = category.value"
          >
            <i :class="category.icon"></i>
            <span>{{ $t(category.nameKey) }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Gallery Grid -->
    <section class="gallery-grid-section">
      <div class="container">
        <transition-group name="fade" tag="div" class="gallery-grid">
          <div
            v-for="item in filteredItems"
            :key="item.id"
            class="gallery-item"
            @click="openLightbox(item)"
          >
            <div class="item-image">
              <img :src="item.image" :alt="$t(item.titleKey)" />
              <div class="item-overlay">
                <i class="fa-solid fa-search-plus"></i>
                <h3>{{ $t(item.titleKey) }}</h3>
                <span class="item-category">{{ $t(item.categoryKey) }}</span>
              </div>
            </div>
          </div>
        </transition-group>

        <!-- Load More Button -->
        <div v-if="hasMore" class="load-more">
          <button class="load-more-btn" @click="loadMore">
            <i class="fa-solid fa-plus"></i>
            {{ $t('loadMore') }}
          </button>
        </div>
      </div>
    </section>

    <!-- Lightbox -->
    <div v-if="lightbox.show" class="lightbox" @click.self="closeLightbox">
      <div class="lightbox-content">
        <button class="lightbox-close" @click="closeLightbox">
          <i class="fa-solid fa-times"></i>
        </button>
        <button class="lightbox-prev" @click="prevImage" :disabled="!hasPrev">
          <i class="fa-solid fa-chevron-left"></i>
        </button>
        <img :src="lightbox.image" :alt="$t(lightbox.titleKey)" />
        <button class="lightbox-next" @click="nextImage" :disabled="!hasNext">
          <i class="fa-solid fa-chevron-right"></i>
        </button>
        <div class="lightbox-info">
          <h3>{{ $t(lightbox.titleKey) }}</h3>
          <p>{{ $t(lightbox.descKey) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue';

// State
const activeCategory = ref('all');
const itemsPerPage = ref(12);
const currentPage = ref(1);

const categories = [
  { value: 'all', nameKey: 'allCategories', icon: 'fa-solid fa-th-large' },
  { value: 'furniture', nameKey: 'furniture', icon: 'fa-solid fa-couch' },
  { value: 'doors', nameKey: 'doors', icon: 'fa-solid fa-door-open' },
  { value: 'walls', nameKey: 'walls', icon: 'fa-solid fa-paint-roller' },
  { value: 'ceilings', nameKey: 'ceilings', icon: 'fa-solid fa-arrow-up' },
  { value: 'tiles', nameKey: 'tiles', icon: 'fa-solid fa-border-all' },
  { value: 'kitchens', nameKey: 'kitchens', icon: 'fa-solid fa-utensils' },
  { value: 'cars', nameKey: 'cars', icon: 'fa-solid fa-car' },
];

const allItems = ref([
  {
    id: 1,
    titleKey: 'galleryItem1Title',
    descKey: 'galleryItem1Desc',
    category: 'furniture',
    categoryKey: 'furniture',
    image: 'https://i.postimg.cc/Qx9tkDDn/wardrobe.png',
  },
  {
    id: 2,
    titleKey: 'galleryItem2Title',
    descKey: 'galleryItem2Desc',
    category: 'furniture',
    categoryKey: 'furniture',
    image: 'https://i.postimg.cc/htCcH3cZ/table1.png',
  },
  {
    id: 3,
    titleKey: 'galleryItem3Title',
    descKey: 'galleryItem3Desc',
    category: 'doors',
    categoryKey: 'doors',
    image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
  },
  {
    id: 4,
    titleKey: 'galleryItem4Title',
    descKey: 'galleryItem4Desc',
    category: 'walls',
    categoryKey: 'walls',
    image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
  },
  {
    id: 5,
    titleKey: 'galleryItem5Title',
    descKey: 'galleryItem5Desc',
    category: 'kitchens',
    categoryKey: 'kitchens',
    image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
  },
  {
    id: 6,
    titleKey: 'galleryItem6Title',
    descKey: 'galleryItem6Desc',
    category: 'cars',
    categoryKey: 'cars',
    image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
  },
  {
    id: 7,
    titleKey: 'galleryItem7Title',
    descKey: 'galleryItem7Desc',
    category: 'ceilings',
    categoryKey: 'ceilings',
    image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
  },
  {
    id: 8,
    titleKey: 'galleryItem8Title',
    descKey: 'galleryItem8Desc',
    category: 'tiles',
    categoryKey: 'tiles',
    image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
  },
]);

const lightbox = reactive({
  show: false,
  image: '',
  titleKey: '',
  descKey: '',
  index: -1,
});

// Computed
const filteredItems = computed(() => {
  let items =
    activeCategory.value === 'all'
      ? allItems.value
      : allItems.value.filter((item) => item.category === activeCategory.value);

  return items.slice(0, currentPage.value * itemsPerPage.value);
});

const hasMore = computed(() => {
  let totalItems =
    activeCategory.value === 'all'
      ? allItems.value.length
      : allItems.value.filter((item) => item.category === activeCategory.value).length;

  return filteredItems.value.length < totalItems;
});

const hasPrev = computed(() => lightbox.index > 0);

const hasNext = computed(() => {
  let items =
    activeCategory.value === 'all'
      ? allItems.value
      : allItems.value.filter((item) => item.category === activeCategory.value);
  return lightbox.index < items.length - 1;
});

// Methods
const loadMore = () => {
  currentPage.value++;
};

const openLightbox = (item) => {
  const items =
    activeCategory.value === 'all'
      ? allItems.value
      : allItems.value.filter((i) => i.category === activeCategory.value);

  lightbox.show = true;
  lightbox.image = item.image;
  lightbox.titleKey = item.titleKey;
  lightbox.descKey = item.descKey;
  lightbox.index = items.findIndex((i) => i.id === item.id);

  document.body.style.overflow = 'hidden';
};

const closeLightbox = () => {
  lightbox.show = false;
  document.body.style.overflow = '';
};

const prevImage = () => {
  if (!hasPrev.value) return;

  const items =
    activeCategory.value === 'all'
      ? allItems.value
      : allItems.value.filter((item) => item.category === activeCategory.value);

  const newIndex = lightbox.index - 1;
  lightbox.image = items[newIndex].image;
  lightbox.titleKey = items[newIndex].titleKey;
  lightbox.descKey = items[newIndex].descKey;
  lightbox.index = newIndex;
};

const nextImage = () => {
  if (!hasNext.value) return;

  const items =
    activeCategory.value === 'all'
      ? allItems.value
      : allItems.value.filter((item) => item.category === activeCategory.value);

  const newIndex = lightbox.index + 1;
  lightbox.image = items[newIndex].image;
  lightbox.titleKey = items[newIndex].titleKey;
  lightbox.descKey = items[newIndex].descKey;
  lightbox.index = newIndex;
};

// Watchers
watch(activeCategory, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.gallery-page {
  background: var(--bg-deep);
  min-height: 100vh;
}

/* Hero Section */
.gallery-hero {
  background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-deep) 100%);
  padding: 60px 0 40px;
  position: relative;
  overflow: hidden;
  text-align: center;
  border-bottom: 1px solid var(--border-subtle);
}

.gallery-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 30%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 70%, rgba(212, 175, 55, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.page-title {
  font-size: 2.5rem;
  color: var(--gold-primary);
  margin-bottom: 15px;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.gallery-intro {
  max-width: 700px;
  margin: 20px auto 0;
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.8;
}

.title-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.gold-bar {
  width: 60px;
  height: 2px;
  background: var(--gold-gradient);
}

.title-decoration i {
  color: var(--gold-primary);
  font-size: 1.2rem;
  animation: pulse 2s infinite;
}

/* Filter Section */
.filter-section {
  padding: 40px 0;
  background: var(--bg-dark);
  border-bottom: 1px solid var(--border-subtle);
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 30px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.filter-btn i {
  color: var(--gold-primary);
  transition: all 0.3s;
}

.filter-btn:hover {
  border-color: var(--gold-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.filter-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.filter-btn.active i {
  color: var(--bg-deep);
}

/* Gallery Grid */
.gallery-grid-section {
  padding: 60px 0;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.gallery-item {
  cursor: pointer;
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  transition: all 0.3s;
}

.gallery-item:hover {
  transform: translateY(-10px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.item-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.gallery-item:hover .item-image img {
  transform: scale(1.1);
}

.item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.3));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  text-align: center;
  padding: 20px;
}

.gallery-item:hover .item-overlay {
  opacity: 1;
}

.item-overlay i {
  font-size: 2rem;
  color: var(--gold-primary);
  margin-bottom: 10px;
  transform: scale(0);
  transition: transform 0.3s 0.1s;
}

.gallery-item:hover .item-overlay i {
  transform: scale(1);
}

.item-overlay h3 {
  font-size: 1.1rem;
  margin-bottom: 5px;
  transform: translateY(20px);
  transition: transform 0.3s 0.2s;
}

.gallery-item:hover .item-overlay h3 {
  transform: translateY(0);
}

.item-category {
  font-size: 0.9rem;
  color: var(--gold-primary);
  transform: translateY(20px);
  transition: transform 0.3s 0.3s;
}

.gallery-item:hover .item-overlay .item-category {
  transform: translateY(0);
}

/* Load More Button */
.load-more {
  text-align: center;
}

.load-more-btn {
  padding: 15px 40px;
  background: transparent;
  border: 2px solid var(--gold-primary);
  border-radius: 30px;
  color: var(--gold-primary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s;
}

.load-more-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold);
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 10px;
  border: 2px solid var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  color: var(--gold-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.lightbox-close:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: rotate(90deg);
}

.lightbox-prev,
.lightbox-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  color: var(--gold-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.lightbox-prev:hover:not(:disabled),
.lightbox-next:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.lightbox-prev:disabled,
.lightbox-next:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.lightbox-prev {
  left: -60px;
}

.lightbox-next {
  right: -60px;
}

.lightbox-info {
  position: absolute;
  bottom: -80px;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
}

.lightbox-info h3 {
  color: var(--gold-primary);
  font-size: 1.3rem;
  margin-bottom: 5px;
}

.lightbox-info p {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Fade Animation */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Animations */
@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

/* Responsive */
@media (max-width: 1200px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .gallery-intro {
    font-size: 1rem;
    padding: 0 15px;
  }

  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .filter-tabs {
    gap: 8px;
  }

  .filter-btn {
    padding: 8px 15px;
    font-size: 0.85rem;
  }

  .lightbox-prev,
  .lightbox-next {
    width: 40px;
    height: 40px;
  }

  .lightbox-prev {
    left: -20px;
  }

  .lightbox-next {
    right: -20px;
  }

  .lightbox-info {
    bottom: -60px;
  }

  .lightbox-info h3 {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }

  .filter-tabs {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-btn {
    justify-content: center;
  }
}
</style>
