<template>
  <div class="info-page container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow-sm border-0 rounded-lg overflow-hidden bg-card">
          <div class="card-header bg-surface border-bottom p-5 text-center">
            <h1 class="display-5 text-gold mb-3 font-weight-bold">
              <i class="fa-solid fa-question-circle me-3"></i> {{ $t('faq') || 'الأسئلة الشائعة' }}
            </h1>
            <p class="lead text-muted">{{ $t('faqIntro') || 'إليك إجابات لأكثر الأسئلة شيوعاً من عملائنا' }}</p>
          </div>

          <div class="card-body p-5">
            <div class="accordion" id="faqAccordion">
              <div v-for="(item, index) in faqItems" :key="index" class="accordion-item mb-3 border-0 rounded shadow-sm overflow-hidden">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button bg-light font-weight-bold text-dark" 
                    type="button" 
                    :class="{ collapsed: index !== 0 }"
                    data-bs-toggle="collapse" 
                    :data-bs-target="'#collapse' + index"
                    aria-expanded="index === 0 ? 'true' : 'false'"
                  >
                    {{ item.question }}
                  </button>
                </h2>
                <div 
                  :id="'collapse' + index" 
                  class="accordion-collapse collapse" 
                  :class="{ show: index === 0 }"
                  data-bs-parent="#faqAccordion"
                >
                  <div class="accordion-body bg-white text-secondary lead small">
                    {{ item.answer }}
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-5 p-5 bg-surface rounded-lg text-center shadow-gold">
              <h3 class="text-gold mb-3 font-weight-bold">{{ $t('stillHaveQuestions') || 'هل لديك أسئلة أخرى؟' }}</h3>
              <p class="text-white mb-4">{{ $t('contactUsFaq') || 'فريق دعمنا الفني جاهز للرد على استفساراتك عبر واتساب أو الهاتف.' }}</p>
              <div class="d-flex justify-content-center gap-3 flex-wrap">
                <a href="https://wa.me/213663140341" target="_blank" class="btn btn-success btn-lg px-4">
                  <i class="fab fa-whatsapp me-2"></i> واتساب
                </a>
                <router-link to="/contact" class="btn btn-gold btn-lg px-4">
                  <i class="fa-solid fa-envelope me-2"></i> اتصل بنا
                </router-link>
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
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const faqItems = computed(() => [
  {
    question: t('faq1Q') || 'هل يمكنني طلب مقاسات مخصصة غير الموجودة في الموقع؟',
    answer: t('faq1A') || 'نعم بكل تأكيد! يمكنك إدخال المقاسات التي تناسب مساحتك (الطول والعرض) في صفحة تفاصيل المنتج، وسيتم حساب السعر تلقائياً.'
  },
  {
    question: t('faq2Q') || 'كيف يتم تثبيت الملصقات على الجدران؟',
    answer: t('faq2A') || 'الملصقات ذاتية اللصق وسهلة التركيب. سنرسل لك دليلاً مطبوعاً مع كل طلب يشرح خطوات التركيب بدقة، كما يمكنك مشاهدة فيديوهات توضيحية على صفحتنا.'
  },
  {
    question: t('faq3Q') || 'ما هي خامات الطباعة المستخدمة؟',
    answer: t('faq3A') || 'نستخدم أفضل خامات الفينيل (Vinyl) المستوردة، وهي مقاومة للماء والحرارة وسهلة التنظيف، وتدوم لسنوات طويلة دون أن تفقد ألوانها.'
  },
  {
    question: t('faq4Q') || 'هل توفرون خدمة التركيب؟',
    answer: t('faq4A') || 'حالياً نوفر خدمة التوصيل فقط، لكن تصاميمنا مصممة لتكون سهلة التركيب لغير المحترفين. كما يمكننا ترشيح فنيين في منطقتك إذا دعت الحاجة.'
  },
  {
    question: t('faq5Q') || 'ما هي مدة تجهيز الطلب؟',
    answer: t('faq5A') || 'يستغرق تجهيز الطلبات المخصصة من 24 إلى 48 ساعة قبل شحنها. الطلبات الجاهزة تُشحن فور تأكيدها.'
  }
]);
</script>

<style scoped>
.bg-card { background: var(--bg-card); }
.bg-surface { background: var(--bg-surface); }
.text-gold { color: var(--gold-primary); }
.btn-gold { background: var(--gold-gradient); color: #000; border: none; font-weight: 700; }
.shadow-gold { box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1); }

.accordion-button:not(.collapsed) {
  background: rgba(212, 175, 55, 0.1);
  color: #000;
  box-shadow: none;
}

.accordion-button:focus {
  box-shadow: none;
  border-color: var(--gold-primary);
}

.accordion-button::after {
  background-size: 1rem;
}
</style>
