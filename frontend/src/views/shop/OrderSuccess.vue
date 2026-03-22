<template>
  <div class="order-success-page">
    <div class="container py-5 text-center">
      <div class="success-animation mb-5">
        <div class="checkmark-circle">
          <div class="background"></div>
          <div class="checkmark draw"></div>
        </div>
      </div>

      <h1 class="display-4 mb-3">{{ $t('orderPlaced') || 'تم استلام طلبك بنجاح!' }}</h1>
      <p class="lead text-muted mb-5">
        {{ $t('orderConfirmationEmail') || 'شكراً لك على ثقتك بـ Vinyl Art. تم إرسال تفاصيل الطلب إلى بريدك الإلكتروني.' }}
      </p>

      <div class="order-details-card card shadow-sm border-0 rounded-lg mx-auto mb-5" style="max-width: 600px">
        <div class="card-header bg-white border-0 py-4">
          <h5 class="mb-0 text-gold">{{ $t('orderDetails') || 'تفاصيل الطلب' }}</h5>
        </div>
        <div class="card-body px-4 pb-4">
          <div class="d-flex justify-content-between mb-3">
            <span class="text-muted">{{ $t('orderNumber') || 'رقم الطلب' }}</span>
            <span class="font-weight-bold">#{{ orderId }}</span>
          </div>
          <div class="d-flex justify-content-between mb-3">
            <span class="text-muted">{{ $t('orderDate') || 'تاريخ الطلب' }}</span>
            <span>{{ new Date().toLocaleDateString('ar-DZ') }}</span>
          </div>
          <div class="d-flex justify-content-between mb-3">
            <span class="text-muted">{{ $t('paymentMethod') || 'طريقة الدفع' }}</span>
            <span class="badge bg-light text-dark border">{{ getPaymentMethodText(paymentMethod) }}</span>
          </div>
          
          <hr class="my-4 opacity-10" />

          <div class="d-flex justify-content-between mb-2 h5">
            <span>{{ $t('total') }}</span>
            <span class="text-gold">{{ total }} د.ج</span>
          </div>
        </div>
      </div>

      <div class="actions d-flex justify-content-center gap-3">
        <router-link to="/shop" class="btn btn-outline-gold btn-lg px-4">
          <i class="fa-solid fa-shopping-bag me-2"></i> {{ $t('continueShopping') || 'مواصلة التسوق' }}
        </router-link>
        <router-link to="/dashboard/orders" class="btn btn-gold btn-lg px-4 shadow-sm">
          <i class="fa-solid fa-list-ul me-2"></i> {{ $t('trackOrder') || 'تتبع الطلب' }}
        </router-link>
      </div>

      <div class="mt-5 p-4 bg-light rounded-lg border-dashed text-muted small mx-auto" style="max-width: 600px">
        <i class="fa-solid fa-info-circle me-2"></i>
        {{ $t('erpSyncNotice') || 'يتم الآن ترحيل طلبك إلى نظام ERPNext الخاص بنا لضمان أسرع عملية توصيل ممكنة.' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const orderId = ref(route.params.orderId || 'ORD-' + Date.now());
const total = ref(route.query.total || 0);
const paymentMethod = ref(route.query.method || 'cod');

const getPaymentMethodText = (method) => {
  const map = {
    cod: 'الدفع عند الاستلام',
    edahabia: 'البطاقة الذهبية (Edahabia)',
    cib: 'بطاقة CIB البنكية',
    card: 'بطاقة دفع إلكتروني'
  };
  return map[method] || method;
};

onMounted(() => {
  // يمكننا هنا التحقق من حالة الدفع فعلياً إذا كان هناك Transaction ID في الرابط
  console.log('✅ تم تحميل صفحة النجاح للطلب:', orderId.value);
});
</script>

<style scoped>
.order-success-page {
  background-color: #fbfbfb;
  min-height: 90vh;
}

.text-gold {
  color: #d4af37;
}

.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #f1d592 100%);
  color: #1a1a2e;
  font-weight: 600;
  border: none;
}

.btn-outline-gold {
  color: #d4af37;
  border: 1.5px solid #d4af37;
  font-weight: 600;
}

.btn-outline-gold:hover {
  background-color: rgba(212, 175, 55, 0.05);
  color: #c4a02c;
  border-color: #c4a02c;
}

.border-dashed {
  border: 1px dashed #ddd;
}

/* Success Animation */
.checkmark-circle {
  width: 120px;
  height: 120px;
  position: relative;
  display: inline-block;
  vertical-align: top;
  margin-bottom: 30px;
}

.checkmark-circle .background {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #28a745;
  position: absolute;
}

.checkmark-circle .checkmark {
  border-radius: 5px;
}

.checkmark-circle .checkmark.draw:after {
  animation-duration: 800ms;
  animation-timing-function: ease;
  animation-name: checkmark;
  transform: scaleX(-1) rotate(135deg);
}

.checkmark-circle .checkmark:after {
  opacity: 1;
  height: 60px;
  width: 30px;
  transform-origin: left top;
  border-right: 8px solid #fff;
  border-top: 8px solid #fff;
  content: "";
  left: 25px;
  top: 65px;
  position: absolute;
}

@keyframes checkmark {
  0% {
    height: 0;
    width: 0;
    opacity: 1;
  }
  20% {
    height: 0;
    width: 30px;
    opacity: 1;
  }
  40% {
    height: 60px;
    width: 30px;
    opacity: 1;
  }
  100% {
    height: 60px;
    width: 30px;
    opacity: 1;
  }
}
</style>
