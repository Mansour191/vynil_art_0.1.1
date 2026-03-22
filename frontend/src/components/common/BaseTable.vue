<template>
  <div class="base-table-wrapper" :class="{ 'is-loading': loading }">
    <!-- Desktop View -->
    <div class="table-responsive d-none d-md-block">
      <table class="table custom-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key" :style="{ width: col.width }">
              <div class="th-content" @click="col.sortable && handleSort(col.key)">
                {{ col.label }}
                <i v-if="col.sortable" class="fas ms-1" :class="getSortIcon(col.key)"></i>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="items.length > 0">
            <tr v-for="(item, index) in items" :key="item.id || index">
              <td v-for="col in columns" :key="col.key">
                <slot :name="`cell(${col.key})`" :item="item" :index="index">
                  {{ item[col.key] }}
                </slot>
              </td>
            </tr>
          </template>
          <tr v-else>
            <td :colspan="columns.length" class="text-center py-5">
              <slot name="empty">
                <div class="empty-state">
                  <i class="fa-solid fa-folder-open fa-3x mb-3 opacity-20"></i>
                  <p class="text-muted">{{ emptyText || $t('noDataFound') }}</p>
                </div>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile View (Cards) -->
    <div class="mobile-table-view d-md-none">
      <template v-if="items.length > 0">
        <div 
          v-for="(item, index) in items" 
          :key="item.id || index" 
          class="mobile-row-card card border-0 shadow-sm mb-3"
        >
          <div class="card-body p-3">
            <div 
              v-for="col in columns" 
              :key="col.key" 
              class="mobile-cell d-flex justify-content-between align-items-start mb-2"
            >
              <span class="mobile-label text-muted small font-weight-bold">{{ col.label }}</span>
              <div class="mobile-value">
                <slot :name="`cell(${col.key})`" :item="item" :index="index">
                  {{ item[col.key] }}
                </slot>
              </div>
            </div>
          </div>
        </div>
      </template>
      <div v-else class="text-center py-5">
        <i class="fa-solid fa-folder-open fa-3x mb-3 opacity-20"></i>
        <p class="text-muted">{{ emptyText || $t('noDataFound') }}</p>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="table-loading-overlay">
      <div class="spinner-border text-gold" role="status"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  items: { type: Array, required: true },
  columns: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: '' }
});

const emit = defineEmits(['sort']);

const sortKey = ref('');
const sortOrder = ref('asc');

const handleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
  emit('sort', { key: sortKey.value, order: sortOrder.value });
};

const getSortIcon = (key) => {
  if (sortKey.value !== key) return 'fa-sort opacity-30';
  return sortOrder.value === 'asc' ? 'fa-sort-up text-gold' : 'fa-sort-down text-gold';
};
</script>

<style scoped>
.base-table-wrapper {
  position: relative;
  min-height: 200px;
}

.custom-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
  margin-top: -10px;
}

.custom-table thead th {
  background: transparent;
  border: none;
  color: var(--text-muted, #888);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  padding: 15px 20px;
  letter-spacing: 1px;
}

.th-content {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.custom-table tbody tr {
  background: var(--bg-surface, #fff);
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

.custom-table tbody tr:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  background: var(--bg-card);
}

.custom-table tbody td {
  padding: 20px;
  border: none;
  vertical-align: middle;
  font-size: 0.9rem;
}

.custom-table tbody tr td:first-child {
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

.custom-table tbody tr td:last-child {
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

[dir="rtl"] .custom-table tbody tr td:first-child {
  border-radius: 0 15px 15px 0;
}

[dir="rtl"] .custom-table tbody tr td:last-child {
  border-radius: 15px 0 0 15px;
}

/* Mobile View */
.mobile-row-card {
  border-radius: 15px;
  background: var(--bg-surface);
}

.mobile-label {
  min-width: 100px;
}

.mobile-value {
  text-align: right;
  flex: 1;
}

[dir="rtl"] .mobile-value {
  text-align: left;
}

/* Loading Overlay */
.table-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.1);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  border-radius: 15px;
}

.text-gold {
  color: var(--gold-primary, #d4af37);
}
</style>
