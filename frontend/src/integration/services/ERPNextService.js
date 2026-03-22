import axios from 'axios';
import config from '../config/erpnext.config';

class ERPNextService {
  constructor() {
    this.config = config;
    this.api = axios.create({
      baseURL: process.env.VUE_APP_ERPNEXT_URL || config.baseUrl,
      timeout: parseInt(process.env.VUE_APP_ERPNEXT_TIMEOUT) || config.timeout,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: `token ${process.env.VUE_APP_ERPNEXT_API_KEY}:${process.env.VUE_APP_ERPNEXT_API_SECRET}`,
      },
    });
    this.connectionStatus = false;
    this.lastSync = null;
    this.syncInProgress = false;
    this.errorLog = [];
    this.cache = new Map();
    this.CACHE_TTL = 5 * 60 * 1000; // 5 minutes

    // وضع الديمو إذا لم تتوفر مفاتيح API
    this.isDemoMode =
      !process.env.VUE_APP_ERPNEXT_API_KEY ||
      process.env.VUE_APP_ERPNEXT_API_KEY === 'your_api_key_here';

    // بيانات وهمية للتجربة
    this.mockProducts = this.generateMockProducts();
    this.mockCustomers = this.generateMockCustomers();
  }

  // ========== دوال مساعدة للبيانات الوهمية ==========

  generateMockProducts() {
    return [
      {
        name: 'PROD-001',
        item_name: 'ملصق جدار وردة حمراء',
        item_code: 'WAL-001',
        stock_uom: 'Unit',
        standard_rate: 45,
        actual_qty: 23,
        item_group: 'Walls',
      },
      {
        name: 'PROD-002',
        item_name: 'ملصق باب خشبي كلاسيكي',
        item_code: 'DR-002',
        stock_uom: 'Unit',
        standard_rate: 89,
        actual_qty: 15,
        item_group: 'Doors',
      },
      {
        name: 'PROD-003',
        item_name: 'إطار سيارة رياضي أحمر',
        item_code: 'CAR-003',
        stock_uom: 'Unit',
        standard_rate: 120,
        actual_qty: 8,
        item_group: 'Cars',
      },
      {
        name: 'PROD-004',
        item_name: 'ملصق مطبخ فواكه',
        item_code: 'KIT-004',
        stock_uom: 'Unit',
        standard_rate: 65,
        actual_qty: 12,
        item_group: 'Kitchens',
      },
      {
        name: 'PROD-005',
        item_name: 'ملصق جدار ثلاثي أبعاد',
        item_code: 'WAL-005',
        stock_uom: 'Unit',
        standard_rate: 200,
        actual_qty: 5,
        item_group: 'Walls',
      },
    ];
  }

  generateMockCustomers() {
    return [
      {
        name: 'CUS-001',
        customer_name: 'أحمد محمد',
        customer_group: 'Individual',
        email_id: 'ahmed@example.com',
        mobile_no: '0555123456',
      },
      {
        name: 'CUS-002',
        customer_name: 'سارة أحمد',
        customer_group: 'Individual',
        email_id: 'sara@example.com',
        mobile_no: '0555987654',
      },
      {
        name: 'CUS-003',
        customer_name: 'محمد علي',
        customer_group: 'Individual',
        email_id: 'mohammed@example.com',
        mobile_no: '0555777888',
      },
    ];
  }

  // ========== دوال الاتصال الأساسية ==========

  // اختبار الاتصال
  async testConnection() {
    if (this.isDemoMode) {
      return this.mockResponse(
        { message: 'Connected to mock ERPNext' },
        'Connected successfully (Demo Mode)'
      );
    }

    try {
      const response = await this.api.get('/api/method/frappe.auth.get_logged_user');
      this.connectionStatus = true;
      return { success: true, data: response.data };
    } catch (error) {
      this.connectionStatus = false;
      return { success: false, message: error.message };
    }
  }

  // ========== دوال المنتجات ==========

  // جلب جميع المنتجات
  async getProducts() {
    const cacheKey = 'products_all';
    if (this.isCacheValid(cacheKey)) {
      return this.mockResponse(this.cache.get(cacheKey).data);
    }

    if (this.isDemoMode) {
      const response = await this.mockResponse(this.mockProducts);
      this.setCache(cacheKey, response.data);
      return response;
    }

    try {
      const response = await this.api.get('/api/resource/Item', {
        params: {
          fields:
            '["name", "item_name", "item_code", "stock_uom", "standard_rate", "actual_qty", "image", "item_group"]',
          limit_page_length: 100,
        },
      });
      this.setCache(cacheKey, response.data.data);
      return { success: true, data: response.data.data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال مساعدة للكاش ==========

  isCacheValid(key) {
    const cached = this.cache.get(key);
    if (!cached) return false;
    return Date.now() - cached.timestamp < this.CACHE_TTL;
  }

  setCache(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });
  }

  clearCache() {
    this.cache.clear();
  }

  // جلب منتج محدد
  async getProduct(itemCode) {
    if (this.isDemoMode) {
      const product = this.mockProducts.find((p) => p.item_code === itemCode);
      return product
        ? this.mockResponse(product)
        : { success: false, message: 'Product not found' };
    }

    try {
      const response = await this.api.get(`/api/resource/Item/${itemCode}`);
      return { success: true, data: response.data.data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // بحث عن منتجات
  async searchProducts(query) {
    if (this.isDemoMode) {
      const results = this.mockProducts.filter(
        (p) => p.item_name.includes(query) || p.item_code.includes(query)
      );
      return this.mockResponse(results);
    }

    try {
      const response = await this.api.get('/api/resource/Item', {
        params: {
          filters: `[["item_name", "like", "%${query}%"]]`,
          fields: '["name", "item_name", "item_code", "standard_rate", "image", "item_group"]',
        },
      });
      return { success: true, data: response.data.data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال العملاء ==========

  async createCustomer(customerData) {
    if (this.isDemoMode) {
      const newCustomer = {
        name: `CUS-${Date.now()}`,
        customer_name: customerData.name,
        customer_group: 'Individual',
        email_id: customerData.email,
        mobile_no: customerData.phone,
      };
      this.mockCustomers.push(newCustomer);
      return this.mockResponse(newCustomer, 'Customer created successfully (Mock)');
    }

    try {
      const response = await this.api.post('/api/resource/Customer', customerData);
      return { success: true, data: response.data.data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال الفواتير وأوامر البيع ==========

  async createSalesOrder(orderData) {
    if (this.isDemoMode) {
      const newOrder = {
        name: `SO-${Date.now()}`,
        ...orderData,
      };
      return this.mockResponse(newOrder, 'Sales order created successfully (Mock)');
    }

    try {
      const response = await this.api.post('/api/resource/Sales Order', orderData);
      return { success: true, data: response.data.data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال مساعدة ==========

  mockResponse(data, message = '') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          data: data,
          message: message,
          count: Array.isArray(data) ? data.length : undefined,
        });
      }, 500);
    });
  }

  getConnectionStatus() {
    return {
      connected: this.connectionStatus,
      lastSync: this.lastSync,
      syncInProgress: this.syncInProgress,
      errors: this.errorLog.length,
      mode: this.isDemoMode ? 'DEMO' : 'LIVE',
    };
  }
}

export default new ERPNextService();
