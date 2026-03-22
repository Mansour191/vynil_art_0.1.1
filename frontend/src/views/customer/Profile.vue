<template>
  <div class="profile-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="profile-container">
      <div class="glass-card">
        <!-- Profile Header -->
        <div class="profile-header">
          <div class="profile-avatar">
            <div class="avatar-circle">
              <img 
                v-if="user && user.avatar" 
                :src="user.avatar" 
                :alt="user.firstName || user.username"
                class="avatar-image"
              />
              <div v-else class="avatar-placeholder">
                <i class="fa-solid fa-user"></i>
              </div>
            </div>
            <button class="avatar-upload-btn" @click="uploadAvatar">
              <i class="fa-solid fa-camera"></i>
            </button>
          </div>
          <div class="profile-info">
            <h1 class="profile-name">{{ user?.firstName || user?.username || 'مستخدم' }}</h1>
            <p class="profile-email">{{ user?.email || 'لا يوجد بريد إلكتروني' }}</p>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userStats.orders || 0 }}</span>
                <span class="stat-label">طلب</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.wishlist || 0 }}</span>
                <span class="stat-label">مفضل</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.points || 0 }}</span>
                <span class="stat-label">نقطة</span>
              </div>
            </div>
          </div>
          <div class="profile-actions">
            <button class="logout-btn" @click="handleLogout" :disabled="authStore.loading">
              <i v-if="!authStore.loading" class="fa-solid fa-sign-out-alt"></i>
              <i v-else class="fa-solid fa-spinner fa-spin"></i>
              {{ authStore.loading ? 'جاري تسجيل الخروج...' : 'تسجيل الخروج' }}
            </button>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="profile-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.name"
            :class="['tab-btn', { active: activeTab === tab.name }]"
            @click="activeTab = tab.name"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'" class="tab-panel">
            <div class="overview-grid">
              <div class="overview-card">
                <div class="card-header">
                  <h3 class="card-title">
                    <i class="fa-solid fa-user"></i>
                    المعلومات الشخصية
                  </h3>
                  <button class="edit-btn" @click="editProfile" :disabled="authStore.loading">
                    <i v-if="!authStore.loading" class="fa-solid fa-edit"></i>
                    <i v-else class="fa-solid fa-spinner fa-spin"></i>
                  </button>
                </div>
                <div class="card-content">
                  <div class="info-row">
                    <span class="info-label">الاسم الكامل:</span>
                    <span v-if="!settingsForm.isEditing" class="info-value">{{ user?.firstName || 'غير محدد' }} {{ user?.lastName || '' }}</span>
                    <input 
                      v-else
                      type="text" 
                      v-model="settingsForm.firstName" 
                      class="info-input"
                    />
                  </div>
                  <div class="info-row">
                    <span class="info-label">البريد الإلكتروني:</span>
                    <span v-if="!settingsForm.isEditing" class="info-value">{{ user?.email || 'غير محدد' }}</span>
                    <input 
                      v-else
                      type="email" 
                      v-model="settingsForm.email" 
                      class="info-input"
                    />
                  </div>
                  <div class="info-row">
                    <span class="info-label">رقم الهاتف:</span>
                    <span v-if="!settingsForm.isEditing" class="info-value">{{ user?.phone || 'غير محدد' }}</span>
                    <input 
                      v-else
                      type="tel" 
                      v-model="settingsForm.phone" 
                      class="info-input"
                    />
                  </div>
                  <div class="info-row">
                    <span class="info-label">تاريخ الانضمام:</span>
                    <span class="info-value">{{ formatDate(user?.dateJoined) }}</span>
                  </div>
                </div>
              </div>

              <div class="overview-card">
                <div class="card-header">
                  <h3 class="card-title">
                    <i class="fa-solid fa-shopping-bag"></i>
                    آخر الطلبات
                  </h3>
                  <router-link to="/profile/orders" class="view-all-btn">
                    عرض الكل
                  </router-link>
                </div>
                <div class="card-content">
                  <div v-if="recentOrders.length === 0" class="empty-state">
                    <i class="fa-solid fa-shopping-cart empty-icon"></i>
                    <p>لا توجد طلبات بعد</p>
                  </div>
                  <div v-else class="orders-list">
                    <div v-for="order in recentOrders" :key="order.id" class="order-item">
                      <div class="order-info">
                        <span class="order-number">#{{ order.id }}</span>
                        <span class="order-date">{{ formatDate(order.createdAt) }}</span>
                      </div>
                      <div class="order-status">
                        <span :class="['status-badge', order.status]">{{ getStatusText(order.status) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="overview-card">
                <div class="card-header">
                  <h3 class="card-title">
                    <i class="fa-solid fa-heart"></i>
                    المفضلة
                  </h3>
                  <router-link to="/profile/wishlist" class="view-all-btn">
                    عرض الكل
                  </router-link>
                </div>
                <div class="card-content">
                  <div v-if="wishlistItems.length === 0" class="empty-state">
                    <i class="fa-solid fa-heart empty-icon"></i>
                    <p>لا توجد عناصر في المفضلة</p>
                  </div>
                  <div v-else class="wishlist-grid">
                    <div v-for="item in wishlistItems" :key="item.id" class="wishlist-item">
                      <img :src="item.image" :alt="item.name" class="wishlist-image" />
                      <div class="wishlist-info">
                        <h4 class="wishlist-name">{{ item.name }}</h4>
                        <p class="wishlist-price">{{ formatPrice(item.price) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Orders Tab -->
          <div v-if="activeTab === 'orders'" class="tab-panel">
            <div class="orders-section">
              <div class="section-header">
                <h3 class="section-title">طلباتي</h3>
                <div class="filter-buttons">
                  <button 
                    v-for="filter in orderFilters" 
                    :key="filter.value"
                    :class="['filter-btn', { active: activeOrderFilter === filter.value }]"
                    @click="activeOrderFilter = filter.value"
                  >
                    {{ filter.label }}
                  </button>
                </div>
              </div>
              <div class="orders-grid">
                <div v-if="filteredOrders.length === 0" class="empty-state">
                  <i class="fa-solid fa-shopping-cart empty-icon"></i>
                  <p>لا توجد طلبات في هذه الفئة</p>
                </div>
                <div v-else class="order-cards">
                  <div v-for="order in filteredOrders" :key="order.id" class="order-card">
                    <div class="order-header">
                      <div class="order-number">طلب #{{ order.id }}</div>
                      <div class="order-date">{{ formatDate(order.createdAt) }}</div>
                    </div>
                    <div class="order-items">
                      <div v-for="item in order.items" :key="item.id" class="order-item">
                        <img :src="item.image" :alt="item.name" class="item-image" />
                        <div class="item-details">
                          <h4 class="item-name">{{ item.name }}</h4>
                          <p class="item-quantity">الكمية: {{ item.quantity }}</p>
                        </div>
                        <div class="item-price">{{ formatPrice(item.price) }}</div>
                      </div>
                    </div>
                    <div class="order-footer">
                      <div class="order-total">
                        <span class="total-label">الإجمالي:</span>
                        <span class="total-amount">{{ formatPrice(order.total) }}</span>
                      </div>
                      <div class="order-actions">
                        <button class="action-btn primary" @click="viewOrderDetails(order.id)">
                          عرض التفاصيل
                        </button>
                        <button class="action-btn secondary" @click="trackOrder(order.id)">
                          تتبع الطلب
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Wishlist Tab -->
          <div v-if="activeTab === 'wishlist'" class="tab-panel">
            <div class="wishlist-section">
              <div class="section-header">
                <h3 class="section-title">المفضلة</h3>
                <div class="wishlist-actions">
                  <button class="action-btn secondary" @click="clearWishlist">
                    <i class="fa-solid fa-trash"></i>
                    تفريغ المفضلة
                  </button>
                </div>
              </div>
              <div class="wishlist-grid">
                <div v-if="wishlistItems.length === 0" class="empty-state">
                  <i class="fa-solid fa-heart empty-icon"></i>
                  <p>لا توجد عناصر في المفضلة</p>
                  <router-link to="/products" class="browse-btn">
                    تصفح المنتجات
                  </router-link>
                </div>
                <div v-else class="wishlist-cards">
                  <div v-for="item in wishlistItems" :key="item.id" class="wishlist-card">
                    <div class="wishlist-image-container">
                      <img :src="item.image" :alt="item.name" class="wishlist-image" />
                      <button class="remove-btn" @click="removeFromWishlist(item.id)">
                        <i class="fa-solid fa-times"></i>
                      </button>
                    </div>
                    <div class="wishlist-content">
                      <h4 class="wishlist-name">{{ item.name }}</h4>
                      <p class="wishlist-description">{{ item.description }}</p>
                      <div class="wishlist-price-section">
                        <span class="wishlist-price">{{ formatPrice(item.price) }}</span>
                        <span v-if="item.originalPrice" class="wishlist-original-price">
                          {{ formatPrice(item.originalPrice) }}
                        </span>
                      </div>
                      <div class="wishlist-actions">
                        <button class="action-btn primary" @click="addToCart(item)">
                          <i class="fa-solid fa-shopping-cart"></i>
                          أضف للسلة
                        </button>
                        <button class="action-btn secondary" @click="viewProduct(item.id)">
                          عرض المنتج
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Settings Tab -->
          <div v-if="activeTab === 'settings'" class="tab-panel">
            <div class="settings-section">
              <div class="section-header">
                <h3 class="section-title">الإعدادات</h3>
              </div>
              <div class="settings-grid">
                <div class="settings-card">
                  <h4 class="settings-card-title">معلومات الحساب</h4>
                  <div class="settings-form">
                    <div class="form-group">
                      <label class="form-label">الاسم الأول</label>
                      <input 
                        type="text" 
                        v-model="settingsForm.firstName" 
                        class="form-input"
                        placeholder="أدخل اسمك الأول"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">الاسم الأخير</label>
                      <input 
                        type="text" 
                        v-model="settingsForm.lastName" 
                        class="form-input"
                        placeholder="أدخل اسمك الأخير"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">البريد الإلكتروني</label>
                      <input 
                        type="email" 
                        v-model="settingsForm.email" 
                        class="form-input"
                        placeholder="أدخل بريدك الإلكتروني"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">رقم الهاتف</label>
                      <input 
                        type="tel" 
                        v-model="settingsForm.phone" 
                        class="form-input"
                        placeholder="أدخل رقم هاتفك"
                      />
                    </div>
                    <button class="save-btn" @click="saveSettings" :disabled="authStore.loading">
                      <i v-if="!authStore.loading" class="fa-solid fa-save"></i>
                      <i v-else class="fa-solid fa-spinner fa-spin"></i>
                      {{ authStore.loading ? 'جاري الحفظ...' : 'حفظ التغييرات' }}
                    </button>
                  </div>
                </div>

                <div class="settings-card">
                  <h4 class="settings-card-title">تغيير كلمة المرور</h4>
                  <div class="settings-form">
                    <div class="form-group">
                      <label class="form-label">كلمة المرور الحالية</label>
                      <input 
                        type="password" 
                        v-model="passwordForm.currentPassword" 
                        class="form-input"
                        placeholder="أدخل كلمة المرور الحالية"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">كلمة المرور الجديدة</label>
                      <input 
                        type="password" 
                        v-model="passwordForm.newPassword" 
                        class="form-input"
                        placeholder="أدخل كلمة المرور الجديدة"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">تأكيد كلمة المرور الجديدة</label>
                      <input 
                        type="password" 
                        v-model="passwordForm.confirmPassword" 
                        class="form-input"
                        placeholder="أعد إدخال كلمة المرور الجديدة"
                      />
                    </div>
                    <button class="save-btn" @click="changePassword" :disabled="authStore.loading">
                      <i v-if="!authStore.loading" class="fa-solid fa-lock"></i>
                      <i v-else class="fa-solid fa-spinner fa-spin"></i>
                      {{ authStore.loading ? 'جاري التغيير...' : 'تغيير كلمة المرور' }}
                    </button>
                  </div>
                </div>

                <div class="settings-card">
                  <h4 class="settings-card-title">الإشعارات</h4>
                  <div class="settings-form">
                    <div class="toggle-group">
                      <label class="toggle-label">
                        <input type="checkbox" v-model="notificationSettings.email" />
                        <span class="toggle-text">الإشعارات عبر البريد الإلكتروني</span>
                      </label>
                      <label class="toggle-label">
                        <input type="checkbox" v-model="notificationSettings.sms" />
                        <span class="toggle-text">الإشعارات عبر الرسائل النصية</span>
                      </label>
                      <label class="toggle-label">
                        <input type="checkbox" v-model="notificationSettings.push" />
                        <span class="toggle-text">الإشعارات الفورية</span>
                      </label>
                    </div>
                    <button class="save-btn" @click="saveNotificationSettings">
                      <i class="fa-solid fa-bell"></i>
                      حفظ إعدادات الإشعارات
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const activeTab = ref('overview');
const activeOrderFilter = ref('all');

const user = computed(() => authStore.user);

const tabs = [
  { name: 'overview', label: 'نظرة عامة', icon: 'fa-solid fa-home' },
  { name: 'orders', label: 'طلباتي', icon: 'fa-solid fa-shopping-bag' },
  { name: 'wishlist', label: 'المفضلة', icon: 'fa-solid fa-heart' },
  { name: 'settings', label: 'الإعدادات', icon: 'fa-solid fa-cog' }
];

const orderFilters = [
  { value: 'all', label: 'الكل' },
  { value: 'pending', label: 'قيد الانتظار' },
  { value: 'processing', label: 'قيد المعالجة' },
  { value: 'shipped', label: 'تم الشحن' },
  { value: 'delivered', label: 'تم التسليم' },
  { value: 'cancelled', label: 'ملغي' }
];

// Real data from DRF Auth Kit - will be loaded in onMounted
const userStats = reactive({
  orders: 0,
  wishlist: 0,
  points: 0
});

const recentOrders = ref([]);
const allOrders = ref([]);
const wishlistItems = ref([]);

const settingsForm = reactive({
  firstName: user.value?.firstName || '',
  lastName: user.value?.lastName || '',
  email: user.value?.email || '',
  phone: user.value?.phone || ''
});

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const notificationSettings = reactive({
  email: true,
  sms: false,
  push: true
});

const filteredOrders = computed(() => {
  if (activeOrderFilter.value === 'all') {
    return allOrders.value;
  }
  return allOrders.value.filter(order => order.status === activeOrderFilter.value);
});

const formatDate = (date) => {
  if (!date) return 'غير محدد';
  return new Date(date).toLocaleDateString('ar-SA');
};

const formatPrice = (price) => {
  return new Intl.NumberFormat('ar-SA', {
    style: 'currency',
    currency: 'DZD'
  }).format(price);
};

const getStatusText = (status) => {
  const statusMap = {
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التسليم',
    cancelled: 'ملغي'
  };
  return statusMap[status] || status;
};

const handleLogout = async () => {
  if (confirm('هل أنت متأكد من تسجيل الخروج؟')) {
    try {
      authStore.loading = true;
      await authStore.logout();
      router.push('/login');
    } catch (error) {
      console.error('Error during logout:', error);
      alert('حدث خطأ أثناء تسجيل الخروج');
    } finally {
      authStore.loading = false;
    }
  }
};

const uploadAvatar = () => {
  // TODO: Implement avatar upload
  console.log('Upload avatar');
};

const editProfile = () => {
  // Toggle edit mode for profile fields
  const isEditing = !settingsForm.isEditing;
  settingsForm.isEditing = isEditing;
  
  if (isEditing) {
    // Enter edit mode - populate form with current user data
    Object.assign(settingsForm, {
      firstName: authStore.user?.firstName || '',
      lastName: authStore.user?.lastName || '',
      email: authStore.user?.email || '',
      phone: authStore.user?.phone || '',
      isEditing: true
    });
  } else {
    // Exit edit mode without saving
    Object.assign(settingsForm, {
      firstName: authStore.user?.firstName || '',
      lastName: authStore.user?.lastName || '',
      email: authStore.user?.email || '',
      phone: authStore.user?.phone || '',
      isEditing: false
    });
  }
};

const viewOrderDetails = (orderId) => {
  router.push(`/profile/orders/${orderId}`);
};

const trackOrder = (orderId) => {
  // TODO: Implement order tracking
  console.log('Track order:', orderId);
};

const removeFromWishlist = (itemId) => {
  wishlistItems.value = wishlistItems.value.filter(item => item.id !== itemId);
};

const addToCart = (item) => {
  // TODO: Implement add to cart
  console.log('Add to cart:', item);
};

const viewProduct = (productId) => {
  router.push(`/products/${productId}`);
};

const clearWishlist = () => {
  if (confirm('هل أنت متأكد من تفريغ المفضلة؟')) {
    wishlistItems.value = [];
  }
};

const saveSettings = async () => {
  try {
    authStore.loading = true;
    await authStore.updateProfile({
      firstName: settingsForm.firstName,
      lastName: settingsForm.lastName,
      email: settingsForm.email,
      phone: settingsForm.phone
    });
    
    // Update local form data
    Object.assign(settingsForm, {
      firstName: authStore.user?.firstName || '',
      lastName: authStore.user?.lastName || '',
      email: authStore.user?.email || '',
      phone: authStore.user?.phone || ''
    });
    
    alert('تم تحديث الملف الشخصي بنجاح!');
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('حدث خطأ أثناء تحديث الملف الشخصي: ' + error.message);
  } finally {
    authStore.loading = false;
  }
};

const changePassword = async () => {
  if (!passwordForm.newPassword || !passwordForm.confirmPassword) {
    alert('يرجى إدخال كلمة المرور الجديدة وتأكيدها');
    return;
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    alert('كلمتا المرور غير متطابقتين');
    return;
  }
  
  try {
    authStore.loading = true;
    await authStore.changePassword(
      passwordForm.currentPassword,
      passwordForm.newPassword,
      passwordForm.confirmPassword
    );
    
    // Clear form
    Object.assign(passwordForm, {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    
    alert('تم تغيير كلمة المرور بنجاح!');
  } catch (error) {
    console.error('Error changing password:', error);
    alert('حدث خطأ أثناء تغيير كلمة المرور: ' + error.message);
  } finally {
    authStore.loading = false;
  }
};

const saveNotificationSettings = () => {
  // TODO: Implement save notification settings to backend
  console.log('Save notification settings:', notificationSettings);
  localStorage.setItem('notificationSettings', JSON.stringify(notificationSettings));
  alert('تم حفظ إعدادات الإشعارات!');
};

onMounted(async () => {
  try {
    // Load real user data from DRF Auth Kit
    await authStore.fetchProfile();
    
    // Update form with real data
    Object.assign(settingsForm, {
      firstName: authStore.user?.firstName || '',
      lastName: authStore.user?.lastName || '',
      email: authStore.user?.email || '',
      phone: authStore.user?.phone || ''
    });
    
    // Load notification settings
    const savedSettings = localStorage.getItem('notificationSettings');
    if (savedSettings) {
      Object.assign(notificationSettings, JSON.parse(savedSettings));
    }
    
    console.log('Profile page mounted with real user data:', authStore.user);
  } catch (error) {
    console.error('Error loading profile data:', error);
    // Continue with mock data if there's an error
  }
});
</script>

<style scoped>
/* ===== Customer Profile Page ===== */
.profile-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

/* Background Effects */
.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 20%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(212, 175, 55, 0.12) 0%, transparent 50%);
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.1) 50%, transparent 100%);
  filter: blur(2px);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-20px) scale(1.05); }
}

