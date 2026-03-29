<template>
  <div class="product-specs-info mt-4">
    <div class="row g-3">
      <div v-for="spec in specs" :key="spec.label" class="col-6 col-md-3">
        <div class="spec-card p-3 rounded-lg bg-light text-center h-100 transition-all border border-transparent hover-border-gold">
          <i :class="['fas mb-2 d-block fs-4 text-gold', spec.icon]"></i>
          <span class="d-block small text-muted text-uppercase mb-1">{{ $t(spec.label) || spec.label }}</span>
          <span class="d-block font-weight-bold small text-dark">{{ spec.value }}</span>
        </div>
      </div>
    </div>

    <!-- Additional Info Tabs -->
    <div class="info-tabs mt-5">
      <ul class="nav nav-pills mb-4 border-bottom pb-2" id="pills-tab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active bg-transparent text-dark font-weight-bold" id="pills-shipping-tab" data-bs-toggle="pill" data-bs-target="#pills-shipping" type="button" role="tab">{{ $t('shippingInfo') || 'الشحن والتوصيل' }}</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link bg-transparent text-dark font-weight-bold" id="pills-return-tab" data-bs-toggle="pill" data-bs-target="#pills-return" type="button" role="tab">{{ $t('returnPolicy') || 'سياسة الإرجاع' }}</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link bg-transparent text-dark font-weight-bold" id="pills-install-tab" data-bs-toggle="pill" data-bs-target="#pills-install" type="button" role="tab">{{ $t('installGuide') || 'دليل التركيب' }}</button>
        </li>
      </ul>
      
      <div class="tab-content bg-white p-4 rounded-lg shadow-sm border" id="pills-tabContent">
        <div class="tab-pane fade show active" id="pills-shipping" role="tabpanel">
          <div class="d-flex align-items-center gap-3 mb-3">
            <i class="fa-solid fa-truck text-gold fs-3"></i>
            <div>
              <h6 class="mb-1 font-weight-bold">وقت التوصيل المتوقع</h6>
              <p class="mb-0 text-muted small">يتم توصيل هذا المنتج خلال 2 - 5 أيام عمل لجميع الولايات.</p>
            </div>
          </div>
          <div class="d-flex align-items-center gap-3">
            <i class="fa-solid fa-shield-alt text-gold fs-3"></i>
            <div>
              <h6 class="mb-1 font-weight-bold">الضمان</h6>
              <p class="mb-0 text-muted small">ضمان لمدة سنة على ثبات الألوان وجودة الخامة ضد الماء والحرارة.</p>
            </div>
          </div>
        </div>
        
        <div class="tab-pane fade" id="pills-return" role="tabpanel">
          <p class="text-muted small">يمكنك إرجاع المنتج خلال 14 يوماً من الاستلام في حال وجود عيب مصنعي أو خطأ في المواصفات المطلوبة.</p>
          <ul class="text-muted small ps-3">
            <li>يجب أن يكون المنتج في حالته الأصلية وتغليفه الأصلي.</li>
            <li>لا يمكن إرجاع المنتجات المخصصة بالمقاسات إلا في حال وجود عيب مصنعي.</li>
          </ul>
        </div>

        <div class="tab-pane fade" id="pills-install" role="tabpanel">
          <div class="text-center py-3">
            <i class="fa-solid fa-file-pdf fa-3x text-danger mb-3"></i>
            <h6 class="font-weight-bold">دليل التركيب (PDF)</h6>
            <p class="text-muted small mb-3">قم بتحميل دليل التركيب الموضح خطوة بخطوة لضمان أفضل نتيجة.</p>
            <a href="#" class="btn btn-outline-dark btn-sm rounded-pill px-4">تحميل الدليل</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  specs: { type: Array, default: () => [] }
});
</script>

<style scoped>
.text-gold { color: var(--gold-primary); }
.hover-border-gold:hover { border-color: var(--gold-primary) !important; transform: translateY(-3px); }
.transition-all { transition: all 0.3s ease; }

.nav-pills .nav-link {
  border-radius: 0;
  border-bottom: 3px solid transparent;
  padding: 10px 20px;
  transition: all 0.3s;
}

.nav-pills .nav-link.active {
  border-bottom-color: var(--gold-primary);
  color: var(--gold-primary) !important;
}

.tab-pane {
  min-height: 150px;
}
</style>
