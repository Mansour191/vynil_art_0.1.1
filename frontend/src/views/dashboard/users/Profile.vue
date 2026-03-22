<template>
  <div class="profile-page">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-user-circle header-icon"></i>
          الملف الشخصي
        </h1>
        <p class="header-subtitle">عرض وتعديل معلوماتك الشخصية وإعدادات الحساب</p>
      </div>
      <div class="header-actions">
        <button class="btn-save-header" @click="saveProfile" v-if="isEditing">
          <i class="fa-solid fa-save"></i>
          <span>حفظ التغييرات</span>
        </button>
        <button class="btn-edit-header" @click="startEditing" v-else>
          <i class="fa-solid fa-edit"></i>
          <span>تعديل الملف</span>
        </button>
      </div>
    </div>

    <!-- محتوى الملف الشخصي -->
    <div class="profile-content">
      <!-- العمود الأيمن - الصورة والمعلومات الأساسية -->
      <div class="profile-sidebar">
        <div class="profile-card">
          <div class="profile-avatar">
            <img :src="profile.avatar" :alt="profile.name" />
            <div v-if="isEditing" class="avatar-overlay" @click="triggerAvatarUpload">
              <i class="fa-solid fa-camera"></i>
              <span>تغيير الصورة</span>
            </div>
            <input
              type="file"
              ref="avatarInput"
              @change="handleAvatarUpload"
              accept="image/*"
              style="display: none"
            />
          </div>
          <h2 class="profile-name">{{ profile.name }}</h2>
          <p class="profile-role">{{ getRoleText(profile.role) }}</p>

          <div class="profile-status">
            <span class="status-badge" :class="profile.status">
              {{ getStatusText(profile.status) }}
            </span>
          </div>

          <div class="profile-meta">
            <div class="meta-item">
              <i class="far fa-calendar-alt"></i>
              <div>
                <span class="meta-label">عضو منذ</span>
                <span class="meta-value">{{ formatDate(profile.joinedAt) }}</span>
              </div>
            </div>
            <div class="meta-item">
              <i class="far fa-clock"></i>
              <div>
                <span class="meta-label">آخر نشاط</span>
                <span class="meta-value">{{ getLastActiveText(profile.lastActive) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- بطاقة الإحصائيات السريعة -->
        <div class="stats-card">
          <h3><i class="fa-solid fa-chart-line"></i> نشاطك</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">{{ profile.stats.orders }}</span>
              <span class="stat-label">الطلبات</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ profile.stats.products }}</span>
              <span class="stat-label">المنتجات</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ profile.stats.reviews }}</span>
              <span class="stat-label">تقييمات</span>
            </div>
          </div>
        </div>
      </div>

      <!-- العمود الأيسر - المعلومات التفصيلية -->
      <div class="profile-main">
        <!-- تبويبات الملف -->
        <div class="profile-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="tab-btn"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.name }}</span>
          </button>
        </div>

        <!-- محتوى التبويبات -->
        <div class="tab-content">
          <!-- ===== المعلومات الشخصية ===== -->
          <div v-if="activeTab === 'personal'" class="info-section">
            <div class="section-header">
              <h3>المعلومات الشخصية</h3>
            </div>

            <div class="info-grid">
              <div class="info-field">
                <label>الاسم الكامل</label>
                <div v-if="!isEditing" class="field-value">{{ profile.name }}</div>
                <input v-else type="text" v-model="editableProfile.name" class="field-input" />
              </div>

              <div class="info-field">
                <label>اسم المستخدم</label>
                <div v-if="!isEditing" class="field-value">@{{ profile.username }}</div>
                <input v-else type="text" v-model="editableProfile.username" class="field-input" />
              </div>

              <div class="info-field">
                <label>البريد الإلكتروني</label>
                <div v-if="!isEditing" class="field-value">{{ profile.email }}</div>
                <input v-else type="email" v-model="editableProfile.email" class="field-input" />
              </div>

              <div class="info-field">
                <label>رقم الهاتف</label>
                <div v-if="!isEditing" class="field-value">{{ profile.phone || 'غير محدد' }}</div>
                <input
                  v-else
                  type="tel"
                  v-model="editableProfile.phone"
                  class="field-input"
                  placeholder="أدخل رقم الهاتف"
                />
              </div>

              <div class="info-field full-width">
                <label>نبذة عني</label>
                <div v-if="!isEditing" class="field-value bio">
                  {{ profile.bio || 'لا توجد نبذة' }}
                </div>
                <textarea
                  v-else
                  v-model="editableProfile.bio"
                  class="field-input bio-input"
                  rows="4"
                  placeholder="اكتب نبذة عن نفسك..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- ===== العنوان ومعلومات الاتصال ===== -->
          <div v-if="activeTab === 'address'" class="info-section">
            <div class="section-header">
              <h3>معلومات العنوان</h3>
            </div>

            <div class="info-grid">
              <div class="info-field">
                <label>المدينة</label>
                <div v-if="!isEditing" class="field-value">
                  {{ profile.address?.city || 'غير محدد' }}
                </div>
                <input
                  v-else
                  type="text"
                  v-model="editableProfile.address.city"
                  class="field-input"
                  placeholder="المدينة"
                />
              </div>

              <div class="info-field">
                <label>المنطقة</label>
                <div v-if="!isEditing" class="field-value">
                  {{ profile.address?.region || 'غير محدد' }}
                </div>
                <input
                  v-else
                  type="text"
                  v-model="editableProfile.address.region"
                  class="field-input"
                  placeholder="المنطقة"
                />
              </div>

              <div class="info-field full-width">
                <label>العنوان التفصيلي</label>
                <div v-if="!isEditing" class="field-value">
                  {{ profile.address?.street || 'غير محدد' }}
                </div>
                <input
                  v-else
                  type="text"
                  v-model="editableProfile.address.street"
                  class="field-input"
                  placeholder="الشارع، الحي، المبنى"
                />
              </div>

              <div class="info-field">
                <label>الرمز البريدي</label>
                <div v-if="!isEditing" class="field-value">
                  {{ profile.address?.zipCode || 'غير محدد' }}
                </div>
                <input
                  v-else
                  type="text"
                  v-model="editableProfile.address.zipCode"
                  class="field-input"
                  placeholder="الرمز البريدي"
                />
              </div>

              <div class="info-field">
                <label>الدولة</label>
                <div v-if="!isEditing" class="field-value">
                  {{ profile.address?.country || 'السعودية' }}
                </div>
                <select v-else v-model="editableProfile.address.country" class="field-input">
                  <option value="SA">السعودية</option>
                  <option value="AE">الإمارات</option>
                  <option value="KW">الكويت</option>
                  <option value="QA">قطر</option>
                  <option value="BH">البحرين</option>
                  <option value="OM">عُمان</option>
                </select>
              </div>
            </div>
          </div>

          <!-- ===== تغيير كلمة المرور ===== -->
          <div v-if="activeTab === 'security'" class="info-section">
            <div class="section-header">
              <h3>تغيير كلمة المرور</h3>
            </div>

            <div class="password-form">
              <div class="info-field">
                <label>كلمة المرور الحالية</label>
                <input
                  type="password"
                  v-model="passwordForm.current"
                  class="field-input"
                  placeholder="أدخل كلمة المرور الحالية"
                />
              </div>

              <div class="info-field">
                <label>كلمة المرور الجديدة</label>
                <input
                  type="password"
                  v-model="passwordForm.new"
                  class="field-input"
                  placeholder="أدخل كلمة المرور الجديدة"
                />
                <div class="password-strength" v-if="passwordForm.new">
                  <div class="strength-bars">
                    <div
                      v-for="n in 4"
                      :key="n"
                      class="strength-bar"
                      :class="{
                        active: n <= passwordStrength.score,
                        weak: passwordStrength.score === 1,
                        medium: passwordStrength.score === 2,
                        strong: passwordStrength.score >= 3,
                      }"
                    ></div>
                  </div>
                  <span class="strength-text">{{ passwordStrength.text }}</span>
                </div>
              </div>

              <div class="info-field">
                <label>تأكيد كلمة المرور</label>
                <input
                  type="password"
                  v-model="passwordForm.confirm"
                  class="field-input"
                  placeholder="أعد إدخال كلمة المرور الجديدة"
                />
                <div
                  v-if="
                    passwordForm.new &&
                    passwordForm.confirm &&
                    passwordForm.new !== passwordForm.confirm
                  "
                  class="error-message"
                >
                  كلمة المرور غير متطابقة
                </div>
              </div>

              <button
                class="btn-change-password"
                @click="changePassword"
                :disabled="!canChangePassword"
              >
                <i class="fa-solid fa-key"></i> تغيير كلمة المرور
              </button>
            </div>

            <div class="security-note">
              <i class="fa-solid fa-shield-alt"></i>
              <span>ننصح باستخدام كلمة مرور قوية تحتوي على أحرف كبيرة وصغيرة وأرقام ورموز</span>
            </div>
          </div>

          <!-- ===== طلباتي الأخيرة ===== -->
          <div v-if="activeTab === 'orders'" class="info-section">
            <div class="section-header">
              <h3>آخر الطلبات</h3>
              <router-link to="/dashboard/orders" class="view-all-link">
                عرض الكل <i class="fa-solid fa-arrow-left"></i>
              </router-link>
            </div>

            <div class="recent-orders">
              <div v-for="order in recentOrders" :key="order.id" class="order-item">
                <div class="order-header">
                  <span class="order-id">#{{ order.id }}</span>
                  <span class="order-date">{{ formatDate(order.date) }}</span>
                </div>
                <div class="order-body">
                  <div class="order-products">
                    <span>{{ order.productsCount }} منتج</span>
                  </div>
                  <div class="order-total">{{ order.total }} ر.س</div>
                </div>
                <div class="order-footer">
                  <span class="order-status" :class="order.status">
                    {{ getStatusText(order.status) }}
                  </span>
                  <button class="order-details-btn" @click="viewOrder(order.id)">التفاصيل</button>
                </div>
              </div>

              <div v-if="recentOrders.length === 0" class="no-orders">
                <i class="fa-solid fa-shopping-cart"></i>
                <p>لا توجد طلبات سابقة</p>
                <router-link to="/shop" class="shop-link">تسوق الآن</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { debounce } from 'lodash';
