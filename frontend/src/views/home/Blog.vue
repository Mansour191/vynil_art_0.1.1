<template>
  <div class="blog-page">
    <!-- Hero Section -->
    <section class="blog-hero">
      <div class="container">
        <h1 class="page-title">{{ $t('blogTitle') }}</h1>
        <div class="title-decoration">
          <span class="gold-bar"></span>
          <i class="fa-solid fa-blog"></i>
          <span class="gold-bar"></span>
        </div>
        <p class="hero-text">{{ $t('blogDescription') }}</p>
      </div>
    </section>

    <!-- Search Bar -->
    <section class="search-section">
      <div class="container">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            :placeholder="$t('searchArticles')"
            @keyup.enter="performSearch"
          />
          <button @click="performSearch">
            <i class="fa-solid fa-search"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="categories-section">
      <div class="container">
        <div class="categories-tabs">
          <button
            v-for="category in categories"
            :key="category.value"
            :class="['category-btn', { active: activeCategory === category.value }]"
            @click="filterByCategory(category.value)"
          >
            <i :class="category.icon"></i>
            <span>{{ $t(category.nameKey) }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Blog Grid -->
    <section class="blog-grid-section">
      <div class="container">
        <LoadingSpinner v-if="loading" :message="$t('loadingArticles')" />

        <div v-else-if="filteredPosts.length === 0" class="no-results">
          <i class="fa-solid fa-search"></i>
          <h3>{{ $t('noArticlesFound') }}</h3>
          <p>{{ $t('tryDifferentSearch') }}</p>
        </div>

        <div v-else class="blog-grid">
          <article v-for="post in paginatedPosts" :key="post.id" class="blog-card">
            <div class="blog-image">
              <router-link :to="`/post/${post.id}`">
                <img :src="post.image" :alt="post.title" loading="lazy" />
              </router-link>
              <span class="blog-category">{{ post.category }}</span>
            </div>

            <div class="blog-content">
              <div class="blog-meta">
                <span class="blog-date">
                  <i class="far fa-calendar-alt"></i>
                  {{ post.date }}
                </span>
                <span class="blog-author">
                  <i class="far fa-user"></i>
                  {{ post.author }}
                </span>
              </div>

              <h3 class="blog-title">
                <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
              </h3>

              <p class="blog-excerpt">{{ post.excerpt }}</p>

              <div class="blog-footer">
                <router-link :to="`/post/${post.id}`" class="read-more">
                  {{ $t('readMore') }} <i class="fa-solid fa-arrow-left"></i>
                </router-link>

                <div class="blog-stats">
                  <span><i class="far fa-eye"></i> {{ post.views }}</span>
                  <span><i class="far fa-comment"></i> {{ post.comments }}</span>
                </div>
              </div>
            </div>
          </article>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
            class="page-btn"
          >
            <i class="fa-solid fa-chevron-right"></i>
          </button>

          <span class="page-info">
            {{ $t('page') }} {{ currentPage }} {{ $t('of') }} {{ totalPages }}
          </span>

          <button
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
            class="page-btn"
          >
            <i class="fa-solid fa-chevron-left"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

const route = useRoute();

// State
const loading = ref(false);
const searchQuery = ref('');
const activeCategory = ref('all');
const currentPage = ref(1);
const postsPerPage = ref(9);

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

const allPosts = ref([
  {
    id: 1,
    title: 'كيف تختار الفينيل المناسب لمشروعك؟',
    excerpt:
      'إذا كنت جديداً في عالم الفينيل اللاصق، هذا الدليل الشامل سيساعدك على فهم كل ما تحتاج معرفته...',
    image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
    category: 'دليل المبتدئين',
    categoryValue: 'walls',
    date: '15 مارس 2026',
    author: 'أحمد منصور',
    views: 1234,
    comments: 23,
  },
  {
    id: 2,
    title: '10 أفكار عبقرية لتجديد غرفة نوم أطفالك بالفينيل',
    excerpt: 'حوّل غرفة أطفالك إلى عالم سحري من الخيال والإبداع باستخدام الفينيل اللاصق...',
    image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
    category: 'أفكار ديكور',
    categoryValue: 'walls',
    date: '12 مارس 2026',
    author: 'سارة أحمد',
    views: 856,
    comments: 15,
  },
  {
    id: 3,
    title: '5 أخطاء شائعة يقع فيها المبتدئون عند تركيب الفينيل',
    excerpt:
      'تعرّف على أكثر 5 أخطاء شائعة وكيف تتجنبها لتحصل على نتيجة احترافية من أول مرة...',
    image: 'https://i.postimg.cc/htCcH3cZ/table1.png',
    category: 'نصائح ودليل',
    categoryValue: 'walls',
    date: '10 مارس 2026',
    author: 'محمد علي',
    views: 2100,
    comments: 42,
  },
  {
    id: 4,
    title: 'تحويل خزانة قديمة إلى تحفة فنية',
    excerpt:
      'هذه الخزانة كانت مهملة منذ سنوات، بألوانها الباهتة وتصميمها القديم. النتيجة كانت مذهلة!',
    image: 'https://i.postimg.cc/Qx9tkDDn/wardrobe.png',
    category: 'مشاريع ناجحة',
    categoryValue: 'furniture',
    date: '8 مارس 2026',
    author: 'نورا حسن',
    views: 3456,
    comments: 67,
  },
  {
    id: 5,
    title: 'أحدث صيحات ديكور الجدران بالفينيل',
    excerpt: 'تعرف على أحدث التصاميم والأفكار لتزيين جدران منزلك باستخدام الفينيل الملون...',
    image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
    category: 'ديكور',
    categoryValue: 'walls',
    date: '5 مارس 2026',
    author: 'أحمد منصور',
    views: 789,
    comments: 12,
  },
  {
    id: 6,
    title: 'كيف تعتني بالفينيل بعد التركيب',
    excerpt: 'دليل شامل للعناية بالفينيل اللاصق ليبقى كالجديد لسنوات طويلة...',
    image: 'https://i.postimg.cc/htCcH3cZ/table1.png',
    category: 'نصائح',
    categoryValue: 'walls',
    date: '3 مارس 2026',
    author: 'سارة أحمد',
    views: 654,
    comments: 9,
  },
  {
    id: 7,
    title: 'أفكار مبتكرة للمطابخ بالفينيل',
    excerpt: 'حوّل مطبخك بتكلفة بسيطة مع هذه الأفكار الإبداعية لتصاميم الفينيل...',
    image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
    category: 'مطابخ',
    categoryValue: 'kitchens',
    date: '1 مارس 2026',
    author: 'محمد علي',
    views: 987,
    comments: 18,
  },
  {
    id: 8,
    title: 'فينيل السيارات: دليل شامل',
    excerpt: 'كل ما تريد معرفته عن ملصقات الفينيل للسيارات وكيفية تطبيقها...',
    image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
    category: 'سيارات',
    categoryValue: 'cars',
    date: '28 فبراير 2026',
    author: 'نورا حسن',
    views: 1567,
    comments: 31,
  },
  {
    id: 9,
    title: 'تصاميم أبواب مودرن',
    excerpt: 'أفكار مبتكرة لتصاميم الأبواب باستخدام الفينيل اللاصق...',
    image: 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
    category: 'أبواب',
    categoryValue: 'doors',
    date: '25 فبراير 2026',
    author: 'أحمد منصور',
    views: 876,
    comments: 14,
  },
  {
    id: 10,
    title: 'تصاميم أسقف فاخرة',
    excerpt: 'أفكار راقية لتصميم الأسقف باستخدام الفينيل...',
    image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
    category: 'أسقف',
    categoryValue: 'ceilings',
    date: '20 فبراير 2026',
    author: 'سارة أحمد',
    views: 543,
    comments: 7,
  },
  {
    id: 11,
    title: 'بلاط بتصاميم هندسية',
    excerpt: 'أفكار حديثة لتصاميم البلاط باستخدام الفينيل...',
    image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
    category: 'بلاط',
    categoryValue: 'tiles',
    date: '18 فبراير 2026',
    author: 'محمد علي',
    views: 432,
    comments: 5,
  },
  {
    id: 12,
    title: 'أثاث كلاسيكي بالفينيل',
    excerpt: 'تحويل الأثاث الكلاسيكي بتصاميم فينيل عصرية...',
    image: 'https://i.postimg.cc/Qx9tkDDn/wardrobe.png',
    category: 'أثاث',
    categoryValue: 'furniture',
    date: '15 فبراير 2026',
    author: 'نورا حسن',
    views: 1098,
    comments: 22,
  },
]);

// Computed
const filteredPosts = computed(() => {
  let posts = allPosts.value;

  // فلترة حسب التصنيف
  if (activeCategory.value !== 'all') {
    posts = posts.filter((post) => post.categoryValue === activeCategory.value);
  }

  // فلترة حسب البحث
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    posts = posts.filter(
      (post) =>
        post.title.toLowerCase().includes(query) ||
        post.excerpt.toLowerCase().includes(query) ||
        post.category.toLowerCase().includes(query)
    );
  }

  return posts;
});

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage.value;
  const end = start + postsPerPage.value;
  return filteredPosts.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / postsPerPage.value));

