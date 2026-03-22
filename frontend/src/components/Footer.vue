<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <!-- About Column -->
        <div class="footer-col about-col">
          <h4><i class="fa-solid fa-info-circle"></i> {{ $t('aboutTitle') }}</h4>
          <p class="footer-about-text">{{ $t('footerAboutText') }}</p>
          <div class="footer-stats-mini">
            <div class="stat-mini">
              <span class="stat-number">500+</span>
              <span class="stat-label">{{ $t('footerProjects') }}</span>
            </div>
            <div class="stat-mini">
              <span class="stat-number">300+</span>
              <span class="stat-label">{{ $t('footerClients') }}</span>
            </div>
            <div class="stat-mini">
              <span class="stat-number">5+</span>
              <span class="stat-label">{{ $t('footerYears') }}</span>
            </div>
          </div>
        </div>

        <!-- Products Column -->
        <div class="footer-col">
          <h4><i class="fa-solid fa-th-large"></i> {{ $t('ourProducts') }}</h4>
          <ul class="footer-links">
            <li v-for="item in productItems" :key="item.route">
              <router-link :to="item.route">
                <i :class="item.icon"></i>
                {{ $t(item.key) }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Quick Links Column -->
        <div class="footer-col">
          <h4><i class="fa-solid fa-link"></i> {{ $t('importantLinks') }}</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/about"><i class="fa-solid fa-users"></i> {{ $t('about') }}</router-link>
            </li>
            <li>
              <router-link to="/contact"
                ><i class="fa-solid fa-phone-alt"></i> {{ $t('contact') }}</router-link
              >
            </li>
            <li>
              <router-link to="/gallery"
                ><i class="fa-solid fa-images"></i> {{ $t('gallery') }}</router-link
              >
            </li>
            <li>
              <router-link to="/privacy"
                ><i class="fa-solid fa-shield-alt"></i> {{ $t('privacy') }}</router-link
              >
            </li>
            <li>
              <router-link to="/terms"
                ><i class="fa-solid fa-file-contract"></i> {{ $t('terms') }}</router-link
              >
            </li>
          </ul>
        </div>

        <!-- Contact Column -->
        <div class="footer-col contact-col">
          <h4><i class="fa-solid fa-phone-alt"></i> {{ $t('contactUs') }}</h4>
          <div class="footer-contact-info">
            <div class="contact-item">
              <i class="fa-solid fa-envelope"></i>
              <a href="mailto:remadnamansour7@gmail.com">remadnamansour7@gmail.com</a>
            </div>
            <div class="contact-item">
              <i class="fa-solid fa-phone-alt"></i>
              <a href="tel:0663140341">0663140341</a>
            </div>
          </div>
          <div class="social-section">
            <h5>{{ $t('followUsTitle') }}</h5>
            <div class="social-icons">
              <a
                v-for="social in socialLinks"
                :key="social.name"
                :href="social.link"
                target="_blank"
                rel="noopener noreferrer"
                :class="['social-icon', social.name]"
                :title="social.name"
              >
                <i :class="social.icon"></i>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-divider">
        <span class="divider-icon">&#10022;</span>
      </div>

      <div class="footer-bottom">
        <div class="copyright">
          <i class="fa-solid fa-copyright"></i> {{ $t('siteTitle') }} {{ new Date().getFullYear() }} -
          {{ $t('allRightsReserved') }}
        </div>
        <div class="footer-legal">
          <router-link to="/privacy">{{ $t('privacy') }}</router-link>
          <span class="separator">|</span>
          <router-link to="/terms">{{ $t('terms') }}</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      productItems: [
        { route: '/furniture', icon: 'fa-solid fa-couch', key: 'furniture' },
        { route: '/doors', icon: 'fa-solid fa-door-open', key: 'doors' },
        { route: '/walls', icon: 'fa-solid fa-paint-roller', key: 'walls' },
        { route: '/ceilings', icon: 'fa-solid fa-arrow-up', key: 'ceilings' },
        { route: '/tiles', icon: 'fa-solid fa-border-all', key: 'tiles' },
        { route: '/kitchens', icon: 'fa-solid fa-utensils', key: 'kitchens' },
        { route: '/cars', icon: 'fa-solid fa-car', key: 'cars' },
      ],
      socialLinks: [
        {
          name: 'facebook',
          icon: 'fab fa-facebook-f',
          link: 'https://www.facebook.com/profile.php?id=61588391030740',
        },
        { name: 'youtube', icon: 'fab fa-youtube', link: 'https://www.youtube.com/@store_paclos' },
        { name: 'whatsapp', icon: 'fab fa-whatsapp', link: 'https://wa.me/213663140341' },
        { name: 'instagram', icon: 'fab fa-instagram', link: '#' },
        { name: 'tiktok', icon: 'fab fa-tiktok', link: 'https://www.tiktok.com/@mansour.2026' },
        { name: 'email', icon: 'fa-solid fa-envelope', link: 'mailto:remadnamansour7@gmail.com' },
      ],
    };
  },
};
</script>

