
<template>
  <v-container fluid class="users-manager pa-4">
    <!-- Header -->
    <v-card class="users-header mb-6" elevation="2">
      <v-card-text class="pa-4">
        <v-row align="center">
          <v-col cols="12" md="8">
            <div class="d-flex align-center">
              <v-avatar
                color="#d4af37"
                size="48"
                class="me-4"
              >
                <v-icon icon="mdi-account-group" size="28"></v-icon>
              </v-avatar>
              <div>
                <h1 class="text-h3 font-weight-bold">
                  {{ $t('users.title', 'إدارة المستخدمين') }}
                </h1>
                <p class="text-body-1 text-dim mt-1">
                  {{ $t('users.subtitle', 'عرض وإدارة جميع مستخدمي النظام والعملاء') }}
                </p>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="4">
            <div class="d-flex gap-2 justify-md-end justify-start">
              <v-btn
                @click="exportUsers"
                variant="outlined"
                prepend-icon="mdi-download"
                class="export-btn"
              >
                {{ $t('users.exportReport', 'تصدير تقرير') }}
              </v-btn>
              <v-btn
                @click="syncAllCustomers"
                variant="elevated"
                prepend-icon="mdi-sync"
                color="#d4af37"
                class="sync-btn"
                :disabled="syncingAll"
                :loading="syncingAll"
              >
                {{ syncingAll ? $t('users.syncing', 'جاري المزامنة...') : $t('users.syncCustomers', 'مزامنة العملاء مع ERPNext') }}
              </v-btn>
              <v-btn
                @click="openUserModal"
                variant="elevated"
                prepend-icon="mdi-account-plus"
                color="#d4af37"
                class="add-btn"
              >
                {{ $t('users.newUser', 'مستخدم جديد') }}
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Sync Progress -->
    <v-expand-transition>
      <div v-if="syncingAll" class="sync-progress-container">
        <v-card variant="outlined" class="mb-4">
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-progress-circular
                indeterminate
                size="20"
                width="2"
                color="#d4af37"
                class="me-3"
              ></v-progress-circular>
              <span class="text-body-2">
                {{ $t('users.syncingCustomers', 'جاري مزامنة العملاء...') }} {{ syncProgress }}%
              </span>
            </div>
            <v-progress-linear
              :model-value="syncProgress"
              color="#d4af37"
              height="8"
              rounded
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </div>
    </v-expand-transition>

    <!-- Sync Results -->
    <v-expand-transition>
      <div v-if="showSyncResults && syncResults" class="mb-4">
        <v-card variant="outlined" color="success">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <v-icon icon="mdi-check-circle" size="24" color="success" class="me-3"></v-icon>
              <div>
                <h4 class="text-h6 font-weight-bold">
                  {{ $t('users.syncResults', 'نتائج مزامنة العملاء') }}
                </h4>
                <p class="text-body-2 mt-1">
                  {{ $t('users.syncedCount', 'تمت مزامنة') }} {{ syncResults.synced }} {{ $t('users.customers', 'عميل') }}
                  {{ syncResults.failed > 0 ? `| ${$t('users.failedCount', 'فشل')}: ${syncResults.failed}` : '' }}
                </p>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </div>
    </v-expand-transition>

    <!-- Statistics Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text class="pa-4 text-center">
            <v-icon icon="mdi-account-group" size="32" color="#d4af37" class="mb-2"></v-icon>
            <h3 class="text-h4 font-weight-bold">{{ userStats.totalUsers }}</h3>
            <p class="text-body-2 text-dim">{{ $t('users.totalUsers', 'إجمالي المستخدمين') }}</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text class="pa-4 text-center">
            <v-icon icon="mdi-account-check" size="32" color="success" class="mb-2"></v-icon>
            <h3 class="text-h4 font-weight-bold">{{ userStats.activeUsers }}</h3>
            <p class="text-body-2 text-dim">{{ $t('users.activeUsers', 'المستخدمين النشطين') }}</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text class="pa-4 text-center">
            <v-icon icon="mdi-account-clock" size="32" color="warning" class="mb-2"></v-icon>
            <h3 class="text-h4 font-weight-bold">{{ userStats.newUsers }}</h3>
            <p class="text-body-2 text-dim">{{ $t('users.newUsers', 'مستخدمين جدد') }}</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text class="pa-4 text-center">
            <v-icon icon="mdi-account-off" size="32" color="error" class="mb-2"></v-icon>
            <h3 class="text-h4 font-weight-bold">{{ userStats.inactiveUsers }}</h3>
            <p class="text-body-2 text-dim">{{ $t('users.inactiveUsers', 'المستخدمين غير النشطين') }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Main Content -->
    <v-card class="users-content" elevation="2">
      <v-card-title class="pa-4">
        <div class="d-flex justify-space-between align-center w-100">
          <h3 class="text-h5 font-weight-bold">
            <v-icon icon="mdi-format-list-bulleted" size="24" class="me-2"></v-icon>
            {{ $t('users.userList', 'قائمة المستخدمين') }}
          </h3>
          <div class="d-flex gap-2">
            <v-text-field
              v-model="searchQuery"
              :label="$t('common.search', 'بحث')"
              variant="outlined"
              prepend-inner-icon="mdi-magnify"
              hide-details
              density="compact"
              style="max-width: 300px;"
              class="me-2"
            ></v-text-field>
            <v-select
              v-model="roleFilter"
              :label="$t('users.filterByRole', 'فلترة بالدور')"
              :items="roleOptions"
              item-title="text"
              item-value="value"
              variant="outlined"
              hide-details
              density="compact"
              style="max-width: 200px;"
              class="me-2"
            ></v-select>
            <v-select
              v-model="statusFilter"
              :label="$t('users.filterByStatus', 'فلترة بالحالة')"
              :items="statusOptions"
              item-title="text"
              item-value="value"
              variant="outlined"
              hide-details
              density="compact"
              style="max-width: 200px;"
            ></v-select>
          </div>
        </div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-4">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="#d4af37" size="48"></v-progress-circular>
          <div class="mt-4 text-body-2 text-dim">{{ $t('common.loading', 'جاري التحميل...') }}</div>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredUsers.length === 0" class="text-center py-8">
          <v-icon icon="mdi-account-group-outline" size="64" color="#d4af37" class="mb-4"></v-icon>
          <h4 class="text-h6 font-weight-bold mb-2">{{ $t('users.noUsers', 'لا توجد مستخدمين') }}</h4>
          <p class="text-body-2 text-dim mb-4">{{ $t('users.noUsersDesc', 'لا توجد مستخدمين حالياً') }}</p>
          <v-btn variant="elevated" color="#d4af37" @click="openUserModal">
            {{ $t('users.addFirstUser', 'إضافة أول مستخدم') }}
          </v-btn>
        </div>

        <!-- Users Table -->
        <v-data-table
          v-else
          :headers="userHeaders"
          :items="paginatedUsers"
          :loading="loading"
          class="users-table"
          hide-default-footer
        >
          <!-- Avatar and Name -->
          <template v-slot:item.name="{ item }">
            <div class="d-flex align-center">
              <v-avatar :image="item.avatar" size="32" class="me-3">
                <v-icon icon="mdi-account" size="16"></v-icon>
              </v-avatar>
              <div>
                <div class="text-body-2 font-weight-bold">{{ item.name }}</div>
                <div class="text-caption text-dim">@{{ item.username }}</div>
              </div>
            </div>
          </template>

          <!-- Email -->
          <template v-slot:item.email="{ item }">
            <div class="text-body-2">{{ item.email }}</div>
          </template>

          <!-- Role -->
          <template v-slot:item.role="{ item }">
            <v-chip
              :color="getRoleColor(item.role)"
              variant="elevated"
              size="small"
            >
              {{ getRoleText(item.role) }}
            </v-chip>
          </template>

          <!-- Status -->
          <template v-slot:item.status="{ item }">
            <v-chip
              :color="getStatusColor(item.status)"
              variant="elevated"
              size="small"
            >
              {{ getStatusText(item.status) }}
            </v-chip>
          </template>

          <!-- Last Active -->
          <template v-slot:item.lastActive="{ item }">
            <div class="text-body-2">{{ getLastActiveText(item.lastActive) }}</div>
          </template>

          <!-- Actions -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex gap-1">
              <v-btn
                variant="text"
                size="small"
                color="#d4af37"
                @click="viewUser(item)"
              >
                <v-icon icon="mdi-eye" size="16"></v-icon>
              </v-btn>
              <v-btn
                variant="text"
                size="small"
                color="info"
                @click="editUser(item)"
              >
                <v-icon icon="mdi-pencil" size="16"></v-icon>
              </v-btn>
              <v-btn
                variant="text"
                size="small"
                :color="item.status === 'active' ? 'warning' : 'success'"
                @click="toggleUserStatus(item)"
              >
                <v-icon :icon="item.status === 'active' ? 'mdi-account-off' : 'mdi-account-check'" size="16"></v-icon>
              </v-btn>
              <v-btn
                variant="text"
                size="small"
                color="error"
                @click="deleteUser(item)"
              >
                <v-icon icon="mdi-delete" size="16"></v-icon>
              </v-btn>
            </div>
          </template>
        </v-data-table>

        <!-- Pagination -->
        <div v-if="filteredUsers.length > itemsPerPage" class="d-flex justify-center mt-4">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="7"
            color="#d4af37"
          ></v-pagination>
        </div>
      </v-card-text>
    </v-card>

    <!-- User Modal -->
    <v-dialog v-model="userModal" max-width="600px">
      <v-card>
        <v-card-title class="pa-4">
          <h3 class="text-h5 font-weight-bold">
            <v-icon icon="mdi-account" size="24" class="me-2"></v-icon>
            {{ editingUser ? $t('users.editUser', 'تعديل المستخدم') : $t('users.addUser', 'إضافة مستخدم') }}
          </h3>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-form ref="userFormRef" v-model="userFormValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="userForm.name"
                  :label="$t('users.name', 'الاسم')"
                  variant="outlined"
                  :rules="[v => !!v || $t('validation.required', 'مطلوب')]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="userForm.username"
                  :label="$t('users.username', 'اسم المستخدم')"
                  variant="outlined"
                  :rules="[v => !!v || $t('validation.required', 'مطلوب')]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="userForm.email"
                  :label="$t('users.email', 'البريد الإلكتروني')"
                  type="email"
                  variant="outlined"
                  :rules="emailRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="userForm.phone"
                  :label="$t('users.phone', 'رقم الهاتف')"
                  type="tel"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="userForm.role"
                  :label="$t('users.role', 'الدور')"
                  :items="roleOptions"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  :rules="[v => !!v || $t('validation.required', 'مطلوب')]"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="userForm.status"
                  :label="$t('users.status', 'الحالة')"
                  :items="statusOptions"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  :rules="[v => !!v || $t('validation.required', 'مطلوب')]"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" v-if="!editingUser">
                <v-text-field
                  v-model="userForm.password"
                  :label="$t('users.password', 'كلمة المرور')"
                  type="password"
                  variant="outlined"
                  :rules="passwordRules"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn @click="closeUserModal" variant="outlined">
            {{ $t('common.cancel', 'إلغاء') }}
          </v-btn>
          <v-btn
            @click="saveUser"
            variant="elevated"
            color="#d4af37"
            :disabled="!userFormValid"
            :loading="saving"
          >
            {{ editingUser ? $t('common.update', 'تحديث') : $t('common.save', 'حفظ') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- User Details Modal -->
    <v-dialog v-model="userDetailsModal" max-width="800px">
      <v-card>
        <v-card-title class="pa-4">
          <h3 class="text-h5 font-weight-bold">
            <v-icon icon="mdi-account-details" size="24" class="me-2"></v-icon>
            {{ $t('users.userDetails', 'تفاصيل المستخدم') }}
          </h3>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <div v-if="selectedUser">
            <!-- User Info -->
            <v-row class="mb-4">
              <v-col cols="12" md="4" class="text-center">
                <v-avatar :image="selectedUser.avatar" size="120" class="mb-3">
                  <v-icon icon="mdi-account" size="60"></v-icon>
                </v-avatar>
                <h4 class="text-h6 font-weight-bold">{{ selectedUser.name }}</h4>
                <p class="text-caption text-dim">@{{ selectedUser.username }}</p>
              </v-col>
              <v-col cols="12" md="8">
                <v-row>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.email', 'البريد الإلكتروني') }}</div>
                    <div class="text-body-2">{{ selectedUser.email }}</div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.phone', 'رقم الهاتف') }}</div>
                    <div class="text-body-2">{{ selectedUser.phone || '-' }}</div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.role', 'الدور') }}</div>
                    <v-chip
                      :color="getRoleColor(selectedUser.role)"
                      variant="elevated"
                      size="small"
                    >
                      {{ getRoleText(selectedUser.role) }}
                    </v-chip>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.status', 'الحالة') }}</div>
                    <v-chip
                      :color="getStatusColor(selectedUser.status)"
                      variant="elevated"
                      size="small"
                    >
                      {{ getStatusText(selectedUser.status) }}
                    </v-chip>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.createdAt', 'تاريخ الإنشاء') }}</div>
                    <div class="text-body-2">{{ formatDate(selectedUser.createdAt) }}</div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-caption text-dim">{{ $t('users.lastActive', 'آخر نشاط') }}</div>
                    <div class="text-body-2">{{ getLastActiveText(selectedUser.lastActive) }}</div>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn @click="userDetailsModal = false" variant="outlined">
            {{ $t('common.close', 'إغلاق') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import UserService from '@/services/UserService';

// Store and i18n
const store = useStore();
const { t } = useI18n();

// State
const loading = ref(false);
const saving = ref(false);
const syncingAll = ref(false);
const syncProgress = ref(0);
const showSyncResults = ref(false);
const syncResults = ref(null);
const searchQuery = ref('');
const roleFilter = ref('all');
const statusFilter = ref('all');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const userModal = ref(false);
const userDetailsModal = ref(false);
const editingUser = ref(null);
const selectedUser = ref(null);
const userFormRef = ref(null);
const userFormValid = ref(false);

// Users data
const users = ref([]);

// User statistics
const userStats = reactive({
  totalUsers: 0,
  activeUsers: 0,
  newUsers: 0,
  inactiveUsers: 0
});

// User form
const userForm = reactive({
  name: '',
  username: '',
  email: '',
  phone: '',
  role: '',
  status: 'active',
  password: ''
});

// Options
const roleOptions = ref([
  { text: t('users.allRoles', 'الكل'), value: 'all' },
  { text: t('roles.admin', 'مدير'), value: 'admin' },
  { text: t('roles.manager', 'مسؤول'), value: 'manager' },
  { text: t('roles.employee', 'موظف'), value: 'employee' },
  { text: t('roles.user', 'مستخدم'), value: 'user' }
]);

const statusOptions = ref([
  { text: t('users.allStatus', 'الكل'), value: 'all' },
  { text: t('status.active', 'نشط'), value: 'active' },
  { text: t('status.inactive', 'غير نشط'), value: 'inactive' },
  { text: t('status.banned', 'محظور'), value: 'banned' }
]);

// Table headers
const userHeaders = ref([
  { title: t('users.name', 'الاسم'), key: 'name', sortable: true },
  { title: t('users.email', 'البريد الإلكتروني'), key: 'email', sortable: true },
  { title: t('users.role', 'الدور'), key: 'role', sortable: true },
  { title: t('users.status', 'الحالة'), key: 'status', sortable: true },
  { title: t('users.lastActive', 'آخر نشاط'), key: 'lastActive', sortable: true },
  { title: t('common.actions', 'الإجراءات'), key: 'actions', sortable: false, width: 120 }
]);

// Form validation rules
const emailRules = [
  v => !!v || t('validation.required', 'مطلوب'),
  v => /.+@.+\..+/.test(v) || t('validation.email', 'البريد الإلكتروني غير صحيح')
];

const passwordRules = [
  v => !!v || t('validation.required', 'مطلوب'),
  v => v.length >= 6 || t('validation.passwordMin', 'كلمة المرور يجب أن تكون 6 أحرف على الأقل')
];

// Computed
const filteredUsers = computed(() => {
  let filtered = users.value;

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(user => 
      user.name.toLowerCase().includes(query) ||
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      (user.phone && user.phone.includes(query))
    );
  }

  // Filter by role
  if (roleFilter.value !== 'all') {
    filtered = filtered.filter(user => user.role === roleFilter.value);
  }

  // Filter by status
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(user => user.status === statusFilter.value);
  }

  return filtered;
});

const totalPages = computed(() => {
  return Math.ceil(filteredUsers.value.length / itemsPerPage.value);
});

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredUsers.value.slice(start, end);
});

// Methods
const loadUsers = async () => {
  try {
    loading.value = true;
    const response = await UserService.getAllUsers();
    
    if (response.success) {
      users.value = response.data.users;
      updateUserStats();
    }
  } catch (error) {
    console.error('Error loading users:', error);
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.loadError', 'فشل في تحميل المستخدمين')
    });
  } finally {
    loading.value = false;
  }
};