import zxcvbn from 'zxcvbn';

const router = useRouter();

// حالة التعديل
const isEditing = ref(false);

// التبويب النشط
const activeTab = ref('personal');

// قائمة التبويبات
const tabs = [
  { id: 'personal', name: 'المعلومات الشخصية', icon: 'fa-solid fa-user' },
  { id: 'address', name: 'العنوان', icon: 'fa-solid fa-map-marker-alt' },
  { id: 'security', name: 'الأمان', icon: 'fa-solid fa-shield-alt' },
  { id: 'orders', name: 'الطلبات', icon: 'fa-solid fa-shopping-cart' },
];

// بيانات الملف الشخصي
const profile = reactive({
  id: 1,
  name: 'أحمد محمد',
  username: 'ahmed_m',
  email: 'ahmed@example.com',
  phone: '0555123456',
  role: 'admin',
  status: 'active',
  bio: 'مصمم جرافيك ومهتم بتصاميم الفينيل والديكور. خبرة 5 سنوات في مجال التصميم.',
  avatar: 'https://ui-avatars.com/api/?name=أحمد+محمد&background=d4af37&color=fff&size=200',
  joinedAt: '2023-01-15T10:30:00',
  lastActive: '2024-03-18T09:15:00',
  address: {
    city: 'الرياض',
    region: 'الرياض',
    street: 'شارع الملك فهد، حي العليا',
    zipCode: '12345',
    country: 'SA',
  },
  stats: {
    orders: 45,
    products: 12,
    reviews: 28,
  },
});

