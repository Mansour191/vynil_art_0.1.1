<template>
  <div class="wishlist-page">
    <div class="container">
      <h1 class="page-title">
        <i class="fa-solid fa-heart"></i>
        {{ $t('myWishlist') }}
        <span class="badge" v-if="wishlistCount > 0">{{ wishlistCount }}</span>
      </h1>

      <!-- حالة المفضلة فارغة -->
      <div v-if="wishlistCount === 0" class="empty-wishlist">
        <div class="empty-icon">
          <i class="fa-solid fa-heart-broken"></i>
          <div class="icon-ring"></div>
        </div>
        <h2>{{ $t('wishlistEmpty') }}</h2>
        <p>{{ $t('wishlistEmptyMessage') }}</p>

        <div class="empty-suggestions">
          <h3>{{ $t('explore') }}</h3>
          <div class="suggestion-cards">
            <router-link to="/gallery" class="suggestion-card">
              <div class="suggestion-icon">
                <i class="fa-solid fa-images"></i>
              </div>
              <span>{{ $t('gallery') }}</span>
            </router-link>

            <router-link to="/furniture" class="suggestion-card">
              <div class="suggestion-icon">
                <i class="fa-solid fa-couch"></i>
              </div>
              <span>{{ $t('furniture') }}</span>
            </router-link>

            <router-link to="/walls" class="suggestion-card">
              <div class="suggestion-icon">
                <i class="fa-solid fa-paint-roller"></i>
              </div>
              <span>{{ $t('walls') }}</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- عرض عناصر المفضلة -->
      <div v-else class="wishlist-grid">
        <div v-for="item in wishlistItems" :key="item.id" class="wishlist-card">
          <div class="card-image">
            <router-link :to="item.link">
              <img :src="item.image" :alt="item.title" loading="lazy" />
              <span class="image-overlay">
                <i class="fa-solid fa-eye"></i>
              </span>
            </router-link>
            <button
              class="remove-btn"
              @click="removeFromWishlist(item.id)"
              :title="$t('removeFromWishlist')"
            >
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <div class="card-info">
            <h3 class="card-title">
              <router-link :to="item.link">{{ item.title }}</router-link>
            </h3>

            <div class="card-meta">
              <span class="card-category">
                <i class="fa-solid fa-tag"></i>
                {{ item.category }}
              </span>
            </div>

            <div class="card-actions">
              <router-link :to="item.link" class="btn-view">
                <i class="fa-solid fa-eye"></i>
                {{ $t('viewDetails') }}
              </router-link>

              <a
                :href="`https://wa.me/213663140341?text=${encodeURIComponent(
                  $t('whatsappInquiry') + ': ' + item.title
                )}`"
                target="_blank"
                class="btn-whatsapp"
              >
                <i class="fab fa-whatsapp"></i>
                {{ $t('inquiry') }}
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- زر مسح الكل -->
      <div v-if="wishlistCount > 0" class="wishlist-footer">
        <button class="clear-btn" @click="clearAll">
          <i class="fa-solid fa-trash-alt"></i>
          {{ $t('clearWishlist') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';

const store = useStore();
const { t } = useI18n();

// Computed
const wishlistItems = computed(() => store.getters['wishlist/wishlistItems']);
const wishlistCount = computed(() => store.getters['wishlist/wishlistCount']);

// Methods
const removeFromWishlist = (id) => {
  store.dispatch('wishlist/toggleWishlist', { id });
};

const clearWishlist = () => {
  store.dispatch('wishlist/clearWishlist');
};

const clearAll = () => {
  if (confirm(t('confirmClearWishlist'))) {
    clearWishlist();
  }
};

// Lifecycle
onMounted(() => {
  console.log('✅ صفحة المفضلة:', wishlistItems.value);
});
</script>

<style scoped>
.wishlist-page {
  min-height: 70vh;
  padding: 40px 0;
  background: var(--bg-deep);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  color: var(--gold-primary);
  font-size: 2.5rem;
  margin-bottom: 40px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.badge {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  padding: 5px 15px;
  border-radius: 30px;
  font-size: 1rem;
}

/* ===== تصميم المفضلة الفارغة ===== */
.empty-wishlist {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border-radius: 30px;
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft);
}

.empty-icon {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon i {
  font-size: 4rem;
  color: var(--gold-primary);
  opacity: 0.5;
  z-index: 2;
  animation: float 3s ease-in-out infinite;
}

.icon-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid var(--gold-primary);
  border-radius: 50%;
  opacity: 0.2;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.1;
  }
  100% {
    transform: scale(1);
    opacity: 0.2;
  }
}

.empty-wishlist h2 {
  color: var(--gold-primary);
  font-size: 2rem;
  margin-bottom: 15px;
}

.empty-wishlist p {
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.empty-suggestions {
  margin-top: 40px;
}

.empty-suggestions h3 {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 20px;
  font-weight: 500;
}

.suggestion-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.suggestion-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s;
  width: 120px;
}

.suggestion-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.suggestion-icon {
  width: 50px;
  height: 50px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-primary);
  font-size: 1.5rem;
  transition: all 0.3s;
}

.suggestion-card:hover .suggestion-icon {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: scale(1.1);
}

.suggestion-card span {
  font-size: 0.9rem;
  font-weight: 500;
}

/* ===== شبكة المفضلة ===== */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
}

@media (max-width: 992px) {
  .wishlist-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .wishlist-grid {
    grid-template-columns: 1fr;
  }
}

.wishlist-card {
  background: var(--bg-card);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  transition: all 0.3s;
  position: relative;
}

.wishlist-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.card-image {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.wishlist-card:hover .card-image img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.wishlist-card:hover .image-overlay {
  opacity: 1;
}

.image-overlay i {
  color: white;
  font-size: 2rem;
  background: rgba(212, 175, 55, 0.8);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: scale(0);
  transition: transform 0.3s;
}

.wishlist-card:hover .image-overlay i {
  transform: scale(1);
}

.remove-btn {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 35px;
  height: 35px;
  background: rgba(244, 67, 54, 0.9);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  opacity: 0;
  z-index: 10;
}

.wishlist-card:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #f44336;
  transform: scale(1.1);
}

.card-info {
  padding: 20px;
}

.card-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.card-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.3s;
}

.card-title a:hover {
  color: var(--gold-primary);
}

.card-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  color: var(--text-muted);
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.card-meta i {
  color: var(--gold-primary);
  margin-left: 5px;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.btn-view,
.btn-whatsapp {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  text-decoration: none;
  text-align: center;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s;
}

.btn-view {
  background: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
}

.btn-view:hover {
  border-color: var(--gold-primary);
  background: var(--bg-deep);
}

.btn-view i {
  color: var(--gold-primary);
}

.btn-whatsapp {
  background: #25d366;
  color: white;
}

.btn-whatsapp:hover {
  background: #128c7e;
  transform: scale(1.02);
}

/* تذييل الصفحة */
.wishlist-footer {
  margin-top: 40px;
  text-align: center;
}

.clear-btn {
  padding: 12px 30px;
  background: transparent;
  border: 1px solid #f44336;
  color: #f44336;
  border-radius: 30px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.clear-btn:hover {
  background: #f44336;
  color: white;
}

@media (max-width: 768px) {
  .suggestion-cards {
    flex-direction: column;
    align-items: center;
  }

  .suggestion-card {
    width: 100%;
    flex-direction: row;
    justify-content: flex-start;
  }
}
</style>