const updateUserStats = () => {
  userStats.totalUsers = users.value.length;
  userStats.activeUsers = users.value.filter(u => u.status === 'active').length;
  userStats.inactiveUsers = users.value.filter(u => u.status === 'inactive').length;
  
  // Calculate new users (last 30 days)
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  userStats.newUsers = users.value.filter(u => new Date(u.createdAt) > thirtyDaysAgo).length;
};

const syncAllCustomers = async () => {
  try {
    syncingAll.value = true;
    syncProgress.value = 0;
    showSyncResults.value = false;
    
    const response = await UserService.syncAllCustomers();
    
    if (response.success) {
      // Simulate progress
      const progressInterval = setInterval(() => {
        syncProgress.value += 10;
        if (syncProgress.value >= 100) {
          clearInterval(progressInterval);
          syncResults.value = response.data;
          showSyncResults.value = true;
          syncingAll.value = false;
          syncProgress.value = 0;
          
          // Reload users after sync
          loadUsers();
          
          store.dispatch('notifications/showNotification', {
            type: 'success',
            message: t('users.syncSuccess', 'تمت مزامنة العملاء بنجاح')
          });
        }
      }, 200);
    }
  } catch (error) {
    console.error('Error syncing customers:', error);
    syncingAll.value = false;
    syncProgress.value = 0;
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.syncError', 'فشل في مزامنة العملاء')
    });
  }
};