// نسخة قابلة للتعديل
const editableProfile = reactive({
  name: '',
  username: '',
  email: '',
  phone: '',
  bio: '',
  address: {
    city: '',
    region: '',
    street: '',
    zipCode: '',
    country: 'SA',
  },
});

// نموذج كلمة المرور
const passwordForm = reactive({
  current: '',
  new: '',
  confirm: '',
});

// قوة كلمة المرور
const passwordStrength = reactive({
  score: 0,
  text: '',
});

// الطلبات الأخيرة (بيانات تجريبية)
const recentOrders = ref([
  {
    id: 'ORD-001',
    date: '2024-03-15T14:30:00',
    productsCount: 3,
    total: 450,
    status: 'delivered',
  },
  {
    id: 'ORD-002',
    date: '2024-03-10T09:15:00',
    productsCount: 2,
    total: 280,
    status: 'processing',
  },
  {
    id: 'ORD-003',
    date: '2024-03-05T16:45:00',
    productsCount: 1,
    total: 120,
    status: 'shipped',
  },
]);

// Computed
const canChangePassword = computed(() => {
  return (
    passwordForm.current &&
    passwordForm.new &&
    passwordForm.confirm &&
    passwordForm.new === passwordForm.confirm &&
    passwordStrength.score >= 2
  );
});

// Methods
const resetEditableProfile = () => {
  editableProfile.name = profile.name;
  editableProfile.username = profile.username;
  editableProfile.email = profile.email;
  editableProfile.phone = profile.phone || '';
  editableProfile.bio = profile.bio || '';
  editableProfile.address = {
    city: profile.address?.city || '',
    region: profile.address?.region || '',
    street: profile.address?.street || '',
    zipCode: profile.address?.zipCode || '',
    country: profile.address?.country || 'SA',
  };
};

