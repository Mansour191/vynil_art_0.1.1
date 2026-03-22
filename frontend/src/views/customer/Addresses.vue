<template>
  <div class="addresses-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="addresses-container">
      <div class="glass-card">
        <!-- Header -->
        <div class="addresses-header">
          <div class="header-content">
            <h1 class="page-title">
              <i class="fa-solid fa-map-marker-alt"></i>
              العناوين
            </h1>
            <p class="page-subtitle">إدارة عناوين الشحن والتوصيل</p>
          </div>
          <button class="add-address-btn" @click="showAddForm = true">
            <i class="fa-solid fa-plus"></i>
            إضافة عنوان
          </button>
        </div>

        <!-- Addresses List -->
        <div class="addresses-list">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner">
              <i class="fa-solid fa-spinner fa-spin"></i>
            </div>
            <p class="loading-text">جاري تحميل العناوين...</p>
          </div>

          <div v-else-if="addresses.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="fa-solid fa-map-marker-alt"></i>
            </div>
            <h3 class="empty-title">لا توجد عناوين</h3>
            <p class="empty-text">لم تقم بإضافة أي عناوين بعد</p>
            <button class="add-first-btn" @click="showAddForm = true">
              <i class="fa-solid fa-plus"></i>
              إضافة أول عنوان
            </button>
          </div>

          <div v-else class="addresses-grid">
            <div 
              v-for="address in addresses" 
              :key="address.id" 
              class="address-card"
              :class="{ default: address.isDefault }"
            >
              <div class="address-header">
                <div class="address-info">
                  <h3 class="address-title">{{ address.title }}</h3>
                  <p class="address-name">{{ address.name }}</p>
                </div>
                <div class="address-actions">
                  <button 
                    v-if="!address.isDefault" 
                    class="default-btn" 
                    @click="setDefault(address.id)"
                  >
                    <i class="fa-solid fa-star"></i>
                    افتراضي
                  </button>
                  <div class="action-buttons">
                    <button class="edit-btn" @click="editAddress(address)">
                      <i class="fa-solid fa-edit"></i>
                    </button>
                    <button class="delete-btn" @click="deleteAddress(address.id)">
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div class="address-details">
                <div class="address-line">
                  <i class="fa-solid fa-user"></i>
                  <span>{{ address.name }}</span>
                </div>
                <div class="address-line">
                  <i class="fa-solid fa-phone"></i>
                  <span>{{ address.phone }}</span>
                </div>
                <div class="address-line">
                  <i class="fa-solid fa-map-marker-alt"></i>
                  <span>{{ address.fullAddress }}</span>
                </div>
                <div v-if="address.instructions" class="address-line">
                  <i class="fa-solid fa-info-circle"></i>
                  <span>{{ address.instructions }}</span>
                </div>
              </div>

              <div v-if="address.isDefault" class="default-badge">
                <i class="fa-solid fa-star"></i>
                العنوان الافتراضي
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Address Modal -->
    <div v-if="showAddForm || editingAddress" class="address-modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingAddress ? 'تعديل العنوان' : 'إضافة عنوان جديد' }}</h2>
          <button class="close-btn" @click="closeModal">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>

        <form @submit.prevent="saveAddress" class="address-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">عنوان العنوان *</label>
              <input 
                type="text" 
                v-model="addressForm.title" 
                class="form-input"
                placeholder="مثلاً: المنزل، العمل"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">الاسم الكامل *</label>
              <input 
                type="text" 
                v-model="addressForm.name" 
                class="form-input"
                placeholder="الاسم المستلم"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">رقم الهاتف *</label>
              <input 
                type="tel" 
                v-model="addressForm.phone" 
                class="form-input"
                placeholder="رقم الهاتف"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">الولاية *</label>
              <select v-model="addressForm.wilaya" class="form-input" required>
                <option value="">اختر الولاية</option>
                <option value="الجزائر">الجزائر</option>
                <option value="وهران">وهران</option>
                <option value="قسنطينة">قسنطينة</option>
                <option value="عنابة">عنابة</option>
                <option value="باتنة">باتنة</option>
                <option value="جيجل">جيجل</option>
                <option value="سطيف">سطيف</option>
                <option value="البليدة">البليدة</option>
                <option value="البويرة">البويرة</option>
                <option value="تمنراست">تمنراست</option>
                <option value="تيسمسيلت">تيسمسيلت</option>
                <option value="الوادي">الوادي</option>
                <option value="المسيلة">المسيلة</option>
                <option value="غرداية">غرداية</option>
                <option value="القليمة">القليمة</option>
                <option value="برج بوعريريج">برج بوعريريج</option>
                <option value="بومرداس">بومرداس</option>
                <option value="الطارف">الطارف</option>
                <option value="تيزي وزو">تيزي وزو</option>
                <option value="الجلفة">الجلفة</option>
                <option value="سعيدة">سعيدة</option>
                <option value="ميلة">ميلة</option>
                <option value="عين الدفلة">عين الدفلة</option>
                <option value="غليزان">غليزان</option>
                <option value="تامنغاست">تامنغاست</option>
                <option value="أدرار">أدرار</option>
                <option value="المدية">المدية</              </option>
                <option value="معسكر">معسكر</option>
                <option value="الشلف">الشلف</option>
                <option value="النعامة">النعامة</option>
                <option value="تقرت">تقرت</option>
                <option value="البيض">البيض</option>
                <option value="إليزي">إليزي</option>
                <option value="تندوف">تندوف</option>
                <option value="تميموسان">تميموسان</option>
                <option value="ورقلة">ورقلة</option>
                <option value="غرداية">غرداية</option>
                <option value="خنشلة">خنشلة</option>
                <option value="سوق أهراس">سوق أهراس</option>
                <option value="أم البواقي">أم البواقي</option>
                <option value="بسكرة">بسكرة</option>
                <option value="الطارف">الطارف</option>
                <option value="تندوف">تندوف</option>
                <option value="الجلفة">الجلفة</option>
                <option value="سعيدة">سعيدة</option>
                <option value="ميلة">ميلة</option>
                <option value="عين الدفلة">عين الدفلة</option>
                <option value="غليزان">غليزان</option>
                <option value="تامنغاست">تامنغاست</option>
                <option value="أدرار">أدرار</option>
                <option value="المدية">المدية</option>
                <option value="معسكر">معسكر</option>
                <option value="الشلف">الشلف</option>
                <option value="النعامة">النعامة</option>
                <option value="تقرت">تقرت</option>
                <option value="البيض">البيض</option>
                <option value="إليزي">إليزي</option>
                <option value="تندوف">تندوف</option>
                <option value="تميموسان">تميموسان</option>
                <option value="ورقلة">ورقلة</option>
                <option value="غرداية">غرداية</option>
                <option value="خنشلة">خنشلة</option>
                <option value="سوق أهراس">سوق أهراس</option>
                <option value="أم البواقي">أم البواقي</option>
                <option value="بسكرة">بسكرة</option>
                <option value="خنشلة">خنشلة</option>
                <option value="سوق أهراس">سوق أهراس</option>
                <option value="أم البواقي">أم البواقي</option>
                <option value="بسكرة">بسكرة</option>
                <option value="الجلفة">الجلفة</option>
                <option value="سعيدة">سعيدة</option>
                <option value="ميلة">ميلة</option>
                <option value="عين الدفلة">عين الدفلة</option>
                <option value="غليزان">غليزان</option>
                <option value="تامنغاست">تامنغاست</option>
                <option value="أدرار">أدرار</option>
                <option value="المدية">المدية</option>
                <option value="معسكر">معسكر</option>
                <option value="الشلف">الشلف</option>
                <option value="النعامة">النعامة</option>
                <option value="تقرت">تقرت</option>
                <option value="البيض">البيض</option>
                <option value="إليزي">إليزي</option>
                <option value="تندوف">تندوف</option>
                <option value="تميموسان">تميموسان</option>
                <option value="ورقلة">ورقلة</option>
                <option value="غرداية">غرداية</option>
                <option value="خنشلة">خنشلة</option>
                <option value="سوق أهراس">سوق أهراس</option>
                <option value="أم البواقي">أم البواقي</option>
                <option value="بسكرة">بسكرة</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">العنوان *</label>
            <input 
              type="text" 
              v-model="addressForm.address" 
              class="form-input"
              placeholder="الشارع، المبنى، الرقم"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">ملاحظات التوصيل</label>
            <textarea 
              v-model="addressForm.instructions" 
              class="form-textarea"
              placeholder="أي ملاحظات إضافية للتوصيل (اختياري)"
              rows="3"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeModal">
              إلغاء
            </button>
            <button type="submit" class="save-btn" :disabled="loading">
              <i class="fa-solid fa-save"></i>
              <span v-if="!loading">{{ editingAddress ? 'تحديث' : 'حفظ' }}</span>
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
const editingAddress = ref(null);

