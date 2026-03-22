<template>
  <div class="cart-page">
    <div class="container py-5">
      <h1 class="mb-5">{{ $t('cart') }}</h1>

      <div v-if="cartItems.length === 0" class="text-center py-5">
        <div class="empty-cart-icon mb-4">
          <i class="fa-solid fa-shopping-basket fa-5x text-muted opacity-50"></i>
        </div>
        <h2>{{ $t('emptyCart') || 'سلتك فارغة حالياً' }}</h2>
        <p class="text-muted mb-4">
          {{ $t('emptyCartMessage') || 'ابدأ بالتسوق لإضافة منتجات إلى سلتك' }}
        </p>
        <router-link to="/shop" class="btn btn-gold btn-lg px-5">
          {{ $t('shopNow') }}
        </router-link>
      </div>

      <div v-else class="row">
        <!-- Cart Items -->
        <div class="col-lg-8 mb-4">
          <BaseTable
            :items="cartItems"
            :columns="[
              { key: 'product', label: $t('product') || 'المنتج' },
              { key: 'price', label: $t('price') },
              { key: 'quantity', label: $t('quantity') || 'الكمية' },
              { key: 'total', label: $t('total') },
              { key: 'actions', label: '', width: '50px' }
            ]"
          >
            <template #cell(product)="{ item }">
              <div class="d-flex align-items-center">
                <img
                  :src="item.image"
                  :alt="item.name"
                  class="rounded-lg me-3"
                  width="60"
                  height="60"
                  style="object-fit: cover"
                />
                <div class="product-info">
                  <h6 class="mb-0 text-truncate" style="max-width: 150px">
                    {{ item.name }}
                  </h6>
                  <small class="text-muted d-block">{{ $t(item.category) }}</small>
                </div>
              </div>
            </template>

            <template #cell(price)="{ item }">
              <span class="price-value">{{ item.price }} د.ج</span>
            </template>

            <template #cell(quantity)="{ item }">
              <div class="input-group input-group-sm quantity-control" style="width: 100px">
                <button
                  class="btn btn-outline-secondary"
                  @click="updateQuantity(item.id, item.quantity - 1)"
                >
                  -
                </button>
                <input
                  type="text"
                  class="form-control text-center"
                  :value="item.quantity"
                  readonly
                />
                <button
                  class="btn btn-outline-secondary"
                  @click="updateQuantity(item.id, item.quantity + 1)"
                >
                  +
                </button>
              </div>
            </template>

            <template #cell(total)="{ item }">
              <span class="font-weight-bold total-value">{{ item.price * item.quantity }} د.ج</span>
            </template>

            <template #cell(actions)="{ item }">
              <button
                class="btn btn-link text-danger p-0"
                @click="removeFromCart(item.id)"
                :title="$t('remove')"
              >
                <i class="fa-solid fa-trash"></i>
              </button>
            </template>
          </BaseTable>

          <div class="d-flex justify-content-between mt-4 flex-wrap gap-3">
            <router-link to="/shop" class="btn btn-outline-secondary">
              <i class="fa-solid fa-arrow-right me-2"></i> {{ $t('backToShop') || 'العودة للمتجر' }}
            </router-link>
            <button class="btn btn-outline-danger" @click="clearCart">
              <i class="fa-solid fa-broom me-2"></i> {{ $t('clearCart') || 'تفريغ السلة' }}
            </button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="col-lg-4">
          <div class="card shadow-sm border-0 rounded-lg sticky-top" style="top: 100px">
            <div class="card-body">
              <h5 class="card-title mb-4">{{ $t('orderSummary') || 'ملخص الطلب' }}</h5>

              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">{{ $t('subtotal') }}</span>
                <span>{{ subtotal }} د.ج</span>
              </div>

              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">{{ $t('shipping') }}</span>
                <span class="text-success">{{ $t('free') }}</span>
              </div>

              <hr class="my-4" />

              <div class="d-flex justify-content-between mb-4">
                <span class="h5 mb-0">{{ $t('total') }}</span>
                <span class="h5 mb-0 text-gold">{{ total }} د.ج</span>
              </div>

              <router-link to="/checkout" class="btn btn-gold btn-lg w-100 shadow-sm">
                {{ $t('checkout') }}
              </router-link>

              <div class="mt-4 text-center">
                <p class="small text-muted mb-2">
                  <i class="fa-solid fa-shield-alt me-1"></i>
                  {{ $t('secureCheckout') || 'دفع آمن 100%' }}
                </p>
                <div class="payment-icons d-flex justify-content-center gap-3 opacity-50">
                  <i class="fab fa-cc-visa fa-2x"></i>
                  <i class="fab fa-cc-mastercard fa-2x"></i>
                  <img src="/assets/cib-logo.png" alt="CIB" height="25" class="grayscale" />
                  <img
                    src="/assets/edahabia-logo.png"
                    alt="Edahabia"
                    height="25"
                    class="grayscale"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import BaseTable from '@/components/common/BaseTable.vue';

const store = useStore();

// استخدام Vuex Getters لجلب البيانات
const cartItems = computed(() => store.getters['cart/cartItems']);
const subtotal = computed(() => store.getters['cart/cartTotalPrice']);
const total = computed(() => subtotal.value);

// استخدام Vuex Actions لتعديل البيانات
const updateQuantity = (productId, quantity) => {
  if (quantity < 1) return;
  store.dispatch('cart/updateQuantity', { productId, quantity });
};

const removeFromCart = (productId) => {
  store.dispatch('cart/removeFromCart', productId);
};

const clearCart = () => {
  if (confirm('هل أنت متأكد من تفريغ السلة بالكامل؟')) {
    store.dispatch('cart/clearCart');
  }
};
</script>

<style scoped>
.cart-page {
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

.grayscale {
  filter: grayscale(1);
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}
</style>
