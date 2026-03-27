import { api } from '@/composables/useApi';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
const ERPNEXT_API_URL = import.meta.env.VITE_ERPNEXT_URL || 'http://127.0.0.1:8001';

class ERPNextService {
  constructor() {
    // ERPNext direct API URL for external connections
    this.erpnextApiUrl = ERPNEXT_API_URL;
  }

  // Customer Migration
  async migrateCustomers() {
    try {
      const response = await api.post('erpnext/migrate/customers');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error migrating customers:', error);
      throw error;
    }
  }

  async syncCustomer(customerId) {
    try {
      const response = await api.post(`erpnext/sync/customer/${customerId}`);
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error syncing customer:', error);
      throw error;
    }
  }

  async getCustomerSyncStatus() {
    try {
      const response = await api.get('erpnext/sync/customers/status');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error fetching customer sync status:', error);
      throw error;
    }
  }

  // Product Migration
  async migrateProducts() {
    try {
      const response = await api.post('erpnext/migrate/products');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error migrating products:', error);
      throw error;
    }
  }

  async syncProduct(productId) {
    try {
      const response = await api.post(`erpnext/sync/product/${productId}`);
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error syncing product:', error);
      throw error;
    }
  }

  async getProductSyncStatus() {
    try {
      const response = await api.get('erpnext/sync/products/status');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error fetching product sync status:', error);
      throw error;
    }
  }

