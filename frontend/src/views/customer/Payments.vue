<template>
  <div class="payments-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="payments-container">
      <div class="glass-card">
        <!-- Header -->
        <div class="payments-header">
          <div class="header-content">
            <h1 class="page-title">
              <i class="fa-solid fa-credit-card"></i>
              طرق الدفع
            </h1>
            <p class="page-subtitle">إدارة بطاقات الدفع وطرق الدفع المحفوظة</p>
          </div>
          <button class="add-payment-btn" @click="showAddForm = true">
            <i class="fa-solid fa-plus"></i>
            إضافة طريقة دفع
          </button>
        </div>

        <!-- Payment Methods List -->
        <div class="payments-list">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner">
              <i class="fa-solid fa-spinner fa-spin"></i>
            </div>
            <p class="loading-text">جاري تحميل طرق الدفع...</p>
          </div>

          <div v-else-if="paymentMethods.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="fa-solid fa-credit-card"></i>
            </div>
            <h3 class="empty-title">لا توجد طرق دفع</h3>
            <p class="empty-text">لم تقم بإضافة أي طرق دفع بعد</p>
            <button class="add-first-btn" @click="showAddForm = true">
              <i class="fa-solid fa-plus"></i>
              إضافة أول طريقة دفع
            </button>
          </div>

          <div v-else class="payment-methods-grid">
            <div 
              v-for="method in paymentMethods" 
              :key="method.id" 
              class="payment-card"
              :class="{ default: method.isDefault }"
            >
              <div class="payment-header">
                <div class="payment-info">
                  <div class="payment-type">
                    <i :class="getPaymentIcon(method.type)"></i>
                    <span>{{ getPaymentTypeName(method.type) }}</span>
                  </div>
                  <h3 class="payment-title">{{ method.title }}</h3>
                </div>
                <div class="payment-actions">
                  <button 
                    v-if="!method.isDefault" 
                    class="default-btn" 
                    @click="setDefault(method.id)"
                  >
                    <i class="fa-solid fa-star"></i>
                    افتراضي
                  </button>
                  <div class="action-buttons">
                    <button class="edit-btn" @click="editPaymentMethod(method)">
                      <i class="fa-solid fa-edit"></i>
                    </button>
                    <button class="delete-btn" @click="deletePaymentMethod(method.id)">
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div class="payment-details">
                <div v-if="method.type === 'card'" class="card-details">
                  <div class="card-number">
                    <i class="fa-solid fa-credit-card"></i>
                    <span>**** **** **** {{ method.last4 }}</span>
                  </div>
                  <div class="card-info">
                    <div class="card-row">
                      <span class="label">صاحب البطاقة:</span>
                      <span class="value">{{ method.cardholderName }}</span>
                    </div>
                    <div class="card-row">
                      <span class="label">تاريخ الانتهاء:</span>
                      <span class="value">{{ method.expiryMonth }}/{{ method.expiryYear }}</span>
                    </div>
                  </div>
                </div>

                <div v-else-if="method.type === 'bank'" class="bank-details">
                  <div class="bank-info">
                    <div class="bank-row">
                      <span class="label">البنك:</span>
                      <span class="value">{{ method.bankName }}</span>
                    </div>
                    <div class="bank-row">
                      <span class="label">اسم الحساب:</span>
                      <span class="value">{{ method.accountName }}</span>
                    </div>
                    <div class="bank-row">
                      <span class="label">رقم الحساب:</span>
                      <span class="value">****{{ method.last4 }}</span>
                    </div>
                  </div>
                </div>

                <div v-else-if="method.type === 'wallet'" class="wallet-details">
                  <div class="wallet-info">
                    <div class="wallet-row">
                      <span class="label">المحفظة:</span>
                      <span class="value">{{ method.walletProvider }}</span>
                    </div>
                    <div class="wallet-row">
                      <span class="label">رقم الهاتف:</span>
                      <span class="value">{{ method.phoneNumber }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="method.isDefault" class="default-badge">
                <i class="fa-solid fa-star"></i>
                طريقة الدفع الافتراضية
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Payment Method Modal -->
    <div v-if="showAddForm || editingPayment" class="payment-modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingPayment ? 'تعديل طريقة الدفع' : 'إضافة طريقة دفع جديدة' }}</h2>
          <button class="close-btn" @click="closeModal">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>

        <form @submit.prevent="savePaymentMethod" class="payment-form">
          <div class="payment-type-selector">
            <label class="form-label">نوع طريقة الدفع *</label>
            <div class="payment-types">
              <label 
                v-for="type in paymentTypes" 
                :key="type.value"
                :class="['payment-type-option', { active: paymentForm.type === type.value }]"
              >
                <input 
                  type="radio" 
                  v-model="paymentForm.type" 
                  :value="type.value"
                  required
                />
                <i :class="type.icon"></i>
                <span>{{ type.label }}</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">عنوان طريقة الدفع *</label>
            <input 
              type="text" 
              v-model="paymentForm.title" 
              class="form-input"
              placeholder="مثلاً: البطاقة الشخصية، حساب البنك"
              required
            />
          </div>

          <!-- Card Payment Fields -->
          <div v-if="paymentForm.type === 'card'" class="card-fields">
            <div class="form-group">
              <label class="form-label">اسم حامل البطاقة *</label>
              <input 
                type="text" 
                v-model="paymentForm.cardholderName" 
                class="form-input"
                placeholder="الاسم كما يظهر على البطاقة"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">رقم البطاقة *</label>
              <input 
                type="text" 
                v-model="paymentForm.cardNumber" 
                class="form-input"
                placeholder="1234 5678 9012 3456"
                maxlength="19"
                required
                @input="formatCardNumber"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">تاريخ الانتهاء *</label>
                <div class="expiry-input">
                  <input 
                    type="text" 
                    v-model="paymentForm.expiryMonth" 
                    class="form-input"
                    placeholder="MM"
                    maxlength="2"
                    required
                  />
                  <span class="expiry-separator">/</span>
                  <input 
                    type="text" 
                    v-model="paymentForm.expiryYear" 
                    class="form-input"
                    placeholder="YY"
                    maxlength="2"
                    required
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">CVV *</label>
                <input 
                  type="text" 
                  v-model="paymentForm.cvv" 
                  class="form-input"
                  placeholder="123"
                  maxlength="4"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Bank Transfer Fields -->
          <div v-else-if="paymentForm.type === 'bank'" class="bank-fields">
            <div class="form-group">
              <label class="form-label">اسم البنك *</label>
              <select v-model="paymentForm.bankName" class="form-input" required>
                <option value="">اختر البنك</option>
                <option value="البنك الوطني الجزائري">البنك الوطني الجزائري</option>
                <option value="البنك الخارجي الجزائري">البنك الخارجي الجزائري</option>
                <option value="البنك الشعبي الجزائري">البنك الشعبي الجزائري</option>
                <option value="البنك الجزائري للتنمية">البنك الجزائري للتنمية</option>
                <option value="البنك الفلاحي الجزائري">البنك الفلاحي الجزائري</option>
                <option value="بنك القرض الشعبي الجزائري">بنك القرض الشعبي الجزائري</option>
                <option value="البنك الأفريكي">البنك الأفريقي</option>
                <option value="سيتي بنك">سيتي بنك</option>
                <option value="بي إن بي باريباس">بي إن بي باريباس</option>
                <option value="سوسيتيه جنرال">سوسيتيه جنرال</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">اسم الحساب *</label>
              <input 
                type="text" 
                v-model="paymentForm.accountName" 
                class="form-input"
                placeholder="اسم صاحب الحساب"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">رقم الحساب *</label>
              <input 
                type="text" 
                v-model="paymentForm.accountNumber" 
                class="form-input"
                placeholder="رقم الحساب البنكي"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">IBAN</label>
              <input 
                type="text" 
                v-model="paymentForm.iban" 
                class="form-input"
                placeholder="DZXX XXXX XXXX XXXX XXXX XXXX XXXX"
              />
            </div>
          </div>

          <!-- E-Wallet Fields -->
          <div v-else-if="paymentForm.type === 'wallet'" class="wallet-fields">
            <div class="form-group">
              <label class="form-label">المحفظة الإلكترونية *</label>
              <select v-model="paymentForm.walletProvider" class="form-input" required>
                <option value="">اختر المحفظة</option>
                <option value="CIB">CIB Pay</option>
                <option value="BaridiMob">BaridiMob</option>
                <option value="Djezzy">Djezzy Cash</option>
                <option value="Mobilis">Mobilis Money</option>
                <option value="Edahabia">Edahabia</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">رقم الهاتف *</label>
              <input 
                type="tel" 
                v-model="paymentForm.phoneNumber" 
                class="form-input"
                placeholder="+213 XXX XXX XXXX"
                required
              />
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeModal">
              إلغاء
            </button>
            <button type="submit" class="save-btn" :disabled="loading">
              <i class="fa-solid fa-save"></i>
              <span v-if="!loading">{{ editingPayment ? 'تحديث' : 'حفظ' }}</span>
              <span v-else class="loading-text">
                <i class="fa-solid fa-spinner fa-spin"></i>
                جاري الحفظ...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';

const loading = ref(false);
const showAddForm = ref(false);
const editingPayment = ref(null);

const paymentMethods = ref([]);

const paymentForm = reactive({
  type: '',
  title: '',
  // Card fields
  cardholderName: '',
  cardNumber: '',
  expiryMonth: '',
  expiryYear: '',
  cvv: '',
  // Bank fields
  bankName: '',
  accountName: '',
  accountNumber: '',
  iban: '',
  // Wallet fields
  walletProvider: '',
  phoneNumber: ''
});

const paymentTypes = [
  { value: 'card', label: 'بطاقة ائتمان', icon: 'fa-solid fa-credit-card' },
  { value: 'bank', label: 'تحويل بنكي', icon: 'fa-solid fa-university' },
  { value: 'wallet', label: 'محفظة إلكترونية', icon: 'fa-solid fa-wallet' }
];

// Mock data - في الواقع سيتم جلبها من GraphQL
const mockPaymentMethods = [
  {
    id: 1,
    type: 'card',
    title: 'البطاقة الشخصية',
    cardholderName: 'أحمد محمد',
    last4: '1234',
    expiryMonth: '12',
    expiryYear: '25',
    isDefault: true
  },
  {
    id: 2,
    type: 'bank',
    title: 'حساب البنك الوطني',
    bankName: 'البنك الوطني الجزائري',
    accountName: 'أحمد محمد',
    last4: '5678',
    isDefault: false
  },
  {
    id: 3,
    type: 'wallet',
    title: 'CIB Pay',
    walletProvider: 'CIB',
    phoneNumber: '+213 66 123 4567',
    isDefault: false
  }
];

const getPaymentIcon = (type) => {
  const icons = {
    card: 'fa-solid fa-credit-card',
    bank: 'fa-solid fa-university',
    wallet: 'fa-solid fa-wallet'
  };
  return icons[type] || 'fa-solid fa-credit-card';
};

const getPaymentTypeName = (type) => {
  const names = {
    card: 'بطاقة ائتمان',
    bank: 'تحويل بنكي',
    wallet: 'محفظة إلكترونية'
  };
  return names[type] || type;
};

const formatCardNumber = () => {
  let value = paymentForm.cardNumber.replace(/\s/g, '');
  let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
  paymentForm.cardNumber = formattedValue;
};

const closeModal = () => {
  showAddForm.value = false;
  editingPayment.value = null;
  resetForm();
};

const resetForm = () => {
  Object.assign(paymentForm, {
    type: '',
    title: '',
    cardholderName: '',
    cardNumber: '',
    expiryMonth: '',
    expiryYear: '',
    cvv: '',
    bankName: '',
    accountName: '',
    accountNumber: '',
    iban: '',
    walletProvider: '',
    phoneNumber: ''
  });
};

const editPaymentMethod = (method) => {
  editingPayment.value = method;
  Object.assign(paymentForm, method);
};

const savePaymentMethod = async () => {
  try {
    loading.value = true;
    
    // TODO: Implement GraphQL mutation to save payment method
    console.log('Save payment method:', paymentForm);
    
    if (editingPayment.value) {
      // Update existing payment method
      const index = paymentMethods.value.findIndex(m => m.id === editingPayment.value.id);
      if (index !== -1) {
        paymentMethods.value[index] = { ...paymentForm, id: editingPayment.value.id };
      }
    } else {
      // Add new payment method
      const newMethod = {
        ...paymentForm,
        id: Date.now(),
        isDefault: paymentMethods.value.length === 0,
        last4: paymentForm.cardNumber?.slice(-4) || paymentForm.accountNumber?.slice(-4) || ''
      };
      paymentMethods.value.push(newMethod);
    }
    
    closeModal();
  } catch (error) {
    console.error('Error saving payment method:', error);
  } finally {
    loading.value = false;
  }
};

const deletePaymentMethod = async (paymentId) => {
  if (confirm('هل أنت متأكد من حذف طريقة الدفع؟')) {
    try {
      // TODO: Implement GraphQL mutation to delete payment method
      console.log('Delete payment method:', paymentId);
      
      paymentMethods.value = paymentMethods.value.filter(m => m.id !== paymentId);
    } catch (error) {
      console.error('Error deleting payment method:', error);
    }
  }
};

const setDefault = async (paymentId) => {
  try {
    // TODO: Implement GraphQL mutation to set default payment method
    console.log('Set default payment method:', paymentId);
    
    paymentMethods.value.forEach(method => {
      method.isDefault = method.id === paymentId;
    });
  } catch (error) {
    console.error('Error setting default payment method:', error);
  }
};

const loadPaymentMethods = async () => {
  try {
    loading.value = true;
    
    // TODO: Implement GraphQL query to fetch payment methods
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    paymentMethods.value = mockPaymentMethods;
  } catch (error) {
    console.error('Error loading payment methods:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadPaymentMethods();
});
</script>

<style scoped>
/* ===== Payments Page ===== */
.payments-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

/* Background Effects */
.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 20%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(212, 175, 55, 0.12) 0%, transparent 50%);
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.1) 50%, transparent 100%);
  filter: blur(2px);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-20px) scale(1.05); }
}