const exportUsers = async () => {
  try {
    const response = await UserService.exportUsers();
    
    if (response.success) {
      // Create download link
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `users_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
      
      store.dispatch('notifications/showNotification', {
        type: 'success',
        message: t('users.exportSuccess', 'تم تصدير البيانات بنجاح')
      });
    }
  } catch (error) {
    console.error('Error exporting users:', error);
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.exportError', 'فشل في تصدير البيانات')
    });
  }
};

const openUserModal = () => {
  editingUser.value = null;
  resetUserForm();
  userModal.value = true;
};

const closeUserModal = () => {
  userModal.value = false;
  resetUserForm();
};

const resetUserForm = () => {
  Object.assign(userForm, {
    name: '',
    username: '',
    email: '',
    phone: '',
    role: '',
    status: 'active',
    password: ''
  });
  userFormValid.value = false;
};

const viewUser = (user) => {
  selectedUser.value = user;
  userDetailsModal.value = true;
};

const editUser = (user) => {
  editingUser.value = user;
  Object.assign(userForm, {
    name: user.name,
    username: user.username,
    email: user.email,
    phone: user.phone || '',
    role: user.role,
    status: user.status,
    password: ''
  });
  userModal.value = true;
};

const saveUser = async () => {
  try {
    saving.value = true;
    
    let response;
    if (editingUser.value) {
      response = await UserService.updateUser(editingUser.value.id, userForm);
    } else {
      response = await UserService.createUser(userForm);
    }
    
    if (response.success) {
      await loadUsers();
      closeUserModal();
      
      store.dispatch('notifications/showNotification', {
        type: 'success',
        message: editingUser.value ? 
          t('users.updateSuccess', 'تم تحديث المستخدم بنجاح') : 
          t('users.createSuccess', 'تم إنشاء المستخدم بنجاح')
      });
    }
  } catch (error) {
    console.error('Error saving user:', error);
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.saveError', 'فشل في حفظ المستخدم')
    });
  } finally {
    saving.value = false;
  }
};

const toggleUserStatus = async (user) => {
  try {
    const newStatus = user.status === 'active' ? 'inactive' : 'active';
    const response = await UserService.updateUserStatus(user.id, newStatus);
    
    if (response.success) {
      user.status = newStatus;
      updateUserStats();
      
      store.dispatch('notifications/showNotification', {
        type: 'success',
        message: t('users.statusUpdateSuccess', 'تم تحديث حالة المستخدم بنجاح')
      });
    }
  } catch (error) {
    console.error('Error updating user status:', error);
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.statusUpdateError', 'فشل في تحديث حالة المستخدم')
    });
  }
};

const deleteUser = async (user) => {
  if (!confirm(t('users.deleteConfirm', 'هل أنت متأكد من حذف هذا المستخدم؟'))) {
    return;
  }
  
  try {
    const response = await UserService.deleteUser(user.id);
    
    if (response.success) {
      users.value = users.value.filter(u => u.id !== user.id);
      updateUserStats();
      
      store.dispatch('notifications/showNotification', {
        type: 'success',
        message: t('users.deleteSuccess', 'تم حذف المستخدم بنجاح')
      });
    }
  } catch (error) {
    console.error('Error deleting user:', error);
    store.dispatch('notifications/showNotification', {
      type: 'error',
      message: t('users.deleteError', 'فشل في حذف المستخدم')
    });
  }
};

// Utility methods
const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-DZ', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const getLastActiveText = (dateString) => {
  if (!dateString) return t('users.never', 'أبداً');
  const lastActive = new Date(dateString);
  const now = new Date();
  const diffMs = now - lastActive;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return t('users.now', 'الآن');
  if (diffMins < 60) return t('users.minutesAgo', `منذ ${diffMins} دقيقة`);
  if (diffHours < 24) return t('users.hoursAgo', `منذ ${diffHours} ساعة`);
  if (diffDays === 1) return t('users.yesterday', 'أمس');
  return formatDate(dateString);
};

const getRoleText = (role) => {
  const map = {
    admin: t('roles.admin', 'مدير'),
    manager: t('roles.manager', 'مسؤول'),
    employee: t('roles.employee', 'موظف'),
    user: t('roles.user', 'مستخدم')
  };
  return map[role] || role;
};

const getRoleColor = (role) => {
  const colors = {
    admin: 'error',
    manager: 'warning',
    employee: 'info',
    user: 'success'
  };
  return colors[role] || 'default';
};

const getStatusText = (status) => {
  const map = {
    active: t('status.active', 'نشط'),
    inactive: t('status.inactive', 'غير نشط'),
    banned: t('status.banned', 'محظور')
  };
  return map[status] || status;
};

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    inactive: 'warning',
    banned: 'error'
  };
  return colors[status] || 'default';
};

// Lifecycle
onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.users-manager {
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  min-height: 100vh;
}

/* Header Styles */
.users-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.1);
  border-radius: 16px;
}

.add-btn,
.sync-btn {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
  font-weight: 600;
  border: none;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
  transition: all 0.3s ease;
}

.add-btn:hover,
.sync-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
}

.export-btn {
  border-color: #d4af37;
  color: #d4af37;
  font-weight: 500;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  transform: translateY(-1px);
}

/* Statistics Cards */
.stat-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* Content Styles */
.users-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.1);
  border-radius: 16px;
}

.sync-progress-container {
  animation: fadeIn 0.6s ease-out;
}

/* Text Styles */
.text-dim {
  color: #666 !important;
}

/* Animation */
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

/* Responsive Design */
@media (max-width: 960px) {
  .users-header .v-btn {
    font-size: 0.875rem;
  }
}

@media (max-width: 600px) {
  .users-manager {
    padding: 1rem;
  }
  
  .users-header,
  .users-content {
    border-radius: 12px;
  }
}
</style>
          <button @click="showSyncResults = false" class="close-results">×</button>
        </div>
        <div class="sync-results-body">
          <div class="result-item">
            <span class="result-label">⏱️ الوقت:</span>
            <span class="result-value">{{ (syncResults.stats.timeMs / 1000).toFixed(1) }} ث</span>
          </div>
          <div class="result-item">
            <span class="result-label">👥 إضافات:</span>
            <span class="result-value" style="color: #2196f3">{{ syncResults.stats.created }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">🔄 تحديثات:</span>
            <span class="result-value" style="color: #ff9800">{{ syncResults.stats.updated }}</span>
          </div>
          <div v-if="syncResults.stats.failed > 0" class="result-item">
            <span class="result-label">❌ فشل:</span>
            <span class="result-value" style="color: #f44336">{{ syncResults.stats.failed }}</span>
          </div>
        </div>
      </div>
    </transition>

    <!-- بطاقات الإحصائيات -->
    <div class="stats-cards">
      <div v-for="stat in userStats" :key="stat.label" class="stat-card">
        <div class="stat-icon" :style="{ background: stat.color + '20' }">
          <i :class="stat.icon" :style="{ color: stat.color }"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
        <div class="stat-trend" :class="{ up: stat.trend > 0, down: stat.trend < 0 }">
          <i :class="stat.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
          {{ Math.abs(stat.trend) }}%
        </div>
      </div>
    </div>

    <!-- فلاتر البحث -->
    <div class="filters-section">
      <div class="search-wrapper">
        <i class="fa-solid fa-search search-icon"></i>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="بحث باسم المستخدم أو البريد الإلكتروني..."
          class="search-input"
          @input="debouncedSearch"
        />
        <button v-if="searchQuery" class="clear-search" @click="clearSearch">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div class="filters-wrapper">
        <select v-model="roleFilter" class="filter-select">
          <option value="">جميع الأدوار</option>
          <option value="admin">مدير</option>
          <option value="manager">مسؤول</option>
          <option value="editor">محرر</option>
          <option value="user">مستخدم عادي</option>
        </select>

        <select v-model="statusFilter" class="filter-select">
          <option value="">جميع الحالات</option>
          <option value="active">نشط</option>
          <option value="inactive">غير نشط</option>
          <option value="banned">محظور</option>
        </select>

        <select v-model="verifiedFilter" class="filter-select">
          <option value="">جميع حالات التحقق</option>
          <option value="verified">موثق</option>
          <option value="unverified">غير موثق</option>
        </select>

        <button class="btn-filter" @click="showAdvancedFilters = !showAdvancedFilters">
          <i class="fa-solid fa-sliders-h"></i>
          <span>فلاتر متقدمة</span>
        </button>
      </div>
    </div>

    <!-- الفلاتر المتقدمة -->
    <transition name="slide">
      <div v-if="showAdvancedFilters" class="advanced-filters">
        <div class="filter-row">
          <div class="filter-group">
            <label>تاريخ التسجيل من</label>
            <input type="date" v-model="dateFrom" class="filter-input" />
          </div>
          <div class="filter-group">
            <label>إلى</label>
            <input type="date" v-model="dateTo" class="filter-input" />
          </div>
        </div>

        <div class="filter-row">
          <div class="filter-group">
            <label>المدينة</label>
            <input
              type="text"
              v-model="cityFilter"
              placeholder="اسم المدينة"
              class="filter-input"
            />
          </div>
          <div class="filter-group">
            <label>آخر نشاط</label>
            <select v-model="lastActiveFilter" class="filter-select">
              <option value="">الكل</option>
              <option value="today">اليوم</option>
              <option value="week">آخر أسبوع</option>
              <option value="month">آخر شهر</option>
              <option value="inactive">غير نشط</option>
            </select>
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn-apply" @click="applyAdvancedFilters">
            <i class="fa-solid fa-check"></i> تطبيق الفلاتر
          </button>
          <button class="btn-reset" @click="resetAdvancedFilters">
            <i class="fa-solid fa-undo"></i> إعادة تعيين
          </button>
        </div>
      </div>
    </transition>

    <!-- رأس الجدول مع الأدوات -->
    <div class="table-toolbar">
      <div class="table-title">
        <i class="fa-solid fa-list-ul"></i>
        <h3>قائمة المستخدمين</h3>
        <span class="users-count">{{ filteredUsers.length }} مستخدم</span>
      </div>
      <div class="toolbar-actions">
        <button class="toolbar-btn" @click="refreshTable">
          <i class="fa-solid fa-sync-alt"></i>
          <span>تحديث</span>
        </button>
        <button class="toolbar-btn" @click="toggleColumns">
          <i class="fa-solid fa-columns"></i>
          <span>أعمدة</span>
        </button>
        <button class="toolbar-btn" @click="exportUsers">
          <i class="fa-solid fa-file-export"></i>
          <span>تصدير</span>
        </button>
      </div>
    </div>

    <!-- منتقي الأعمدة -->
    <transition name="slide-down">
      <div v-if="showColumnsSelector" class="columns-selector">
        <div class="selector-title">
          <i class="fa-solid fa-eye"></i>
          <span>إظهار/إخفاء الأعمدة</span>
        </div>
        <div class="columns-grid">
          <label v-for="column in columns" :key="column.key" class="column-checkbox">
            <input type="checkbox" v-model="column.visible" />
            <span class="checkbox-custom"></span>
            <span class="checkbox-label">{{ column.label }}</span>
          </label>
        </div>
      </div>
    </transition>

    <!-- جدول المستخدمين -->
    <div class="table-wrapper">
      <table class="users-table">
        <thead>
          <tr>
            <th v-if="columns.find((c) => c.key === 'select').visible" class="select-col">
              <label class="checkbox-container">
                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
                <span class="checkbox-custom"></span>
              </label>
            </th>
            <th
              v-for="column in visibleColumns"
              :key="column.key"
              :class="[column.key + '-col', { sortable: column.sortable }]"
              @click="column.sortable && sortBy(column.key)"
            >
              <div class="th-content">
                <i :class="column.icon"></i>
                <span>{{ column.label }}</span>
                <span v-if="sortKey === column.key" class="sort-indicator">
                  <i :class="sortOrder === 'asc' ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
                </span>
              </div>
            </th>
            <th class="actions-col">الإجراءات</th>
            <th class="erpnext-col">حالة ERPNext</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="user in paginatedUsers"
            :key="user.id"
            class="user-row"
            :class="{
              selected: selectedUsers.includes(user.id),
              [user.status]: true,
            }"
            @click="toggleRowSelection(user.id, $event)"
          >
            <td v-if="columns.find((c) => c.key === 'select').visible" class="select-col">
              <label class="checkbox-container">
                <input
                  type="checkbox"
                  :checked="selectedUsers.includes(user.id)"
                  @change="toggleUserSelection(user.id)"
                  @click.stop
                />
                <span class="checkbox-custom"></span>
              </label>
            </td>

            <td v-if="columns.find((c) => c.key === 'avatar').visible" class="avatar-col">
              <div class="user-avatar-wrapper">
                <img :src="user.avatar" :alt="user.name" class="user-avatar" />
                <span class="online-status" :class="{ online: user.online }"></span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'name').visible" class="name-col">
              <div class="user-info">
                <span class="user-fullname">{{ user.name }}</span>
                <span class="user-username">@{{ user.username }}</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'email').visible" class="email-col">
              <div class="email-info">
                <i class="fa-solid fa-envelope"></i>
                <span>{{ user.email }}</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'role').visible" class="role-col">
              <span class="role-badge" :class="user.role">
                {{ getRoleText(user.role) }}
              </span>
            </td>

            <td v-if="columns.find((c) => c.key === 'status').visible" class="status-col">
              <span class="status-badge" :class="user.status">
                {{ getStatusText(user.status) }}
              </span>
            </td>

            <td v-if="columns.find((c) => c.key === 'verified').visible" class="verified-col">
              <span class="verified-badge" :class="{ verified: user.verified }">
                <i :class="user.verified ? 'fa-solid fa-check-circle' : 'fa-solid fa-times-circle'"></i>
                {{ user.verified ? 'موثق' : 'غير موثق' }}
              </span>
            </td>

            <td v-if="columns.find((c) => c.key === 'joined').visible" class="joined-col">
              <div class="joined-info">
                <i class="far fa-calendar-alt"></i>
                <span>{{ formatDate(user.joined) }}</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'lastActive').visible" class="last-active-col">
              <div class="last-active-info">
                <i class="far fa-clock"></i>
                <span>{{ getLastActiveText(user.lastActive) }}</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'orders').visible" class="orders-col">
              <span class="orders-count">{{ user.ordersCount || 0 }}</span>
            </td>

            <td class="actions-col">
              <div class="action-buttons">
                <button class="action-btn view" @click.stop="viewUser(user)" title="عرض التفاصيل">
                  <i class="fa-solid fa-eye"></i>
                </button>
                <button class="action-btn edit" @click.stop="editUser(user)" title="تعديل">
                  <i class="fa-solid fa-edit"></i>
                </button>
                <button
                  class="action-btn permissions"
                  @click.stop="managePermissions(user)"
                  title="الصلاحيات"
                >
                  <i class="fa-solid fa-key"></i>
                </button>
                <div class="more-actions" @click.stop>
                  <button class="action-btn more" @click="toggleUserMenu(user.id)">
                    <i class="fa-solid fa-ellipsis-v"></i>
                  </button>
                  <transition name="fade">
                    <div v-if="activeUserMenu === user.id" class="action-menu">
                      <button @click="updateUserStatus(user, 'active')">
                        <i class="fa-solid fa-check-circle"></i> <span>تفعيل</span>
                      </button>
                      <button @click="updateUserStatus(user, 'inactive')">
                        <i class="fa-solid fa-pause-circle"></i> <span>تعطيل</span>
                      </button>
                      <button @click="banUser(user)" class="text-danger">
                        <i class="fa-solid fa-ban"></i> <span>حظر</span>
                      </button>
                      <button
                        v-if="user.status === 'banned'"
                        @click="unbanUser(user)"
                        class="text-success"
                      >
                        <i class="fa-solid fa-check-circle"></i> <span>رفع الحظر</span>
                      </button>
                      <div class="menu-divider"></div>
                      <button @click="sendMessage(user)">
                        <i class="fa-solid fa-envelope"></i> <span>إرسال رسالة</span>
                      </button>
                      <button @click="resetPassword(user)">
                        <i class="fa-solid fa-key"></i> <span>إعادة تعيين كلمة المرور</span>
                      </button>
                      <div class="menu-divider"></div>
                      <button @click="confirmDelete(user)" class="text-danger">
                        <i class="fa-solid fa-trash"></i> <span>حذف</span>
                      </button>
                    </div>
                  </transition>
                </div>
              </div>
            </td>

            <td class="erpnext-col">
              <div class="erpnext-status" :class="{ synced: user.erpnextSynced }">
                <i :class="user.erpnextSynced ? 'fa-solid fa-check-circle' : 'fa-solid fa-clock'"></i>
                <span>{{ user.erpnextSynced ? 'متزامن' : 'قيد الانتظار' }}</span>
                <button
                  v-if="!user.erpnextSynced"
                  class="sync-btn-small"
                  @click.stop="syncSingleCustomer(user)"
                  title="مزامنة مع ERPNext"
                >
                  <i class="fa-solid fa-sync-alt"></i>
                </button>
              </div>
            </td>
          </tr>

          <!-- حالة عدم وجود بيانات -->
          <tr v-if="paginatedUsers.length === 0" class="no-data-row">
            <td :colspan="visibleColumns.length + 3" class="no-data">
              <div class="no-data-content">
                <div class="no-data-icon">
                  <i class="fa-solid fa-users"></i>
                  <i class="fa-solid fa-search"></i>
                </div>
                <h4>لا يوجد مستخدمين</h4>
                <p>لم يتم العثور على مستخدمين يطابقون معايير البحث</p>
                <button class="btn-primary" @click="resetFilters">
                  <i class="fa-solid fa-undo"></i> إعادة تعيين الفلاتر
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- شريط الإجراءات السفلية -->
    <div class="table-footer">
      <div v-if="selectedUsers.length > 0" class="selected-info">
        <i class="fa-solid fa-check-circle"></i>
        <span>تم تحديد {{ selectedUsers.length }} مستخدم</span>
        <button class="clear-selection" @click="clearSelection">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div v-if="selectedUsers.length > 0" class="bulk-actions">
        <button class="bulk-btn" @click="bulkUpdateStatus('active')">
          <i class="fa-solid fa-check-circle"></i> <span>تفعيل</span>
        </button>
        <button class="bulk-btn" @click="bulkUpdateStatus('inactive')">
          <i class="fa-solid fa-pause-circle"></i> <span>تعطيل</span>
        </button>
        <button class="bulk-btn danger" @click="bulkUpdateStatus('banned')">
          <i class="fa-solid fa-ban"></i> <span>حظر</span>
        </button>
        <button class="bulk-btn" @click="bulkSendMessage">
          <i class="fa-solid fa-envelope"></i> <span>رسالة جماعية</span>
        </button>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <div class="pagination-info">
          عرض {{ (currentPage - 1) * itemsPerPage + 1 }} -
          {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }}
          من {{ filteredUsers.length }}
        </div>

        <div class="pagination-controls">
          <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
            <i class="fa-solid fa-chevron-right"></i>
          </button>

          <template v-for="page in displayedPages">
            <button
              v-if="page !== '...'"
              :key="page"
              class="page-btn"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
            <span v-else :key="page" class="page-dots">...</span>
          </template>

          <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
            <i class="fa-solid fa-chevron-left"></i>
          </button>
        </div>

        <select v-model="itemsPerPage" class="per-page-select">
          <option :value="5">5 لكل صفحة</option>
          <option :value="10">10 لكل صفحة</option>
          <option :value="25">25 لكل صفحة</option>
          <option :value="50">50 لكل صفحة</option>
          <option :value="100">100 لكل صفحة</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { debounce } from 'lodash';
import CustomerSyncService from '@/integration/services/CustomerSyncService';

// State
const showColumnsSelector = ref(false);
const selectedUsers = ref([]);
const selectAll = ref(false);
const syncingAll = ref(false);
const syncProgress = ref(0);
const syncResults = ref(null);
const showSyncResults = ref(false);
const loading = ref(false);

const columns = ref([
  {
    key: 'select',
    label: 'تحديد',
    visible: true,
    sortable: false,
    icon: 'fa-solid fa-check-square',
  },
  { key: 'avatar', label: '', visible: true, sortable: false, icon: 'fa-solid fa-user-circle' },
  { key: 'name', label: 'الاسم', visible: true, sortable: true, icon: 'fa-solid fa-user' },
  {
    key: 'email',
    label: 'البريد الإلكتروني',
    visible: true,
    sortable: true,
    icon: 'fa-solid fa-envelope',
  },
  { key: 'role', label: 'الدور', visible: true, sortable: true, icon: 'fa-solid fa-shield-alt' },
  { key: 'status', label: 'الحالة', visible: true, sortable: true, icon: 'fa-solid fa-circle' },
  {
    key: 'verified',
    label: 'توثيق',
    visible: true,
    sortable: true,
    icon: 'fa-solid fa-check-circle',
  },
  {
    key: 'joined',
    label: 'تاريخ التسجيل',
    visible: true,
    sortable: true,
    icon: 'far fa-calendar-alt',
  },
  {
    key: 'lastActive',
    label: 'آخر نشاط',
    visible: true,
    sortable: true,
    icon: 'far fa-clock',
  },
  {
    key: 'orders',
    label: 'الطلبات',
    visible: false,
    sortable: true,
    icon: 'fa-solid fa-shopping-cart',
  },
]);

// قائمة المستخدمين - جلب من API
const users = ref([]);

// دالة جلب بيانات المستخدمين
const fetchUsers = async () => {
  try {
    const response = await fetch('/api/users');
    if (response.ok) {
      const data = await response.json();
      users.value = data.map(user => ({
        id: user.id,
        name: user.name,
        username: user.username,
        email: user.email,
        phone: user.phone,
        avatar: user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=d4af37&color=fff`,
        role: user.role,
        status: user.status,
        verified: user.verified || false,
        online: user.online || false,
        joined: user.created_at,
        lastActive: user.last_active,
        city: user.city,
        address: user.address,
        ordersCount: user.orders_count || 0,
        erpnextSynced: user.erpnext_synced || false,
        erpnextCustomerId: user.erpnext_customer_id
      }));
    }
  } catch (error) {
    console.error('Failed to fetch users:', error);
    // Fallback to mock data if API fails
    users.value = [
  {
    id: 1,
    name: 'أحمد محمد',
    username: 'ahmed_m',
    email: 'ahmed@example.com',
    phone: '0555123456',
    avatar: 'https://ui-avatars.com/api/?name=أحمد+محمد&background=d4af37&color=fff',
    role: 'admin',
    status: 'active',
    verified: true,
    online: true,
    joined: '2023-01-15T10:30:00',
    lastActive: '2024-03-18T09:15:00',
    city: 'الرياض',
    address: 'شارع الملك فهد',
    ordersCount: 45,
    erpnextSynced: false,
    erpnextCustomerId: null,
  },
  {
    id: 2,
    name: 'سارة أحمد',
    username: 'sara_a',
    email: 'sara@example.com',
    phone: '0555987654',
    avatar: 'https://ui-avatars.com/api/?name=سارة+أحمد&background=d4af37&color=fff',
    role: 'manager',
    status: 'active',
    verified: true,
    online: true,
    joined: '2023-03-20T14:20:00',
    lastActive: '2024-03-18T08:30:00',
    city: 'جدة',
    address: 'شارع التحلية',
    ordersCount: 23,
  },
  {
    id: 3,
    name: 'محمد علي',
    username: 'mohammed_a',
    email: 'mohammed@example.com',
    phone: '0555777888',
    avatar: 'https://ui-avatars.com/api/?name=محمد+علي&background=d4af37&color=fff',
    role: 'editor',
    status: 'active',
    verified: true,
    online: false,
    joined: '2023-06-10T09:45:00',
    lastActive: '2024-03-17T14:20:00',
    city: 'الدمام',
    address: 'شارع الأمير محمد',
    ordersCount: 12,
  },
  {
    id: 4,
    name: 'فاطمة عمر',
    username: 'fatima_o',
    email: 'fatima@example.com',
    phone: '0555666777',
    avatar: 'https://ui-avatars.com/api/?name=فاطمة+عمر&background=d4af37&color=fff',
    role: 'user',
    status: 'inactive',
    verified: false,
    online: false,
    joined: '2023-09-05T11:15:00',
    lastActive: '2024-03-10T16:45:00',
    city: 'مكة',
    address: 'شارع إبراهيم الخليل',
    ordersCount: 3,
  },
  {
    id: 5,
    name: 'خالد عبدالله',
    username: 'khaled_a',
    email: 'khaled@example.com',
    phone: '0555999000',
    avatar: 'https://ui-avatars.com/api/?name=خالد+عبدالله&background=d4af37&color=fff',
    role: 'user',
    status: 'banned',
    verified: false,
    online: false,
    joined: '2023-12-01T13:30:00',
    lastActive: '2024-03-01T10:00:00',
    city: 'الرياض',
    address: 'شارع العليا',
    ordersCount: 0,
  },
    ];
  }
};