const startEditing = () => {
  isEditing.value = true;
};

const saveProfile = () => {
  Object.assign(profile, editableProfile);
  if (!profile.address) profile.address = {};
  Object.assign(profile.address, editableProfile.address);
  isEditing.value = false;
  // toast notification could be added here
};

const avatarInput = ref(null);
const triggerAvatarUpload = () => {
  avatarInput.value.click();
};

const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      alert('حجم الصورة يجب أن يكون أقل من 2MB');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      profile.avatar = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const getLastActiveText = (dateString) => {
  if (!dateString) return 'غير معروف';
  const lastActive = new Date(dateString);
  const now = new Date();
  const diffMs = now - lastActive;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'الآن';
  if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
  if (diffHours < 24) return `منذ ${diffHours} ساعة`;
  if (diffDays === 1) return 'أمس';
  return formatDate(dateString);
};

const getRoleText = (role) => {
  const map = {
    admin: 'مدير',
    manager: 'مسؤول',
    editor: 'محرر',
    user: 'مستخدم',
  };
  return map[role] || role;
};

const getStatusText = (status) => {
  const map = {
    active: 'نشط',
    inactive: 'غير نشط',
    banned: 'محظور',
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التوصيل',
    cancelled: 'ملغي',
  };
  return map[status] || status;
};

const changePassword = () => {
  if (passwordForm.new !== passwordForm.confirm) {
    alert('كلمة المرور غير متطابقة');
    return;
  }
  console.log('Changing password...');
  passwordForm.current = '';
  passwordForm.new = '';
  passwordForm.confirm = '';
  alert('تم تغيير كلمة المرور بنجاح');
};

const viewOrder = (orderId) => {
  router.push(`/dashboard/orders/${orderId}`);
};

const checkPasswordStrength = debounce(() => {
  if (passwordForm.new) {
    const result = zxcvbn(passwordForm.new);
    passwordStrength.score = result.score;
    const strengthTexts = {
      0: 'ضعيفة جداً',
      1: 'ضعيفة',
      2: 'متوسطة',
      3: 'قوية',
      4: 'قوية جداً',
    };
    passwordStrength.text = strengthTexts[result.score];
  } else {
    passwordStrength.score = 0;
    passwordStrength.text = '';
  }
}, 300);

// Watchers
watch(() => passwordForm.new, () => {
  checkPasswordStrength();
});

// Lifecycle
onMounted(() => {
  resetEditableProfile();
});
</script>

<style scoped>
@import '@/assets/theme.css';

.profile-page {
  padding: 25px;
  min-height: 100vh;
  background: var(--bg-primary);
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== رأس الصفحة ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 25px 30px;
  border-radius: 24px;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-md);
}

.header-title h1 {
  font-size: 2rem;
  color: white;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: var(--gold-1);
  font-size: 2rem;
  animation: iconPulse 2s ease infinite;
}

@keyframes iconPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.header-subtitle {
  color: var(--text-dim);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-save-header,
.btn-edit-header {
  padding: 14px 28px;
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition-smooth);
}

.btn-save-header {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-edit-header {
  background: var(--bg-primary);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-save-header:hover,
.btn-edit-header:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== محتوى الملف الشخصي ===== */
.profile-content {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 25px;
}

/* ===== العمود الجانبي ===== */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.profile-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 30px 25px;
  border: 1px solid var(--border-light);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.profile-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: var(--gold-gradient-soft);
  opacity: 0.2;
}

.profile-avatar {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid var(--gold-1);
  box-shadow: var(--shadow-gold);
  cursor: pointer;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.profile-avatar:hover img {
  transform: scale(1.1);
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s;
}

.profile-avatar:hover .avatar-overlay {
  opacity: 1;
}

.avatar-overlay i {
  font-size: 1.5rem;
  margin-bottom: 5px;
}

.avatar-overlay span {
  font-size: 0.8rem;
}

.profile-name {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 5px;
}

.profile-role {
  color: var(--gold-1);
  font-size: 0.95rem;
  margin-bottom: 15px;
}

.profile-status {
  margin-bottom: 20px;
}

.status-badge {
  padding: 5px 15px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.status-badge.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}

.profile-meta {
  text-align: right;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.meta-item i {
  width: 35px;
  height: 35px;
  background: var(--bg-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-1);
}

.meta-item div {
  flex: 1;
}

.meta-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 3px;
}

.meta-value {
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
}

/* ===== بطاقة الإحصائيات ===== */
.stats-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.stats-card h3 {
  color: var(--gold-1);
  font-size: 1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  text-align: center;
}

.stat-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-dim);
  font-size: 0.8rem;
}