const addresses = ref([]);

const addressForm = reactive({
  title: '',
  name: '',
  phone: '',
  wilaya: '',
  address: '',
  instructions: ''
});

// Mock data - في الواقع سيتم جلبها من GraphQL
const mockAddresses = [
  {
    id: 1,
    title: 'المنزل',
    name: 'أحمد محمد',
    phone: '+213 66 123 4567',
    wilaya: 'الجزائر',
    address: 'شارع العربي بن مهدي، رقم 45، الدائرة 1',
    instructions: 'بجانب البنك، الطابق الثاني',
    isDefault: true
  },
  {
    id: 2,
    title: 'العمل',
    name: 'أحمد محمد',
    phone: '+213 66 123 4567',
    wilaya: 'الجزائر',
    address: 'مركز الأعمال، شارع ديدوش مراد، رقم 12',
    instructions: 'استقبال في الطابق الأول',
    isDefault: false
  }
];

const closeModal = () => {
  showAddForm.value = false;
  editingAddress.value = null;
  resetForm();
};

const resetForm = () => {
  Object.assign(addressForm, {
    title: '',
    name: '',
    phone: '',
    wilaya: '',
    address: '',
    instructions: ''
  });
};

const editAddress = (address) => {
  editingAddress.value = address;
  Object.assign(addressForm, address);
};

