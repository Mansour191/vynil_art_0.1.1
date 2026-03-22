<template>
  <div
    class="product-sync-test"
    style="padding: 30px; max-width: 1200px; margin: 0 auto; direction: rtl"
  >
    <h1 style="color: #d4af37; text-align: center">🔄 اختبار مزامنة المنتجات مع ERPNext</h1>

    <!-- أزرار التحكم -->
    <div style="margin: 20px 0; display: flex; gap: 10px; flex-wrap: wrap">
      <button
        @click="runSync"
        :disabled="loading"
        style="
          padding: 12px 24px;
          background: #d4af37;
          color: black;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: bold;
        "
      >
        {{ loading ? 'جاري المزامنة...' : '🚀 بدء المزامنة' }}
      </button>

      <button
        @click="compareOnly"
        :disabled="loading"
        style="
          padding: 12px 24px;
          background: #2196f3;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: bold;
        "
      >
        📊 مقارنة فقط
      </button>

      <button
        @click="getStatus"
        style="
          padding: 12px 24px;
          background: #4caf50;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: bold;
        "
      >
        📈 حالة المزامنة
      </button>
    </div>

    <!-- حالة المزامنة -->
    <div
      v-if="status"
      class="status-card"
      style="
        background: #1a1a1a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
      "
    >
      <h3 style="color: #d4af37">📊 حالة المزامنة</h3>
      <p>🔄 جاري المزامنة: {{ status.inProgress ? 'نعم' : 'لا' }}</p>
      <p>⏰ آخر مزامنة: {{ status.lastSync || 'لم تتم بعد' }}</p>
    </div>

    <!-- نتائج المقارنة -->
    <div
      v-if="comparison"
      class="comparison-results"
      style="
        background: #1a1a1a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
      "
    >
      <h3 style="color: #d4af37">📋 نتائج المقارنة</h3>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0">
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #2196f3">{{ comparison.toCreate.length }}</div>
          <div style="color: #aaa">للإضافة</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #ff9800">{{ comparison.toUpdate.length }}</div>
          <div style="color: #aaa">للتحديث</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #4caf50">{{ comparison.alreadySynced.length }}</div>
          <div style="color: #aaa">متزامن</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #f44336">{{ comparison.toDelete.length }}</div>
          <div style="color: #aaa">للحذف</div>
        </div>
      </div>

      <!-- تفاصيل المنتجات للإضافة -->
      <div v-if="comparison.toCreate.length > 0" style="margin-top: 20px">
        <h4 style="color: #2196f3">📦 منتجات جديدة للإضافة ({{ comparison.toCreate.length }})</h4>
        <div
          style="
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 10px;
          "
        >
          <div
            v-for="product in comparison.toCreate"
            :key="product.id"
            style="background: #2a2a2a; padding: 10px; border-radius: 8px"
          >
            <strong>{{ product.name }}</strong>
            <div style="color: #aaa; font-size: 12px">السعر: {{ product.price }} ر.س</div>
          </div>
        </div>
      </div>
    </div>

    <!-- نتائج المزامنة -->
    <div
      v-if="syncResult"
      class="sync-results"
      style="background: #1a1a1a; color: white; padding: 20px; border-radius: 12px"
    >
      <h3 style="color: #d4af37">✅ نتائج المزامنة</h3>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0">
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #4caf50">{{ syncResult.stats.created }}</div>
          <div style="color: #aaa">تمت الإضافة</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #ff9800">{{ syncResult.stats.updated }}</div>
          <div style="color: #aaa">تم التحديث</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #f44336">{{ syncResult.stats.failed }}</div>
          <div style="color: #aaa">فشل</div>
        </div>
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #aaa">{{ syncResult.stats.timeMs }}ms</div>
          <div style="color: #aaa">الوقت</div>
        </div>
      </div>

      <!-- الأخطاء إن وجدت -->
      <div
        v-if="syncResult.errors.length > 0"
        style="margin-top: 20px; background: #331111; padding: 15px; border-radius: 8px"
      >
        <h4 style="color: #f44336">⚠️ الأخطاء ({{ syncResult.errors.length }})</h4>
        <div
          v-for="(error, index) in syncResult.errors"
          :key="index"
          style="margin-top: 5px; color: #ff9999"
        >
          {{ error.product }}: {{ error.error }}
        </div>
      </div>
    </div>

    <!-- عرض JSON الخام للتطوير -->
    <div v-if="rawResult" style="margin-top: 20px">
      <button
        @click="showRaw = !showRaw"
        style="
          background: none;
          border: 1px solid #d4af37;
          color: #d4af37;
          padding: 5px 10px;
          border-radius: 4px;
          cursor: pointer;
        "
      >
        {{ showRaw ? 'إخفاء' : 'عرض' }} JSON الخام
      </button>

      <pre
        v-if="showRaw"
        style="
          background: #1a1a1a;
          color: #0f0;
          padding: 20px;
          border-radius: 8px;
          margin-top: 10px;
          overflow-x: auto;
        "
        >{{ JSON.stringify(rawResult, null, 2) }}</pre
      >
    </div>
  </div>
</template>

<script>
import ProductSyncService from '@/integration/services/ProductSyncService';
import ERPNextService from '@/integration/services/ERPNextService';

export default {
  name: 'ProductSyncTest',
  data() {
    return {
      loading: false,
      comparison: null,
      syncResult: null,
      status: null,
      rawResult: null,
      showRaw: false,
    };
  },
  methods: {
    async runSync() {
      this.loading = true;
      this.comparison = null;
      this.syncResult = null;

      try {
        const result = await ProductSyncService.syncProducts({
          create: true,
          update: true,
          delete: false,
        });

        this.syncResult = result;
        this.rawResult = result;
      } catch (error) {
        alert('خطأ: ' + error.message);
      } finally {
        this.loading = false;
      }
    },

    async compareOnly() {
      this.loading = true;

      try {
        // جلب المنتجات من المصدرين والمقارنة بدون مزامنة
        const siteProducts = await ProductSyncService.getSiteProducts();
        const erpnextResponse = await ERPNextService.getProducts();
        const erpnextProducts = erpnextResponse.data || [];

        this.comparison = ProductSyncService.compareProducts(siteProducts, erpnextProducts);
        this.rawResult = this.comparison;
      } catch (error) {
        alert('خطأ: ' + error.message);
      } finally {
        this.loading = false;
      }
    },

    getStatus() {
      this.status = ProductSyncService.getSyncStatus();
    },
  },
};
</script>
