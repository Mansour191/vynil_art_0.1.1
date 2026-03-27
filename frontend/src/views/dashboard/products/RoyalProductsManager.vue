<template>
  <div class="royal-products-manager marble-bg min-h-screen p-6">
    <!-- Header -->
    <div
      class="bg-white/80 backdrop-blur-md rounded-2xl shadow-marble p-6 mb-6"
      v-motion="fadeUpVariants"
    >
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-royal-600 to-gold-500 bg-clip-text text-transparent">
            <i class="fas fa-box mr-3"></i>
            إدارة المنتجات
          </h1>
          <p class="text-marble-600 mt-2">إدارة جميع منتجات الفينيل والتصاميم</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <Button
            icon="fas fa-plus"
            label="إضافة منتج"
            class="p-button-gold"
            @click="showAddDialog = true"
          />
          <Button
            icon="fas fa-upload"
            label="استيراد"
            class="p-button-outlined p-button-royal"
            @click="importProducts"
          />
          <Button
            icon="fas fa-download"
            label="تصدير"
            class="p-button-outlined p-button-royal"
            @click="exportProducts"
          />
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div
      class="bg-white/80 backdrop-blur-md rounded-2xl shadow-marble p-6 mb-6"
      v-motion="fadeUpVariants"
    >
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">البحث</label>
          <InputText
            v-model="filters.global.value"
            placeholder="بحث في المنتجات..."
            class="w-full"
          />
        </div>
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">الفئة</label>
          <Dropdown
            v-model="filters.category.value"
            :options="categories"
            placeholder="اختر الفئة"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">الحالة</label>
          <Dropdown
            v-model="filters.status.value"
            :options="statusOptions"
            placeholder="اختر الحالة"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">السعر</label>
          <Dropdown
            v-model="filters.priceRange.value"
            :options="priceRanges"
            placeholder="نطاق السعر"
            class="w-full"
            showClear
          />
        </div>
      </div>
    </div>

    <!-- Products Table -->
    <div
      class="card-royal"
      v-motion="fadeUpVariants"
    >
      <RoyalDataTable
        :data="products"
        :loading="loading"
        :filters="filters"
        :columns="tableColumns"
        title="قائمة المنتجات"
        :badge="products.length"
        badgeSeverity="info"
        @refresh="loadProducts"
        @export="exportProducts"
        @selection-change="onSelectionChange"
        selectionMode="multiple"
        :paginator="true"
        :rows="10"
        :rowsPerPageOptions="[10, 20, 50]"
        responsiveLayout="scroll"
        scrollHeight="600px"
        v-auto-animate
      >
        <template #column-actions="{ data }">
          <div class="flex items-center space-x-2">
            <Button
              icon="fas fa-eye"
              class="p-button-rounded p-button-text p-button-plain"
              @click="viewProduct(data)"
            />
            <Button
              icon="fas fa-edit"
              class="p-button-rounded p-button-text p-button-plain"
              @click="editProduct(data)"
            />
            <Button
              icon="fas fa-trash"
              class="p-button-rounded p-button-text p-button-plain p-button-danger"
              @click="deleteProduct(data)"
            />
          </div>
        </template>

        <template #column-status="{ data }">
          <Tag
            :value="getStatusText(data.status)"
            :severity="getStatusSeverity(data.status)"
            class="rounded-full"
          />
        </template>

        <template #column-price="{ data }">
          <div class="flex items-center space-x-2">
            <span class="font-medium text-marble-900">{{ formatCurrency(data.price) }}</span>
            <Tag
              v-if="data.discount"
              :value="`${data.discount}%`"
              severity="success"
              class="rounded-full text-xs"
            />
          </div>
        </template>

        <template #column-stock="{ data }">
          <div class="flex items-center space-x-2">
            <span class="font-medium">{{ data.stock }}</span>
            <div
              class="w-2 h-2 rounded-full"
              :class="getStockStatus(data.stock)"
            ></div>
          </div>
        </template>

        <template #column-image="{ data }">
          <Image
            :src="data.image || '/placeholder-product.png'"
            :alt="data.name"
            width="50"
            height="50"
            class="rounded-xl"
            preview
          />
        </template>
      </RoyalDataTable>
    </div>

    <!-- Add/Edit Product Dialog -->
    <Dialog
      v-model:visible="showAddDialog"
      :header="editingProduct ? 'تعديل منتج' : 'إضافة منتج جديد'"
      :modal="true"
      :style="{ width: '600px' }"
      class="royal-dialog"
    >
      <form @submit.prevent="saveProduct" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">اسم المنتج</label>
            <InputText
              v-model="productForm.name"
              placeholder="أدخل اسم المنتج"
              required
            />
          </div>
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">الفئة</label>
            <Dropdown
              v-model="productForm.category"
              :options="categories"
              placeholder="اختر الفئة"
              required
            />
          </div>
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">السعر</label>
            <InputNumber
              v-model="productForm.price"
              mode="currency"
              currency="DZD"
              placeholder="0.00"
              required
            />
          </div>
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">الخصم (%)</label>
            <InputNumber
              v-model="productForm.discount"
              :min="0"
              :max="100"
              placeholder="0"
            />
          </div>
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">المخزون</label>
            <InputNumber
              v-model="productForm.stock"
              :min="0"
              placeholder="0"
              required
            />
          </div>
          <div class="flex flex-col">
            <label class="text-sm font-medium text-marble-700 mb-2">الحالة</label>
            <Dropdown
              v-model="productForm.status"
              :options="statusOptions"
              placeholder="اختر الحالة"
              required
            />
          </div>
        </div>
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">الوصف</label>
          <Textarea
            v-model="productForm.description"
            rows="4"
            placeholder="أدخل وصف المنتج"
          />
        </div>
        <div class="flex flex-col">
          <label class="text-sm font-medium text-marble-700 mb-2">صورة المنتج</label>
          <div class="flex items-center space-x-4">
            <Image
              v-if="productForm.image"
              :src="productForm.image"
              :alt="productForm.name"
              width="100"
              height="100"
              class="rounded-xl"
              preview
            />
            <Button
              icon="fas fa-upload"
              label="رفع صورة"
              class="p-button-outlined p-button-royal"
              @click="uploadImage"
            />
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button
          label="إلغاء"
          class="p-button-outlined p-button-royal"
          @click="showAddDialog = false"
        />
        <Button
          label="حفظ"
          class="p-button-royal"
          @click="saveProduct"
          :loading="saving"
        />
      </template>
    </Dialog>

    <!-- Product Details Dialog -->
    <Dialog
      v-model:visible="showDetailsDialog"
      header="تفاصيل المنتج"
      :modal="true"
      :style="{ width: '800px' }"
      class="royal-dialog"
    >
      <div v-if="selectedProduct" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Image
              :src="selectedProduct.image || '/placeholder-product.png'"
              :alt="selectedProduct.name"
              class="rounded-xl w-full"
              preview
            />
          </div>
          <div class="space-y-4">
            <div>
              <h3 class="text-xl font-bold text-marble-900">{{ selectedProduct.name }}</h3>
              <p class="text-marble-600 mt-2">{{ selectedProduct.description }}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-marble-600">الفئة</p>
                <p class="font-medium text-marble-900">{{ selectedProduct.category }}</p>
              </div>
              <div>
                <p class="text-sm text-marble-600">السعر</p>
                <p class="font-medium text-marble-900">{{ formatCurrency(selectedProduct.price) }}</p>
              </div>
              <div>
                <p class="text-sm text-marble-600">المخزون</p>
                <p class="font-medium text-marble-900">{{ selectedProduct.stock }}</p>
              </div>
              <div>
                <p class="text-sm text-marble-600">الحالة</p>
                <Tag
                  :value="getStatusText(selectedProduct.status)"
                  :severity="getStatusSeverity(selectedProduct.status)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button
          label="إغلاق"
          class="p-button-royal"
          @click="showDetailsDialog = false"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useFadeInUp } from '@/composables/useAnimations';
