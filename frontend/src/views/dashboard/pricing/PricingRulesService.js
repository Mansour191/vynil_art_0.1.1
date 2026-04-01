// Pricing Rules Service - API Integration for Pricing Rules Management
import BaseService from '@/services/BaseService';

class PricingRulesService extends BaseService {
  constructor() {
    super();
    this.endpoint = '/pricing/rules';
  }

  // Get all pricing rules with pagination and filters
  async getPricingRules(params = {}) {
    try {
      const response = await this.apiRequest(this.endpoint, {
        method: 'GET',
        params
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rules fetched successfully'
      };
    } catch (error) {
      console.error('Error fetching pricing rules:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to fetch pricing rules',
        mockData: this.getMockRules()
      };
    }
  }

  // Get pricing rule by ID
  async getPricingRuleById(ruleId) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/${ruleId}`, {
        method: 'GET'
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule fetched successfully'
      };
    } catch (error) {
      console.error('Error fetching pricing rule:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to fetch pricing rule'
      };
    }
  }

  // Create new pricing rule
  async createPricingRule(ruleData) {
    try {
      const response = await this.apiRequest(this.endpoint, {
        method: 'POST',
        body: JSON.stringify(ruleData)
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule created successfully'
      };
    } catch (error) {
      console.error('Error creating pricing rule:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to create pricing rule'
      };
    }
  }

  // Update pricing rule
  async updatePricingRule(ruleId, ruleData) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/${ruleId}`, {
        method: 'PUT',
        body: JSON.stringify(ruleData)
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule updated successfully'
      };
    } catch (error) {
      console.error('Error updating pricing rule:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to update pricing rule'
      };
    }
  }

  // Delete pricing rule
  async deletePricingRule(ruleId) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/${ruleId}`, {
        method: 'DELETE'
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule deleted successfully'
      };
    } catch (error) {
      console.error('Error deleting pricing rule:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to delete pricing rule'
      };
    }
  }

  // Toggle pricing rule status (active/inactive)
  async togglePricingRuleStatus(ruleId) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/${ruleId}/toggle`, {
        method: 'PATCH'
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule status updated successfully'
      };
    } catch (error) {
      console.error('Error toggling pricing rule status:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to toggle pricing rule status'
      };
    }
  }

  // Get pricing analytics
  async getPricingAnalytics(params = {}) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/analytics`, {
        method: 'GET',
        params
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing analytics fetched successfully'
      };
    } catch (error) {
      console.error('Error fetching pricing analytics:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to fetch pricing analytics',
        mockData: this.getMockAnalytics()
      };
    }
  }

  // Run pricing optimization
  async runPricingOptimization(params = {}) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/optimize`, {
        method: 'POST',
        body: JSON.stringify(params)
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing optimization completed successfully'
      };
    } catch (error) {
      console.error('Error running pricing optimization:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to run pricing optimization'
      };
    }
  }

  // Test pricing rule
  async testPricingRule(ruleData, productId) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/test`, {
        method: 'POST',
        body: JSON.stringify({ rule: ruleData, productId })
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rule test completed successfully'
      };
    } catch (error) {
      console.error('Error testing pricing rule:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to test pricing rule'
      };
    }
  }

  // Export pricing rules
  async exportPricingRules(params = {}) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/export`, {
        method: 'GET',
        params
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Pricing rules exported successfully'
      };
    } catch (error) {
      console.error('Error exporting pricing rules:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to export pricing rules'
      };
    }
  }

  // Bulk operations
  async bulkUpdateRules(ruleIds, updateData) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/bulk-update`, {
        method: 'PATCH',
        body: JSON.stringify({ ruleIds, updateData })
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Bulk update successful'
      };
    } catch (error) {
      console.error('Error bulk updating rules:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to bulk update rules'
      };
    }
  }

  async bulkDeleteRules(ruleIds) {
    try {
      const response = await this.apiRequest(`${this.endpoint}/bulk-delete`, {
        method: 'DELETE',
        body: JSON.stringify({ ruleIds })
      });
      return {
        success: true,
        data: response.data || response,
        message: 'Bulk delete successful'
      };
    } catch (error) {
      console.error('Error bulk deleting rules:', error);
      return {
        success: false,
        error: error.message,
        message: 'Failed to bulk delete rules'
      };
    }
  }

  // Mock data for fallback
  getMockRules() {
    return {
      rules: [
        {
          id: 1,
          name: 'زيادة الأسعار في المواسم',
          description: 'زيادة أسعار المنتجات بنسبة 20% خلال مواسم الأعياد',
          type: 'percentage',
          value: 20,
          conditions: ['مواسم الأعياد', 'زيادة الطلب'],
          targetProducts: [1, 2, 3],
          isActive: true,
          priority: 'high',
          createdAt: '2024-01-15T10:30:00Z',
          updatedAt: '2024-01-20T14:45:00Z'
        },
        {
          id: 2,
          name: 'خصم للعملاء الجدد',
          description: 'خصم 15% للعملاء الجدد على أول عملية شراء',
          type: 'percentage',
          value: -15,
          conditions: ['عميل جديد', 'أول عملية شراء'],
          targetProducts: [4, 5, 6],
          isActive: true,
          priority: 'medium',
          createdAt: '2024-01-10T09:15:00Z',
          updatedAt: '2024-01-18T11:30:00Z'
        },
        {
          id: 3,
          name: 'تسعير ديناميكي للمنتجات المباعة',
          description: 'تعديل الأسعار بناءً على مستوى المخزون',
          type: 'conditional',
          value: 'inventory_based',
          conditions: ['مخزون منخفض', 'طلب مرتفع'],
          targetProducts: [7, 8],
          isActive: false,
          priority: 'low',
          createdAt: '2024-01-05T16:20:00Z',
          updatedAt: '2024-01-12T13:10:00Z'
        }
      ],
      total: 3,
      page: 1,
      totalPages: 1
    };
  }

  getMockAnalytics() {
    return {
      overview: {
        totalRules: 12,
        activeRules: 8,
        inactiveRules: 4,
        avgPriceIncrease: 15.5,
        revenueImpact: 25000
      },
      trends: {
        monthly: [
          { month: 'يناير', revenue: 120000, orders: 450 },
          { month: 'فبراير', revenue: 135000, orders: 520 },
          { month: 'مارس', revenue: 142000, orders: 580 },
          { month: 'أبريل', revenue: 138000, orders: 560 },
          { month: 'مايو', revenue: 155000, orders: 620 },
          { month: 'يونيو', revenue: 168000, orders: 680 }
        ]
      },
      performance: {
        topPerformingRules: [
          { name: 'زيادة الأسعار في المواسم', impact: 8500, usage: 45 },
          { name: 'خصم للعملاء الجدد', impact: 6200, usage: 38 },
          { name: 'تسعير ديناميكي', impact: 4800, usage: 28 }
        ],
        categoryBreakdown: [
          { category: 'إلكترونيات', avgPrice: 2500, change: 5.2 },
          { category: 'ملابس', avgPrice: 350, change: -2.1 },
          { category: 'أثاث', avgPrice: 1200, change: 8.7 }
        ]
      }
    };
  }
}

// Export singleton instance
const pricingRulesServiceInstance = new PricingRulesService();
export default pricingRulesServiceInstance;
export { PricingRulesService };