/* ===== العمود الرئيسي ===== */
.profile-main {
  background: var(--bg-card);
  border-radius: 24px;
  border: 1px solid var(--border-light);
  overflow: hidden;
}

/* ===== تبويبات الملف ===== */
.profile-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-sidebar);
  padding: 0 20px;
}

.tab-btn {
  padding: 18px 25px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
  position: relative;
}

.tab-btn i {
  color: var(--gold-1);
  transition: all 0.3s;
}

.tab-btn::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--gold-gradient);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.tab-btn:hover {
  color: white;
}

.tab-btn.active {
  color: var(--gold-1);
}

.tab-btn.active::after {
  transform: scaleX(1);
}

/* ===== محتوى التبويبات ===== */
.tab-content {
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h3 {
  color: white;
  font-size: 1.2rem;
}

.view-all-link {
  color: var(--gold-1);
  text-decoration: none;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s;
}

.view-all-link:hover {
  gap: 8px;
}

/* ===== شبكة المعلومات ===== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-field {
  margin-bottom: 15px;
}

.info-field.full-width {
  grid-column: span 2;
}

.info-field label {
  display: block;
  color: var(--text-dim);
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.field-value {
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: white;
  min-height: 48px;
}

.field-value.bio {
  white-space: pre-wrap;
  line-height: 1.6;
}

.field-input {
  width: 100%;
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.field-input:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.field-input.bio-input {
  resize: vertical;
}

/* ===== نموذج كلمة المرور ===== */
.password-form {
  max-width: 500px;
}

.password-strength {
  margin-top: 8px;
}

.strength-bars {
  display: flex;
  gap: 5px;
  margin-bottom: 5px;
}

.strength-bar {
  height: 4px;
  flex: 1;
  background: var(--border-light);
  border-radius: 2px;
  transition: all 0.3s;
}

.strength-bar.active.weak {
  background: #f44336;
}

.strength-bar.active.medium {
  background: #ff9800;
}

.strength-bar.active.strong {
  background: #4caf50;
}

.strength-text {
  font-size: 0.8rem;
  color: var(--text-dim);
}

.error-message {
  color: #f44336;
  font-size: 0.8rem;
  margin-top: 5px;
}

.btn-change-password {
  margin-top: 20px;
  padding: 14px 28px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.btn-change-password:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

.btn-change-password:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.security-note {
  margin-top: 20px;
  padding: 15px;
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid #2196f3;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2196f3;
}

.security-note i {
  font-size: 1.2rem;
}

/* ===== الطلبات الأخيرة ===== */
.recent-orders {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.order-item {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.order-item:hover {
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.order-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.order-id {
  color: var(--gold-1);
  font-weight: 600;
}

.order-date {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.order-body {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-light);
}

.order-products {
  color: var(--text-secondary);
}

.order-total {
  color: white;
  font-weight: 700;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.order-status.pending {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border: 1px solid #ffc107;
}

.order-status.processing {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid #2196f3;
}

.order-status.shipped {
  background: rgba(156, 39, 176, 0.2);
  color: #9c27b0;
  border: 1px solid #9c27b0;
}

.order-status.delivered {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}

.order-details-btn {
  padding: 6px 15px;
  background: transparent;
  border: 1px solid var(--gold-1);
  border-radius: 20px;
  color: var(--gold-1);
  cursor: pointer;
  transition: all 0.3s;
}

.order-details-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.no-orders {
  text-align: center;
  padding: 40px;
  color: var(--text-dim);
}

.no-orders i {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.no-orders p {
  margin-bottom: 15px;
}

.shop-link {
  display: inline-block;
  padding: 10px 20px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  text-decoration: none;
  border-radius: 30px;
  font-weight: 600;
  transition: all 0.3s;
}

.shop-link:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

/* ===== استجابة ===== */
@media (max-width: 992px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .info-field.full-width {
    grid-column: span 1;
  }

  .profile-tabs {
    overflow-x: auto;
    padding: 0 10px;
  }

  .tab-btn {
    white-space: nowrap;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 15px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background: var(--bg-primary);
    border-radius: 12px;
  }

  .stat-value {
    margin-bottom: 0;
  }
}
</style>