/* Payments Container */
.payments-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1000px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.08),
              inset 0 0 30px rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

/* Header */
.payments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.page-title i {
  color: #d4af37;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  margin: 0;
}

.add-payment-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-payment-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  font-size: 48px;
  color: #d4af37;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 18px;
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.empty-icon {
  font-size: 64px;
  color: rgba(255, 255, 255, 0.3);
  margin-bottom: 24px;
}

.empty-title {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.empty-text {
  font-size: 16px;
  margin: 0 0 32px 0;
}

.add-first-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.add-first-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

/* Payment Methods Grid */
.payment-methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.payment-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.payment-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
}

.payment-card.default {
  border-color: rgba(212, 175, 55, 0.3);
  background: rgba(212, 175, 55, 0.05);
}

.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.payment-info {
  flex: 1;
}

.payment-type {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.payment-type i {
  font-size: 16px;
}

.payment-title {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.payment-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.default-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  color: #d4af37;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.default-btn:hover {
  background: rgba(212, 175, 55, 0.3);
  color: #ffffff;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.edit-btn,
.delete-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
}

.edit-btn:hover {
  background: rgba(0, 123, 255, 0.3);
  color: #ffffff;
}

.delete-btn {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.delete-btn:hover {
  background: rgba(220, 53, 69, 0.3);
  color: #ffffff;
}

/* Payment Details */
.card-details,
.bank-details,
.wallet-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-number {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
}

.card-number i {
  color: #d4af37;
}

.card-info,
.bank-info,
.wallet-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-row,
.bank-row,
.wallet-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.value {
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
}

.default-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 4px;
  color: #d4af37;
  font-size: 12px;
  font-weight: 500;
}

/* Modal */
.payment-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
}

.modal-header h2 {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #dc3545;
}

.payment-form {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.payment-type-selector {
  margin-bottom: 20px;
}

.payment-types {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.payment-type-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.payment-type-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.payment-type-option.active {
  background: rgba(212, 175, 55, 0.2);
  border-color: rgba(212, 175, 55, 0.3);
}

.payment-type-option i {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s ease;
}

.payment-type-option.active i {
  color: #d4af37;
}

.payment-type-option span {
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

.payment-type-option input {
  display: none;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.expiry-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.expiry-separator {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.cancel-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .payments-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .payments-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .payment-methods-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .payment-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .payment-actions {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
  
  .payment-types {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .save-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
