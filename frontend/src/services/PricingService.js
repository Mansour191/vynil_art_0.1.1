import axios from 'axios';
import AIService from './AIService';
import ERPNextService from './ERPNextService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

class PricingService {
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

    this.pricingCache = new Map();
    this.competitorPrices = new Map();
  }

  // Dynamic Pricing Algorithm
  async calculateDynamicPrice(productId, context = {}) {
    try {
      const cacheKey = `price_${productId}_${JSON.stringify(context)}`;
      
      // Check cache first
      if (this.pricingCache.has(cacheKey)) {
        const cached = this.pricingCache.get(cacheKey);
        if (Date.now() - cached.timestamp < 300000) { // 5 minutes cache
          return cached.data;
        }
      }

      // Fetch product data and market analysis
      const [product, marketAnalysis, competitorData, demandForecast] = await Promise.all([
        this.getProductData(productId),
        AIService.getMarketTrends(product.category),
        this.getCompetitorPrices(productId),
        AIService.predictDemand(productId)
      ]);

      // Calculate optimal price using AI
      const optimalPrice = await this.calculateOptimalPrice(product, marketAnalysis, competitorData, demandForecast, context);

      // Cache the result
      this.pricingCache.set(cacheKey, {
        data: optimalPrice,
        timestamp: Date.now()
      });

      return optimalPrice;
    } catch (error) {
      console.error('Error calculating dynamic price:', error);
      throw error;
    }
  }

  // AI-Powered Price Optimization
  async calculateOptimalPrice(product, marketAnalysis, competitorData, demandForecast, context) {
    const factors = {
      // Market demand factor
      demand: this.calculateDemandFactor(demandForecast),
      
      // Competitor pricing factor
      competition: this.calculateCompetitionFactor(competitorData),
      
      // Seasonal factor
      seasonality: this.calculateSeasonalityFactor(product.category),
      
      // Customer segment factor
      customerSegment: this.calculateCustomerSegmentFactor(context.customerSegment),
      
      // Inventory level factor
      inventory: this.calculateInventoryFactor(product.stock),
      
      // Profit margin factor
      profitMargin: this.calculateProfitMarginFactor(product.cost),
      
      // Brand value factor
      brandValue: this.calculateBrandValueFactor(product.brand),
      
      // Time-based factor (peak hours, weekends)
      timeBased: this.calculateTimeBasedFactor()
    };

    // Calculate base price from cost
    const basePrice = product.cost * (1 + factors.profitMargin);

    // Apply all factors
    let finalPrice = basePrice;
    finalPrice *= factors.demand;
    finalPrice *= factors.competition;
    finalPrice *= factors.seasonality;
    finalPrice *= factors.customerSegment;
    finalPrice *= factors.inventory;
    finalPrice *= factors.brandValue;
    finalPrice *= factors.timeBased;

    // Apply AI prediction
    const aiAdjustment = await this.getAIPriceAdjustment(product, factors);
    finalPrice *= aiAdjustment;

    return {
      basePrice,
      finalPrice,
      factors: {
        demand: factors.demand,
        competition: factors.competition,
        seasonality: factors.seasonality,
        customerSegment: factors.customerSegment,
        inventory: factors.inventory,
        profitMargin: factors.profitMargin,
        brandValue: factors.brandValue,
        timeBased: factors.timeBased,
        aiAdjustment
      },
      recommendations: this.generatePricingRecommendations(factors),
      confidence: this.calculatePricingConfidence(factors),
      validUntil: new Date(Date.now() + 3600000) // 1 hour validity
    };
  }

  // Factor Calculation Methods
  calculateDemandFactor(demandForecast) {
    const predictedDemand = demandForecast.predictedDemand || 100;
    const averageDemand = demandForecast.averageDemand || 100;
    
    // Higher demand = higher price (elasticity)
    if (predictedDemand > averageDemand * 1.5) return 1.2; // Very high demand
    if (predictedDemand > averageDemand * 1.2) return 1.1; // High demand
    if (predictedDemand < averageDemand * 0.8) return 0.9; // Low demand
    if (predictedDemand < averageDemand * 0.5) return 0.8; // Very low demand
    
    return 1.0; // Normal demand
  }

  calculateCompetitionFactor(competitorData) {
    const avgCompetitorPrice = competitorData.averagePrice || 0;
    const minCompetitorPrice = competitorData.minPrice || 0;
    const maxCompetitorPrice = competitorData.maxPrice || 0;

    if (avgCompetitorPrice === 0) return 1.0;

    // Price relative to competition
    const priceSpread = (maxCompetitorPrice - minCompetitorPrice) / avgCompetitorPrice;

    if (priceSpread > 0.3) return 0.95; // Highly competitive market
    if (priceSpread > 0.2) return 0.98; // Competitive market
    if (priceSpread < 0.1) return 1.05; // Less competitive market
    if (priceSpread < 0.05) return 1.1; // Monopoly-like situation

    return 1.0; // Normal competition
  }

  calculateSeasonalityFactor(category) {
    const month = new Date().getMonth();
    const seasonalityFactors = {
      'furniture': {
        0: 1.1, 1: 1.05, 2: 1.0, 3: 0.95, 4: 0.9, 5: 0.85, // Winter months
        6: 0.9, 7: 0.95, 8: 1.0, 9: 1.05, 10: 1.1, 11: 1.15, 12: 1.2 // Holiday season
      },
      'doors': {
        0: 1.05, 1: 1.1, 2: 1.15, 3: 1.2, 4: 1.15, 5: 1.1, // Spring/Summer
        6: 1.05, 7: 1.0, 8: 0.95, 9: 0.9, 10: 0.95, 11: 1.0, 12: 1.05 // Fall/Winter
      },
      'walls': {
        0: 0.9, 1: 0.95, 2: 1.0, 3: 1.05, 4: 1.1, 5: 1.15, // Renovation season
        6: 1.2, 7: 1.15, 8: 1.1, 9: 1.05, 10: 1.0, 11: 0.95, 12: 0.9
      },
      'default': { // Default seasonality for other categories
        0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0,
        6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0
      }
    };

    return seasonalityFactors[category]?.[month] || seasonalityFactors.default[month] || 1.0;
  }

  calculateCustomerSegmentFactor(customerSegment) {
    const segmentFactors = {
      'premium': 1.2,      // Premium customers willing to pay more
      'business': 1.15,     // Business customers
      'regular': 1.0,       // Regular customers
      'price_sensitive': 0.85, // Price-sensitive customers
      'new': 0.9           // New customers (introductory pricing)
    };

    return segmentFactors[customerSegment] || 1.0;
  }

  calculateInventoryFactor(stock) {
    // Low inventory = higher price (scarcity)
    // High inventory = lower price (clearance)
    
    if (stock <= 5) return 1.1;      // Very low stock
    if (stock <= 10) return 1.05;    // Low stock
    if (stock <= 20) return 1.0;     // Normal stock
    if (stock <= 50) return 0.95;    // High stock
    return 0.9;                     // Very high stock
  }

  calculateProfitMarginFactor(cost) {
    // Base profit margin calculation
    const baseMargin = 0.3; // 30% base margin
    
    // Adjust based on cost
    if (cost > 10000) return baseMargin * 1.1;  // High-value items
    if (cost < 1000) return baseMargin * 0.9;   // Low-value items
    
    return baseMargin;
  }

  calculateBrandValueFactor(brand) {
    const brandFactors = {
      'premium': 1.2,
      'designer': 1.15,
      'established': 1.05,
      'new': 0.95,
      'generic': 0.9
    };

    return brandFactors[brand] || 1.0;
  }

  calculateTimeBasedFactor() {
    const hour = new Date().getHours();
    const dayOfWeek = new Date().getDay();
    
    let timeFactor = 1.0;
    
    // Peak hours (9 AM - 5 PM)
    if (hour >= 9 && hour <= 17) {
      timeFactor *= 1.02;
    }
    
    // Weekend premium
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      timeFactor *= 1.03;
    }
    
    // Late night discount
    if (hour >= 22 || hour <= 6) {
      timeFactor *= 0.98;
    }
    
    return timeFactor;
  }

  // AI Integration
  async getAIPriceAdjustment(product, factors) {
    try {
      const aiAnalysis = await AIService.analyzePricingFactors({
        product,
        factors,
        marketContext: {
          region: 'algeria',
          currency: 'DZD',
          season: this.getCurrentSeason()
        }
      });

      return aiAnalysis.recommendedAdjustment || 1.0;
    } catch (error) {
      console.error('Error getting AI price adjustment:', error);
      return 1.0;
    }
  }

  // Helper Methods
  async getProductData(productId) {
    try {
      const response = await this.api.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching product data:', error);
      return {};
    }
  }

  async getCompetitorPrices(productId) {
    try {
      const response = await this.api.get(`/pricing/competitors/${productId}`);
      this.competitorPrices.set(productId, response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching competitor prices:', error);
      return { averagePrice: 0, minPrice: 0, maxPrice: 0 };
    }
  }

  getCurrentSeason() {
    const month = new Date().getMonth();
    if (month >= 2 && month <= 4) return 'spring';
    if (month >= 5 && month <= 7) return 'summer';
    if (month >= 8 && month <= 10) return 'fall';
    return 'winter';
  }

  generatePricingRecommendations(factors) {
    const recommendations = [];

    if (factors.demand > 1.1) {
      recommendations.push({
        type: 'opportunity',
        message: 'الطلب مرتفع - يمكن زيادة السعر',
        confidence: 0.8
      });
    }

    if (factors.competition < 0.95) {
      recommendations.push({
        type: 'warning',
        message: 'السوق تنافسي جداً - قد تحتاج لتخفيض السعر',
        confidence: 0.9
      });
    }

    if (factors.inventory < 0.9) {
      recommendations.push({
        type: 'action',
        message: 'المخزون مرتفع - فكر في عرض خصم',
        confidence: 0.7
      });
    }

    return recommendations;
  }

  calculatePricingConfidence(factors) {
    // Calculate confidence based on factor stability
    const factorVariance = Object.values(factors).reduce((acc, val) => {
      return acc + Math.abs(val - 1.0);
    }, 0) / Object.keys(factors).length;

    // Higher variance = lower confidence
    return Math.max(0.5, 1 - factorVariance);
  }

  // Batch Pricing Operations
  async updateMultiplePrices(priceUpdates) {
    try {
      const response = await this.api.post('/pricing/batch-update', {
        updates: priceUpdates
      });

      // Sync with ERPNext
      await ERPNextService.syncToERPNext('pricing_updates', {
        updates: priceUpdates,
        timestamp: new Date().toISOString()
      });

      // Clear cache for updated products
      priceUpdates.forEach(update => {
        this.clearPriceCache(update.productId);
      });

      return response.data;
    } catch (error) {
      console.error('Error updating multiple prices:', error);
      throw error;
    }
  }

  // Pricing Analytics
  async getPricingAnalytics(productId = null, period = '30days') {
    try {
      const response = await this.api.get(`/pricing/analytics?product_id=${productId}&period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching pricing analytics:', error);
      throw error;
    }
  }

  async getPriceHistory(productId, period = '90days') {
    try {
      const response = await this.api.get(`/pricing/history/${productId}?period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching price history:', error);
      throw error;
    }
  }

  // Price Optimization Rules
  async createPricingRule(rule) {
    try {
      const response = await this.api.post('/pricing/rules', rule);
      return response.data;
    } catch (error) {
      console.error('Error creating pricing rule:', error);
      throw error;
    }
  }

  async getPricingRules() {
    try {
      const response = await this.api.get('/pricing/rules');
      return response.data;
    } catch (error) {
      console.error('Error fetching pricing rules:', error);
      throw error;
    }
  }

  async updatePricingRule(ruleId, rule) {
    try {
      const response = await this.api.put(`/pricing/rules/${ruleId}`, rule);
      return response.data;
    } catch (error) {
      console.error('Error updating pricing rule:', error);
      throw error;
    }
  }

  async deletePricingRule(ruleId) {
    try {
      const response = await this.api.delete(`/pricing/rules/${ruleId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting pricing rule:', error);
      throw error;
    }
  }

  // Cache Management
  clearPriceCache(productId) {
    // Clear all cache entries for a product
    for (const [key, value] of this.pricingCache.entries()) {
      if (key.startsWith(`price_${productId}_`)) {
        this.pricingCache.delete(key);
      }
    }
  }

  clearAllCache() {
    this.pricingCache.clear();
    this.competitorPrices.clear();
  }

  // Price Testing
  async runPriceTest(testConfig) {
    try {
      const response = await this.api.post('/pricing/test', testConfig);
      return response.data;
    } catch (error) {
      console.error('Error running price test:', error);
      throw error;
    }
  }

  // Real-time Price Updates
  subscribeToPriceUpdates(callback) {
    // WebSocket connection for real-time pricing updates
    const ws = new WebSocket(`${API_BASE_URL.replace('http', 'ws')}/pricing/updates`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      callback(data);
      
      // Clear cache for updated products
      if (data.productId) {
        this.clearPriceCache(data.productId);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return ws;
  }
}

export default new PricingService();