import RoyalDataTable from '@/components/ui/RoyalDataTable.vue';
import { FilterMatchMode } from 'primevue/api';

const { variants: fadeUpVariants } = useFadeInUp();

// State
const loading = ref(false);
const saving = ref(false);
const showAddDialog = ref(false);
const showDetailsDialog = ref(false);
const editingProduct = ref(null);
const selectedProduct = ref(null);
const selectedProducts = ref([]);

const products = ref([
  {
    id: 1,
    name: 'فينيل ديكوري ذهبي',
    category: 'فينيل جدران',
    price: 2500,
    discount: 10,
    stock: 45,
    status: 'active',
    description: 'فينيل ديكوري عالي الجودة بتصميم ذهبي أنيق',
    image: '/api/placeholder/300/200'
  },
  {
    id: 2,
    name: 'فينيل أرضيات خشبي',
    category: 'فينيل أرضيات',
    price: 3200,
    discount: 0,
    stock: 23,
    status: 'active',
    description: 'فينيل أرضيات بتصميم خشبي طبيعي',
    image: '/api/placeholder/300/200'
  },
  {
    id: 3,
    name: 'فينيل سقف أزرق',
    category: 'فينيل أسقف',
    price: 1800,
    discount: 15,
    stock: 0,
    status: 'out_of_stock',
    description: 'فينيل سقف بلون أزرق سماوي',
    image: '/api/placeholder/300/200'
  }
]);

