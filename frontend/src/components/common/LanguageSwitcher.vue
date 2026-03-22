<template>
  <div class="language-switcher" v-click-outside="closeMenu">
    <button 
      class="lang-btn" 
      @click="toggleLanguageMenu"
      aria-haspopup="true"
      :aria-expanded="showLanguageMenu"
      :aria-label="$t('chooseLanguage')"
    >
      <i class="fa-solid fa-globe" aria-hidden="true"></i>
      <span class="lang-text">{{
        currentLang === 'ar' ? 'AR' : currentLang === 'en' ? 'EN' : (currentLang === 'fr' ? 'FR' : currentLang.toUpperCase())
      }}</span>
      <i class="fa-solid fa-chevron-down" :class="{ 'rotate': showLanguageMenu }"></i>
    </button>
    
    <transition name="slide-up">
      <div 
        class="lang-dropdown" 
        v-if="showLanguageMenu"
        role="menu"
      >
        <div
          v-for="lang in languages"
          :key="lang.code"
          class="lang-option"
          :class="{ active: currentLang === lang.code }"
          @click="changeLanguage(lang.code)"
          role="menuitem"
          tabindex="0"
        >
          <div class="lang-info">
            <i class="fa-solid fa-language" aria-hidden="true"></i>
            <span>{{ lang.name }}</span>
          </div>
          <i v-if="currentLang === lang.code" class="fa-solid fa-check check-icon"></i>
        </div>

        <div class="dropdown-divider"></div>
        
        <!-- AI Translation Option -->
        <div 
          class="lang-option ai-option"
          @click="handleAITranslate"
          role="menuitem"
          tabindex="0"
        >
          <div class="lang-info">
            <i class="fa-solid fa-robot ai-icon" aria-hidden="true"></i>
            <span>{{ $t('aiTranslate') || 'ترجمة بالذكاء الاصطناعي' }}</span>
          </div>
          <div class="ai-badge">AI</div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue';
import { useI18n } from 'vue-i18n';
import AIService from '@/integration/services/AIService';

const { locale, t } = useI18n();
const aiTranslate = inject('aiTranslate');
const aiState = inject('aiState');

const showLanguageMenu = ref(false);
const isTranslating = ref(false);
const languages = [
  { code: 'ar', name: 'العربية' },
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'Français' },
];

const currentLang = computed(() => locale.value);

const toggleLanguageMenu = () => {
  showLanguageMenu.value = !showLanguageMenu.value;
};

const closeMenu = () => {
  showLanguageMenu.value = false;
};

const changeLanguage = (lang) => {
  locale.value = lang;
  localStorage.setItem('language', lang);
  document.documentElement.lang = lang;
  document.body.dir = lang === 'ar' ? 'rtl' : 'ltr';
  showLanguageMenu.value = false;
  
  // Dispatch a global event for language change if needed
  window.dispatchEvent(new CustomEvent('language-changed', { detail: lang }));
};

const handleAITranslate = async () => {
  showLanguageMenu.value = false;
  
  if (currentLang.value === 'ar') {
    alert(t('aiSelectLanguageFirst') || 'يرجى اختيار لغة غير العربية أولاً للترجمة');
    return;
  }

  isTranslating.value = true;
  console.log('AI Translation requested for locale:', currentLang.value);
  
  try {
    // ترجمة العناصر التي تحمل توجيه v-ai-t تلقائياً
    // بالإضافة إلى ذلك، سنبحث عن أي نص غير مترجم في الصفحة (اختياري)
    const elementsToTranslate = document.querySelectorAll('[v-ai-t]');
    // Note: directives handle this automatically through state change
    
    // We can also trigger a global "AI Mode" that component can react to
    aiState.isAITranslateEnabled = true;
    localStorage.setItem('ai_translate_enabled', 'true');
    
    alert(t('aiTranslationStarted') || 'بدأت الترجمة الذكية للمحتوى المفتوح حالياً');
  } catch (error) {
    console.error('AI Translation Error:', error);
  } finally {
    isTranslating.value = false;
  }
};

// Custom directive for clicking outside
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
};
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.lang-btn {
  background: var(--bg-surface, rgba(255, 255, 255, 0.05));
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1));
  color: var(--text-main, #fff);
  padding: 8px 15px;
  border-radius: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 0.9rem;
  font-weight: 600;
}

.lang-btn:hover {
  border-color: var(--gold-primary, #d4af37);
  background: rgba(212, 175, 55, 0.1);
  transform: translateY(-1px);
}

.lang-btn .fa-chevron-down {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
  opacity: 0.7;
}

.lang-btn .fa-chevron-down.rotate {
  transform: rotate(180deg);
}

.lang-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background: var(--bg-card, #1a1a2e);
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1));
  border-radius: 16px;
  min-width: 200px;
  padding: 8px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  backdrop-filter: blur(15px);
}

[dir="rtl"] .lang-dropdown {
  right: auto;
  left: 0;
}

.lang-option {
  padding: 12px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  color: var(--text-secondary, #a0a0a0);
}

.lang-option:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--gold-primary, #d4af37);
  padding-inline-start: 20px;
}

.lang-option.active {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-primary, #d4af37);
  font-weight: 700;
}

.lang-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.check-icon {
  font-size: 0.8rem;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-subtle, rgba(255, 255, 255, 0.1));
  margin: 8px;
}

.ai-option {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, rgba(212, 175, 55, 0.1) 100%);
  border: 1px solid rgba(212, 175, 55, 0.1);
}

.ai-option:hover {
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  color: #1a1a2e;
}

.ai-icon {
  color: var(--gold-primary, #d4af37);
}

.ai-option:hover .ai-icon {
  color: #1a1a2e;
}

.ai-badge {
  font-size: 0.65rem;
  background: var(--gold-primary, #d4af37);
  color: #1a1a2e;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 800;
}

.ai-option:hover .ai-badge {
  background: #1a1a2e;
  color: var(--gold-primary, #d4af37);
}

/* Transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
