<template>
  <div class="checkout-page">
    <div class="container py-5">
      <h1 class="mb-5">{{ $t('checkout') }}</h1>

      <div class="row">
        <!-- Billing Details -->
        <div class="col-lg-7 mb-4">
          <div class="card shadow-sm border-0 rounded-lg">
            <div class="card-body">
              <h5 class="card-title mb-4">{{ $t('billingDetails') || 'تفاصيل الشحن والدفع' }}</h5>

              <form @submit.prevent="submitOrder" class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">{{ $t('firstName') || 'الاسم الأول' }} *</label>
                  <input type="text" class="form-control" v-model="form.firstName" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label">{{ $t('lastName') || 'الاسم الأخير' }} *</label>
                  <input type="text" class="form-control" v-model="form.lastName" required />
                </div>
                <div class="col-12">
                  <label class="form-label">{{ $t('email') }} *</label>
                  <input type="email" class="form-control" v-model="form.email" required />
                </div>
                <div class="col-12">
                  <label class="form-label">{{ $t('phone') }} *</label>
                  <input
                    type="tel"
                    class="form-control"
                    v-model="form.phone"
                    required
                    placeholder="05 / 06 / 07 ..."
                  />
                </div>
                <div class="col-md-8">
                  <label class="form-label">{{ $t('address') }} *</label>
                  <input type="text" class="form-control" v-model="form.address" required />
                </div>
                <div class="col-md-4">
                  <label class="form-label">{{ $t('wilaya') || 'الولاية' }} *</label>
                  <select class="form-select" v-model="form.wilaya" required>
                    <option v-for="w in wilayas" :key="w.id" :value="w.id">
                      {{ w.id }} - {{ w.name }}
                    </option>
                  </select>
                </div>

                <div class="col-12 mt-4">
                  <h6>{{ $t('paymentMethod') || 'طريقة الدفع' }}</h6>
                  <div class="payment-methods mt-3">
                    <div
                      class="form-check payment-method-card mb-3 p-3 rounded border"
                      :class="{ active: form.paymentMethod === 'cod' }"
                    >
                      <input
                        class="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="cod"
                        value="cod"
                        v-model="form.paymentMethod"
                      />
                      <label
                        class="form-check-label w-100 ms-2 d-flex justify-content-between align-items-center"
                        for="cod"
                      >
                        <div>
                          <strong>{{ $t('cod') || 'الدفع عند الاستلام' }}</strong>
                          <p class="small text-muted mb-0">
                            {{ $t('codDesc') || 'ادفع نقداً عند استلام طلبك' }}
                          </p>
                        </div>
                        <i class="fa-solid fa-money-bill-wave fa-2x text-muted opacity-50"></i>
                      </label>
                    </div>

                    <div
                      class="form-check payment-method-card mb-3 p-3 rounded border"
                      :class="{ active: form.paymentMethod === 'card' }"
                    >
                      <input
                        class="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="card"
                        value="card"
                        v-model="form.paymentMethod"
                      />
                      <label
                        class="form-check-label w-100 ms-2 d-flex justify-content-between align-items-center"
                        for="card"
                      >
                        <div>
                          <strong>{{
                            $t('onlinePayment') || 'دفع إلكتروني (الذهبية / CIB)'
                          }}</strong>
                          <p class="small text-muted mb-0">
                            {{
                              $t('onlinePaymentDesc') || 'ادفع الآن بأمان باستخدام بطاقتك البنكية'
                            }}
                          </p>
                        </div>
                        <div class="d-flex gap-2">
                          <img src="/assets/cib-logo.png" alt="CIB" height="25" />
                          <img src="/assets/edahabia-logo.png" alt="Edahabia" height="25" />
                        </div>
                      </label>
                    </div>
                  </div>
                </div>

                <div class="col-12 mt-4">
                  <button
                    type="submit"
                    class="btn btn-gold btn-lg w-100 shadow-sm"
                    :disabled="isSubmitting"
                  >
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                    {{
                      form.paymentMethod === 'card'
                        ? $t('payAndCompleteOrder') || 'ادفع وأتمم الطلب'
                        : $t('placeOrder') || 'تأكيد الطلب'
                    }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="col-lg-5">
          <div class="card shadow-sm border-0 rounded-lg">
            <div class="card-body">
              <h5 class="card-title mb-4">{{ $t('yourOrder') || 'طلبك' }}</h5>

              <ul class="list-group list-group-flush mb-4">
                <li
                  v-for="item in cartItems"
                  :key="item.id"
                  class="list-group-item px-0 d-flex justify-content-between align-items-center"
                >
                  <div>
                    <span class="text-gold font-weight-bold">{{ item.quantity }}x</span>
                    {{ item.name }}
                  </div>
                  <span>{{ item.price * item.quantity }} د.ج</span>
                </li>
              </ul>

              <div class="d-flex justify-content-between mb-2">
                <span class="text-muted">{{ $t('subtotal') }}</span>
                <span>{{ subtotal }} د.ج</span>
              </div>

              <div class="d-flex justify-content-between mb-2">
                <span class="text-muted">{{ $t('shipping') }}</span>
                <span class="text-success">{{ $t('free') }}</span>
              </div>

              <hr class="my-3" />

              <div class="d-flex justify-content-between mb-0">
                <span class="h5 mb-0">{{ $t('total') }}</span>
                <span class="h5 mb-0 text-gold">{{ total }} د.ج</span>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0 rounded-lg mt-4 bg-light">
            <div class="card-body">
              <div class="d-flex align-items-center text-muted">
                <i class="fa-solid fa-lock fa-2x me-3 opacity-50"></i>
                <p class="small mb-0">
                  {{
                    $t('securityNotice') ||
                    'جميع بياناتك مشفرة ومحمية بالكامل. نحن لا نقوم بتخزين بيانات بطاقتك البنكية على خوادمنا.'
                  }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NotificationService from '@/integration/services/NotificationService';
import { CREATE_ORDER, graphqlMutation } from '@/integration/services/graphql';

const router = useRouter();

// State
const cartItems = ref([]);
const isSubmitting = ref(false);
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  address: '',
  wilaya: '16', // الجزائر العاصمة افتراضياً
  paymentMethod: 'cod',
});

