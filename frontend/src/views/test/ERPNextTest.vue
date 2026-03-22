<!-- src/views/ERPNextTest.vue -->
<template>
  <div class="erpnext-test" style="padding: 30px; max-width: 800px; margin: 0 auto">
    <h1>🧪 اختبار ERPNext</h1>

    <div style="margin: 20px 0; display: flex; gap: 10px">
      <button
        @click="testERPNext"
        style="
          padding: 10px 20px;
          background: #d4af37;
          color: black;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        "
      >
        🔌 اختبار الاتصال
      </button>
      <button
        @click="getProducts"
        style="
          padding: 10px 20px;
          background: #2196f3;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        "
      >
        📦 عرض المنتجات
      </button>
      <button
        @click="createTestProduct"
        style="
          padding: 10px 20px;
          background: #4caf50;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        "
      >
        ➕ إضافة منتج تجريبي
      </button>
    </div>

    <div v-if="loading" style="text-align: center; padding: 20px">جاري التحميل...</div>

    <div
      v-if="result"
      style="
        margin-top: 20px;
        padding: 20px;
        background: #1a1a1a;
        color: #fff;
        border-radius: 12px;
        overflow-x: auto;
      "
    >
      <h3 style="color: #d4af37; margin-bottom: 10px">النتيجة:</h3>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
import { ERPNextService } from '@/integration';

export default {
  name: 'ERPNextTest',
  data() {
    return {
      result: null,
      loading: false,
    };
  },
  methods: {
    async testERPNext() {
      this.loading = true;
      this.result = await ERPNextService.testConnection();
      this.loading = false;
    },
    async getProducts() {
      this.loading = true;
      this.result = await ERPNextService.getProducts();
      this.loading = false;
    },
    async createTestProduct() {
      this.loading = true;
      this.result = await ERPNextService.createProduct({
        name: 'منتج تجريبي',
        sku: `TEST-${Date.now()}`,
        price: 99,
        category: 'walls',
        description: 'هذا منتج للتجربة',
      });
      this.loading = false;
    },
  },
};
</script>
