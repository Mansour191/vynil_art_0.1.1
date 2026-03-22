<template>
  <div class="contact-page">
    <h1>
      <i class="fa-solid fa-headset"></i>
      <span>{{ $t('contactPageTitle') }}</span>
    </h1>

    <!-- رسالة الترحيب -->
    <div class="intro-box">
      <p>{{ $t('contactIntroText') }}</p>
    </div>

    <!-- بطاقات التواصل -->
    <div class="contact-grid">
      <!-- البريد الإلكتروني -->
      <div class="contact-card">
        <div class="contact-icon">
          <i class="fa-solid fa-envelope"></i>
        </div>
        <h3>{{ $t('contactEmailTitle') }}</h3>
        <div class="contact-label">{{ $t('contactEmailLabel') }}</div>
        <div class="contact-value">
          <a href="mailto:remadnamansour7@gmail.com">remadnamansour7@gmail.com</a>
        </div>
      </div>

      <!-- رقم الهاتف -->
      <div class="contact-card">
        <div class="contact-icon">
          <i class="fa-solid fa-phone-alt"></i>
        </div>
        <h3>{{ $t('contactPhoneTitle') }}</h3>
        <div class="contact-label">{{ $t('contactPhoneLabel') }}</div>
        <div class="contact-value">
          <a href="tel:0663140341">0663140341</a>
        </div>
      </div>

      <!-- واتساب -->
      <div class="contact-card">
        <div class="contact-icon">
          <i class="fab fa-whatsapp"></i>
        </div>
        <h3>{{ $t('contactWhatsappTitle') }}</h3>
        <div class="contact-label">{{ $t('contactWhatsappLabel') }}</div>
        <div class="contact-value">
          <a href="https://wa.me/213663140341" target="_blank">0663140341</a>
        </div>
      </div>
    </div>

    <!-- فيسبوك - بطاقة منفصلة -->
    <div class="facebook-card">
      <div class="facebook-content">
        <div class="facebook-icon">
          <i class="fab fa-facebook-f"></i>
        </div>
        <div class="facebook-text">
          <h3>{{ $t('contactFacebookTitle') }}</h3>
          <p>{{ $t('contactFacebookText') }}</p>
        </div>
        <a
          href="https://www.facebook.com/profile.php?id=61588391030740"
          target="_blank"
          class="facebook-button"
        >
          <i class="fab fa-facebook-f"></i>
          <span>{{ $t('contactFacebookButton') }}</span>
        </a>
      </div>
    </div>

    <!-- رسالة التقدير -->
    <div class="footer-box">
      <p>
        <i class="fa-solid fa-heart"></i>
        {{ $t('contactFooterText') }}
        <i class="fa-solid fa-heart"></i>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactView',
};
</script>

<style scoped>
.contact-page {
  max-width: 1000px;
  margin: 0 auto;
  font-family: var(--font-arabic, 'Cairo', sans-serif);
  line-height: 1.8;
  color: var(--text-primary, #ffffff);
  padding: 20px;
}

.contact-page h1 {
  text-align: center;
  margin-bottom: 35px;
  font-size: 2.4rem;
  font-weight: 800;
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

.contact-page h1 i {
  font-size: 2.8rem;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.contact-page h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  border-radius: 3px;
}

.contact-page .intro-box {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px 40px;
  border-radius: 25px;
  margin-bottom: 30px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-soft, 0 8px 32px rgba(0, 0, 0, 0.4));
  text-align: center;
}

.contact-page .intro-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
}

.contact-page .intro-box p {
  margin: 0;
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.15rem;
  line-height: 1.8;
}

.contact-page .contact-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 30px 0;
}