/* Profile Container */
.profile-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1200px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.08),
              inset 0 0 30px rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

/* Profile Header */
.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-avatar {
  position: relative;
}

.avatar-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: #1a1a2e;
  font-size: 48px;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.9);
  border: 2px solid rgba(255, 255, 255, 0.2);
  color: #1a1a2e;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  background: #d4af37;
  transform: scale(1.1);
}

.profile-info {
  flex: 1;
}

.profile-actions {
  display: flex;
  align-items: center;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #c82333 0%, #a02622 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(220, 53, 69, 0.3);
}

.logout-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.profile-name {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 8px 0;
}

.profile-email {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  margin: 0 0 20px 0;
}

.profile-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #d4af37;
  margin-bottom: 4px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

/* Profile Tabs */
.profile-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: transparent;
  border: none;
  border-radius: 8px 8px 0 0;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.tab-btn.active {
  color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.tab-btn i {
  font-size: 16px;
}

/* Tab Content */
.tab-content {
  min-height: 400px;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Overview Grid */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.overview-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.overview-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.card-title i {
  color: #d4af37;
}

.edit-btn, .view-all-btn {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 8px;
  padding: 8px 12px;
  color: #d4af37;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover, .view-all-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  transform: translateY(-1px);
}

.view-all-btn {
  text-decoration: none;
}

.card-content {
  color: rgba(255, 255, 255, 0.8);
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.info-value {
  color: #ffffff;
  font-weight: 500;
}

.info-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  padding: 8px 12px;
  color: #ffffff;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
}

.info-input:focus {
  outline: none;
  border-color: rgba(212, 175, 55, 0.6);
  background: rgba(255, 255, 255, 0.15);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.empty-icon {
  font-size: 48px;
  color: rgba(255, 255, 255, 0.3);
  margin-bottom: 16px;
}

.browse-btn {
  display: inline-block;
  margin-top: 16px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.browse-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-number {
  color: #ffffff;
  font-weight: 600;
}

.order-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.delivered {
  background: rgba(0, 200, 81, 0.2);
  color: #00c851;
}

.status-badge.shipped {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
}

.status-badge.processing {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-badge.pending {
  background: rgba(108, 117, 125, 0.2);
  color: #6c757d;
}

.status-badge.cancelled {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

/* Wishlist Grid */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.wishlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.wishlist-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.wishlist-info {
  flex: 1;
}

.wishlist-name {
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.wishlist-price {
  color: #d4af37;
  font-size: 14px;
  font-weight: 600;
}

/* Section Headers */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.filter-buttons {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.filter-btn.active {
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  border-color: rgba(212, 175, 55, 0.3);
}

/* Orders Grid */
.orders-grid {
  display: grid;
  gap: 20px;
}

.order-cards {
  display: grid;
  gap: 20px;
}

.order-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.order-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.order-number {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.order-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.item-details {
  flex: 1;
}

.item-name {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.item-quantity {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.item-price {
  color: #d4af37;
  font-size: 16px;
  font-weight: 600;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.order-total {
  display: flex;
  align-items: center;
  gap: 8px;
}

.total-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.total-amount {
  color: #d4af37;
  font-size: 18px;
  font-weight: 700;
}

.order-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Wishlist Cards */
.wishlist-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.wishlist-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.wishlist-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.wishlist-image-container {
  position: relative;
  height: 200px;
}

.wishlist-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(220, 53, 69, 0.9);
  border: none;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: #dc3545;
  transform: scale(1.1);
}

.wishlist-content {
  padding: 20px;
}

.wishlist-name {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.wishlist-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0 0 16px 0;
}

.wishlist-price-section {
  margin-bottom: 16px;
}

.wishlist-price {
  color: #d4af37;
  font-size: 20px;
  font-weight: 700;
}

.wishlist-original-price {
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  text-decoration: line-through;
  margin-right: 8px;
}

.wishlist-actions {
  display: flex;
  gap: 12px;
}

/* Settings Section */
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.settings-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
}

.settings-card-title {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.save-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  cursor: pointer;
}

.toggle-label input[type="checkbox"] {
  accent-color: #d4af37;
  width: 16px;
  height: 16px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .profile-tabs {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .tab-btn {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .order-cards {
    grid-template-columns: 1fr;
  }
  
  .wishlist-cards {
    grid-template-columns: 1fr;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-buttons {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .filter-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  .order-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .wishlist-actions {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
