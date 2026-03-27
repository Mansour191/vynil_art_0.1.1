import { api } from '@/composables/useApi';
import config from '../config/erpnext.config';

// Singleton instance and request coordination
let erpServiceInstance = null;
let erpHealthCheckPromise = null;

class ERPNextService {
  constructor() {
    // Singleton pattern
    if (erpServiceInstance) {
      return erpServiceInstance;
    }
    
    this.config = config;
    // Use the base URL from config for external ERPNext API calls
    this.erpnextBaseUrl = import.meta.env.VITE_ERPNEXT_URL || config.baseUrl;
    this.timeout = parseInt(import.meta.env.VITE_ERPNEXT_TIMEOUT) || config.timeout;
    
    this.connectionStatus = false;
    this.lastSync = null;
    this.syncInProgress = false;
    this.errorLog = [];
    this.cache = new Map();
    this.CACHE_TTL = 5 * 60 * 1000; // 5 minutes

    // وضع الديمو إذا لم تتوفر مفاتيح API
    this.isDemoMode =
      !import.meta.env.VITE_ERPNEXT_API_KEY ||
      import.meta.env.VITE_ERPNEXT_API_KEY === 'your_api_key_here';

    // بيانات وهمية للتجربة
    this.mockProducts = this.generateMockProducts();
    this.mockCustomers = this.generateMockCustomers();
    
    erpServiceInstance = this;
  }
  
  // Static method to get instance
  static getInstance() {
    if (!erpServiceInstance) {
      erpServiceInstance = new ERPNextService();
    }
    return erpServiceInstance;
  }

  // Health Check - FIXED with request coordination
  async checkIntegrationHealth() {
    // If health check is already in progress, return the existing promise
    if (erpHealthCheckPromise) {
      console.log('🔄 ERPNext health check already in progress, waiting for result...');
      return erpHealthCheckPromise;
    }
    
    // Create new health check promise
    erpHealthCheckPromise = this._performHealthCheck();
    
    try {
      const result = await erpHealthCheckPromise;
      return result;
    } finally {
      // Clear the promise after completion (whether success or failure)
      erpHealthCheckPromise = null;
    }
  }
  
  // Internal health check implementation
  async _performHealthCheck() {
    try {
      console.log('🏥 ERPNextService - Performing integration health check...');
      
      // Use the api composable with proper error handling
      const response = api.get('erpnext/health/');
      
      // Set timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Health check timeout')), 5000);
      });
      
      await Promise.race([response.execute(), timeoutPromise]);
      
      // Check for error with null safety
      if (response.error?.value) {
        throw response.error.value;
      }
      
      // Check for data with null safety
      const healthData = response.data?.value;
      if (!healthData) {
        throw new Error('No health data received');
      }
      
      console.log('✅ Integration health check successful:', healthData);
      
      this.connectionStatus = true;
      this.lastSync = new Date().toISOString();
      
