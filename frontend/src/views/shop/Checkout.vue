<template>
  <v-main class="checkout-page">
    <!-- Background Effects -->
    <div class="bg-effects">
      <v-overlay 
        v-model="overlayActive" 
        class="gradient-overlay" 
        persistent 
        opacity="0.1"
      />
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <v-container>
      <v-card class="glass-card" elevation="8">
        <!-- Header -->
        <v-card-title class="pa-6">
          <h1 class="text-h4 font-weight-bold">
            <v-icon class="me-2">mdi-credit-card</v-icon>
            {{ $t('checkout') || 'الدفع' }}
          </h1>
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-6">
          <v-row>
            <!-- Billing Details -->
            <v-col cols="12" md="7">
              <v-card class="billing-card" elevation="2">
                <v-card-title class="text-h6">
                  <v-icon class="me-2">mdi-account-details</v-icon>
                  {{ $t('billingDetails') || 'تفاصيل الشحن والدفع' }}
                </v-card-title>
                
                <v-divider />

                <v-card-text>
                  <v-form ref="checkoutForm" v-model="formValid">
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-text-field
                          v-model="form.firstName"
                          :label="$t('firstName') || 'الاسم الأول'"
                          variant="outlined"
                          :rules="[v => !!v || 'هذا الحقل مطلوب']"
                          required
                        />
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field
                          v-model="form.lastName"
                          :label="$t('lastName') || 'الاسم الأخير'"
                          variant="outlined"
                          :rules="[v => !!v || 'هذا الحقل مطلوب']"
                          required
                        />
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="form.email"
                          :label="$t('email')"
                          variant="outlined"
                          type="email"
                          :rules="[v => !!v || 'هذا الحقل مطلوب', v => /.+@.+\..+/.test(v) || 'بريد إلكتروني غير صالح']"
                          required
                        />
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="form.phone"
                          :label="$t('phone')"
                          variant="outlined"
                          type="tel"
                          :placeholder="$t('phonePlaceholder') || '05 / 06 / 07 ...'"
                          :rules="[v => !!v || 'هذا الحقل مطلوب', v => /^(05|06|07)\d{8}$/.test(v) || 'رقم هاتف غير صالح']"
                          required
                        />
                      </v-col>
                      <v-col cols="12" sm="8">
                        <v-text-field
                          v-model="form.address"
                          :label="$t('address')"
                          variant="outlined"
                          :rules="[v => !!v || 'هذا الحقل مطلوب']"
                          required
                        />
                      </v-col>
                      <v-col cols="12" sm="4">
                        <v-select
                          v-model="form.wilaya"
                          :label="$t('wilaya') || 'الولاية'"
                          :items="wilayas"
                          item-title="name"
                          item-value="id"
                          variant="outlined"
                          :rules="[v => !!v || 'هذا الحقل مطلوب']"
                          required
                        />
                      </v-col>
                    </v-row>

                    <!-- Payment Method -->
                    <v-divider class="my-4" />
                    
                    <h6 class="text-h6 mb-4">{{ $t('paymentMethod') || 'طريقة الدفع' }}</h6>
                    
                    <v-radio-group v-model="form.paymentMethod" class="payment-methods">
                      <v-radio 
                        v-for="method in paymentMethods" 
                        :key="method.value"
                        :value="method.value"
                        class="payment-option"
                      >
                        <template v-slot:label>
                          <div class="d-flex align-center">
                            <v-icon :icon="method.icon" class="me-3" />
                            <div>
                              <div class="text-body-1">{{ method.label }}</div>
                              <div class="text-caption text-medium-emphasis">{{ method.description }}</div>
                            </div>
                          </div>
                        </template>
                      </v-radio>
                    </v-radio-group>

                    <!-- Order Notes -->
                    <v-divider class="my-4" />
                    
                    <v-textarea
                      v-model="form.notes"
                      :label="$t('orderNotes') || 'ملاحظات الطلب'"
                      variant="outlined"
                      rows="3"
                      :placeholder="$t('orderNotesPlaceholder') || 'أي ملاحظات خاصة بالطلب...'"
                    />
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Order Summary -->
            <v-col cols="12" md="5">
              <v-card class="order-summary-card" elevation="2">
                <v-card-title class="text-h6">
                  <v-icon class="me-2">mdi-receipt</v-icon>
                  {{ $t('orderSummary') || 'ملخص الطلب' }}
                </v-card-title>
                
                <v-divider />

                <v-card-text>
                  <!-- Cart Items -->
                  <div class="cart-items mb-4">
                    <v-list density="compact">
                      <v-list-item
                        v-for="item in cartItems"
                        :key="item.id"
                        class="cart-summary-item"
                      >
                        <template v-slot:prepend>
                          <v-avatar size="40" rounded>
                            <v-img
                              :src="item.image"
                              :alt="item.name"
                              cover
                            />
                          </v-avatar>
                        </template>

                        <v-list-item-content>
                          <v-list-item-title class="text-body-2">{{ item.name }}</v-list-item-title>
                          <v-list-item-subtitle class="text-caption">
                            {{ $t('quantity') || 'الكمية' }}: {{ item.quantity }}
                          </v-list-item-subtitle>
                        </v-list-item-content>

                        <template v-slot:append>
                          <span class="text-body-2 font-weight-bold">
                            {{ formatCurrency(item.price * item.quantity) }}
                          </span>
                        </template>
                      </v-list-item>
                    </v-list>
                  </div>

                  <!-- Price Summary -->
                  <v-divider class="my-3" />
                  
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon>mdi-shopping-bag</v-icon>
                      </template>
                      <v-list-item-title>{{ $t('subtotal') || 'المجموع الفرعي' }}</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-body-2">{{ formatCurrency(subtotal) }}</span>
                      </template>
                    </v-list-item>
                    
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon>mdi-truck</v-icon>
                      </template>
                      <v-list-item-title>{{ $t('shipping') || 'الشحن' }}</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-body-2">{{ formatCurrency(shippingCost) }}</span>
                      </template>
                    </v-list-item>
                    
                    <v-list-item v-if="discountAmount > 0">
                      <template v-slot:prepend>
                        <v-icon>mdi-tag</v-icon>
                      </template>
                      <v-list-item-title>{{ $t('discount') || 'الخصم' }}</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-body-2 text-success">-{{ formatCurrency(discountAmount) }}</span>
                      </template>
                    </v-list-item>
                    
                    <v-divider class="my-2" />
                    
                    <v-list-item>
                      <v-list-item-title class="text-h6 font-weight-bold">
                        {{ $t('total') || 'الإجمالي' }}
                      </v-list-item-title>
                      <template v-slot:append>
                        <span class="text-h5 font-weight-bold text-primary">{{ formatCurrency(total) }}</span>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card-text>

                <v-divider />

                <!-- Submit Button -->
                <v-card-actions class="pa-4">
                  <v-btn
                    color="primary"
                    variant="elevated"
                    size="large"
                    block
                    prepend-icon="mdi-check"
                    @click="submitOrder"
                    :loading="submitting"
                    :disabled="!formValid || cartItems.length === 0"
                  >
                    {{ $t('placeOrder') || 'تأكيد الطلب' }}
                  </v-btn>
                </v-card-actions>

                <!-- Security Note -->
                <v-card-text class="text-center text-caption text-medium-emphasis">
                  <v-icon size="small" class="me-1">mdi-shield-check</v-icon>
                  {{ $t('securePayment') || 'دفع آمن ومشفر' }}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CheckoutService from '@/integration/services/CheckoutService';