// إحصائيات - جلب من API
const userStats = ref([]);

// دالة جلب إحصائيات المستخدمين
const fetchUserStats = async () => {
  try {
    const response = await fetch('/api/users/statistics');
    if (response.ok) {
      const data = await response.json();
      userStats.value = [
        {
          label: 'إجمالي المستخدمين',
          value: data.total_users?.toLocaleString('ar-SA') || '0',
          icon: 'fa-solid fa-users',
          color: '#d4af37',
          trend: data.total_users_trend || 0,
        },
        {
          label: 'مستخدمين نشطين',
          value: data.active_users?.toLocaleString('ar-SA') || '0',
          icon: 'fa-solid fa-user-check',
          color: '#4CAF50',
          trend: data.active_users_trend || 0,
        },
        {
          label: 'مستخدمين جدد',
          value: data.new_users?.toLocaleString('ar-SA') || '0',
          icon: 'fa-solid fa-user-plus',
          color: '#2196F3',
          trend: data.new_users_trend || 0,
        },
        {
          label: 'مستخدمين محظورين',
          value: data.banned_users?.toLocaleString('ar-SA') || '0',
          icon: 'fa-solid fa-user-slash',
          color: '#f44336',
          trend: data.banned_users_trend || 0,
        },
      ];
    }
  } catch (error) {
    console.error('Failed to fetch user statistics:', error);
    // Fallback to mock data
    userStats.value = [
  {
    label: 'إجمالي المستخدمين',
    value: '1,543',
    icon: 'fa-solid fa-users',
    color: '#d4af37',
    trend: 12,
  },
  {
    label: 'مستخدمين نشطين',
    value: '1,234',
    icon: 'fa-solid fa-user-check',
    color: '#4CAF50',
    trend: 8,
  },
  {
    label: 'مستخدمين جدد',
    value: '156',
    icon: 'fa-solid fa-user-plus',
    color: '#2196F3',
    trend: 15,
  },
  {
    label: 'مستخدمين محظورين',
    value: '23',
    icon: 'fa-solid fa-user-slash',
    color: '#f44336',
    trend: -5,
  },
    ];
  }
};

