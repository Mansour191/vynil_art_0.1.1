<template>
  <div class="currency-selector" ref="el">
    <button class="currency-btn" @click="toggleDropdown">
      <i class="fa-solid fa-coins"></i>
      <span>{{ currentCurrency.symbol }}</span>
    </button>

    <div class="currency-dropdown" v-if="showDropdown">
      <div
        v-for="currency in currencies"
        :key="currency.code"
        class="currency-option"
        :class="{ active: currentCode === currency.code }"
        @click="selectCurrency(currency.code)"
      >
        <span class="currency-symbol">{{ currency.symbol }}</span>
        <span class="currency-name">{{ currency.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import CurrencyService from '@/integration/services/CurrencyService';

const router = useRouter();
const el = ref(null);

// State
const showDropdown = ref(false);
const currentCode = ref(CurrencyService.currentCurrency);
const currencies = [
  { code: 'DZD', symbol: 'د.ج', name: 'الدينار الجزائري' },
  { code: 'EUR', symbol: 'يورو', name: 'اليورو الأوروبي' },
  { code: 'USD', symbol: 'دولار', name: 'الدولار الأمريكي' },
];

// Computed
const currentCurrency = computed(() => CurrencyService.getCurrentCurrency());

// Methods
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const selectCurrency = (code) => {
  CurrencyService.setCurrency(code);
  currentCode.value = code;
  showDropdown.value = false;

  // إعادة تحميل الصفحة الحالية لتحديث الأرقام
  router.go();
};

const handleClickOutside = (event) => {
  if (el.value && !el.value.contains(event.target)) {
    showDropdown.value = false;
  }
};

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.currency-selector {
  position: relative;
}

.currency-btn {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--gold-1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.currency-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.currency-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 150px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  margin-top: 5px;
  box-shadow: var(--shadow-lg);
  z-index: 100;
  overflow: hidden;
}

.currency-option {
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.currency-option:hover {
  background: var(--bg-primary);
  color: var(--gold-1);
}

.currency-option.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.currency-symbol {
  font-weight: 700;
  width: 30px;
}

.currency-name {
  flex: 1;
  font-size: 0.9rem;
}
</style>