import CartService from '@/integration/services/CartService';

// Reactive data
const overlayActive = ref(true);
const submitting = ref(false);
const formValid = ref(false);
const checkoutForm = ref(null);
const cartItems = ref([]);

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  address: '',
  wilaya: '',
  paymentMethod: 'cash_on_delivery',
  notes: ''
});

const wilayas = ref([
  { id: '1', name: 'أدرار' },
  { id: '2', name: 'الشلف' },
  { id: '3', name: 'الأغواط' },
  { id: '4', name: 'أم البواقي' },
  { id: '5', name: 'باتنة' },
  { id: '6', name: 'بجاية' },
  { id: '7', name: 'بسكرة' },
  { id: '8', name: 'بشار' },
  { id: '9', name: 'البليدة' },
  { id: '10', name: 'البويرة' },
  { id: '11', name: 'تمنراست' },
  { id: '12', name: 'تبسة' },
  { id: '13', name: 'تلمسان' },
  { id: '14', name: 'تيارت' },
  { id: '15', name: 'تيزي وزو' },
  { id: '16', name: 'الجزائر' },
  { id: '17', name: 'الجلفة' },
  { id: '18', name: 'جيجل' },
  { id: '19', name: 'سوق أهراس' },
  { id: '20', name: 'سيدي بلعباس' },
  { id: '21', name: 'عنابة' },
  { id: '22', name: 'قالمة' },
  { id: '23', name: 'قسنطينة' },
  { id: '24', name: 'المدية' },
  { id: '25', name: 'ميلة' },
  { id: '26', name: 'معسكر' },
  { id: '27', name: 'مسردة' },
  { id: '28', name: 'مستغانم' },
  { id: '29', name: 'ميلة' },
  { id: '30', name: 'ورقلة' },
  { id: '31', name: 'وهران' },
  { id: '32', name: 'البيض' },
  { id: '33', name: 'إليزي' },
  { id: '34', name: 'برج بوعريريج' },
  { id: '35', name: 'بومرداس' },
  { id: '36', name: 'الطارف' },
  { id: '37', name: 'تندوف' },
  { id: '38', name: 'تميمون' },
  { id: '39', name: 'غرداية' },
  { id: '40', name: 'غليزان' },
  { id: '41', name: 'قايدي بلعباس' },
  { id: '42', name: 'خنشلة' },
  { id: '43', name: 'سطيف' },
  { id: '44', name: 'سيدي عبد الله' },
  { id: '45', name: 'ميلة' },
  { id: '46', name: 'عين الدفلى' },
  { id: '47', name: 'عين تموشنت' },
  { id: '48', name: 'عين صالح' },
  { id: '49', name: 'عين قزام' },
  { id: '50', name: 'الجلفة' },
  { id: '51', name: 'المدية' },
  { id: '52', name: 'خنشلة' },
  { id: '53', name: 'سطيف' },
  { id: '54', name: 'المنطقة' },
  { id: '55', name: 'نعامة' },
  { id: '56', name: 'تيميمون' },
  { id: '57', name: 'برج بوعريريج' },
  { id: '58', name: 'تلمسان' }
]);