// جلب البيانات عند تحميل المكون
onMounted(async () => {
  await Promise.all([
    fetchUsers(),
    fetchUserStats()
  ]);
});

// الفلاتر
const searchQuery = ref('');
const roleFilter = ref('');
const statusFilter = ref('');
const verifiedFilter = ref('');
const cityFilter = ref('');
const lastActiveFilter = ref('');
const dateFrom = ref('');
const dateTo = ref('');
const showAdvancedFilters = ref(false);

// الترتيب
const sortKey = ref('joined');
const sortOrder = ref('desc');

// Pagination
const currentPage = ref(1);
const itemsPerPage = ref(10);

// حالة النوافذ
const showUserModal = ref(false);
const showPermissionsModal = ref(false);
const showMessageModal = ref(false);
const showDeleteModal = ref(false);
const showEditModal = ref(false);
const showBanModal = ref(false);
const selectedUser = ref(null);
const userToDelete = ref(null);
const userToEdit = ref(null);
const userToBan = ref(null);
const activeUserMenu = ref(null);
const isEditing = ref(false);

// بيانات الحظر
const banReason = ref('');
const banDuration = ref('permanent');
const deletePermanently = ref(false);

// نموذج المستخدم
const userForm = ref({
  name: '',
  username: '',
  email: '',
  phone: '',
  role: 'user',
  status: 'active',
  verified: false,
  city: '',
  address: '',
  password: '',
  passwordConfirm: '',
});