// Methods
const filterByCategory = (category) => {
  activeCategory.value = category;
  currentPage.value = 1;
};

const performSearch = () => {
  currentPage.value = 1;
};

const changePage = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Watchers
watch(() => route.query.q, (query) => {
  if (query) {
    searchQuery.value = query;
    performSearch();
  }
}, { immediate: true });
</script>

<style scoped>
.blog-page {
  background: var(--bg-deep);
  min-height: 100vh;
}

/* Hero Section */
.blog-hero {
  background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-deep) 100%);
  padding: 60px 0 40px;
  position: relative;
  overflow: hidden;
  text-align: center;
  border-bottom: 1px solid var(--border-subtle);
}

.blog-hero::before {
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

.hero-text {
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

/* Search Section */
.search-section {
  padding: 30px 0;
  background: var(--bg-dark);
}

.search-box {
  display: flex;
  gap: 10px;
  max-width: 600px;
  margin: 0 auto;
}

.search-box input {
  flex: 1;
  padding: 15px 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s;
}

.search-box input:focus {
  border-color: var(--gold-primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

.search-box button {
  width: 55px;
  height: 55px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 12px;
  color: var(--bg-deep);
  cursor: pointer;
  transition: all 0.3s;
}

.search-box button:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-gold);
}

/* Categories Section */
.categories-section {
  padding: 20px 0;
  background: var(--bg-dark);
  border-bottom: 1px solid var(--border-subtle);
}

.categories-tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 30px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.category-btn i {
  color: var(--gold-primary);
}

.category-btn:hover {
  border-color: var(--gold-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.category-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.category-btn.active i {
  color: var(--bg-deep);
}

/* Blog Grid */
.blog-grid-section {
  padding: 60px 0;
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

@media (max-width: 1024px) {
  .blog-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .blog-grid {
    grid-template-columns: 1fr;
  }
}

.blog-card {
  background: var(--bg-card);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  transition: all 0.3s;
}

.blog-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.blog-image {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.blog-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.blog-card:hover .blog-image img {
  transform: scale(1.1);
}

.blog-category {
  position: absolute;
  top: 15px;
  right: 15px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 2;
}

.blog-content {
  padding: 20px;
}

.blog-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.blog-meta i {
  color: var(--gold-primary);
  margin-left: 5px;
}

.blog-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  line-height: 1.4;
}

.blog-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.3s;
}

.blog-title a:hover {
  color: var(--gold-primary);
}

.blog-excerpt {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 15px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-subtle);
  padding-top: 15px;
}

.read-more {
  color: var(--gold-primary);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s;
}

.read-more:hover {
  gap: 12px;
}

.blog-stats {
  display: flex;
  gap: 15px;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.blog-stats i {
  color: var(--gold-primary);
  margin-left: 3px;
}

/* No Results */
.no-results {
  text-align: center;
  padding: 60px 20px;
}

.no-results i {
  font-size: 4rem;
  color: var(--gold-primary);
  margin-bottom: 20px;
  opacity: 0.5;
}

.no-results h3 {
  color: var(--text-primary);
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.no-results p {
  color: var(--text-muted);
  font-size: 1.1rem;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.page-btn {
  width: 45px;
  height: 45px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 50%;
  color: var(--gold-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: scale(1.1);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}
</style>
