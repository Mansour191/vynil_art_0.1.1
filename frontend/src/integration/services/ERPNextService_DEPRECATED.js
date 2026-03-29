// DEPRECATED - MIGRATED TO GRAPHQL
// This service has been completely replaced by GraphQLERPNextService.js
// All ERPNext operations should now use GraphQL mutations
// 
// MIGRATION GUIDE:
// OLD: ERPNextService.syncCustomer(id)
// NEW: GraphQLERPNextService.syncWithERPNext('customers')
//
// OLD: ERPNextService.syncProduct(id)  
// NEW: GraphQLERPNextService.syncWithERPNext('products')
//
// OLD: ERPNextService.syncOrder(id)
// NEW: GraphQLERPNextService.syncWithERPNext('orders')

import config from '../config/erpnext.config';

// Singleton instance and request coordination
let erpServiceInstance = null;
let erpHealthCheckPromise = null;

class ERPNextService {
  constructor() {
    console.warn('⚠️ ERPNextService is deprecated. Please use GraphQLERPNextService.js instead.');
    
    // ALL METHODS BELOW ARE DEPRECATED - USE GraphQLERPNextService INSTEAD
    throw new Error('ERPNextService is deprecated. Please use GraphQLERPNextService.js instead.');
  }

  // Static method to get instance
  static getInstance() {
    console.error('❌ ERPNextService.getInstance() is deprecated. Use GraphQLERPNextService instead.');
    throw new Error('This service has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  // ALL OTHER METHODS ARE DEPRECATED - USE GraphQLERPNextService INSTEAD
  
  async checkIntegrationHealth() {
    console.error('❌ checkIntegrationHealth() is deprecated. Use GraphQLERPNextService.testConnection() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async syncCustomers() {
    console.error('❌ syncCustomers() is deprecated. Use GraphQLERPNextService.syncWithERPNext("customers") instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async syncProducts() {
    console.error('❌ syncProducts() is deprecated. Use GraphQLERPNextService.syncWithERPNext("products") instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async syncOrders() {
    console.error('❌ syncOrders() is deprecated. Use GraphQLERPNextService.syncWithERPNext("orders") instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getSyncStatus() {
    console.error('❌ getSyncStatus() is deprecated. Use GraphQLERPNextService.getSyncStatus() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getCustomers() {
    console.error('❌ getCustomers() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async getProducts() {
    console.error('❌ getProducts() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async getOrders() {
    console.error('❌ getOrders() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async createCustomer(customerData) {
    console.error('❌ createCustomer() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async createProduct(productData) {
    console.error('❌ createProduct() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async createOrder(orderData) {
    console.error('❌ createOrder() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async updateCustomer(customerId, customerData) {
    console.error('❌ updateCustomer() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async updateProduct(productId, productData) {
    console.error('❌ updateProduct() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async updateOrder(orderId, orderData) {
    console.error('❌ updateOrder() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async deleteCustomer(customerId) {
    console.error('❌ deleteCustomer() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async deleteProduct(productId) {
    console.error('❌ deleteProduct() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async deleteOrder(orderId) {
    console.error('❌ deleteOrder() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async getInventory() {
    console.error('❌ getInventory() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async syncInventory() {
    console.error('❌ syncInventory() is deprecated. Use GraphQLERPNextService.syncWithERPNext("inventory") instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getReports(reportType, filters = {}) {
    console.error('❌ getReports() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async getAnalytics(timeRange = '30d') {
    console.error('❌ getAnalytics() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async validateConfig() {
    console.error('❌ validateConfig() is deprecated. Use GraphQLERPNextService.validateConfig() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async updateConfig(newConfig) {
    console.error('❌ updateConfig() is deprecated. Use GraphQLERPNextService.updateConfig() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getConfig() {
    console.error('❌ getConfig() is deprecated. Use GraphQLERPNextService.getConfig() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getSyncHistory(limit = 50) {
    console.error('❌ getSyncHistory() is deprecated. Use GraphQLERPNextService.getSyncHistory() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async retryFailedSync(syncId) {
    console.error('❌ retryFailedSync() is deprecated. Use GraphQLERPNextService.retryFailedSync() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async scheduleSync(syncType, schedule) {
    console.error('❌ scheduleSync() is deprecated. Use GraphQLERPNextService.scheduleAutoSync() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async cancelScheduledSync(syncId) {
    console.error('❌ cancelScheduledSync() is deprecated. Use GraphQLERPNextService.cancelScheduledSync() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async getSyncMetrics() {
    console.error('❌ getSyncMetrics() is deprecated. Use GraphQLERPNextService.getSyncMetrics() instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQLERPNextService.');
  }

  async exportData(dataType, filters = {}) {
    console.error('❌ exportData() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async importData(dataType, data) {
    console.error('❌ importData() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async search(query, filters = {}) {
    console.error('❌ search() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async getNotifications() {
    console.error('❌ getNotifications() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async markNotificationRead(notificationId) {
    console.error('❌ markNotificationRead() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async createNotification(notificationData) {
    console.error('❌ createNotification() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async deleteNotification(notificationId) {
    console.error('❌ deleteNotification() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async getAuditLog(filters = {}) {
    console.error('❌ getAuditLog() is deprecated. Use GraphQL queries instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL queries.');
  }

  async backupData(dataType) {
    console.error('❌ backupData() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }

  async restoreData(backupId) {
    console.error('❌ restoreData() is deprecated. Use GraphQL mutations instead.');
    throw new Error('This method has been migrated to GraphQL. Please use GraphQL mutations.');
  }
}

// Create singleton instance
export const erpNextService = new ERPNextService();

// Export class for custom instances
export default ERPNextService;

console.log('📦 ERPNextService - FULLY DEPRECATED - Use GraphQLERPNextService.js instead');