  // Order Migration
  async migrateOrders(startDate = null, endDate = null) {
    try {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate);
      if (endDate) params.append('end_date', endDate);
      
      const response = await api.post(`erpnext/migrate/orders?${params}`);
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error migrating orders:', error);
      throw error;
    }
  }

  async syncOrder(orderId) {
    try {
      const response = await api.post(`erpnext/sync/order/${orderId}`);
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error syncing order:', error);
      throw error;
    }
  }

  async getOrderSyncStatus() {
    try {
      const response = await api.get('erpnext/sync/orders/status');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error fetching order sync status:', error);
      throw error;
    }
  }

  // Inventory Migration
  async migrateInventory() {
    try {
      const response = await api.post('erpnext/migrate/inventory');
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error migrating inventory:', error);
      throw error;
    }
  }

  async syncInventoryItem(itemId) {
    try {
      const response = await api.post(`erpnext/sync/inventory/${itemId}`);
      await response.execute();
      if (response.error.value) {
        throw response.error.value;
      }
      return response.data.value;
    } catch (error) {
      console.error('Error syncing inventory item:', error);
      throw error;
    }
  }

  // Financial Data Migration
  async migrateFinancialData(type = 'all', period = 'last_30_days') {
    try {
      const response = await this.api.post('/erpnext/migrate/financial', {
        type,
        period
      });
      return response.data;
    } catch (error) {
      console.error('Error migrating financial data:', error);
      throw error;
    }
  }

  // Two-way Sync
  async syncFromERPNext(dataType = 'all') {
    try {
      const response = await this.api.get(`/erpnext/sync/from-erpnext?type=${dataType}`);
      return response.data;
    } catch (error) {
      console.error('Error syncing from ERPNext:', error);
      throw error;
    }
  }

  async syncToERPNext(dataType, data) {
    try {
      const response = await this.api.post(`/erpnext/sync/to-erpnext/${dataType}`, data);
      return response.data;
    } catch (error) {
      console.error('Error syncing to ERPNext:', error);
      throw error;
    }
  }

  // ERPNext Direct API Methods
  async getERPNextCustomers(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.erpnextApi.get(`/api/resource/Customer?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching ERPNext customers:', error);
      throw error;
    }
  }

  async createERPNextCustomer(customerData) {
    try {
      const response = await this.erpnextApi.post('/api/resource/Customer', customerData);
      return response.data;
    } catch (error) {
      console.error('Error creating ERPNext customer:', error);
      throw error;
    }
  }

  async getERPNextProducts(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.erpnextApi.get(`/api/resource/Item?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching ERPNext products:', error);
      throw error;
    }
  }

  async createERPNextProduct(productData) {
    try {
      const response = await this.erpnextApi.post('/api/resource/Item', productData);
      return response.data;
    } catch (error) {
      console.error('Error creating ERPNext product:', error);
      throw error;
    }
  }

  async getERPNextOrders(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.erpnextApi.get(`/api/resource/Sales Order?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching ERPNext orders:', error);
      throw error;
    }
  }

  async createERPNextOrder(orderData) {
    try {
      const response = await this.erpnextApi.post('/api/resource/Sales Order', orderData);
      return response.data;
    } catch (error) {
      console.error('Error creating ERPNext order:', error);
      throw error;
    }
  }

  // Real-time Sync
  async startRealTimeSync() {
    try {
      const response = await this.api.post('/erpnext/realtime-sync/start');
      return response.data;
    } catch (error) {
      console.error('Error starting real-time sync:', error);
      throw error;
    }
  }

  async stopRealTimeSync() {
    try {
      const response = await this.api.post('/erpnext/realtime-sync/stop');
      return response.data;
    } catch (error) {
      console.error('Error stopping real-time sync:', error);
      throw error;
    }
  }

  async getRealTimeSyncStatus() {
    try {
      const response = await this.api.get('/erpnext/realtime-sync/status');
      return response.data;
    } catch (error) {
      console.error('Error fetching real-time sync status:', error);
      throw error;
    }
  }

  // Conflict Resolution
  async getSyncConflicts(dataType = 'all') {
    try {
      const response = await this.api.get(`/erpnext/conflicts?type=${dataType}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching sync conflicts:', error);
      throw error;
    }
  }

  async resolveSyncConflict(conflictId, resolution) {
    try {
      const response = await this.api.post(`/erpnext/conflicts/${conflictId}/resolve`, {
        resolution
      });
      return response.data;
    } catch (error) {
      console.error('Error resolving sync conflict:', error);
      throw error;
    }
  }

  // Audit Logs
  async getSyncAuditLogs(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.api.get(`/erpnext/audit/logs?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      throw error;
    }
  }

  // Backup and Restore
  async createBackup(dataType = 'all') {
    try {
      const response = await this.api.post(`/erpnext/backup/create?type=${dataType}`);
      return response.data;
    } catch (error) {
      console.error('Error creating backup:', error);
      throw error;
    }
  }

  async restoreFromBackup(backupId) {
    try {
      const response = await this.api.post(`/erpnext/backup/restore/${backupId}`);
      return response.data;
    } catch (error) {
      console.error('Error restoring from backup:', error);
      throw error;
    }
  }

  async getBackupHistory() {
    try {
      const response = await this.api.get('/erpnext/backup/history');
      return response.data;
    } catch (error) {
      console.error('Error fetching backup history:', error);
      throw error;
    }
  }

  // Configuration Management
  async getERPNextConfig() {
    try {
      const response = await this.api.get('/erpnext/config');
      return response.data;
    } catch (error) {
      console.error('Error fetching ERPNext config:', error);
      throw error;
    }
  }

  async updateERPNextConfig(config) {
    try {
      const response = await this.api.put('/erpnext/config', config);
      return response.data;
    } catch (error) {
      console.error('Error updating ERPNext config:', error);
      throw error;
    }
  }

  // Health Check
  async checkERPNextHealth() {
    try {
      const response = await this.erpnextApi.get('/api/method/ping');
      return response.data;
    } catch (error) {
      console.error('ERPNext health check failed:', error);
      throw error;
    }
  }

  async checkIntegrationHealth() {
    try {
      const response = await this.api.get('/erpnext/health/');
      return response.data;
    } catch (error) {
      console.error('Integration health check failed:', error);
      throw error;
    }
  }
}

export default new ERPNextService();