const wilayas = [
  { id: '01', name: 'أدرار' }, { id: '02', name: 'الشلف' }, { id: '03', name: 'الأغواط' },
  { id: '04', name: 'أم البواقي' }, { id: '05', name: 'باتنة' }, { id: '06', name: 'بجاية' },
  { id: '07', name: 'بسكرة' }, { id: '08', name: 'بشار' }, { id: '09', name: 'البليدة' },
  { id: '10', name: 'البويرة' }, { id: '11', name: 'تمنراست' }, { id: '12', name: 'تبسة' },
  { id: '13', name: 'تلمسان' }, { id: '14', name: 'تيارت' }, { id: '15', name: 'تيزي وزو' },
  { id: '16', name: 'الجزائر' }, { id: '17', name: 'الجلفة' }, { id: '18', name: 'جيجل' },
  { id: '19', name: 'سطيف' }, { id: '20', name: 'سعيدة' }, { id: '21', name: 'سكيكدة' },
  { id: '22', name: 'سيدي بلعباس' }, { id: '23', name: 'عنابة' }, { id: '24', name: 'قالمة' },
  { id: '25', name: 'قسنطينة' }, { id: '26', name: 'المدية' }, { id: '27', name: 'مستغانم' },
  { id: '28', name: 'المسيلة' }, { id: '29', name: 'معسكر' }, { id: '30', name: 'ورقلة' },
  { id: '31', name: 'وهران' }, { id: '32', name: 'البيض' }, { id: '33', name: 'إليزي' },
  { id: '34', name: 'برج بوعريريج' }, { id: '35', name: 'بومرداس' }, { id: '36', name: 'الطارف' },
  { id: '37', name: 'تندوف' }, { id: '38', name: 'تيسمسيلت' }, { id: '39', name: 'الوادي' },
  { id: '40', name: 'خنشلة' }, { id: '41', name: 'سوق أهراس' }, { id: '42', name: 'تيبازة' },
  { id: '43', name: 'ميلة' }, { id: '44', name: 'عين الدفلى' }, { id: '45', name: 'النعامة' },
  { id: '46', name: 'عين تموشنت' }, { id: '47', name: 'غرداية' }, { id: '48', name: 'غليزان' }
];

// Computed
const subtotal = computed(() => cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0));
const total = computed(() => subtotal.value);

// Methods
const loadCart = () => {
  const savedCart = localStorage.getItem('cart');
  if (savedCart) {
    cartItems.value = JSON.parse(savedCart);
  }
};

const prepareOrderData = () => {
  return {
    customerName: `${form.value.firstName} ${form.value.lastName}`,
    phone: form.value.phone,
    email: form.value.email,
    address: form.value.address,
    wilayaId: form.value.wilaya,
    subtotal: subtotal.value,
    shippingCost: 0,
    total: total.value,
    paymentMethod: form.value.paymentMethod,
    items: cartItems.value.map(item => ({
      productId: item.id,
      materialId: item.material_id || null,
      width: item.width || 0,
      height: item.height || 0,
      quantity: item.quantity,
      price: item.price
    }))
  };
};

const finalizeOrder = (orderNumber, method) => {
  localStorage.removeItem('cart');
  
  // إشعار تأكيد الطلب
  NotificationService.success(
    'تم تأكيد طلبك', 
    `الطلب رقم ${orderNumber} قيد المعالجة الآن. شكراً لك!`
  );

  router.push({
    name: 'OrderSuccess',
    params: { orderId: orderNumber },
    query: { total: total.value, method }
  });
};

const submitOrder = async () => {
  if (cartItems.value.length === 0) return;
  
  isSubmitting.value = true;
  const orderData = prepareOrderData();
  
  try {
    const data = await graphqlMutation(CREATE_ORDER, orderData);
    finalizeOrder(data.createOrder.order.orderNumber, form.value.paymentMethod);
  } catch (error) {
    console.error('Error during order submission:', error);
    alert('حدث خطأ أثناء إرسال الطلب: ' + (error.message || 'خطأ غير متوقع'));
  } finally {
    isSubmitting.value = false;
  }
};

// Lifecycle
onMounted(() => {
  loadCart();
  if (cartItems.value.length === 0) {
    router.push('/shop');
  }
});
</script>

<style scoped>
.checkout-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.btn-gold {
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #f1d592 100%));
  color: #1a1a2e;
  font-weight: 600;
  border: none;
}

.btn-gold:hover {
  background: linear-gradient(135deg, #f1d592 0%, #d4af37 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.text-gold {
  color: #d4af37;
}

.payment-method-card {
  cursor: pointer;
  transition: all 0.2s;
}

.payment-method-card:hover {
  border-color: #d4af37 !important;
  background-color: #fff;
}

.payment-method-card.active {
  border-color: #d4af37 !important;
  background-color: rgba(212, 175, 55, 0.05);
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
}

.grayscale {
  filter: grayscale(1);
}
</style>
