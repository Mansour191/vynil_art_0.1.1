import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

class DashboardService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Dashboard Statistics
  async getDashboardStats() {
    try {
      const response = await this.api.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw error;
    }
  }

  // Sales Data
  async getSalesData(period = '7days') {
    try {
      const response = await this.api.get(`/dashboard/sales?period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching sales data:', error);
      throw error;
    }
  }

  // Top Products
  async getTopProducts(limit = 10) {
    try {
      const response = await this.api.get(`/dashboard/products/top?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching top products:', error);
      throw error;
    }
  }

  // Recent Orders
  async getRecentOrders(limit = 10) {
    try {
      const response = await this.api.get(`/dashboard/orders/recent?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recent orders:', error);
      throw error;
    }
  }

  // Customer Analytics
  async getCustomerAnalytics() {
    try {
      const response = await this.api.get('/dashboard/customers/analytics');
      return response.data;
    } catch (error) {
      console.error('Error fetching customer analytics:', error);
      throw error;
    }
  }

  // Orders Management
  async getOrders(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.api.get(`/orders?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching orders:', error);
      throw error;
    }
  }

  async updateOrderStatus(orderId, status) {
    try {
      const response = await this.api.patch(`/orders/${orderId}/status`, { status });
      return response.data;
    } catch (error) {
      console.error('Error updating order status:', error);
      throw error;
    }
  }

  // Products Management
  async getProducts(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.api.get(`/products?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  }

  async createProduct(productData) {
    try {
      const response = await this.api.post('/products', productData);
      return response.data;
    } catch (error) {
      console.error('Error creating product:', error);
      throw error;
    }
  }

  async updateProduct(productId, productData) {
    try {
      const response = await this.api.put(`/products/${productId}`, productData);
      return response.data;
    } catch (error) {
      console.error('Error updating product:', error);
      throw error;
    }
  }

  async deleteProduct(productId) {
    try {
      const response = await this.api.delete(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting product:', error);
      throw error;
    }
  }

  // Users Management
  async getUsers(filters = {}) {
    try {
      const params = new URLSearchParams(filters);
      const response = await this.api.get(`/users?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  }

  async createUser(userData) {
    try {
      const response = await this.api.post('/users', userData);
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  }

  async updateUser(userId, userData) {
    try {
      const response = await this.api.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  }

  async deleteUser(userId) {
    try {
      const response = await this.api.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting user:', error);
      throw error;
    }
  }
}

export default new DashboardService();