// نموذج التعديل
const editForm = ref({
  name: '',
  username: '',
  email: '',
  phone: '',
  role: '',
  status: '',
  verified: false,
  city: '',
  address: '',
});

// Computed
const visibleColumns = computed(() => columns.value.filter((c) => c.visible && c.key !== 'select'));

const filteredUsers = computed(() => {
  return users.value.filter((user) => {
    const matchesSearch =
      !searchQuery.value ||
      user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.username.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesRole = !roleFilter.value || user.role === roleFilter.value;
    const matchesStatus = !statusFilter.value || user.status === statusFilter.value;
    const matchesVerified =
      !verifiedFilter.value ||
      (verifiedFilter.value === 'verified' ? user.verified : !user.verified);
    const matchesCity = !cityFilter.value || user.city?.includes(cityFilter.value);

    return matchesSearch && matchesRole && matchesStatus && matchesVerified && matchesCity;
  });
});

const sortedUsers = computed(() => {
  const sorted = [...filteredUsers.value];
  sorted.sort((a, b) => {
    let aVal = a[sortKey.value];
    let bVal = b[sortKey.value];

    if (sortKey.value === 'joined' || sortKey.value === 'lastActive') {
      return sortOrder.value === 'asc'
        ? new Date(aVal) - new Date(bVal)
        : new Date(bVal) - new Date(aVal);
    }

    if (sortKey.value === 'orders') {
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal;
    }

    aVal = String(aVal).toLowerCase();
    bVal = String(bVal).toLowerCase();

    return sortOrder.value === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  });
  return sorted;
});

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedUsers.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage.value));