const saveAddress = async () => {
  try {
    loading.value = true;
    
    // TODO: Implement GraphQL mutation to save address
    console.log('Save address:', addressForm);
    
    if (editingAddress.value) {
      // Update existing address
      const index = addresses.value.findIndex(a => a.id === editingAddress.value.id);
      if (index !== -1) {
        addresses.value[index] = { ...addressForm, id: editingAddress.value.id };
      }
    } else {
      // Add new address
      const newAddress = {
        ...addressForm,
        id: Date.now(),
        isDefault: addresses.value.length === 0
      };
      addresses.value.push(newAddress);
    }
    
    closeModal();
  } catch (error) {
    console.error('Error saving address:', error);
  } finally {
    loading.value = false;
  }
};

const deleteAddress = async (addressId) => {
  if (confirm('هل أنت متأكد من حذف هذا العنوان؟')) {
    try {
      // TODO: Implement GraphQL mutation to delete address
      console.log('Delete address:', addressId);
      
      addresses.value = addresses.value.filter(a => a.id !== addressId);
    } catch (error) {
      console.error('Error deleting address:', error);
    }
  }
};

const setDefault = async (addressId) => {
  try {
    // TODO: Implement GraphQL mutation to set default address
    console.log('Set default address:', addressId);
    
    addresses.value.forEach(address => {
      address.isDefault = address.id === addressId;
    });
  } catch (error) {
    console.error('Error setting default address:', error);
  }
};

const loadAddresses = async () => {
  try {
    loading.value = true;
    
    // TODO: Implement GraphQL query to fetch addresses
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    addresses.value = mockAddresses;
  } catch (error) {
    console.error('Error loading addresses:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadAddresses();
});
</script>

<style scoped>
/* ===== Addresses Page ===== */
.addresses-page {
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

/* Addresses Container */
.addresses-container {
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
.addresses-header {
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

.add-address-btn {
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

.add-address-btn:hover {
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

/* Addresses Grid */
.addresses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.address-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.address-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
}

.address-card.default {
  border-color: rgba(212, 175, 55, 0.3);
  background: rgba(212, 175, 55, 0.05);
}

.address-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.address-info {
  flex: 1;
}

.address-title {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.address-name {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 0;
}

.address-actions {
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

.address-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.address-line {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.address-line i {
  color: #d4af37;
  width: 16px;
  text-align: center;
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
.address-modal {
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

.address-form {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.form-input,
.form-textarea {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus,
.form-textarea:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
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
  .addresses-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .addresses-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .addresses-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .address-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .address-actions {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
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
