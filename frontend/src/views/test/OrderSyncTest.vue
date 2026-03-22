<template>
  <div
    class="order-sync-test"
    style="padding: 30px; max-width: 1200px; margin: 0 auto; direction: rtl"
  >
    <h1 style="color: #d4af37; text-align: center">📦 اختبار مزامنة الطلبات مع ERPNext</h1>

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
        {{ loading ? 'جاري المزامنة...' : '🚀 بدء مزامنة الطلبات' }}
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
        📊 حالة المزامنة
      </button>
    </div>

    <!-- نتائج المزامنة -->
    <div
      v-if="syncResult"
      class="sync-results"
      style="
        background: #1a1a1a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
      "
    >
      <h3 style="color: #d4af37">📋 نتائج مزامنة الطلبات</h3>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0">
        <div
          class="stat-box"
          style="background: #2a2a2a; padding: 15px; border-radius: 8px; text-align: center"
        >
          <div style="font-size: 24px; color: #4caf50">{{ syncResult.stats.created }}</div>
          <div style="color: #aaa">فواتير جديدة</div>
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

      <!-- الفواتير الجديدة -->
      <div v-if="syncResult.created.length > 0" style="margin-top: 20px">
        <h4 style="color: #4caf50">✅ فواتير جديدة ({{ syncResult.created.length }})</h4>
        <div
          style="
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 10px;
          "
        >
          <div
            v-for="item in syncResult.created"
            :key="item.orderId"
            style="background: #2a2a2a; padding: 10px; border-radius: 8px"
          >
            <strong>طلب {{ item.orderId }}</strong>
            <div style="color: #aaa; font-size: 12px">فاتورة: {{ item.invoiceId }}</div>
          </div>
        </div>
      </div>

      <!-- الأخطاء -->
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
          طلب {{ error.order }}: {{ error.error }}
        </div>
      </div>
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
        margin-top: 20px;
      "
    >
      <h3 style="color: #d4af37">📊 حالة المزامنة</h3>
      <p>🔄 جاري المزامنة: {{ status.inProgress ? 'نعم' : 'لا' }}</p>
      <p>⏰ آخر مزامنة: {{ status.lastSync || 'لم تتم بعد' }}</p>
    </div>
  </div>
</template>

<script>
import OrderSyncService from '@/integration/services/OrderSyncService';

export default {
  name: 'OrderSyncTest',
  data() {
    return {
      loading: false,
      syncResult: null,
      status: null,
    };
  },
  methods: {
    async runSync() {
      this.loading = true;
      try {
        this.syncResult = await OrderSyncService.syncOrders();
      } catch (error) {
        alert('خطأ: ' + error.message);
      } finally {
        this.loading = false;
      }
    },

    getStatus() {
      this.status = OrderSyncService.getSyncStatus();
    },
  },
};
</script>
