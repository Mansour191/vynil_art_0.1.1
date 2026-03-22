<template>
  <div class="about-page">
    <!-- عنوان الصفحة -->
    <h1>
      <i class="fa-solid fa-users"></i>
      <span>{{ $t('about') }}</span>
    </h1>

    <!-- إحصائيات -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fa-solid fa-project-diagram"></i>
        </div>
        <div class="stat-number">500+</div>
        <div class="stat-label">{{ $t('statProjects') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fa-solid fa-smile"></i>
        </div>
        <div class="stat-number">300+</div>
        <div class="stat-label">{{ $t('statClients') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fa-solid fa-trophy"></i>
        </div>
        <div class="stat-number">5+</div>
        <div class="stat-label">{{ $t('statYears') }}</div>
      </div>
    </div>

    <!-- رؤيتنا -->
    <div class="vision-card">
      <h2>
        <i class="fa-solid fa-eye"></i>
        <span>{{ $t('visionTitle') }}</span>
      </h2>
      <p>{{ $t('visionText') }}</p>
    </div>

    <!-- قيمنا الأساسية -->
    <div class="values-grid">
      <div class="value-item">
        <div class="value-icon">
          <i class="fa-solid fa-gem"></i>
        </div>
        <h3>{{ $t('valueQualityTitle') }}</h3>
        <p>{{ $t('valueQualityText') }}</p>
      </div>
      <div class="value-item">
        <div class="value-icon">
          <i class="fa-solid fa-lightbulb"></i>
        </div>
        <h3>{{ $t('valueCreativityTitle') }}</h3>
        <p>{{ $t('valueCreativityText') }}</p>
      </div>
      <div class="value-item">
        <div class="value-icon">
          <i class="fa-solid fa-handshake"></i>
        </div>
        <h3>{{ $t('valueTrustTitle') }}</h3>
        <p>{{ $t('valueTrustText') }}</p>
      </div>
    </div>

    <!-- خبرتنا - تصميم جديد أنيق (محدث) -->
    <div class="expertise-showcase">
      <div class="section-header-center">
        <h2 class="section-title-center">
          <i class="fa-solid fa-star"></i>
          <span>{{ $t('expertiseTitle') || 'خبرتنا' }}</span>
        </h2>
        <div class="title-decoration">
          <span class="gold-bar"></span>
          <i class="fa-solid fa-certificate"></i>
          <span class="gold-bar"></span>
        </div>
      </div>

      <div class="expertise-grid">
        <!-- بطاقة الخبرة الفنية -->
        <div class="expertise-card-modern">
          <div class="card-badge">
            <span class="badge-number">01</span>
          </div>
          <div class="card-icon">
            <i class="fa-solid fa-paint-brush"></i>
          </div>
          <h3>{{ $t('expertiseArtTitle') }}</h3>
          <p>{{ $t('expertiseArtText') }}</p>
          <div class="card-features">
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('uniqueDesigns') || 'تصاميم فريدة' }}</span>
            </div>
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('vibrantColors') || 'ألوان زاهية' }}</span>
            </div>
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('highPrecision') || 'دقة عالية' }}</span>
            </div>
          </div>
        </div>

        <!-- بطاقة التقنيات الحديثة -->
        <div class="expertise-card-modern highlight">
          <div class="card-badge">
            <span class="badge-number">02</span>
          </div>
          <div class="card-icon">
            <i class="fa-solid fa-microchip"></i>
          </div>
          <h3>{{ $t('expertiseTechTitle') }}</h3>
          <p>{{ $t('expertiseTechText') }}</p>
          <div class="card-features">
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('modernPrinting') || 'طباعة حديثة' }}</span>
            </div>
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('preciseCutting') || 'قص دقيق' }}</span>
            </div>
            <div class="feature">
              <i class="fa-solid fa-check-circle"></i>
              <span>{{ $t('highQualityMaterials') || 'مواد عالية الجودة' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ماذا نقدم -->
    <div class="mission-box">
      <h2>
        <i class="fa-solid fa-blog"></i>
        <span>{{ $t('missionTitle') }}</span>
      </h2>
      <p>{{ $t('missionText') }}</p>
    </div>

    <!-- إضافة لمسة جمالية في النهاية -->
    <div class="quote-footer">
      <i class="fa-solid fa-quote-right"></i>
      <p>{{ $t('quoteText') }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
};
</script>

<style scoped>
.about-page {
  max-width: 1000px;
  margin: 0 auto;
  font-family: var(--font-arabic, 'Cairo', sans-serif);
  line-height: 1.8;
  color: var(--text-primary, #ffffff);
  padding: 20px;
}

.about-page h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.5rem;
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

.about-page h1 i {
  font-size: 3rem;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.about-page h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  border-radius: 3px;
}

.about-page .stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.about-page .stat-card {
  background: var(--bg-card, #222222);
  padding: 25px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.about-page .stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary, #d4af37);
  box-shadow: var(--shadow-gold, 0 8px 25px rgba(212, 175, 55, 0.3));
}

.about-page .stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  transform: translateX(-100%);
  transition: transform 0.6s;
}

.about-page .stat-card:hover::before {
  transform: translateX(0);
}

.about-page .stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg-deep, #0f0f0f);
  font-size: 2rem;
  margin: 0 auto 20px;
  transition: all 0.3s;
}

.about-page .stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(360deg);
}

.about-page .stat-number {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--gold-primary, #d4af37);
  margin-bottom: 5px;
}

.about-page .stat-label {
  color: var(--text-muted, #a0a0a0);
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.about-page .vision-card {
  background: linear-gradient(135deg, var(--bg-surface, #2a2a2a), var(--bg-card, #222222));
  padding: 40px;
  border-radius: 30px;
  margin-bottom: 30px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-soft, 0 8px 32px rgba(0, 0, 0, 0.4));
}

.about-page .vision-card::before {
  content: '"';
  position: absolute;
  top: -20px;
  right: 20px;
  font-size: 150px;
  font-family: var(--font-artistic, 'Playfair Display', serif);
  color: var(--gold-primary, #d4af37);
  opacity: 0.1;
  line-height: 1;
}

body[dir='ltr'] .about-page .vision-card::before {
  right: auto;
  left: 20px;
}

.about-page .vision-card h2 {
  color: var(--gold-primary, #d4af37);
  font-size: 2rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
  z-index: 2;
}

.about-page .vision-card h2 i {
  font-size: 2.2rem;
}

.about-page .vision-card p {
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.15rem;
  line-height: 1.9;
  margin-bottom: 20px;
  position: relative;
  z-index: 2;
}

.about-page .values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 40px 0;
}

.about-page .value-item {
  background: var(--bg-card, #222222);
  padding: 25px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle, #333333);
  text-align: center;
  transition: all 0.3s;
}

.about-page .value-item:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary, #d4af37);
}

.about-page .value-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg-deep, #0f0f0f);
  font-size: 1.5rem;
  margin: 0 auto 15px;
}

.about-page .value-item h3 {
  color: var(--gold-primary, #d4af37);
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.about-page .value-item p {
  color: var(--text-muted, #a0a0a0);
  font-size: 0.95rem;
}

/* ===== قسم الخبرة الجديد ===== */
.section-header-center {
  text-align: center;
  margin-bottom: 40px;
}

.section-title-center {
  color: var(--gold-primary, #d4af37);
  font-size: 2rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.section-title-center i {
  font-size: 2rem;
  color: var(--gold-primary, #d4af37);
}

.title-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.gold-bar {
  width: 60px;
  height: 2px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
}

.title-decoration i {
  color: var(--gold-primary, #d4af37);
  font-size: 1.2rem;
  animation: pulse 2s infinite;
}

.expertise-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin: 40px 0;
}

.expertise-card-modern {
  background: var(--bg-card, #222222);
  border-radius: 30px;
  padding: 40px 30px;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border-subtle, #333333);
  transition: all 0.4s ease;
}

.expertise-card-modern:hover {
  transform: translateY(-10px);
  border-color: var(--gold-primary, #d4af37);
  box-shadow: var(--shadow-gold, 0 8px 32px rgba(212, 175, 55, 0.3));
}

.expertise-card-modern.highlight {
  background: linear-gradient(135deg, var(--bg-surface, #2a2a2a), var(--bg-card, #222222));
  border-color: var(--gold-primary, #d4af37);
}

.card-badge {
  position: absolute;
  top: 20px;
  right: 20px;
}

body[dir='ltr'] .card-badge {
  right: auto;
  left: 20px;
}

.badge-number {
  font-size: 3rem;
  font-weight: 800;
  color: var(--gold-primary, #d4af37);
  opacity: 0.2;
  font-family: var(--font-artistic, 'Playfair Display', serif);
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 25px;
  color: var(--bg-deep, #0f0f0f);
  font-size: 2rem;
  transition: all 0.4s;
}

.expertise-card-modern:hover .card-icon {
  transform: scale(1.1) rotate(360deg);
}

.expertise-card-modern h3 {
  color: var(--gold-primary, #d4af37);
  font-size: 1.6rem;
  margin-bottom: 15px;
  position: relative;
  padding-bottom: 15px;
}

.expertise-card-modern h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 3px;
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #ffd700 100%));
  border-radius: 3px;
}

body[dir='ltr'] .expertise-card-modern h3::after {
  right: auto;
  left: 0;
}

.expertise-card-modern p {
  color: var(--text-secondary, #e0e0e0);
  font-size: 1rem;
  line-height: 1.8;
  margin-bottom: 20px;
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-muted, #a0a0a0);
  font-size: 0.95rem;
}

.feature i {
  color: var(--gold-primary, #d4af37);
  font-size: 1.1rem;
}

.feature:hover {
  color: var(--text-primary, #ffffff);
  transform: translateX(5px);
  transition: all 0.3s;
}

body[dir='ltr'] .feature:hover {
  transform: translateX(-5px);
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

/* ===== نهاية قسم الخبرة الجديد ===== */

.about-page .mission-box {
  background: linear-gradient(135deg, var(--bg-card, #222222), var(--bg-surface, #2a2a2a));
  padding: 40px;
  border-radius: 30px;
  margin: 40px 0 30px;
  border: 1px solid var(--border-subtle, #333333);
  position: relative;
  overflow: hidden;
  text-align: center;
}

.about-page .mission-box::before {
  content: '✦';
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 40px;
  color: var(--gold-primary, #d4af37);
  opacity: 0.1;
}

.about-page .mission-box::after {
  content: '✦';
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-size: 40px;
  color: var(--gold-primary, #d4af37);
  opacity: 0.1;
}

.about-page .mission-box h2 {
  color: var(--gold-primary, #d4af37);
  font-size: 2rem;
  margin-bottom: 20px;
}

.about-page .mission-box p {
  color: var(--text-secondary, #e0e0e0);
  font-size: 1.2rem;
  line-height: 1.9;
  max-width: 800px;
  margin: 0 auto;
}

.about-page .quote-footer {
  text-align: center;
  margin-top: 40px;
  color: var(--text-muted, #a0a0a0);
}

.about-page .quote-footer i {
  font-size: 2rem;
  opacity: 0.3;
}

.about-page .quote-footer p {
  margin-top: 10px;
  font-style: italic;
}

/* RTL Support */
body[dir='rtl'] .about-page .vision-card::before {
  right: auto;
  left: 20px;
}

body[dir='rtl'] .about-page .mission-box::before {
  left: auto;
  right: 20px;
}

body[dir='rtl'] .about-page .mission-box::after {
  right: auto;
  left: 20px;
}

/* Responsive Design */
@media (max-width: 992px) {
  .about-page .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .about-page .values-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .expertise-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .about-page {
    padding: 15px;
  }

  .about-page h1 {
    font-size: 2rem;
  }

  .about-page h1 i {
    font-size: 2.2rem;
  }

  .about-page .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .about-page .values-grid {
    grid-template-columns: 1fr;
  }

  .expertise-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .about-page .vision-card {
    padding: 25px;
  }

  .about-page .vision-card h2 {
    font-size: 1.6rem;
  }

  .expertise-card-modern {
    padding: 30px 20px;
  }

  .expertise-card-modern h3 {
    font-size: 1.4rem;
  }

  .about-page .mission-box {
    padding: 25px;
  }

  .about-page .mission-box h2 {
    font-size: 1.6rem;
  }

  .about-page .mission-box p {
    font-size: 1.1rem;
  }

  .section-title-center {
    font-size: 1.6rem;
  }
}

@media (max-width: 480px) {
  .about-page h1 {
    font-size: 1.8rem;
    flex-direction: column;
    gap: 10px;
  }

  .about-page h1 i {
    font-size: 2rem;
  }

  .about-page .stat-number {
    font-size: 1.8rem;
  }

  .about-page .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .about-page .vision-card p,
  .expertise-card-modern p,
  .about-page .mission-box p {
    font-size: 1rem;
  }

  .card-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .badge-number {
    font-size: 2.5rem;
  }
}
</style>