<style scoped>
.footer {
  background: linear-gradient(180deg, var(--bg-dark) 0%, var(--bg-deep) 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 0 20px;
  margin-top: 40px;
  border-top: 1px solid var(--border-subtle);
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gold-gradient);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 25px;
  margin-bottom: 30px;
}

.footer-col {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-subtle);
  border-radius: 15px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.footer-col:hover {
  border-color: var(--gold-primary);
  transform: translateY(-5px);
  box-shadow: var(--shadow-gold);
}

.footer-col h4 {
  color: var(--gold-primary);
  font-size: 1.1rem;
  margin-bottom: 15px;
  position: relative;
  padding-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-col h4::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 2px;
  background: var(--gold-gradient);
  transition: width 0.3s;
}

.footer-col:hover h4::after {
  width: 60px;
}

[dir='ltr'] .footer-col h4::after {
  right: auto;
  left: 0;
}

.footer-about-text {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.7;
  margin-bottom: 20px;
}

.footer-stats-mini {
  display: flex;
  gap: 15px;
  justify-content: space-around;
  background: rgba(212, 175, 55, 0.05);
  border-radius: 15px;
  padding: 15px;
}

.stat-mini {
  text-align: center;
}

.stat-number {
  display: block;
  color: var(--gold-primary);
  font-size: 1.3rem;
  font-weight: 800;
  line-height: 1.2;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 10px;
}

.footer-links li a {
  color: var(--text-muted);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.footer-links li a i {
  color: var(--gold-primary);
  width: 20px;
  text-align: center;
  transition: all 0.3s;
}

.footer-links li a:hover {
  color: var(--text-primary);
  transform: translateX(-5px);
}

[dir='ltr'] .footer-links li a:hover {
  transform: translateX(5px);
}

.footer-links li a:hover i {
  color: var(--gold-light);
  transform: scale(1.2);
}

.footer-contact-info {
  margin-bottom: 15px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
  transition: all 0.3s;
}

.contact-item:hover {
  background: rgba(212, 175, 55, 0.1);
  transform: translateX(-3px);
}

[dir='ltr'] .contact-item:hover {
  transform: translateX(3px);
}

.contact-item i {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gold-gradient);
  border-radius: 50%;
  color: var(--bg-deep);
  font-size: 0.85rem;
}

.contact-item a {
  color: var(--text-muted);
  font-size: 0.9rem;
  transition: color 0.3s;
  word-break: break-word;
  text-decoration: none;
}

.contact-item:hover a {
  color: var(--text-primary);
}

.social-section {
  margin-top: 15px;
}

.social-section h5 {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 10px;
  font-weight: 500;
}

.social-icons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.social-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.02);
  text-decoration: none;
  color: var(--text-primary);
}

.social-icon:hover {
  transform: translateY(-5px) scale(1.1);
  border-color: transparent;
}

.social-icon.facebook:hover {
  background: #1877f2;
}
.social-icon.youtube:hover {
  background: #ff0000;
}
.social-icon.whatsapp:hover {
  background: #25d366;
}
.social-icon.instagram:hover {
  background: linear-gradient(45deg, #f09433, #d62976, #962fbf, #4f5bd5);
}
.social-icon.tiktok:hover {
  background: #000000;
}
.social-icon.email:hover {
  background: #d44638;
}

.social-icon:hover i {
  color: white;
  transform: scale(1.1);
}

.footer-divider {
  position: relative;
  margin: 30px 0 20px;
  text-align: center;
}

.footer-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
}

.divider-icon {
  position: relative;
  background: var(--bg-deep);
  padding: 0 20px;
  color: var(--gold-primary);
  font-size: 1.2rem;
  animation: spin 6s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-subtle);
}

.copyright {
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.copyright i {
  color: var(--gold-primary);
}

.footer-legal {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.footer-legal a {
  color: var(--text-muted);
  font-size: 0.8rem;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-legal a:hover {
  color: var(--gold-primary);
}

.separator {
  color: var(--border-subtle);
}

/* Responsive */
@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .footer-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 600px) {
  .footer-stats-mini {
    flex-direction: column;
    gap: 10px;
  }

  .contact-item {
    flex-direction: column;
    text-align: center;
  }

  .footer-legal {
    flex-direction: column;
    gap: 8px;
  }

  .separator {
    display: none;
  }
}
</style>
