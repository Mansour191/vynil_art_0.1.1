<template>
  <div class="user-guide-page container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <!-- Header -->
        <div class="card shadow-sm border-0 rounded-lg overflow-hidden bg-card mb-5">
          <div class="card-header bg-surface border-bottom p-5 text-center">
            <h1 class="display-5 text-gold mb-3 font-weight-bold">
              <i class="fa-solid fa-book-reader me-3"></i> {{ $t('userGuide') || 'دليل المستخدم للمبتدئين' }}
            </h1>
            <p class="lead text-muted">{{ $t('userGuideIntro') || 'كل ما تحتاجه لتبدأ رحلتك مع فينيل آرت باحترافية' }}</p>
          </div>

          <div class="card-body p-5">
            <!-- Beginner's Steps -->
            <section class="mb-5">
              <h2 class="h3 text-gold mb-4 border-bottom pb-2 font-weight-bold">
                <i class="fa-solid fa-rocket me-2"></i> البداية السريعة
              </h2>
              <div class="row g-4">
                <div v-for="(step, index) in steps" :key="index" class="col-md-4">
                  <div class="guide-step-card p-4 rounded-lg bg-light h-100 text-center shadow-sm hover-shadow transition-all">
                    <div class="step-num mb-3">{{ index + 1 }}</div>
                    <i :class="['fa-solid fa-2x text-gold mb-3', step.icon]"></i>
                    <h5 class="font-weight-bold">{{ step.title }}</h5>
                    <p class="text-secondary small mb-0">{{ step.desc }}</p>
                  </div>
                </div>
              </div>
            </section>

            <!-- Video Tutorials -->
            <section class="mb-5 pt-4">
              <h2 class="h3 text-gold mb-4 border-bottom pb-2 font-weight-bold">
                <i class="fa-solid fa-play-circle me-2"></i> دروس فيديو تعليمية
              </h2>
              <div class="row g-4">
                <div v-for="(video, index) in tutorials" :key="index" class="col-md-6">
                  <div class="video-card card border-0 shadow-sm rounded-lg overflow-hidden bg-surface h-100">
                    <div class="ratio ratio-16x9 bg-dark">
                      <iframe 
                        :src="video.embedUrl" 
                        title="YouTube video player" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen
                      ></iframe>
                    </div>
                    <div class="card-body">
                      <h5 class="card-title text-gold font-weight-bold">{{ video.title }}</h5>
                      <p class="card-text text-muted small mb-0">{{ video.desc }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Trusted & Quality Badges -->
            <section class="pt-4">
              <div class="p-5 bg-surface rounded-lg text-center shadow-gold border-gold-subtle">
                <h3 class="text-gold mb-4 font-weight-bold"><i class="fa-solid fa-award me-2"></i> ضمان الجودة والموثوقية</h3>
                <div class="d-flex justify-content-center gap-5 flex-wrap">
                  <div class="badge-item">
                    <i class="fa-solid fa-check-circle fa-3x text-success mb-3"></i>
                    <h6 class="text-white">موثوق ومجرب</h6>
                    <p class="small text-muted mb-0">أكثر من 5000+ عميل راضٍ</p>
                  </div>
                  <div class="badge-item">
                    <i class="fa-solid fa-shield-alt fa-3x text-gold mb-3"></i>
                    <h6 class="text-white">ضمان لمدة سنة</h6>
                    <p class="small text-muted mb-0">على جميع أنواع الطباعة</p>
                  </div>
                  <div class="badge-item">
                    <i class="fa-solid fa-hand-holding-heart fa-3x text-info mb-3"></i>
                    <h6 class="text-white">صديق للبيئة</h6>
                    <p class="small text-muted mb-0">خامات غير سامة وآمنة</p>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const steps = computed(() => [
  { icon: 'fa-user-plus', title: 'إنشاء حساب', desc: 'قم بإنشاء حسابك لتتبع طلباتك والحصول على خصومات حصرية.' },
  { icon: 'fa-search', title: 'تصفح التصاميم', desc: 'استخدم محرك البحث المتقدم للعثور على ما يناسب ذوقك.' },
  { icon: 'fa-pencil-ruler', title: 'التخصيص', desc: 'أدخل مقاساتك الخاصة واختر الألوان المناسبة لمساحتك.' }
]);

const tutorials = computed(() => [
  { 
    title: 'كيفية أخذ المقاسات بدقة', 
    desc: 'تعلم الطريقة الصحيحة لقياس الجدران والأسطح لتجنب أي أخطاء في الطلب.',
    embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ' // رابط تجريبي
  },
  { 
    title: 'طريقة تركيب الفينيل المخصص', 
    desc: 'خطوات بسيطة وسهلة لتركيب ملصقات الفينيل على الجدران دون فقاعات هواء.',
    embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ' // رابط تجريبي
  }
]);
</script>

<style scoped>
.bg-card { background: var(--bg-card); }
.bg-surface { background: var(--bg-surface); }
.text-gold { color: var(--gold-primary); }
.border-gold-subtle { border: 1px solid rgba(212, 175, 55, 0.2); }
.shadow-gold { box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1); }

.step-num {
  width: 35px;
  height: 35px;
  background: var(--gold-gradient);
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border-radius: 50%;
  margin: 0 auto;
}

.hover-shadow:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1) !important;
}

.transition-all {
  transition: all 0.3s ease;
}

.badge-item {
  width: 150px;
}
</style>
