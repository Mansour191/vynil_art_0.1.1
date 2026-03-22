<template>
  <div class="terms-container">
    <h1>
      <span>{{ $t('termsPageTitle') }}</span>
    </h1>

    <!-- مقدمة -->
    <div class="intro-box">
      <p>{{ $t('termsIntroText') }}</p>
    </div>

    <!-- البند 1 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-newspaper"></i>
        <span>{{ $t('termsSection1Title') }}</span>
      </h2>
      <p>{{ $t('termsSection1Text') }}</p>
    </div>

    <!-- البند 2 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-copyright"></i>
        <span>{{ $t('termsSection2Title') }}</span>
      </h2>
      <p>{{ $t('termsSection2Text') }}</p>
    </div>

    <!-- البند 3 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-check-circle"></i>
        <span>{{ $t('termsSection3Title') }}</span>
      </h2>
      <p>{{ $t('termsSection3Text') }}</p>
    </div>

    <!-- البند 4 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-shopping-cart"></i>
        <span>{{ $t('termsSection4Title') }}</span>
      </h2>
      <p>{{ $t('termsSection4Text') }}</p>
    </div>

    <!-- البند 5 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-external-link-alt"></i>
        <span>{{ $t('termsSection5Title') }}</span>
      </h2>
      <p>{{ $t('termsSection5Text') }}</p>
    </div>

    <!-- البند 6 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-edit"></i>
        <span>{{ $t('termsSection6Title') }}</span>
      </h2>
      <p>{{ $t('termsSection6Text') }}</p>
    </div>

    <!-- البند 7 مع معلومات التواصل -->
    <div class="contact-card">
      <h2>
        <i class="fa-solid fa-headset"></i>
        <span>{{ $t('termsSection7Title') }}</span>
      </h2>
      <p>{{ $t('termsSection7Intro') }}</p>

      <!-- البريد الإلكتروني -->
      <div class="contact-info">
        <div class="contact-icon">
          <i class="fa-solid fa-envelope"></i>
        </div>
        <div class="contact-details">
          <strong>{{ $t('termsContactEmailTitle') }}</strong>
          <a href="mailto:remadnamansour7@gmail.com">remadnamansour7@gmail.com</a>
        </div>
      </div>

      <!-- رقم الهاتف -->
      <div class="contact-info">
        <div class="contact-icon">
          <i class="fa-solid fa-phone-alt"></i>
        </div>
        <div class="contact-details">
          <strong>{{ $t('termsContactPhoneTitle') }}</strong>
          <a href="tel:0663140341">0663140341</a>
        </div>
      </div>

      <!-- واتساب -->
      <div class="contact-info">
        <div class="contact-icon">
          <i class="fab fa-whatsapp"></i>
        </div>
        <div class="contact-details">
          <strong>{{ $t('termsContactWhatsappTitle') }}</strong>
          <a href="https://wa.me/213663140341" target="_blank" rel="noopener noreferrer"
            >0663140341</a
          >
        </div>
      </div>
    </div>

    <!-- تاريخ آخر تحديث -->
    <p class="last-updated">
      <i class="fa-solid fa-calendar-alt"></i>
      <span>{{ $t('termsLastUpdated') }}</span>
    </p>
  </div>
</template>

<script>
export default {
  name: 'TermsView',
};
</script>

<style scoped>
.terms-container {
  max-width: 900px;
  margin: 0 auto;
  font-family: var(--font-arabic, 'Cairo', sans-serif);
  line-height: 1.9;
  color: var(--text-primary, #ffffff);
  padding: 20px;
}

.terms-container h1 {
  text-align: center;
  margin-bottom: 35px;
  font-size: 2.2rem;
  font-weight: 700;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 50%, #d4af37 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  padding-bottom: 15px;
}

.terms-container h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  border-radius: 3px;
}

.terms-container .intro-box {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 25px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  overflow: hidden;
}

.terms-container .intro-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
}

.terms-container .intro-box p {
  margin: 0;
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.1rem;
}

.terms-container .section-card {
  background: var(--bg-card, #222222);
  padding: 25px;
  border-radius: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.terms-container .section-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold, 0 4px 20px rgba(212, 175, 55, 0.2));
  border-color: var(--gold-primary, #d4af37);
}

.terms-container .section-card:nth-child(even) {
  background: var(--bg-surface, #2a2a2a);
}

.terms-container h2 {
  color: var(--gold-primary, #d4af37);
  font-size: 1.4rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.terms-container h2 i {
  font-size: 1.6rem;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.terms-container p {
  color: var(--text-secondary, #e0e0e0);
  margin-bottom: 15px;
  font-size: 1rem;
  line-height: 1.8;
}

.terms-container p:last-child {
  margin-bottom: 0;
}

.terms-container .contact-card {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  margin-top: 25px;
}

.terms-container .contact-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px;
  background: var(--bg-card, #222222);
  border-radius: 15px;
  margin-top: 15px;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.3s ease;
}

.terms-container .contact-info:hover {
  transform: translateX(-5px);
  border-color: var(--gold-primary, #d4af37);
}

[dir='ltr'] .terms-container .contact-info:hover {
  transform: translateX(5px);
}

.terms-container .contact-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg-deep, #0f0f0f);
  font-size: 1.3rem;
  flex-shrink: 0;
}

.terms-container .contact-details {
  flex: 1;
}

.terms-container .contact-details strong {
  display: block;
  color: var(--text-primary, #ffffff);
  margin-bottom: 5px;
  font-size: 0.95rem;
}

.terms-container .contact-details a {
  color: var(--gold-primary, #d4af37);
  text-decoration: none;
  font-size: 1rem;
  word-break: break-word;
}

.terms-container .contact-details a:hover {
  text-decoration: underline;
}

.terms-container .last-updated {
  text-align: left;
  color: var(--text-muted, #a0a0a0);
  font-size: 0.9rem;
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px solid var(--border-subtle, #333333);
}

[dir='ltr'] .terms-container .last-updated {
  text-align: right;
}

.terms-container .last-updated i {
  color: var(--gold-primary, #d4af37);
  margin-left: 5px;
}

[dir='ltr'] .terms-container .last-updated i {
  margin-left: 0;
  margin-right: 5px;
}

/* RTL Support */
[dir='rtl'] .terms-container h2 i {
  margin-left: 10px;
  margin-right: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .terms-container {
    padding: 15px;
  }

  .terms-container h1 {
    font-size: 1.8rem;
  }

  .terms-container .intro-box {
    padding: 20px;
  }

  .terms-container .section-card {
    padding: 20px;
  }

  .terms-container h2 {
    font-size: 1.3rem;
  }

  .terms-container .contact-info {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .terms-container .contact-info:hover {
    transform: translateY(-3px);
  }

  [dir='rtl'] .terms-container .contact-info:hover {
    transform: translateY(-3px);
  }

  .terms-container .contact-icon {
    margin-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .terms-container h1 {
    font-size: 1.6rem;
  }

  .terms-container .section-card {
    padding: 15px;
  }

  .terms-container h2 {
    font-size: 1.2rem;
  }

  .terms-container p {
    font-size: 0.95rem;
  }
}
</style>
