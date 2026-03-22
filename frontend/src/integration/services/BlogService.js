import i18n from '@/plugins/i18n';

class BlogService {
  constructor() {
    this.baseUrl = 'https://storepaclos.blogspot.com';
    this.cache = new Map();
    this.cacheTTL = 5 * 60 * 1000; // 5 دقائق
  }

  /**
   * جلب أحدث المقالات من Blogger
   * @param {number} limit - عدد المقالات المطلوبة
   * @returns {Promise<Array>} - مصفوفة المقالات
   */
  async getLatestPosts(limit = 4) {
    const cacheKey = `latest_${limit}_${i18n.global.locale.value || i18n.global.locale}`;
    
    if (this._isCacheValid(cacheKey)) {
      return this.cache.get(cacheKey).data;
    }

    try {
      // تجربة جلب البيانات مع محاولة تجاوز CORS عبر إضافة معلمات معينة
      const url = `${this.baseUrl}/feeds/posts/default?alt=json&max-results=${limit}&orderby=published`;
      const response = await fetch(url, {
        method: 'GET',
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const json = await response.json();
      
      const entries = json.feed?.entry || [];
      const posts = this._transformEntries(entries);
      
      this._setCache(cacheKey, posts);
      return posts;
    } catch (error) {
      console.warn('⚠️ Blogger API failed, using fallback data:', error.message);
      // إرجاع بيانات افتراضية في حال فشل الـ API لضمان عدم تعطل الواجهة
      return this._getFallbackPosts(limit);
    }
  }

  /**
   * بيانات افتراضية عالية الجودة تظهر في حال فشل الاتصال بـ Blogger
   */
  _getFallbackPosts(limit) {
    const fallbackData = [
      {
        id: 'fallback-1',
        title: 'أفضل 5 تصاميم فينيل لجدران غرف النوم في 2026',
        link: '/blog',
        image: 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800&auto=format&fit=crop',
        published: new Date().toISOString(),
        summary: 'تعرف على أحدث صيحات الديكور باستخدام ورق الحائط والفينيل المخصص لغرف النوم العصرية...'
      },
      {
        id: 'fallback-2',
        title: 'كيفية العناية بملصقات السيارات لضمان بقائها سنوات طويلة',
        link: '/blog',
        image: 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?q=80&w=800&auto=format&fit=crop',
        published: new Date().toISOString(),
        summary: 'نصائح احترافية لتنظيف وحماية ملصقات الفينيل على سيارتك من أشعة الشمس والحرارة العالية...'
      },
      {
        id: 'fallback-3',
        title: 'تجديد المطبخ بأقل التكاليف: سحر الفينيل اللاصق',
        link: '/blog',
        image: 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?q=80&w=800&auto=format&fit=crop',
        published: new Date().toISOString(),
        summary: 'لا حاجة لتغيير خزائن المطبخ بالكامل، اكتشف كيف يمكن للفينيل أن يحول مطبخك القديم لآخر عصري...'
      },
      {
        id: 'fallback-4',
        title: 'دليل شامل لاختيار الألوان المناسبة لمساحتك الصغيرة',
        link: '/blog',
        image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop',
        published: new Date().toISOString(),
        summary: 'الألوان الفاتحة أم الداكنة؟ تعلم كيف تختار التدرج اللوني الذي يعطي اتساعاً وهمياً لغرفتك...'
      }
    ];
    return fallbackData.slice(0, limit);
  }

  /**
   * جلب المقالات حسب التسمية (Label)
   */
  async getPostsByLabel(label, maxResults = 4) {
    const lang = i18n.global.locale.value || i18n.global.locale;
    const langLabel = typeof label === 'object' ? (lang === 'ar' ? label.ar : label.en) : label;
    const cacheKey = `label_${langLabel}_${maxResults}_${lang}`;

    if (this._isCacheValid(cacheKey)) {
      return this.cache.get(cacheKey).data;
    }

    try {
      const url = `${this.baseUrl}/feeds/posts/default/-/${encodeURIComponent(langLabel)}?alt=json&max-results=${maxResults}`;
      const response = await fetch(url, { method: 'GET' });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const json = await response.json();
      const entries = json.feed?.entry || [];
      const posts = this._transformEntries(entries);
      
      this._setCache(cacheKey, posts);
      return posts;
    } catch (error) {
      console.warn(`⚠️ Blogger API failed for label ${langLabel}, using fallback:`, error.message);
      return this._getFallbackPosts(maxResults);
    }
  }

  /**
   * تحويل بيانات Blogger إلى هيكل بيانات المشروع
   */
  _transformEntries(entries) {
    return entries.map((entry) => {
      const alternateLink = entry.link.find((l) => l.rel === 'alternate');
      const thumbUrl = entry.media$thumbnail ? entry.media$thumbnail.url : '';
      
      return {
        id: entry.id.$t,
        title: entry.title.$t,
        link: alternateLink ? alternateLink.href : '#',
        image: thumbUrl
          ? thumbUrl.replace('s72-c', 's1600')
          : 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=800&auto=format&fit=crop', // Unsplash placeholder
        published: entry.published.$t,
        summary: this._stripHtml(entry.summary ? entry.summary.$t : (entry.content ? entry.content.$t : '')).substring(0, 120) + '...',
        translations: {
          ar: {
            title: entry.title.$t,
            summary: this._stripHtml(entry.summary ? entry.summary.$t : (entry.content ? entry.content.$t : '')).substring(0, 120) + '...'
          },
          en: {
            title: entry.title.$t, // Blogger doesn't support built-in translations easily
            summary: this._stripHtml(entry.summary ? entry.summary.$t : (entry.content ? entry.content.$t : '')).substring(0, 120) + '...'
          }
        }
      };
    });
  }

  _stripHtml(html) {
    const tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  }

  _isCacheValid(key) {
    const cached = this.cache.get(key);
    return cached && (Date.now() - cached.timestamp < this.cacheTTL);
  }

  _setCache(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
}

export default new BlogService();