const displayedPages = computed(() => {
  const pages = [];
  const maxDisplayed = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxDisplayed / 2));
  let end = Math.min(totalPages.value, start + maxDisplayed - 1);

  if (end - start + 1 < maxDisplayed) {
    start = Math.max(1, end - maxDisplayed + 1);
  }

  for (let i = start; i <= end; i++) pages.push(i);
  return pages;
});

// Methods
const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-SA', { year: 'numeric', month: 'short', day: 'numeric' });
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
  };
  return map[status] || status;
};

const refreshTable = () => {
  currentPage.value = 1;
};

const toggleColumns = () => {
  showColumnsSelector.value = !showColumnsSelector.value;
};

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedUsers.value = paginatedUsers.value.map((u) => u.id);
  } else {
    selectedUsers.value = [];
  }
};

const toggleUserSelection = (userId) => {
  const index = selectedUsers.value.indexOf(userId);
  if (index === -1) {
    selectedUsers.value.push(userId);
  } else {
    selectedUsers.value.splice(index, 1);
  }
  selectAll.value = selectedUsers.value.length === paginatedUsers.value.length;
};

const toggleRowSelection = (userId, event) => {
  if (event.target.type === 'checkbox' || event.target.closest('button')) return;
  toggleUserSelection(userId);
};

const clearSelection = () => {
  selectedUsers.value = [];
  selectAll.value = false;
};

const bulkUpdateStatus = (status) => {
  selectedUsers.value.forEach((userId) => {
    const user = users.value.find((u) => u.id === userId);
    if (user) user.status = status;
  });
  clearSelection();
};

const bulkSendMessage = () => {
  console.log('Sending message to:', selectedUsers.value);
  alert('تم فتح نافذة المراسلة الجماعية');
};

