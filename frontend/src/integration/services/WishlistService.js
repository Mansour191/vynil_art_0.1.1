/**
 * WishlistService.js
 * خدمة إدارة قائمة المفضلة والربط مع قاعدة البيانات
 */

class WishlistService {
  constructor() {
    this.apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
    this.cache = new Map();
    this.cacheTTL = 5 * 60 * 1000; // 5 دقائق
  }

  /**
   * جلب عناصر المفضلة للمستخدم
   * @returns {Promise<Array>} - قائمة عناصر المفضلة
   */
  async getWishlistItems() {
    const cacheKey = 'wishlist_items';
    
    if (this._isCacheValid(cacheKey)) {
      return this.cache.get(cacheKey).data;
    }

    try {
      const url = `${this.apiBaseUrl}/wishlist/`;
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this._getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const items = this._transformWishlistItems(data.results || data);
      
      this._setCache(cacheKey, items);
      return items;
    } catch (error) {
      console.error('❌ Error fetching wishlist items:', error);
      return this.getFallbackWishlistItems();
    }
  }

  /**
   * إضافة منتج إلى المفضلة
   * @param {number} productId - معرف المنتج
   * @returns {Promise<Object>} - العنصر المضاف
   */
  async addToWishlist(productId) {
    try {
      const url = `${this.apiBaseUrl}/wishlist/`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this._getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const item = this._transformWishlistItem(data);
      
      // Clear cache to force refresh
      this.cache.delete('wishlist_items');
      
      return item;
    } catch (error) {
      console.error('❌ Error adding to wishlist:', error);
      throw error;
    }
  }

  /**
   * إزالة منتج من المفضلة
   * @param {number} itemId - معرف عنصر المفضلة
   * @returns {Promise<boolean>} - نجاح العملية
   */
  async removeFromWishlist(itemId) {
    try {
      const url = `${this.apiBaseUrl}/wishlist/${itemId}/`;
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this._getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      // Clear cache to force refresh
      this.cache.delete('wishlist_items');
      
      return true;
    } catch (error) {
      console.error('❌ Error removing from wishlist:', error);
      throw error;
    }
  }

  /**
   * تفريغ المفضلة بالكامل
   * @returns {Promise<boolean>} - نجاح العملية
   */
  async clearWishlist() {
    try {
      const url = `${this.apiBaseUrl}/wishlist/clear/`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this._getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      // Clear cache to force refresh
      this.cache.delete('wishlist_items');
      
      return true;
    } catch (error) {
      console.error('❌ Error clearing wishlist:', error);
      throw error;
    }
  }

  /**
   * التحقق مما إذا كان المنتج في المفضلة
   * @param {number} productId - معرف المنتج
   * @returns {Promise<boolean>} - هل المنتج في المفضلة
   */
  async isInWishlist(productId) {
    try {
      const url = `${this.apiBaseUrl}/wishlist/check/?product_id=${productId}`;
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this._getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      return data.in_wishlist || false;
    } catch (error) {
      console.error('❌ Error checking wishlist status:', error);
      return false;
    }
  }

  /**
   * تبديل حالة المنتج في المفضلة
   * @param {number} productId - معرف المنتج
   * @returns {Promise<Object>} - النتيجة والعملية المنفذة
   */
  async toggleWishlistItem(productId) {
    try {
      const isInWishlist = await this.isInWishlist(productId);
      
      if (isInWishlist) {
        // Find and remove from wishlist
        const items = await this.getWishlistItems();
        const item = items.find(item => item.productId === productId);
        if (item) {
          await this.removeFromWishlist(item.id);
          return { action: 'removed', success: true };
        }
      } else {
        // Add to wishlist
        await this.addToWishlist(productId);
        return { action: 'added', success: true };
      }
      
      return { success: false };
    } catch (error) {
      console.error('❌ Error toggling wishlist item:', error);
      throw error;
    }
  }

  // ========== دوال مساعدة ==========

  /**
   * تحويل بيانات عناصر المفضلة من الـ API
   */
  _transformWishlistItems(data) {
    return data.map(item => this._transformWishlistItem(item));
  }

  /**
   * تحصر عنصر المفضلة واحد
   */
  _transformWishlistItem(item) {
    return {
      id: item.id,
      productId: item.product_id,
      name: item.name,
      name_ar: item.name_ar,
      name_en: item.name_en,
      description: item.description,
      price: item.price,
      originalPrice: item.original_price,
      discount: item.discount,
      image: item.image || 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800&auto=format&fit=crop',
      category: item.category,
      rating: item.rating || 4.5,
      reviews: item.reviews || 0,
      inStock: item.in_stock !== false,
      addedAt: item.added_at
    };
  }

  /**
   * بيانات احتياطية للمفضلة
   */
  getFallbackWishlistItems() {
    return [
      {
        id: 1,
        productId: 1,
        name: 'فينيل جدران ثلاثي الأبعاد',
        name_ar: 'فينيل جدران ثلاثي الأبعاد',
        name_en: '3D Wall Vinyl',
        description: 'فينيل عالي الجودة للجدران مع تأثير ثلاثي الأبعاد',
        price: 8500,
        originalPrice: 10000,
        discount: 15,
        image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop',
        category: 'جدران',
        rating: 4.8,
        reviews: 124,
        inStock: true,
        addedAt: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        productId: 2,
        name: 'فينيل سيارة مطفي',
        name_ar: 'فينيل سيارة مطفي',
        name_en: 'Matte Car Vinyl',
        description: 'فينيل سيارة مخصص بلمسة مطفي أنيقة',
        price: 6500,
        originalPrice: null,
        discount: null,
        image: 'https://images.unsplash.com/photo-1552519507-da3b142c42e3?q=80&w=800&auto=format&fit=crop',
        category: 'سيارات',
        rating: 4.6,
        reviews: 89,
        inStock: true,
        addedAt: '2024-01-20T14:15:00Z'
      },
      {
        id: 3,
        productId: 3,
        name: 'فينيل مطبخ كلاسيكي',
        name_ar: 'فينيل مطبخ كلاسيكي',
        name_en: 'Classic Kitchen Vinyl',
        description: 'فينيل مطبخ بتصميم كلاسيكي عالي الجودة',
        price: 12000,
        originalPrice: 15000,
        discount: 20,
        image: 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?q=80&w=800&auto=format&fit=crop',
        category: 'مطابخ',
        rating: 4.9,
        reviews: 203,
        inStock: true,
        addedAt: '2024-01-25T09:45:00Z'
      },
      {
        id: 4,
        productId: 4,
        name: 'فينيل باب خشبي',
        name_ar: 'فينيل باب خشبي',
        name_en: 'Wooden Door Vinyl',
        description: 'فينيل باب بتشطيب خشبي طبيعي',
        price: 10000,
        originalPrice: null,
        discount: null,
        image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=800&auto=format&fit=crop',
        category: 'أبواب',
        rating: 4.7,
        reviews: 156,
        inStock: false,
        addedAt: '2024-01-30T16:20:00Z'
      }
    ];
  }

  /**
   * الحصول على توكن المصادقة
   */
  _getAuthToken() {
    return localStorage.getItem('authToken') || 'mock-token';
  }

  /**
   * التحقق من صلاحية الكاش
   */
  _isCacheValid(key) {
    const cached = this.cache.get(key);
    return cached && (Date.now() - cached.timestamp < this.cacheTTL);
  }

  /**
   * حفظ البيانات في الكاش
   */
  _setCache(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  /**
   * مسح الكاش
   */
  clearCache() {
    this.cache.clear();
  }
}

export default new WishlistService();
