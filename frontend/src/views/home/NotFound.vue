<template>
  <div class="not-found-page">
    <div class="container">
      <div class="error-content">
        <div class="error-icon">
          <i class="fa-solid fa-exclamation-triangle"></i>
        </div>

        <h1 class="error-code">404</h1>
        <h2 class="error-title">{{ $t('pageNotFound') }}</h2>
        <p class="error-message">{{ $t('pageNotFoundMessage') }}</p>

        <div class="error-suggestions">
          <h3>{{ $t('youCanTry') }}</h3>
          <ul>
            <li>
              <router-link to="/">
                <i class="fa-solid fa-home"></i>
                {{ $t('backToHome') }}
              </router-link>
            </li>
            <li>
              <router-link to="/gallery">
                <i class="fa-solid fa-images"></i>
                {{ $t('browseGallery') }}
              </router-link>
            </li>
            <li>
              <router-link to="/blog">
                <i class="fa-solid fa-blog"></i>
                {{ $t('readBlog') }}
              </router-link>
            </li>
            <li>
              <router-link to="/contact">
                <i class="fa-solid fa-phone-alt"></i>
                {{ $t('contactSupport') }}
              </router-link>
            </li>
          </ul>
        </div>

        <div class="search-box">
          <h3>{{ $t('searchInSite') }}</h3>
          <div class="search-input-group">
            <input
              type="text"
              v-model="searchQuery"
              :placeholder="$t('searchPlaceholder')"
              @keyup.enter="performSearch"
            />
            <button @click="performSearch">
              <i class="fa-solid fa-search"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView',
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    performSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push(`/search?q=${encodeURIComponent(this.searchQuery)}`);
      }
    },
  },
};
</script>

<style scoped>
.not-found-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: var(--bg-deep);
}

.container {
  max-width: 800px;
  width: 100%;
}

.error-content {
  background: var(--bg-card);
  border-radius: 30px;
  padding: 50px;
  text-align: center;
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft);
}

.error-icon {
  font-size: 5rem;
  color: var(--gold-primary);
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

.error-code {
  font-size: 6rem;
  font-weight: 800;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 10px;
}

.error-title {
  color: var(--gold-primary);
  font-size: 2rem;
  margin-bottom: 15px;
}

.error-message {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.error-suggestions {
  background: var(--bg-surface);
  border-radius: 20px;
  padding: 25px;
  margin: 30px 0;
  text-align: right;
}

.error-suggestions h3 {
  color: var(--gold-primary);
  font-size: 1.2rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-suggestions ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

@media (max-width: 480px) {
  .error-suggestions ul {
    grid-template-columns: 1fr;
  }
}

.error-suggestions li a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 15px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s;
}

.error-suggestions li a:hover {
  border-color: var(--gold-primary);
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-primary);
  transform: translateY(-3px);
}

.error-suggestions li a i {
  color: var(--gold-primary);
  font-size: 1.1rem;
}

.search-box {
  margin-top: 30px;
}

.search-box h3 {
  color: var(--gold-primary);
  font-size: 1.2rem;
  margin-bottom: 15px;
}

.search-input-group {
  display: flex;
  gap: 10px;
}

.search-input-group input {
  flex: 1;
  padding: 15px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s;
}

.search-input-group input:focus {
  border-color: var(--gold-primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

.search-input-group button {
  width: 55px;
  height: 55px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 12px;
  color: var(--bg-deep);
  cursor: pointer;
  transition: all 0.3s;
}

.search-input-group button:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-gold);
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>
