<template>
  <div class="privacy-container">
    <h1>
      <i class="fa-solid fa-shield-alt"></i>
      <span>{{ $t('privacyPageTitle') }}</span>
    </h1>

    <!-- مقدمة -->
    <div class="intro-box">
      <p>{{ $t('privacyIntroText') }}</p>
    </div>

    <!-- البند 1 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-database"></i>
        <span>{{ $t('privacySection1Title') }}</span>
      </h2>
      <ul>
        <li>{{ $t('privacySection1Item1') }}</li>
        <li>{{ $t('privacySection1Item2') }}</li>
      </ul>
      <div class="info-box">
        <p><i class="fa-solid fa-info-circle"></i> {{ $t('privacySection1Note') }}</p>
      </div>
    </div>

    <!-- البند 2 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-chart-line"></i>
        <span>{{ $t('privacySection2Title') }}</span>
      </h2>
      <ul>
        <li>{{ $t('privacySection2Item1') }}</li>
        <li>{{ $t('privacySection2Item2') }}</li>
        <li>{{ $t('privacySection2Item3') }}</li>
      </ul>
    </div>

    <!-- البند 3 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-lock"></i>
        <span>{{ $t('privacySection3Title') }}</span>
      </h2>
      <p>{{ $t('privacySection3Text') }}</p>
      <div class="warning-box">
        <p><i class="fa-solid fa-shield-alt"></i> {{ $t('privacySection3Note') }}</p>
      </div>
    </div>

    <!-- البند 4 - حقوق الملكية الفكرية -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-copyright"></i>
        <span>{{ $t('privacySection4Title') }}</span>
      </h2>
      <ul>
        <li>{{ $t('privacySection4Item1') }}</li>
        <li>{{ $t('privacySection4Item2') }}</li>
        <li>{{ $t('privacySection4Item3') }}</li>
      </ul>
      <div class="warning-box">
        <p>
          <strong>{{ $t('privacySection4Warning') }}</strong>
          {{ $t('privacySection4WarningText') }}
        </p>
      </div>
    </div>

    <!-- البند 5 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-share-alt"></i>
        <span>{{ $t('privacySection5Title') }}</span>
      </h2>
      <p>{{ $t('privacySection5Text') }}</p>
    </div>

    <!-- البند 6 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-link"></i>
        <span>{{ $t('privacySection6Title') }}</span>
      </h2>
      <p>{{ $t('privacySection6Text') }}</p>
    </div>

    <!-- البند 7 -->
    <div class="section-card">
      <h2>
        <i class="fa-solid fa-sync-alt"></i>
        <span>{{ $t('privacySection7Title') }}</span>
      </h2>
      <p>{{ $t('privacySection7Text') }}</p>
    </div>

    <!-- البند 8 - التواصل -->
    <div class="contact-card">
      <h2>
        <i class="fa-solid fa-headset"></i>
        <span>{{ $t('privacySection8Title') }}</span>
      </h2>
      <p>{{ $t('privacySection8Text') }}</p>

      <div class="contact-grid">
        <!-- البريد الإلكتروني -->
        <div class="contact-info">
          <div class="contact-icon">
            <i class="fa-solid fa-envelope"></i>
          </div>
          <div class="contact-details">
            <strong>{{ $t('privacyContactEmailTitle') }}</strong>
            <a href="mailto:remadnamansour7@gmail.com">remadnamansour7@gmail.com</a>
          </div>
        </div>

        <!-- رقم الهاتف -->
        <div class="contact-info">
          <div class="contact-icon">
            <i class="fa-solid fa-phone-alt"></i>
          </div>
          <div class="contact-details">
            <strong>{{ $t('privacyContactPhoneTitle') }}</strong>
            <a href="tel:0663140341">0663140341</a>
          </div>
        </div>

        <!-- واتساب -->
        <div class="contact-info">
          <div class="contact-icon">
            <i class="fab fa-whatsapp"></i>
          </div>
          <div class="contact-details">
            <strong>{{ $t('privacyContactWhatsappTitle') }}</strong>
            <a href="https://wa.me/213663140341" target="_blank" rel="noopener noreferrer"
              >0663140341</a
            >
          </div>
        </div>

        <!-- فيسبوك -->
        <div class="contact-info">
          <div class="contact-icon">
            <i class="fab fa-facebook-f"></i>
          </div>
          <div class="contact-details">
            <strong>{{ $t('privacyContactFacebookTitle') }}</strong>
            <a
              href="https://www.facebook.com/profile.php?id=61588391030740"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ $t('facebookPage') }}
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- تاريخ آخر تحديث -->
    <div class="last-updated">
      <i class="fa-solid fa-calendar-alt"></i>
      <span>{{ $t('privacyLastUpdated') }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrivacyView',
};
</script>

<style scoped>
.privacy-container {
  max-width: 900px;
  margin: 0 auto;
  font-family: var(--font-arabic, 'Cairo', sans-serif);
  line-height: 1.9;
  color: var(--text-primary, #ffffff);
  padding: 20px;
}

.privacy-container h1 {
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.privacy-container h1 i {
  font-size: 2.5rem;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.privacy-container h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  border-radius: 3px;
}

.privacy-container .intro-box {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 25px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-soft, 0 8px 32px rgba(0, 0, 0, 0.4));
}

.privacy-container .intro-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
}