const productForm = ref({
  name: '',
  category: '',
  price: null,
  discount: 0,
  stock: null,
  status: '',
  description: '',
  image: ''
});

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  category: { value: null, matchMode: FilterMatchMode.EQUALS },
  status: { value: null, matchMode: FilterMatchMode.EQUALS },
  priceRange: { value: null, matchMode: FilterMatchMode.EQUALS }
});

// Options
const categories = ref(['فينيل جدران', 'فينيل أرضيات', 'فينيل أسقف', 'فينيل أبواب', 'فينيل نوافذ']);
const statusOptions = ref([
  { label: 'نشط', value: 'active' },
  { label: 'غير نشط', value: 'inactive' },
  { label: 'نفد المخزون', value: 'out_of_stock' }
]);
const priceRanges = ref([
  { label: 'أقل من 1000 دج', value: 'low' },
  { label: '1000 - 3000 دج', value: 'medium' },
  { label: 'أكثر من 3000 دج', value: 'high' }
]);

// Table columns
const tableColumns = ref([
  {
    field: 'image',
    header: 'الصورة',
    sortable: false
  },
  {
    field: 'name',
    header: 'اسم المنتج',
    sortable: true
  },
  {
    field: 'category',
    header: 'الفئة',
    sortable: true
  },
  {
    field: 'price',
    header: 'السعر',
    sortable: true
  },
  {
    field: 'stock',
    header: 'المخزون',
    sortable: true
  },
  {
    field: 'status',
    header: 'الحالة',
    sortable: true
  },
  {
    field: 'actions',
    header: 'الإجراءات',
    sortable: false
  }
]);

// Methods
const loadProducts = async () => {
  loading.value = true;
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    // Products already loaded
  } catch (error) {
    console.error('Error loading products:', error);
  } finally {
    loading.value = false;
  }
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ar-DZ', {
    style: 'currency',
    currency: 'DZD'
  }).format(value);
};

const getStatusText = (status) => {
  const statusMap = {
    active: 'نشط',
    inactive: 'غير نشط',
    out_of_stock: 'نفد المخزون'
  };
  return statusMap[status] || status;
};

const getStatusSeverity = (status) => {
  const severityMap = {
    active: 'success',
    inactive: 'warning',
    out_of_stock: 'danger'
  };
  return severityMap[status] || 'info';
};

const getStockStatus = (stock) => {
  if (stock === 0) return 'bg-red-500';
  if (stock < 10) return 'bg-yellow-500';
  return 'bg-green-500';
};

const viewProduct = (product) => {
  selectedProduct.value = product;
  showDetailsDialog.value = true;
};

const editProduct = (product) => {
  editingProduct.value = product;
  productForm.value = { ...product };
  showAddDialog.value = true;
};

const deleteProduct = (product) => {
  if (confirm(`هل أنت متأكد من حذف المنتج "${product.name}"؟`)) {
    // Delete logic here
    console.log('Deleting product:', product);
  }
};

const saveProduct = async () => {
  saving.value = true;
  try {
    // Save logic here
    await new Promise(resolve => setTimeout(resolve, 1000));
    showAddDialog.value = false;
    editingProduct.value = null;
    productForm.value = {
      name: '',
      category: '',
      price: null,
      discount: 0,
      stock: null,
      status: '',
      description: '',
      image: ''
    };
    await loadProducts();
  } catch (error) {
    console.error('Error saving product:', error);
  } finally {
    saving.value = false;
  }
};

const onSelectionChange = (event) => {
  selectedProducts.value = event.value;
};

const importProducts = () => {
  console.log('Import products');
};

const exportProducts = () => {
  console.log('Export products');
};

const uploadImage = () => {
  console.log('Upload image');
};

onMounted(() => {
  loadProducts();
});
</script>

<style scoped>
.royal-products-manager {
  font-family: 'Inter', system-ui, sans-serif;
}

:deep(.royal-dialog) {
  @apply bg-white rounded-2xl shadow-marble;
}

:deep(.royal-dialog .p-dialog-header) {
  @apply bg-gradient-to-r from-royal-50 to-marble-50 border-b border-marble-200 p-4;
}

:deep(.royal-dialog .p-dialog-content) {
  @apply p-4;
}

:deep(.royal-dialog .p-dialog-footer) {
  @apply bg-gradient-to-r from-royal-50 to-marble-50 border-t border-marble-200 p-4;
}

/* Auto animate classes */
.auto-animate {
  --auto-animate-duration: 0.3s;
  --auto-animate-easing: ease-in-out;
}
</style>
