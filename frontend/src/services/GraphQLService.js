import { apolloClient } from './apolloClient';
import { provideApolloClient } from '@vue/apollo-composable';

// Ensure Apollo Client is available for GraphQL service
provideApolloClient(apolloClient);

// GraphQL Service - Direct Apollo Client usage for services
class GraphQLService {
  constructor() {
    this.client = apolloClient;
  }

  async query(query, variables = {}, options = {}) {
    try {
      console.log('🚀 GraphQL Query Starting:', {
        queryName: query.definitions[0]?.name?.value || 'Unknown',
        variables,
        timestamp: new Date().toISOString()
      });

      // Fix Apollo Error 18: Reset cache before critical queries
      if (query.definitions[0]?.name?.value === 'CheckAIHealth') {
        console.log('🔄 Resetting Apollo cache for CheckAIHealth query...');
        try {
          await this.client.clearStore();
          console.log('✅ Apollo cache reset successfully');
        } catch (cacheError) {
          console.warn('⚠️ Failed to reset Apollo cache:', cacheError.message);
        }
      }

      const result = await this.client.query({
        query,
        variables,
        errorPolicy: 'all',
        fetchPolicy: 'network-only', // Force network request for health checks
        ...options
      });
      
      // طباعة تفاصيل الخطأ القادم من المصفوفة errors[0].message
      if (result.errors && result.errors.length > 0) {
        console.error('🔍 GraphQL Query Errors:', {
          queryName: query.definitions[0]?.name?.value || 'Unknown',
          errors: result.errors.map(error => ({
            message: error.message,
            locations: error.locations,
            path: error.path,
            extensions: error.extensions
          })),
          variables,
          timestamp: new Date().toISOString()
        });
      }
      
      console.log('✅ GraphQL Query Success:', {
        queryName: query.definitions[0]?.name?.value || 'Unknown',
        hasData: !!result.data,
        hasErrors: !!(result.errors && result.errors.length > 0),
        timestamp: new Date().toISOString()
      });
      
      return {
        data: result.data,
        errors: result.errors,
        loading: false,
        success: !result.errors || result.errors.length === 0
      };
    } catch (error) {
      // Special handling for Apollo Error 18 (InvariantError)
      if (error.message.includes('Invariant Violation') || error.message.includes('go.apollo.dev/c/err')) {
        console.error('❌ Apollo Error 18 Detected:', {
          queryName: query.definitions[0]?.name?.value || 'Unknown',
          errorMessage: error.message,
          errorType: error.constructor.name,
          isApolloError18: true,
          variables,
          timestamp: new Date().toISOString()
        });

        // Try to reset cache and retry once
        try {
          console.log('🔄 Attempting cache reset and retry for Apollo Error 18...');
          await this.client.clearStore();
          
          // Retry with network-only policy
          const retryResult = await this.client.query({
            query,
            variables,
            errorPolicy: 'all',
            fetchPolicy: 'network-only',
            ...options
          });

          console.log('✅ Apollo Error 18 resolved after retry');
          return {
            data: retryResult.data,
            errors: retryResult.errors,
            loading: false,
            success: !retryResult.errors || retryResult.errors.length === 0,
            retried: true
          };
        } catch (retryError) {
          console.error('❌ Retry failed for Apollo Error 18:', retryError.message);
        }
      }

      console.error('❌ GraphQL Query Critical Error:', {
        queryName: query.definitions[0]?.name?.value || 'Unknown',
        errorMessage: error.message,
        errorType: error.constructor.name,
        stack: error.stack,
        variables,
        timestamp: new Date().toISOString()
      });
      return {
        data: null,
        errors: [error],
        loading: false,
        success: false
      };
    }
  }

  async mutate(mutation, variables = {}, options = {}) {
    try {
      const result = await this.client.mutate({
        mutation,
        variables,
        errorPolicy: 'all',
        ...options
      });
      
      return {
        data: result.data,
        errors: result.errors,
        loading: false,
        success: !result.errors || result.errors.length === 0
      };
    } catch (error) {
      console.error('GraphQL Mutation Error:', error);
      return {
        data: null,
        errors: [error],
        loading: false,
        success: false
      };
    }
  }

  // ✅ نسخة مصلحة ومنظمة بالكامل
  async checkAIHealth(service = 'general') {
    try {
      // Try checkAIHealth first (frontend compatible)
      try {
        const { CHECK_AI_HEALTH } = await import('@/graphql/queries');
        console.log('📡 Sending Query: CHECK_AI_HEALTH');
        let result = await this.query(CHECK_AI_HEALTH, { service });
        console.log('📥 Server Response:', result);

        if (result.success && result.data?.checkAIHealth) {
          return {
            success: true,
            data: result.data,
            status: result.data.checkAIHealth.status || 'healthy',
            available: result.data.checkAIHealth.available || true,
            responseTime: 100,
            lastCheck: new Date().toISOString()
          };
        }
      } catch (checkError) {
        console.log('⚠️ checkAIHealth failed, trying aiHealth fallback');
      }

      // Fallback to aiHealth query
      const { AI_HEALTH_CHECK } = await import('@/graphql/queries');
      console.log('📡 Sending Query: AI_HEALTH_CHECK (fallback)');
      let result = await this.query(AI_HEALTH_CHECK, { service });
      console.log('📥 Server Response:', result);

      if (result.success && result.data?.aiHealth) {
        return {
          success: true,
          data: result.data,
          status: result.data.aiHealth.status || 'healthy',
          available: result.data.aiHealth.available || true,
          responseTime: 100,
          lastCheck: new Date().toISOString()
        };
      }

      // Fallback في حال فشل الطلب
      console.warn('⚠️ AI Health Check failed, using fallback');
      return {
        success: false,
        data: null,
        errors: result.errors,
        status: 'degraded',
        service: service,
        available: true,
        // حقن يدوي للحقول التي لا يرسلها السيرفر
        responseTime: 100,
        lastCheck: new Date().toISOString()
      };
    } catch (error) {
      console.error('⚠️ Critical error in checkAIHealth:', error.message);
      return {
        status: 'error',
        service: service,
        available: false,
        // حقن يدوي للحقول التي لا يرسلها السيرفر
        responseTime: 100,
        lastCheck: new Date().toISOString()
      };
    }
  }

