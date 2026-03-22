<template>
  <div class="admin-dashboard">
    <AdminSidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <AdminHeader
        :sidebar-collapsed="sidebarCollapsed"
        @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed"
      />

      <div class="content">
        <h1 class="page-title">{{ $t('dashboard') }}</h1>

        <!-- بطاقات الإحصائيات -->
        <div class="stats-grid">
          <StatsCard
            icon="fa-solid fa-newspaper"
            :title="$t('totalPosts')"
            :value="stats.posts"
            color="#D4AF37"
          />
          <StatsCard
            icon="fa-solid fa-tags"
            :title="$t('totalCategories')"
            :value="stats.categories"
            color="#4CAF50"
          />
          <StatsCard
            icon="fa-solid fa-couch"
            :title="$t('totalProducts')"
            :value="stats.products"
            color="#2196F3"
          />
          <StatsCard
            icon="fa-solid fa-comments"
            :title="$t('totalComments')"
            :value="stats.comments"
            color="#FF9800"
          />
          <StatsCard
            icon="fa-solid fa-users"
            :title="$t('totalUsers')"
            :value="stats.users"
            color="#9C27B0"
          />
          <StatsCard
            icon="fa-solid fa-eye"
            :title="$t('totalViews')"
            :value="stats.views"
            color="#F44336"
          />
        </div>

        <!-- رسالة ترحيب -->
        <div class="welcome-card">
          <i class="fa-solid fa-crown welcome-icon"></i>
          <div class="welcome-text">
            <h2>{{ $t('welcomeAdmin') }}</h2>
            <p>{{ $t('welcomeAdminMessage') }}</p>
          </div>
        </div>

        <!-- آخر المقالات -->
        <div class="section-header">
          <h2><i class="fa-solid fa-clock"></i> {{ $t('recentPosts') }}</h2>
          <router-link to="/admin/posts" class="view-all">
            {{ $t('viewAll') }} <i class="fa-solid fa-arrow-left"></i>
          </router-link>
        </div>

        <div class="recent-posts-grid">
          <div v-for="post in recentPosts" :key="post.id" class="recent-post-card">
            <div class="post-image">
              <img :src="post.image" :alt="post.title" />
            </div>
            <div class="post-info">
              <h3>{{ post.title }}</h3>
              <div class="post-meta">
                <span><i class="fa-solid fa-calendar"></i> {{ post.date }}</span>
                <span><i class="fa-solid fa-eye"></i> {{ post.views }}</span>
                <span><i class="fa-solid fa-comment"></i> {{ post.comments }}</span>
              </div>
              <div class="post-actions">
                <router-link :to="`/admin/posts/edit/${post.id}`" class="btn-edit">
                  <i class="fa-solid fa-edit"></i>
                </router-link>
                <button class="btn-delete" @click="deletePost(post.id)">
                  <i class="fa-solid fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from './components/Sidebar.vue';
import AdminHeader from './components/Header.vue';
import StatsCard from './components/StatsCard.vue';

export default {
  name: 'AdminDashboard',
  components: {
    AdminSidebar,
    AdminHeader,
    StatsCard,
  },
  data() {
    return {
      sidebarCollapsed: false,
      stats: {
        posts: 128,
        categories: 8,
        products: 256,
        comments: 342,
        users: 89,
        views: '45.2K',
      },
      recentPosts: [
        {
          id: 1,
          title: 'كيف تختار الفينيل المناسب لمشروعك؟',
          image: 'https://i.postimg.cc/0QKmBBJ9/kitchen2.png',
          date: '15 مارس 2026',
          views: 1234,
          comments: 23,
        },
        {
          id: 2,
          title: '10 أفكار لتجديد غرفة نوم أطفالك بالفينيل',
          image: 'https://i.postimg.cc/7L0DfPgY/Entrance1.png',
          date: '12 مارس 2026',
          views: 856,
          comments: 15,
        },
        {
          id: 3,
          title: '5 أخطاء شائعة عند تركيب الفينيل',
          image: 'https://i.postimg.cc/htCcH3cZ/table1.png',
          date: '10 مارس 2026',
          views: 2100,
          comments: 42,
        },
      ],
    };
  },
  methods: {
    deletePost(id) {
      if (confirm('هل أنت متأكد من حذف هذا المقال؟')) {
        // منطق الحذف
        console.log('Deleting post:', id);
      }
    },
  },
  beforeRouteEnter(to, from, next) {
    // التحقق من تسجيل الدخول
    const token = localStorage.getItem('adminToken');
    if (!token) {
      next('/admin/login');
    } else {
      next();
    }
  },
};
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background: var(--bg-deep);
}

.main-content {
  flex: 1;
  margin-right: 280px;
  transition: margin-right 0.3s;
}

[dir='ltr'] .main-content {
  margin-right: 0;
  margin-left: 280px;
}

.main-content.sidebar-collapsed {
  margin-right: 80px;
}

[dir='ltr'] .main-content.sidebar-collapsed {
  margin-right: 0;
  margin-left: 80px;
}

.content {
  padding: 80px 30px 30px;
}

.page-title {
  color: var(--gold-primary);
  font-size: 2rem;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.welcome-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 30px;
  border: 1px solid var(--border-subtle);
}

.welcome-icon {
  font-size: 4rem;
  color: var(--gold-primary);
}

.welcome-text h2 {
  color: var(--gold-primary);
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.welcome-text p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 30px 0 20px;
}

.section-header h2 {
  color: var(--gold-primary);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.view-all {
  color: var(--gold-primary);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: gap 0.3s;
}

.view-all:hover {
  gap: 12px;
}

.recent-posts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 992px) {
  .recent-posts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .recent-posts-grid {
    grid-template-columns: 1fr;
  }
}

.recent-post-card {
  background: var(--bg-card);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  display: flex;
  gap: 15px;
  padding: 15px;
}

.post-image {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-info {
  flex: 1;
}

.post-info h3 {
  color: var(--text-primary);
  font-size: 1rem;
  margin-bottom: 8px;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 8px;
}

.post-meta i {
  color: var(--gold-primary);
  margin-left: 3px;
}

.post-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
  text-decoration: none;
}

.btn-edit:hover {
  background: #2196f3;
  color: white;
}

.btn-delete {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.btn-delete:hover {
  background: #f44336;
  color: white;
}
</style>