.privacy-container .intro-box p {
  margin: 0;
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.1rem;
  line-height: 1.8;
}

.privacy-container .section-card {
  background: var(--bg-card, #222222);
  padding: 25px;
  border-radius: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.privacy-container .section-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold, 0 4px 20px rgba(212, 175, 55, 0.2));
  border-color: var(--gold-primary, #d4af37);
}

.privacy-container .section-card:nth-child(even) {
  background: var(--bg-surface, #2a2a2a);
}

.privacy-container h2 {
  color: var(--gold-primary, #d4af37);
  font-size: 1.4rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-subtle, #333333);
}

.privacy-container h2 i {
  font-size: 1.6rem;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.privacy-container p {
  color: var(--text-secondary, #e0e0e0);
  margin-bottom: 15px;
  font-size: 1rem;
  line-height: 1.8;
}

.privacy-container p:last-child {
  margin-bottom: 0;
}

.privacy-container ul {
  list-style: none;
  padding: 0;
  margin: 15px 0 5px;
}

.privacy-container ul li {
  color: var(--text-secondary, #e0e0e0);
  margin-bottom: 15px;
  padding-right: 30px;
  position: relative;
  font-size: 1rem;
  line-height: 1.8;
}

body[dir='ltr'] .privacy-container ul li {
  padding-right: 0;
  padding-left: 30px;
}

.privacy-container ul li::before {
  content: '\f00c';
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
  position: absolute;
  right: 0;
  color: var(--gold-primary, #d4af37);
  font-size: 1rem;
}

body[dir='ltr'] .privacy-container ul li::before {
  right: auto;
  left: 0;
}

.privacy-container .warning-box {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid var(--gold-primary, #d4af37);
  color: var(--text-primary, #ffffff);
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0 10px;
  position: relative;
  overflow: hidden;
}

.privacy-container .warning-box::before {
  content: '⚠️';
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 1.5rem;
  opacity: 0.3;
}

body[dir='ltr'] .privacy-container .warning-box::before {
  right: auto;
  left: 15px;
}

.privacy-container .warning-box p {
  margin: 0;
  color: var(--text-primary, #ffffff);
  font-weight: 500;
}

.privacy-container .info-box {
  background: var(--bg-card, #222222);
  border: 1px solid var(--gold-primary, #d4af37);
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0 10px;
}

.privacy-container .contact-card {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  margin-top: 25px;
  position: relative;
  overflow: hidden;
}

.privacy-container .contact-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
}

.privacy-container .contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.privacy-container .contact-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: var(--bg-card, #222222);
  border-radius: 15px;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.3s ease;
}

.privacy-container .contact-info:hover {
  transform: translateY(-3px);
  border-color: var(--gold-primary, #d4af37);
  box-shadow: var(--shadow-gold, 0 4px 20px rgba(212, 175, 55, 0.2));
}

.privacy-container .contact-icon {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg-deep, #0f0f0f);
  font-size: 1.5rem;
  flex-shrink: 0;
}

.privacy-container .contact-details {
  flex: 1;
}

.privacy-container .contact-details strong {
  display: block;
  color: var(--text-primary, #ffffff);
  margin-bottom: 5px;
  font-size: 1rem;
}

.privacy-container .contact-details a {
  color: var(--gold-primary, #d4af37);
  text-decoration: none;
  font-size: 1rem;
  word-break: break-word;
  transition: color 0.3s;
}

.privacy-container .contact-details a:hover {
  color: var(--gold-light, #ffd700);
  text-decoration: underline;
}

.privacy-container .last-updated {
  text-align: left;
  color: var(--text-muted, #a0a0a0);
  font-size: 0.9rem;
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px solid var(--border-subtle, #333333);
  display: flex;
  align-items: center;
  gap: 8px;
}

body[dir='ltr'] .privacy-container .last-updated {
  text-align: right;
}

.privacy-container .last-updated i {
  color: var(--gold-primary, #d4af37);
}

/* RTL Support */
body[dir='rtl'] .privacy-container .contact-info:hover {
  transform: translateY(-3px);
}

body[dir='rtl'] .privacy-container h2 i {
  margin-left: 10px;
  margin-right: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .privacy-container {
    padding: 15px;
  }

  .privacy-container h1 {
    font-size: 1.8rem;
  }

  .privacy-container h1 i {
    font-size: 2rem;
  }

  .privacy-container .intro-box {
    padding: 20px;
  }

  .privacy-container .section-card {
    padding: 20px;
  }

  .privacy-container h2 {
    font-size: 1.3rem;
  }

  .privacy-container .contact-grid {
    grid-template-columns: 1fr;
  }

  .privacy-container .contact-info {
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .privacy-container h1 {
    font-size: 1.6rem;
    flex-direction: column;
    gap: 10px;
  }

  .privacy-container h1 i {
    font-size: 1.8rem;
  }

  .privacy-container .section-card {
    padding: 15px;
  }

  .privacy-container h2 {
    font-size: 1.2rem;
  }

  .privacy-container p,
  .privacy-container ul li {
    font-size: 0.95rem;
  }

  .privacy-container .contact-info {
    flex-direction: column;
    text-align: center;
  }

  .privacy-container .contact-icon {
    margin-bottom: 10px;
  }
}
</style>