const paymentMethods = ref([
  {
    value: 'cash_on_delivery',
    label: 'الدفع عند الاستلام',
    description: 'الدفع عند استلام المنتجات',
    icon: 'mdi-cash'
  },
  {
    value: 'credit_card',
    label: 'بطاقة بنكية',
    description: 'الدفع الآمن بالبطاقة البنكية',
    icon: 'mdi-credit-card'
  },
  {
    value: 'cib',
    label: 'CIB',
    description: 'الدفع عبر CIB',
    icon: 'mdi-bank'
  },
  {
    value: 'edahabia',
    label: 'Edahabia',
    description: 'الدفع عبر محفظة Edahabia',
    icon: 'mdi-wallet'
  }
]);

// Computed
const subtotal = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

const shippingCost = computed(() => {
  return subtotal.value > 15000 ? 0 : 800; // شحن مجاني فوق 15000 د.ج
});

const discountAmount = computed(() => {
  return cartItems.value.reduce((sum, item) => {
    if (item.originalPrice) {
      return sum + ((item.originalPrice - item.price) * item.quantity);
    }
    return sum;
  }, 0);
});

const total = computed(() => {
  return subtotal.value + shippingCost.value - discountAmount.value;
});

// Methods
const loadCart = async () => {
  try {
    const items = await CartService.getCartItems();
    cartItems.value = items;
    console.log('✅ Cart loaded for checkout:', items);
  } catch (error) {
    console.error('❌ Error loading cart:', error);
    cartItems.value = CartService.getFallbackCartItems();
  }
};

const submitOrder = async () => {
  if (!formValid.value) return;
  
  submitting.value = true;
  try {
    const orderData = {
      customer: {
        firstName: form.value.firstName,
        lastName: form.value.lastName,
        email: form.value.email,
        phone: form.value.phone
      },
      shipping: {
        address: form.value.address,
        wilaya: form.value.wilaya
      },
      payment: {
        method: form.value.paymentMethod
      },
      items: cartItems.value.map(item => ({
        productId: item.productId,
        quantity: item.quantity,
        price: item.price,
        variant: item.variant
      })),
      notes: form.value.notes,
      totals: {
        subtotal: subtotal.value,
        shippingCost: shippingCost.value,
        discountAmount: discountAmount.value,
        total: total.value
      }
    };

    const order = await CheckoutService.createOrder(orderData);
    
    console.log('✅ Order created successfully:', order);
    
    // Navigate to success page
    // router.push(`/shop/order-success?orderId=${order.id}`);
    
  } catch (error) {
    console.error('❌ Error submitting order:', error);
  } finally {
    submitting.value = false;
  }
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ar-DZ', {
    style: 'currency',
    currency: 'DZD'
  }).format(amount);
};

onMounted(() => {
  loadCart();
});
</script>

<style scoped>
.bg-effects {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, transparent 70%);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  bottom: 20%;
  left: 60%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.glass-card {
  background: rgba(var(--v-theme-surface), 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  border-radius: 24px;
  margin-top: 80px;
}

.cart-summary-item {
  transition: all 0.3s ease;
}

.cart-summary-item:hover {
  background: rgba(var(--v-theme-surface-variant), 0.05);
}

.payment-methods :deep(.v-radio) {
  margin-bottom: 16px;
}

.payment-option {
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
}

.payment-option:hover {
  border-color: var(--v-theme-primary);
  background: rgba(var(--v-theme-primary), 0.05);
}

@media (max-width: 768px) {
  .glass-card {
    margin-top: 20px;
    border-radius: 16px;
  }
}
</style>
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