const resetFilters = () => {
  searchQuery.value = '';
  roleFilter.value = '';
  statusFilter.value = '';
  verifiedFilter.value = '';
  cityFilter.value = '';
  lastActiveFilter.value = '';
  dateFrom.value = '';
  dateTo.value = '';
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const debouncedSearch = debounce(() => {
  currentPage.value = 1;
}, 300);

const clearSearch = () => {
  searchQuery.value = '';
  currentPage.value = 1;
};

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const applyAdvancedFilters = () => {
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const resetAdvancedFilters = () => {
  cityFilter.value = '';
  lastActiveFilter.value = '';
  dateFrom.value = '';
  dateTo.value = '';
};

const openUserModal = () => {
  isEditing.value = false;
  showUserModal.value = true;
};

const viewUser = (user) => {
  selectedUser.value = user;
  console.log('View user:', user);
};

const editUser = (user) => {
  userToEdit.value = user;
  editForm.value = {
    name: user.name,
    username: user.username,
    email: user.email,
    phone: user.phone || '',
    role: user.role,
    status: user.status,
    verified: user.verified,
    city: user.city || '',
    address: user.address || '',
  };
  showEditModal.value = true;
};

const managePermissions = (user) => {
  selectedUser.value = user;
  showPermissionsModal.value = true;
};

const toggleUserMenu = (userId) => {
  activeUserMenu.value = activeUserMenu.value === userId ? null : userId;
};

const updateUserStatus = (user, status) => {
  user.status = status;
  activeUserMenu.value = null;
};

const banUser = (user) => {
  userToBan.value = user;
  showBanModal.value = true;
};

const unbanUser = (user) => {
  if (confirm(`هل أنت متأكد من إلغاء حظر المستخدم ${user.name}؟`)) {
    user.status = 'active';
  }
};

const sendMessage = (user) => {
  console.log('Send message to:', user);
};

const resetPassword = (user) => {
  alert(`تم إرسال رابط إعادة تعيين كلمة المرور إلى ${user.email}`);
};

const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

const syncSingleCustomer = async (user) => {
  try {
    loading.value = true;
    const result = await CustomerSyncService.syncSingleCustomer(user.id);
    if (result.success) {
      user.erpnextSynced = true;
    }
  } catch (error) {
    console.error('Sync error:', error);
  } finally {
    loading.value = false;
  }
};

const syncAllCustomers = async () => {
  if (syncingAll.value) return;
  if (!confirm('هل أنت متأكد من مزامنة جميع العملاء مع ERPNext؟')) return;

  syncingAll.value = true;
  try {
    const result = await CustomerSyncService.syncAllCustomers((progress) => {
      syncProgress.value = progress;
    });
    syncResults.value = result;
    showSyncResults.value = true;
  } catch (error) {
    console.error('Sync error:', error);
  } finally {
    syncingAll.value = false;
  }
};

const exportUsers = () => {
  alert('تم تصدير بيانات المستخدمين بنجاح');
};

// Watchers
watch(searchQuery, () => {
  currentPage.value = 1;
});
watch(roleFilter, () => {
  currentPage.value = 1;
});
watch(statusFilter, () => {
  currentPage.value = 1;
});
watch(verifiedFilter, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
@import '@/assets/theme.css';

.users-manager {
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

.btn-primary,
.btn-export {
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
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.btn-export {
  background: var(--bg-card);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-primary:hover,
.btn-export:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== بطاقات الإحصائيات ===== */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
  animation: rotate 10s linear infinite;
  pointer-events: none;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  position: relative;
  z-index: 1;
}

.stat-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.stat-trend {
  position: absolute;
  top: 15px;
  left: 15px;
  padding: 4px 8px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
}

.stat-trend.up {
  color: var(--success);
}
.stat-trend.down {
  color: var(--danger);
}

/* ===== شريط الفلاتر ===== */
.filters-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-light);
}

.search-wrapper {
  position: relative;
  margin-bottom: 15px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 15px 45px 15px 15px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  transition: var(--transition-smooth);
}

.search-input:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.clear-search {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  transition: color 0.3s;
}

.clear-search:hover {
  color: var(--danger);
}

.filters-wrapper {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  flex: 1;
  min-width: 150px;
  padding: 12px 15px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 0.95rem;
  cursor: pointer;
  transition: var(--transition-smooth);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23d4af37' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 15px center;
  padding-left: 40px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.btn-filter {
  padding: 12px 25px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--gold-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.btn-filter:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

/* ===== الفلاتر المتقدمة ===== */
.advanced-filters {
  margin-top: 20px;
  padding: 20px;
  background: var(--bg-primary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  color: var(--text-dim);
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.filter-input {
  padding: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
}

.filter-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-apply,
.btn-reset {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: var(--transition-smooth);
}

.btn-apply {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-reset {
  background: var(--bg-card);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-apply:hover,
.btn-reset:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

/* ===== رأس الجدول ===== */
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-title i {
  color: var(--gold-1);
  font-size: 1.3rem;
}

.table-title h3 {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
}

.users-count {
  background: linear-gradient(135deg, var(--gold-1) 0%, var(--gold-light) 100%);
  color: var(--bg-deep);
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 700;
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.toolbar-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  border-color: var(--gold-1);
  transform: translateY(-2px);
}

/* ===== منتقي الأعمدة ===== */
.columns-selector {
  padding: 20px;
  background: var(--bg-primary);
  border-radius: 16px;
  margin: 0 20px 20px 20px;
  border: 1px solid var(--border-light);
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--gold-1);
  margin-bottom: 15px;
  font-weight: 600;
}

.columns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.column-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: color 0.3s;
}

.column-checkbox:hover {
  color: var(--gold-1);
}

.column-checkbox input[type='checkbox'] {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-light);
  border-radius: 5px;
  position: relative;
  transition: var(--transition-smooth);
}

.column-checkbox input:checked + .checkbox-custom {
  background: var(--gold-gradient);
  border-color: transparent;
}

.column-checkbox input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--bg-deep);
  font-size: 0.7rem;
  font-weight: 700;
}

/* ===== الجدول الرئيسي ===== */
.table-wrapper {
  background: var(--bg-card);
  border-radius: 20px;
  border: 1px solid var(--border-light);
  overflow-x: auto;
  margin-bottom: 20px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px;
}

/* رأس الجدول */
.users-table thead tr {
  background: var(--bg-sidebar);
  border-bottom: 2px solid var(--gold-1);
}

.users-table th {
  padding: 16px 12px;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  text-align: right;
  cursor: pointer;
  transition: background 0.3s;
}

.users-table th:hover {
  background: var(--bg-primary);
}

.th-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.th-content i {
  color: var(--gold-1);
  font-size: 0.9rem;
}

.sort-indicator i {
  color: var(--gold-1);
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* عرض الأعمدة */
.select-col {
  width: 50px;
  text-align: center;
}
.avatar-col {
  width: 60px;
}
.name-col {
  min-width: 150px;
}
.email-col {
  min-width: 200px;
}
.role-col {
  width: 100px;
}
.status-col {
  width: 100px;
}
.verified-col {
  width: 100px;
}
.joined-col {
  width: 120px;
}
.last-active-col {
  width: 120px;
}
.orders-col {
  width: 80px;
  text-align: center;
}
.actions-col {
  width: 150px;
}

/* صفوف الجدول */
.users-table tbody tr {
  border-bottom: 1px solid var(--border-light);
  transition: var(--transition-smooth);
  cursor: pointer;
}

.users-table tbody tr:hover {
  background: var(--bg-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.users-table tbody tr.selected {
  background: linear-gradient(135deg, var(--bg-card), rgba(212, 175, 55, 0.15));
  border-right: 4px solid var(--gold-1);
}

.users-table tbody tr.active {
  border-right: 4px solid #4caf50;
}
.users-table tbody tr.inactive {
  border-right: 4px solid #ff9800;
}
.users-table tbody tr.banned {
  border-right: 4px solid #f44336;
  opacity: 0.8;
}

.users-table td {
  padding: 15px 12px;
  color: var(--text-secondary);
  vertical-align: middle;
}

/* عمود الاختيار */
.checkbox-container {
  display: inline-block;
  cursor: pointer;
}

.checkbox-container input {
  display: none;
}

/* عمود الصورة */
.user-avatar-wrapper {
  position: relative;
  width: 40px;
  height: 40px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--gold-1);
  transition: var(--transition-smooth);
}

.user-row:hover .user-avatar {
  transform: scale(1.1);
}

.online-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
  border: 2px solid var(--bg-card);
}

.online-status.online {
  background: #4caf50;
  box-shadow: 0 0 10px #4caf50;
}

/* عمود الاسم */
.user-info {
  display: flex;
  flex-direction: column;
}

.user-fullname {
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 3px;
}

.user-username {
  color: var(--gold-1);
  font-size: 0.8rem;
}

/* عمود البريد */
.email-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.email-info i {
  color: var(--gold-1);
  font-size: 0.9rem;
  width: 16px;
}

/* عمود الدور */
.role-badge {
  padding: 5px 12px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.role-badge.admin {
  background: rgba(212, 175, 55, 0.2);
  color: var(--gold-1);
  border: 1px solid var(--gold-1);
}

.role-badge.manager {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid #2196f3;
}

.role-badge.editor {
  background: rgba(156, 39, 176, 0.2);
  color: #9c27b0;
  border: 1px solid #9c27b0;
}

.role-badge.user {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}

/* عمود الحالة */
.status-badge {
  padding: 5px 12px;
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

.status-badge.inactive {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
  border: 1px solid #ff9800;
}

.status-badge.banned {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid #f44336;
}

/* عمود التوثيق */
.verified-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
}

.verified-badge.verified i {
  color: #4caf50;
}

.verified-badge i {
  color: #f44336;
}

/* عمود تاريخ التسجيل */
.joined-info,
.last-active-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.joined-info i,
.last-active-info i {
  color: var(--gold-1);
  font-size: 0.9rem;
  width: 16px;
}

/* عمود عدد الطلبات */
.orders-col {
  font-weight: 600;
  color: white;
}

/* أزرار الإجراءات */
.action-buttons {
  position: relative;
  display: flex;
  gap: 5px;
}

.action-btn {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  border: none;
  background: var(--bg-primary);
  color: var(--text-dim);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
  border-radius: 50%;
}

.action-btn:hover::before {
  width: 70px;
  height: 70px;
}

.action-btn.view:hover {
  background: #2196f3;
  color: white;
}
.action-btn.edit:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}
.action-btn.permissions:hover {
  background: #9c27b0;
  color: white;
}
.action-btn.more:hover {
  background: #ff9800;
  color: white;
}

.more-actions {
  position: relative;
}

.action-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 8px;
  box-shadow: var(--shadow-lg), var(--shadow-gold);
  z-index: 100;
  animation: menuSlide 0.2s ease;
}

@keyframes menuSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.action-menu button {
  width: 100%;
  padding: 10px 12px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  text-align: right;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.action-menu button:hover {
  background: var(--bg-primary);
  color: var(--gold-1);
}

.action-menu .text-danger:hover {
  color: var(--danger);
}

.action-menu .text-success:hover {
  color: #4caf50;
}

.menu-divider {
  height: 1px;
  background: var(--border-light);
  margin: 8px 0;
}

/* شريط الإجراءات السفلية */
.table-footer {
  padding: 20px;
  border-top: 1px solid var(--border-light);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.selected-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 15px;
  background: var(--bg-primary);
  border-radius: 40px;
  color: var(--gold-1);
}

.selected-info i {
  font-size: 1.1rem;
}

.clear-selection {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-dim);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.clear-selection:hover {
  background: var(--danger);
  color: white;
  border-color: transparent;
}

.bulk-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.bulk-btn {
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 40px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  gap: 8px;
}

.bulk-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  border-color: var(--gold-1);
}

.bulk-btn.danger:hover {
  background: var(--danger);
  color: white;
  border-color: transparent;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.pagination-info {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid var(--border-light);
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.page-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-dots {
  color: var(--text-dim);
  padding: 0 5px;
}

.per-page-select {
  padding: 8px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23d4af37' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 10px center;
  appearance: none;
  padding-left: 35px;
}

/* حالة عدم وجود بيانات */
.no-data-row td {
  padding: 60px 20px;
}

.no-data-content {
  text-align: center;
  color: var(--text-dim);
}

.no-data-icon {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.3));
}

.no-data-icon i {
  position: absolute;
  font-size: 4rem;
  color: var(--border-light);
}

.no-data-icon i:first-child {
  top: 0;
  left: 0;
  animation: floatIcon 3s ease infinite;
}

.no-data-icon i:last-child {
  bottom: 0;
  right: 0;
  font-size: 2rem;
  animation: floatIcon 3s ease infinite reverse;
}

@keyframes floatIcon {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(-10px, -10px);
  }
}

.no-data-content h4 {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.no-data-content p {
  margin-bottom: 20px;
}

/* ===== استجابة للشاشات الصغيرة ===== */
@media (max-width: 768px) {
  .sync-progress-container {
    width: 280px;
    bottom: 20px;
    right: 20px;
  }

  .sync-results-card {
    width: 280px;
    bottom: 80px;
    right: 20px;
  }

  .btn-sync-all span {
    display: none;
  }

  .btn-sync-all {
    padding: 12px 16px;
    border-radius: 50%;
  }

  .btn-sync-all i {
    font-size: 1.2rem;
    margin: 0;
  }
}

@media (max-width: 480px) {
  .erpnext-status span {
    display: none;
  }

  .erpnext-col {
    min-width: 60px;
  }

  .erpnext-status {
    padding: 6px;
    justify-content: center;
  }

  .sync-btn-small {
    width: 24px;
    height: 24px;
  }

  .sync-btn-small i {
    font-size: 0.8rem;
  }
}
/* أيقونة متزامن مع تأثير نبض */
.erpnext-status.synced i {
  animation: softPulse 2s infinite;
}

@keyframes softPulse {
  0%,
  100% {
    opacity: 1;
    filter: drop-shadow(0 0 5px rgba(76, 175, 80, 0.3));
  }
  50% {
    opacity: 0.8;
    filter: drop-shadow(0 0 15px rgba(76, 175, 80, 0.8));
  }
}

/* أيقونة قيد الانتظار مع تأثير دوران خفيف */
.erpnext-status i.fa-clock {
  animation: gentleRotate 3s infinite;
}

@keyframes gentleRotate {
  0%,
  100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(5deg);
  }
  75% {
    transform: rotate(-5deg);
  }
}

/* زر المزامنة مع تأثير توهج */
.sync-btn-small {
  position: relative;
}

.sync-btn-small::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gold-gradient);
  border-radius: 50%;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s;
}

.sync-btn-small:hover::after {
  opacity: 0.5;
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
