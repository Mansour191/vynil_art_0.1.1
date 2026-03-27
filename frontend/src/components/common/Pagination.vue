<template>
  <div class="pagination">
    <div class="pagination-info">
      عرض {{ (currentPage - 1) * itemsPerPage + 1 }} -
      {{ Math.min(currentPage * itemsPerPage, totalItems) }}
      من {{ totalItems }}
    </div>

    <div class="pagination-controls">
      <button class="page-btn" :disabled="currentPage === 1" @click="$emit('update:currentPage', currentPage - 1)">
        <i class="fa-solid fa-chevron-right"></i>
      </button>

      <template v-for="page in visiblePages" :key="page">
        <button 
          v-if="page === currentPage" 
          class="page-active"
        >
          {{ page }}
        </button>
        <button 
          v-else-if="page !== '...'" 
          class="page-number"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        <span v-else class="page-dots">...</span>
      </template>

      <button class="page-btn" :disabled="currentPage === totalPages" @click="$emit('update:currentPage', currentPage + 1)">
        <i class="fa-solid fa-chevron-left"></i>
      </button>
    </div>

    <select :value="itemsPerPage" class="per-page-select" @change="$emit('update:itemsPerPage', parseInt($event.target.value))">
      <option v-for="size in pageSizes" :key="size" :value="size">{{ size }} لكل صفحة</option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentPage: { type: Number, required: true },
  itemsPerPage: { type: Number, required: true },
  totalItems: { type: Number, required: true },
  pageSizes: { type: Array, default: () => [5, 10, 25, 50, 100] },
});

const emit = defineEmits(['update:currentPage', 'update:itemsPerPage']);

const totalPages = computed(() => Math.ceil(props.totalItems / props.itemsPerPage));

const displayedPages = computed(() => {
  const total = totalPages.value;
  const current = props.currentPage;
  const delta = 2;
  const left = current - delta;
  const right = current + delta + 1;
  const range = [];
  const rangeWithDots = [];
  let l;

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= left && i < right)) {
      range.push(i);
    }
  }

  for (const i of range) {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1);
      } else if (i - l !== 1) {
        rangeWithDots.push('...');
      }
    }
    rangeWithDots.push(i);
    l = i;
  }

  return rangeWithDots;
});
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.pagination-info {
  font-size: 14px;
  color: #6c757d;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #dee2e6;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
  color: #1a1a2e;
}

.page-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #d4af37;
  color: #d4af37;
}

.page-btn.active {
  background: #d4af37;
  border-color: #d4af37;
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-dots {
  color: #6c757d;
  padding: 0 4px;
}

.per-page-select {
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  color: #1a1a2e;
  background: white;
  cursor: pointer;
}
</style>