      return { 
        status: 'healthy', 
        connected: true,
        lastSync: this.lastSync,
        services: healthData?.services || 'all_active',
        url: 'erpnext/health/',
        method: 'GET'
      };
    } catch (error) {
      console.error('❌ Integration health check failed:', error.message);
      console.error('Request details:', {
        url: 'erpnext/health/',
        method: 'GET',
        errorType: error.name,
        errorMessage: error.message
      });
      
      this.connectionStatus = false;
      this.errorLog.push({
        timestamp: new Date().toISOString(),
        type: 'health_check_failed',
        message: error.message,
        url: 'erpnext/health/',
        method: 'GET'
      });
      
      return { 
        status: 'unhealthy', 
        connected: false,
        error: error.message,
        services: 'unavailable',
        url: 'erpnext/health/',
        method: 'GET'
      };
    }
  }

  // Fetch real products from database - FIXED with request coordination
  async getProducts() {
    try {
      console.log('📦 ERPNextService - Fetching products from database...');
      
      // Use api composable with proper error handling and timeout
      const response = api.get('/products/');
      
      // Set timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Products fetch timeout')), 15000);
      });
      
      await Promise.race([response.execute(), timeoutPromise]);
      
      // Check for error with null safety
      if (response.error?.value) {
        throw response.error.value;
      }
      
      // Check for data with null safety
      const products = response.data?.value?.results || response.data?.value || [];
      
      if (products.length === 0) {
        console.warn('⚠️ No products found in database, using mock data');
        return this.generateMockProducts();
      }
      
      console.log(`✅ Successfully fetched ${products.length} products from database`);
      return products;
      
    } catch (error) {
      console.error('❌ Error fetching products from database:', error);
      console.error('Error details:', {
        url: '/products/',
        method: 'GET',
        errorType: error.name,
        errorMessage: error.message,
        isAborted: error.isAborted || false
      });
      
      // Fallback to mock data only if database fails
      if (error.name === 'AbortError') {
        console.warn('⚠️ Products request was aborted, this is normal during coordination');
      } else {
        console.warn('⚠️ Falling back to mock products due to database error');
      }
      
      return this.generateMockProducts();
    }
  }

  // Fetch real customers from database
  async getCustomers() {
    try {
      console.log('👥 ERPNextService - Fetching customers from database...');
      
      const response = await api.get('/customers/');
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const customers = response.data.value?.results || response.data.value || [];
      console.log(`✅ Successfully fetched ${customers.length} customers from database`);
      
      return customers;
    } catch (error) {
      console.error('❌ Error fetching customers from database:', error);
      
      // Fallback to mock data only if database fails
      console.warn('⚠️ Falling back to mock customers due to database error');
      return this.generateMockCustomers();
    }
  }

  // ========== دوال مساعدة للبيانات الوهمية (Fallback only) ==========

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

  // جلب جميع المنتجات (Updated to use real database)
  async getAllProducts() {
    const cacheKey = 'products_all';
    if (this.isCacheValid(cacheKey)) {
      return this.mockResponse(this.cache.get(cacheKey).data);
    }

    if (this.isDemoMode) {
      const products = await this.getProducts(); // This now fetches from DB
      this.cache.set(cacheKey, { data: products, timestamp: Date.now() });
      return this.mockResponse(products);
    }

    try {
      const response = await api.get('/products/');
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const products = response.data.value?.results || response.data.value || [];
      this.cache.set(cacheKey, { data: products, timestamp: Date.now() });
      this.connectionStatus = true;
      this.lastSync = new Date().toISOString();
      
      return { success: true, data: products };
    } catch (error) {
      this.connectionStatus = false;
      this.errorLog.push({
        timestamp: new Date().toISOString(),
        type: 'products_fetch_failed',
        message: error.message
      });
      return { success: false, message: error.message };
    }
  }

  // جلب منتج واحد
  async getProduct(productId) {
    const cacheKey = `product_${productId}`;
    if (this.isCacheValid(cacheKey)) {
      return this.mockResponse(this.cache.get(cacheKey).data);
    }

    if (this.isDemoMode) {
      const products = await this.getProducts();
      const product = products.find(p => p.item_code === productId || p.id === productId);
      return this.mockResponse(product);
    }

    try {
      const response = await api.get(`/products/${productId}/`);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const product = response.data.value;
      this.cache.set(cacheKey, { data: product, timestamp: Date.now() });
      
      return { success: true, data: product };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال العملاء ==========

  // جلب جميع العملاء (Updated to use real database)
  async getAllCustomers() {
    const cacheKey = 'customers_all';
    if (this.isCacheValid(cacheKey)) {
      return this.mockResponse(this.cache.get(cacheKey).data);
    }

    if (this.isDemoMode) {
      const customers = await this.getCustomers(); // This now fetches from DB
      this.cache.set(cacheKey, { data: customers, timestamp: Date.now() });
      return this.mockResponse(customers);
    }

    try {
      const response = await api.get('/customers/');
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const customers = response.data.value?.results || response.data.value || [];
      this.cache.set(cacheKey, { data: customers, timestamp: Date.now() });
      this.connectionStatus = true;
      this.lastSync = new Date().toISOString();
      
      return { success: true, data: customers };
    } catch (error) {
      this.connectionStatus = false;
      this.errorLog.push({
        timestamp: new Date().toISOString(),
        type: 'customers_fetch_failed',
        message: error.message
      });
      return { success: false, message: error.message };
    }
  }

  // جلب عميل واحد
  async getCustomer(customerId) {
    const cacheKey = `customer_${customerId}`;
    if (this.isCacheValid(cacheKey)) {
      return this.mockResponse(this.cache.get(cacheKey).data);
    }

    if (this.isDemoMode) {
      const customers = await this.getCustomers();
      const customer = customers.find(c => c.name === customerId || c.id === customerId);
      return this.mockResponse(customer);
    }

    try {
      const response = await api.get(`/customers/${customerId}/`);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const customer = response.data.value;
      this.cache.set(cacheKey, { data: customer, timestamp: Date.now() });
      
      return { success: true, data: customer };
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

  // بحث عن منتجات (Updated to use real database)
  async searchProducts(query) {
    if (this.isDemoMode) {
      const products = await this.getProducts();
      const results = products.filter(
        (p) => p.item_name?.includes(query) || p.item_code?.includes(query) || p.name?.includes(query)
      );
      return this.mockResponse(results);
    }

    try {
      const response = await api.get(`/products/?search=${encodeURIComponent(query)}`);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const results = response.data.value?.results || response.data.value || [];
      return { success: true, data: results };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // بحث عن عملاء (Updated to use real database)
  async searchCustomers(query) {
    if (this.isDemoMode) {
      const customers = await this.getCustomers();
      const results = customers.filter(
        (c) => c.customer_name?.includes(query) || c.name?.includes(query) || c.email_id?.includes(query)
      );
      return this.mockResponse(results);
    }

    try {
      const response = await api.get(`/customers/?search=${encodeURIComponent(query)}`);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const results = response.data.value?.results || response.data.value || [];
      return { success: true, data: results };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال العملاء ==========

  // إنشاء عميل جديد (Updated to use real database)
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
      const response = await api.post('/customers/', customerData);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const newCustomer = response.data.value;
      this.clearCache(); // Clear cache to refresh data
      return { success: true, data: newCustomer };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  // ========== دوال الفواتير وأوامر البيع ==========

  // إنشاء أمر بيع جديد (Updated to use real database)
  async createSalesOrder(orderData) {
    if (this.isDemoMode) {
      const newOrder = {
        name: `SO-${Date.now()}`,
        ...orderData,
      };
      return this.mockResponse(newOrder, 'Sales order created successfully (Mock)');
    }

    try {
      const response = await api.post('/sales-orders/', orderData);
      await response.execute();
      
      if (response.error.value) {
        throw response.error.value;
      }
      
      const newOrder = response.data.value;
      return { success: true, data: newOrder };
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

// Export the singleton instance directly for backward compatibility
export default ERPNextService.getInstance();

// Also export the class for direct access
export { ERPNextService };
