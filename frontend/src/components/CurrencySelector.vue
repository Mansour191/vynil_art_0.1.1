<template>
  <v-menu
    v-model="showDropdown"
    location="bottom end"
    offset="10"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        prepend-icon="mdi-cash"
        variant="outlined"
        color="primary"
        class="currency-btn"
      >
        {{ currentCurrency.symbol }}
      </v-btn>
    </template>
    
    <v-card min-width="200" elevation="8">
      <v-list density="compact">
        <v-list-item
          v-for="currency in currencies"
          :key="currency.code"
          :class="{ 'bg-primary': currentCode === currency.code }"
          @click="selectCurrency(currency.code)"
        >
          <template v-slot:prepend>
            <span class="currency-symbol">{{ currency.symbol }}</span>
          </template>
          <v-list-item-title class="currency-name">{{ currency.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import CurrencyService from '@/integration/services/CurrencyService';

const router = useRouter();

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
const selectCurrency = (code) => {
  CurrencyService.setCurrency(code);
  currentCode.value = code;
  showDropdown.value = false;
  
  // إعادة تحميل الصفحة الحالية لتحديث الأرقام
  router.go();
};
</script>

