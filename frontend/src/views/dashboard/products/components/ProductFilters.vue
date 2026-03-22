<template>
  <div class="filters-card">
    <div class="search-bar">
      <i class="fa-solid fa-search search-icon"></i>
      <input
        :value="searchQuery"
        type="text"
        placeholder="البحث باسم المنتج، SKU، أو الوصف..."
        @input="$emit('update:searchQuery', $event.target.value)"
      />
      <button v-if="searchQuery" class="clear-search" @click="$emit('clear-search')">
        <i class="fa-solid fa-times"></i>
      </button>
    </div>

    <div class="quick-filters">
      <select 
        :value="categoryFilter" 
        class="filter-select"
        @change="$emit('update:categoryFilter', $event.target.value)"
      >
        <option value="">جميع التصنيفات</option>
        <option v-for="cat in categories" :key="cat.value" :value="cat.value">
          {{ cat.label }}
        </option>
      </select>

      <select 
        :value="stockFilter" 
        class="filter-select"
        @change="$emit('update:stockFilter', $event.target.value)"
      >
        <option value="">جميع مستويات المخزون</option>
        <option value="in-stock">متوفر</option>
        <option value="low-stock">منخفض</option>
        <option value="out-stock">نفد</option>
      </select>

      <div class="view-toggle">
        <button 
          :class="{ active: viewMode === 'grid' }" 
          @click="$emit('update:viewMode', 'grid')"
          title="عرض شبكي"
        >
          <i class="fa-solid fa-th-large"></i>
        </button>
        <button 
          :class="{ active: viewMode === 'table' }" 
          @click="$emit('update:viewMode', 'table')"
          title="عرض جدول"
        >
          <i class="fa-solid fa-list"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  searchQuery: { type: String, default: '' },
  categoryFilter: { type: String, default: '' },
  stockFilter: { type: String, default: '' },
  viewMode: { type: String, default: 'grid' },
  categories: { type: Array, required: true }
});

defineEmits([
  'update:searchQuery', 
  'update:categoryFilter', 
  'update:stockFilter', 
  'update:viewMode',
  'clear-search'
]);
</script>

<style scoped>
.filters-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: right;
}

.search-bar { position: relative; }
.search-icon { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); color: #adb5bd; }
.search-bar input { 
  width: 100%; 
  padding: 12px 48px 12px 16px; 
  border-radius: 12px; 
  border: 1px solid #dee2e6; 
  text-align: right;
}

.clear-search {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  color: #adb5bd;
  cursor: pointer;
}

.quick-filters { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.filter-select { padding: 8px 16px; border-radius: 10px; border: 1px solid #dee2e6; background: white; }

.view-toggle { display: flex; background: #f8f9fa; padding: 4px; border-radius: 10px; margin-right: auto; }
.view-toggle button {
  width: 36px; height: 36px; border: none; background: none; border-radius: 8px; cursor: pointer; color: #6c757d;
  display: flex; align-items: center; justify-content: center;
}
.view-toggle button.active { background: white; color: #d4af37; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
</style>