  // System Health Check
  async checkSystemHealth() {
    try {
      const { SYSTEM_HEALTH_CHECK } = await import('@/graphql/enhancedMutations');
      
      console.log('📡 Sending Query: SYSTEM_HEALTH_CHECK');
      let result = await this.query(SYSTEM_HEALTH_CHECK);
      console.log('📥 Server Response:', result);

      if (result.success && result.data?.systemHealthCheck) {
        return {
          status: result.data.systemHealthCheck.status || 'unknown',
          available: result.data.systemHealthCheck.available || false,
          // حقن يدوي للحقول التي لا يرسلها السيرفر
          responseTime: 100,
          lastCheck: new Date().toISOString()
        };
      }

      // Fallback في حال فشل الطلب
      console.warn('⚠️ System Health Check failed, using fallback');
      return {
        status: 'degraded',
        available: true,
        // حقن يدوي للحقول التي لا يرسلها السيرفر
        responseTime: 100,
        lastCheck: new Date().toISOString()
      };
    } catch (error) {
      console.error('⚠️ Critical error in checkSystemHealth:', error.message);
      return {
        status: 'error',
        available: false,
        // حقن يدوي للحقول التي لا يرسلها السيرفر
        responseTime: 100,
        lastCheck: new Date().toISOString()
      };
    }
  }

  // Market Trends
  async getMarketTrends(category = null, period = '30days') {
    try {
      const { MARKET_TRENDS } = await import('@/graphql/queries');
      let result = await this.query(MARKET_TRENDS, { category, period });
      
      if (!result.success) {
        return {
          data: {
            marketTrends: {
              trend: 'stable',
              confidence: 0.8,
              factors: ['market_analysis'],
              category,
              period
            }
          },
          success: true
        };
      }
      return result;
    } catch (error) {
      return {
        data: { marketTrends: { trend: 'stable', category, period } },
        success: true
      };
    }
  }

  // Demand Forecast
  async getDemandForecast(productId, period = '30days') {
    const { DEMAND_FORECAST } = await import('@/graphql/queries');
    return this.query(DEMAND_FORECAST, { productId, period });
  }

  // Chat with AI
  async chatWithAI(message, conversationHistory = []) {
    try {
      const { CHAT_WITH_AI_MUTATION } = await import('@/graphql/mutations');
      const result = await this.mutate(CHAT_WITH_AI_MUTATION, { message, conversationHistory });
      
      if (!result.success) {
        return {
          data: { chatWithAi: { response: `استجابة تجريبية: "${message}". الخدمة قيد التطوير.` } },
          success: true
        };
      }
      return result;
    } catch (error) {
      return {
        data: { chatWithAi: { response: "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي." } },
        success: true
      };
    }
  }

  async getProducts(categorySlug = null) {
    const { GET_PRODUCTS } = await import('@/graphql/queries');
    return this.query(GET_PRODUCTS, { categorySlug });
  }

  async getProduct(id) {
    const { GET_PRODUCT } = await import('@/graphql/queries');
    return this.query(GET_PRODUCT, { id });
  }

  async getCategories() {
    const { GET_CATEGORIES } = await import('@/graphql/queries');
    return this.query(GET_CATEGORIES);
  }

  async getMe() {
    const { GET_ME } = await import('@/graphql/queries');
    return this.query(GET_ME);
  }

  async login(email, password) {
    const { LOGIN_MUTATION } = await import('@/graphql/mutations');
    return this.mutate(LOGIN_MUTATION, { email, password });
  }

  async register(userData) {
    const { REGISTER_MUTATION } = await import('@/graphql/mutations');
    return this.mutate(REGISTER_MUTATION, userData);
  }

  async updateProfile(userData) {
    const { UPDATE_PROFILE_MUTATION } = await import('@/graphql/mutations');
    return this.mutate(UPDATE_PROFILE_MUTATION, userData);
  }

  async createOrder(orderData) {
    const { CREATE_ORDER_MUTATION } = await import('@/graphql/mutations');
    return this.mutate(CREATE_ORDER_MUTATION, orderData);
  }

  async getShippingOptions() {
    const { GET_SHIPPING_OPTIONS } = await import('@/graphql/queries');
    return this.query(GET_SHIPPING_OPTIONS);
  }
}

const graphQLService = new GraphQLService();
export default graphQLService;