.contact-page .contact-card {
  background: var(--bg-card, #222222);
  padding: 30px 20px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.contact-page .contact-card:hover {
  transform: translateY(-8px);
  border-color: var(--gold-primary, #d4af37);
  box-shadow: var(--shadow-gold, 0 8px 25px rgba(212, 175, 55, 0.3));
}

.contact-page .contact-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, transparent 0%, rgba(212, 175, 55, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.contact-page .contact-card:hover::before {
  opacity: 1;
}

.contact-page .contact-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg-deep, #0f0f0f);
  font-size: 2rem;
  margin-bottom: 10px;
  transition: all 0.3s;
}

.contact-page .contact-card:hover .contact-icon {
  transform: scale(1.1) rotate(5deg);
}

.contact-page .contact-card h3 {
  color: var(--gold-primary, #d4af37);
  font-size: 1.3rem;
  margin-bottom: 5px;
  font-weight: 700;
}

.contact-page .contact-card .contact-label {
  color: var(--text-muted, #a0a0a0);
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.contact-page .contact-card .contact-value {
  color: var(--text-primary, #ffffff);
  font-size: 1.1rem;
  font-weight: 500;
  word-break: break-word;
  padding: 8px 20px;
  background: var(--bg-surface, #2a2a2a);
  border-radius: 50px;
  border: 1px solid var(--border-subtle, #333333);
  width: 100%;
  transition: all 0.3s;
}

.contact-page .contact-card:hover .contact-value {
  border-color: var(--gold-primary, #d4af37);
  background: var(--bg-deep, #0f0f0f);
}

.contact-page .contact-card .contact-value a {
  color: var(--text-primary, #ffffff);
  text-decoration: none;
  transition: color 0.3s;
}

.contact-page .contact-card .contact-value a:hover {
  color: var(--gold-primary, #d4af37);
}

.contact-page .facebook-card {
  grid-column: span 3;
  background: linear-gradient(135deg, var(--bg-card, #222222), var(--bg-surface, #2a2a2a));
  padding: 30px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  margin: 20px 0;
  transition: all 0.3s;
}

.contact-page .facebook-card:hover {
  border-color: #1877f2;
  box-shadow: 0 8px 25px rgba(24, 119, 242, 0.2);
}

.contact-page .facebook-card .facebook-content {
  display: flex;
  align-items: center;
  gap: 25px;
  flex-wrap: wrap;
}

.contact-page .facebook-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #1877f2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  flex-shrink: 0;
}

.contact-page .facebook-text {
  flex: 1;
}

.contact-page .facebook-text h3 {
  color: #1877f2;
  font-size: 1.4rem;
  margin-bottom: 8px;
}

.contact-page .facebook-text p {
  color: var(--text-secondary, #e0e0e0);
  font-size: 1rem;
}

.contact-page .facebook-button {
  background: #1877f2;
  color: white;
  padding: 15px 35px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.contact-page .facebook-button:hover {
  background: #0d65d9;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(24, 119, 242, 0.4);
}

.contact-page .footer-box {
  background: var(--bg-surface, #2a2a2a);
  padding: 30px 40px;
  border-radius: 25px;
  margin-top: 30px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  text-align: center;
}

.contact-page .footer-box p {
  margin: 0;
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.1rem;
  font-weight: 500;
}

.contact-page .footer-box i {
  color: var(--gold-primary, #d4af37);
  margin: 0 5px;
}

/* RTL Support */
body[dir='rtl'] .contact-page .contact-card:hover {
  transform: translateY(-8px);
}

body[dir='rtl'] .facebook-content {
  flex-direction: row-reverse;
}

/* Responsive Design */
@media (max-width: 992px) {
  .contact-page .contact-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .contact-page .facebook-card {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .contact-page {
    padding: 15px;
  }

  .contact-page h1 {
    font-size: 2rem;
  }

  .contact-page h1 i {
    font-size: 2.2rem;
  }

  .contact-page .intro-box {
    padding: 20px;
  }

  .contact-page .intro-box p {
    font-size: 1rem;
  }

  .contact-page .contact-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .contact-page .facebook-card {
    grid-column: span 1;
  }

  .contact-page .facebook-content {
    flex-direction: column;
    text-align: center;
  }

  body[dir='rtl'] .facebook-content {
    flex-direction: column;
  }

  .contact-page .facebook-button {
    width: 100%;
    justify-content: center;
  }

  .contact-page .footer-box {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .contact-page h1 {
    font-size: 1.8rem;
    flex-direction: column;
    gap: 10px;
  }

  .contact-page h1 i {
    font-size: 2rem;
  }

  .contact-page .contact-card {
    padding: 20px;
  }

  .contact-page .contact-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .contact-page .contact-card h3 {
    font-size: 1.2rem;
  }

  .contact-page .contact-value {
    font-size: 1rem;
    padding: 8px 15px;
  }
}
</style>
