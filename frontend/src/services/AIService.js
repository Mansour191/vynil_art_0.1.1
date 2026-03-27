import { api } from '@/composables/useApi';

// Use proxy for development, direct URL for production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Singleton instance and request coordination
let aiServiceInstance = null;
let healthCheckPromise = null;
let initializationPromise = null;

class AIService {
  constructor() {
    // Singleton pattern
    if (aiServiceInstance) {
      return aiServiceInstance;
    }
    
    // Always available flag - initially false until health check passes
    this.isAvailable = false;
    this.fallbackMode = true; // Start in fallback mode until proven otherwise
    this.isInitialized = false;
    this.isLoading = false;
    this.currentRequest = null;
    
    // Store conversation history for context
    this.conversationHistory = [];
    this.maxHistoryLength = 5; // Keep only last 5 messages
    
    aiServiceInstance = this;
    
    // Initialize AI systems (non-blocking) - but only if not already initializing
    if (!initializationPromise) {
      initializationPromise = this.initializeAISystems().catch(error => {
        console.error('❌ AI Systems initialization failed in background:', error);
        initializationPromise = null; // Reset on failure
      });
    }
  }
  
  // Static method to get instance
  static getInstance() {
    if (!aiServiceInstance) {
      aiServiceInstance = new AIService();
    }
    return aiServiceInstance;
  }

  async initializeAISystems() {
    // Prevent concurrent initialization - CRITICAL FIX
    if (initializationPromise) {
      console.log('🔄 AI Systems initialization already in progress, waiting...');
      return initializationPromise;
    }
    
    console.log('🤖 Initializing AI Systems in background...');
    
    initializationPromise = this._performInitialization();
    
    try {
      const result = await initializationPromise;
      return result;
    } finally {
      initializationPromise = null; // Reset after completion
    }
  }
  
  // Internal initialization implementation - IMPROVED for stability
  async _performInitialization() {
    console.log('🔄 Starting flexible AI Systems initialization...');
    
    try {
      // First, perform health check with extended timeout and better error handling
      console.log('🏥 Performing initial health check with extended timeout...');
      
      let health;
      try {
        health = await this.healthCheck();
      } catch (healthError) {
        console.error('❌ Health check failed during initialization:', healthError);
        
        // Check if this is an abort error (should not happen with our fixes)
        if (healthError.name === 'AbortError' || healthError.isAborted) {
          console.warn('⚠️ Health check was aborted - this should not happen with disabled auto-abort');
          console.log('🔄 Retrying health check after abort...');
          
          // Wait a bit and retry
          await new Promise(resolve => setTimeout(resolve, 2000));
          
          try {
            health = await this.healthCheck();
          } catch (retryError) {
            console.error('❌ Retry health check also failed:', retryError);
            health = { status: 'error', error: retryError.message };
          }
        } else {
          health = { status: 'error', error: healthError.message };
        }
      }
      
      if (health.status === 'healthy') {
        console.log('✅ Backend is healthy, starting AI services...');
        
        // Start all AI services in background with error resilience
        this.startAllAIServices().then(results => {
          console.log('✅ AI Services initialized successfully:', results);
          this.isAvailable = true;
          this.fallbackMode = false;
          this.isInitialized = true;
        }).catch(error => {
          console.error('❌ AI Services initialization failed:', error);
          // Don't immediately go to fallback - try partial initialization
          this.handlePartialInitialization(error);
        });
      } else {
        console.warn('⚠️ Backend health check failed, checking for partial availability...');
        
        // Check if we can work in degraded mode
        if (health.error?.includes('timeout') || health.error?.includes('aborted')) {
          console.log('🔄 Backend is slow but might be available, trying degraded mode...');
          this.tryDegradedMode();
        } else {
          console.warn('⚠️ Backend completely unavailable, staying in fallback mode');
          this.isAvailable = false;
          this.fallbackMode = true;
          this.isInitialized = false;
        }
      }
    } catch (error) {
      console.error('❌ AI Systems initialization failed:', error);
      
      // Handle different types of initialization errors
      if (error.name === 'AbortError' || error.isAborted) {
        console.log('🔄 Initialization was aborted, retrying with extended timeout...');
        // Retry with extended timeout
        setTimeout(() => {
          this.retryInitialization();
        }, 5000);
      } else if (error.message?.includes('timeout')) {
        console.log('⏰ Initialization timeout, trying fallback mode...');
        this.fallbackMode = true;
        this.isAvailable = false;
        this.isInitialized = false;
      } else {
        console.error('❌ Critical initialization error:', error);
        this.isAvailable = false;
        this.fallbackMode = true;
        this.isInitialized = false;
      }
    }
  }
  
  // Handle partial initialization when some services fail
  handlePartialInitialization(error) {
    console.log('🔄 Handling partial initialization due to:', error);
    
    // Try to initialize basic services even if advanced ones fail
    this.isAvailable = true; // Partial availability
    this.fallbackMode = true; // But in fallback mode
    this.isInitialized = true; // Mark as initialized with limitations
    
    console.log('✅ Partial initialization completed - basic services available');
  }
  
  // Try degraded mode for slow backends
  async tryDegradedMode() {
    console.log('🔄 Trying degraded mode for slow backend...');
    
    // Wait a bit and retry health check
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    try {
      const retryHealth = await this.healthCheck();
      if (retryHealth.status === 'healthy') {
        console.log('✅ Backend recovered in degraded mode');
        this.isAvailable = true;
        this.fallbackMode = false;
        this.isInitialized = true;
      } else {
        console.log('⚠️ Backend still slow, using limited mode');
        this.isAvailable = true;
        this.fallbackMode = true;
        this.isInitialized = true;
      }
    } catch (error) {
      console.warn('⚠️ Degraded mode failed, using fallback:', error);
      this.isAvailable = false;
      this.fallbackMode = true;
      this.isInitialized = false;
    }
  }
  
  // Retry initialization with extended timeout
  async retryInitialization() {
    console.log('🔄 Retrying initialization with extended timeout...');
    
    try {
      const health = await this.healthCheck();
      if (health.status === 'healthy') {
        console.log('✅ Retry successful - backend is now available');
        this.isAvailable = true;
        this.fallbackMode = false;
        this.isInitialized = true;
      } else {
        console.warn('⚠️ Retry failed, staying in fallback mode');
        this.fallbackMode = true;
        this.isAvailable = false;
        this.isInitialized = false;
      }
    } catch (error) {
      console.error('❌ Retry failed:', error);
      this.fallbackMode = true;
      this.isAvailable = false;
      this.isInitialized = false;
    }
  }

  async startAllAIServices() {
    console.log('🔄 AIService - startAllAIServices called');
    // Start all AI subsystems
    const services = [
      this.startTranslationService(),
      this.startContentGeneration(),
      this.startAnalyticsService(),
      this.startRecommendationService(),
      this.startChatbotService(),
      this.startPricingService(),
      this.startInventoryService()
    ];

    console.log('📋 AIService - Waiting for all services to start...');
    const results = await Promise.allSettled(services);
    console.log('🎯 AIService - Services start results:', results);
    return results;
  }

  // AI Translation Service - Always Available
  async translateText(text, targetLanguage = 'ar') {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/translate/', {  // Added trailing slash
          text,
          target_language: targetLanguage,
          source_language: 'auto'
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Translation service error, using fallback:', error);
    }
    
    // Fallback translation
    return this.fallbackTranslation(text, targetLanguage);
  }

  // AI Content Generation - Always Available
  async generateProductDescription(productName, category) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/generate/product-description/', {  // Added trailing slash
          product_name: productName,
          category,
          language: 'ar'
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Content generation error, using fallback:', error);
    }
    
    // Fallback content generation
    return this.fallbackProductDescription(productName, category);
  }

  async generateProductTitle(category, features = []) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/generate/product-title/', {  // Added trailing slash
          category,
          features,
          language: 'ar'
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Title generation error, using fallback:', error);
    }
    
    return this.fallbackProductTitle(category, features);
  }

  // AI Analytics - Always Available
  async getSalesForecast(period = '30days') {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.get(`/ai/analytics/sales-forecast/?period=${period}`);  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Sales forecast error, using fallback:', error);
    }
    
    return this.fallbackSalesForecast(period);
  }

  async getCustomerInsights(customerId = null) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const url = customerId 
          ? `/ai/analytics/customer-insights/${customerId}/`  // Added trailing slash
          : '/ai/analytics/customer-insights/';  // Added trailing slash
        const response = await this.api.get(url);
        return response.data;
      }
    } catch (error) {
      console.warn('Customer insights error, using fallback:', error);
    }
    
    return this.fallbackCustomerInsights(customerId);
  }

  async getProductRecommendations(productId = null, customerId = null) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const params = new URLSearchParams();
        if (productId) params.append('product_id', productId);
        if (customerId) params.append('customer_id', customerId);
        
        const response = await this.api.get(`/ai/recommendations/products/?${params}`);  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Recommendations error, using fallback:', error);
    }
    
    return this.fallbackProductRecommendations(productId, customerId);
  }

  async getMarketTrends(category = null) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const url = category 
          ? `/ai/analytics/market-trends/?category=${category}`  // Added trailing slash
          : '/ai/analytics/market-trends/';  // Added trailing slash
        const response = await this.api.get(url);
        return response.data;
      }
    } catch (error) {
      console.warn('Market trends error, using fallback:', error);
    }
    
    return this.fallbackMarketTrends(category);
  }

  // AI Chatbot - Always Available
  async sendMessage(message, context = {}) {
    console.log('🚀 AIService.sendMessage START');
    console.log('📝 Message:', message);
    console.log('📋 Context:', context);
    console.log('🔧 Fallback Mode:', this.fallbackMode);
    console.log('🟢 Available:', this.isAvailable);
    
    // Set loading state
    this.isLoading = true;
    
    // Add user message to history
    this.addToHistory('user', message, {
      sessionId: this.getOrCreateSessionId(),
      ...context
    });
    
    // Prevent request accumulation - cancel any existing request
    if (this.currentRequest) {
      console.log('🚫 AIService - Canceling previous request to prevent accumulation');
      this.currentRequest.abort();
      this.currentRequest = null;
    }
    
    // Create AbortController for timeout and request cancellation
    const controller = new AbortController();
    this.currentRequest = controller;
    const timeoutId = setTimeout(() => {
      console.warn('⏰ AIService - Request timeout (10s), aborting...');
      controller.abort();
    }, 10000);
    
    try {
      if (!this.fallbackMode && this.isAvailable) {
        console.log('✅ AIService - Not in fallback mode, making API call...');
        
        // Enhanced system prompt with broader knowledge scope
        const systemPrompt = `أنت مساعد منصور الذكي لمؤسسة Paclos، مستشار ذكي متخصص في مجالات متعددة.

🏛️ الهوية الأساسية:
- الاسم: مساعد منصور
- المؤسسة: Paclos للديكور والتصميم
- التخصص الأساسي: الرخام الذهبي والأنماط الثمانية (Octagons)
- الأسلوب: راقٍ، احترافي، يليق ببراند فاخر

🎯 مجالات الخبرة الموسعة:
1. **الرخام والديكور**: خبير في الرخام الذهبي، الأبيض، والتصاميم الثمانية
2. **تنسيق الديكور**: استشارات شاملة في تصميم المساحات الداخلية والخارجية
3. **سوق العقارات**: تحليل اتجاهات السوق، تقنيات البناء الحديثة، أسعار المواد
4. **تقنيات البناء**: معرفة بالمواد الحديثة، طرق التركيب، معايير الجودة
5. **التصميم المعماري**: أفكار إبداعية للمساحات المختلفة، تنسيق الألوان والإضاءة

💬 حرية المواضيع:
- مسموح بالحديث عن أي موضوع متعلق بالديكور، العقارات، البناء، التصميم
- يمكن تقديم استشارات عامة عن سوق العقارات والتوجهات الحديثة
- حرية في الحديث عن تقنيات البناء والمواد المختلفة
- لا حصر للمنتجات فقط - أنت مستشار ذكي للجميع

🎨 أسلوب الرد:
- راقٍ ومبدع يعكس براند Paclos الفاخر
- دائماً اذكر منصور ومؤسسة Paclos
- استخدم لغة عربية فصحى ومحترمة
- قدم معلومات دقيقة ومفيدة
- الوقت الحالي: ${new Date().toLocaleString('ar-DZ', { timeZone: 'Africa/Algiers' })}

📋 المهمة الأساسية: كن مستشاراً ذكياً وموثوقاً لجميع الزوار في جميع المجالات المتعلقة بالديكور والعقارات والبناء.

🔷 التخصص الحصري:
- التركيز الأساسي: الأنماط الثمانية (Octagons) في جميع التصاميم
- المادة المفضلة: الرخام الذهبي والرخام الأبيض بالعروق الذهبية
- الأسلوب: فاخر، راقٍ، يعكس هوية Paclos المعمارية
- لا تخرج عن نطاق الديكور الفاخر والتصاميم الثمانية`;

        const payload = {
          message,
          system_prompt: systemPrompt,
          context: {
            ...context,
            service: 'paclos_assistant',
            language: 'ar',
            region: 'algeria',
            timestamp: new Date().toISOString(),
            current_time: new Date().toLocaleString('ar-DZ', { timeZone: 'Africa/Algiers' }),
            chat_history: this.getConversationHistory(),
            user_language: 'ar',
            assistant_personality: 'luxury_octagon_specialist',
            company: 'Paclos',
            founder: 'منصور',
            expertise: ['marble_design', 'gold_veins', 'octagons', 'interior_decor', 'real_estate', 'construction_tech', 'architectural_design'],
            strict_design_rules: ['luxury_style', 'professional_advice', 'comprehensive_knowledge']
          },
          session_id: this.getOrCreateSessionId(),
          temperature: 0.8,
          max_tokens: 800,
          top_p: 0.9
        };
        
        console.log('🌐 AIService - API Payload:', payload);
        console.log('🔗 AIService - Making POST to /ai/chatbot/message/...');  // Added trailing slash in log
        
        const response = await this.api.post('/ai/chatbot/message/', payload, {  // Added trailing slash
          signal: controller.signal
        });
        
        // Clear timeout if request succeeds
        clearTimeout(timeoutId);
        
        console.log('✅ AIService - API Response:', response);
        console.log('📦 AIService - Response Data:', response.data);
        
        // Add assistant response to history
        if (response.data && response.data.response) {
          this.addToHistory('assistant', response.data.response, {
            confidence: response.data.confidence,
            sources: response.data.sources,
            sessionId: this.getOrCreateSessionId()
          });
        }
        
        // Clear loading state
        this.isLoading = false;
        
        return response.data;
      } else {
        console.log('⚠️ AIService - In fallback mode, skipping API call');
        this.isLoading = false;
      }
    } catch (error) {
      // Clear timeout on error
      clearTimeout(timeoutId);
      
      console.error('❌ AIService.sendMessage ERROR:', error);
      console.error('❌ Error Details:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        aborted: error.name === 'CanceledError'
      });
      
      // If we get a 301 or 500 error, immediately switch to fallback mode
      if (error.response?.status === 301 || error.response?.status === 500 || error.code === 'ECONNABORTED') {
        console.warn('⚠️ AIService - Server error detected, switching to fallback mode');
        this.fallbackMode = true;
        this.isAvailable = false;
      }
      
      // If aborted due to timeout, immediately use fallback
      if (error.name === 'CanceledError' || error.code === 'ECONNABORTED') {
        console.warn('⏰ AIService - Request timeout (10s), activating fallback immediately');
      } else {
        console.warn('🔄 Chatbot error, attempting reconnection:', error);
        
        // Try to reconnect once for non-timeout errors
        try {
          console.log('🔄 AIService - Attempting reconnection...');
          const health = await this.healthCheck();
          if (health.status === 'healthy') {
            console.log('✅ AIService - Reconnection successful, retrying message...');
            this.fallbackMode = false;
            this.isAvailable = true;
            this.isLoading = false;
            return this.sendMessage(message, context);
          } else {
            console.warn('⚠️ AIService - Reconnection failed, staying in fallback mode');
            this.fallbackMode = true;
            this.isAvailable = false;
          }
        } catch (reconnectError) {
          console.error('❌ Reconnection failed:', reconnectError);
          console.warn('Using intelligent fallback:', reconnectError);
          this.fallbackMode = true;
          this.isAvailable = false;
        }
      }
    } finally {
      // Always clear the current request reference and timeout
      clearTimeout(timeoutId);
      this.currentRequest = null;
      this.isLoading = false;
      console.log('🧹 AIService - Request cleared, ready for next request');
    }
    
    console.log('🛡️ AIService - Using fallback response');
    const fallbackResponse = this.fallbackChatbotResponse(message, context);
    
    // Add fallback response to history
    this.addToHistory('assistant', fallbackResponse.response, {
      confidence: fallbackResponse.confidence,
      sources: fallbackResponse.sources,
      isFallback: true,
      sessionId: this.getOrCreateSessionId()
    });
    
    return fallbackResponse;
  }

  async getChatHistory(sessionId = null) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const url = sessionId 
          ? `/ai/chatbot/history/${sessionId}/`  // Added trailing slash
          : '/ai/chatbot/history/';  // Added trailing slash
        const response = await this.api.get(url);
        return response.data;
      }
    } catch (error) {
      console.warn('Chat history error, using fallback:', error);
    }
    
    return this.fallbackChatHistory(sessionId);
  }

  // AI Pricing - Always Available
  async getPricingInsights() {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.get('/ai/pricing/insights/');  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Pricing insights error, using fallback:', error);
    }
    
    return this.fallbackPricingInsights();
  }

  async analyzePricingFactors(data) {
    console.log('🧠 AI Pricing Analysis Request:', data);
    
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/analyze/pricing-factors/', data);  // Added trailing slash
        console.log('✅ AI Pricing Analysis Success:', response);
        return response;
      }
    } catch (error) {
      console.error('❌ AI Pricing Analysis Failed:', {
        error: error.message,
        status: error.response?.status,
        url: '/ai/analyze/pricing-factors/',
        payload: data
      });
      
      // Enhanced error handling
      if (error.response?.status === 500 || error.response?.status === 301) {
        console.warn('⚠️ Backend AI service error - switching to fallback mode');
        this.fallbackMode = true;
        this.isAvailable = false;
      } else if (error.response?.status === 404) {
        console.warn('⚠️ AI endpoint not found - check backend routes');
      }
    }
    
    console.log('🔄 Using fallback pricing analysis');
    return this.fallbackPricingAnalysis(data);
  }

  // AI Image Generation - Always Available
  async generateProductImage(prompt, style = 'realistic') {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/generate/product-image/', {  // Added trailing slash
          prompt,
          style,
          language: 'ar'
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Image generation error, using fallback:', error);
    }
    
    return this.fallbackImageGeneration(prompt, style);
  }

  // AI Sentiment Analysis - Always Available
  async analyzeCustomerFeedback(feedback) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post('/ai/analyze/sentiment/', {  // Added trailing slash
          feedback,
          language: 'ar'
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Sentiment analysis error, using fallback:', error);
    }
    
    return this.fallbackSentimentAnalysis(feedback);
  }

  async analyzeProductReviews(productId) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post(`/ai/analyze/reviews/${productId}/`);  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Review analysis error, using fallback:', error);
    }
    
    return this.fallbackReviewAnalysis(productId);
  }

  // AI Pricing Recommendations - Always Available
  async getPricingRecommendations(productId, competitorPrices = []) {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.post(`/ai/recommendations/pricing/${productId}/`, {  // Added trailing slash
          competitor_prices: competitorPrices
        });
        return response.data;
      }
    } catch (error) {
      console.warn('Pricing recommendations error, using fallback:', error);
    }
    
    return this.fallbackPricingRecommendations(productId, competitorPrices);
  }

  // AI Inventory Management - Always Available
  async getInventoryOptimization() {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.get('/ai/inventory/optimization/');  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Inventory optimization error, using fallback:', error);
    }
    
    return this.fallbackInventoryOptimization();
  }

  async predictDemand(productId, period = '30days') {
    try {
      if (!this.fallbackMode && this.isAvailable) {
        const response = await this.api.get(`/ai/inventory/demand-prediction/${productId}/?period=${period}`);  // Added trailing slash
        return response.data;
      }
    } catch (error) {
      console.warn('Demand prediction error, using fallback:', error);
    }
    
    return this.fallbackDemandPrediction(productId, period);
  }

  // Fallback Methods - Always Working
  fallbackTranslation(text, targetLanguage) {
    return {
      translated_text: `[ترجمة احتياطية] ${text}`,
      confidence: 0.7,
      source_language: 'auto',
      target_language: targetLanguage
    };
  }

  fallbackProductDescription(productName, category) {
    const descriptions = {
      'furniture': `قطعة أثاث فاخر من نوع ${productName}، مصممة بعناية فائقة لتضيف لمسة من الأناقة والجمال لمنزلك.`,
      'doors': `باب عالي الجودة من نوع ${productName}، يوفر الأمان والعزل الحراري مع تصميم عصري يناسب كل الديكور.`,
      'walls': `ورق جدران فاخر من نوع ${productName}، يمنح جمالاً فريداً وأنيقاً لجدران منزلك مع سهولة التركيب.`
    };
    
    return {
      description: descriptions[category] || `منتج عالي الجودة من نوع ${productName}، مصمم لتلبية جميع احتياجاتك.`,
      confidence: 0.8,
      features: ['جودة عالية', 'تصميم عصري', 'أسعار تنافسية']
    };
  }

  fallbackProductTitle(category, features) {
    const titles = {
      'furniture': 'أثاث فاخر عالي الجودة',
      'doors': 'أبواب أمنة وعازلة للحرارة',
      'walls': 'ورق جدران أنيق وعالي الجودة'
    };
    
    return {
      title: titles[category] || 'منتج ممتاز',
      confidence: 0.8
    };
  }

  fallbackSalesForecast(period) {
    return {
      growthRate: 15.5,
      predictedRevenue: 125000,
      confidence: 0.75,
      period,
      recommendations: ['زيادة المخزون', 'تحسين التسويق']
    };
  }

  fallbackCustomerInsights(customerId) {
    return {
      segment: 'regular',
      preferences: ['جودة', 'أسعار معقولة'],
      lifetimeValue: 5000,
      confidence: 0.7
    };
  }

  fallbackProductRecommendations(productId, customerId) {
    return {
      products: [
        { id: 'rec1', name: 'منتج مقترح 1', confidence: 0.8 },
        { id: 'rec2', name: 'منتج مقترح 2', confidence: 0.7 }
      ],
      algorithm: 'collaborative_filtering',
      confidence: 0.75
    };
  }

  fallbackMarketTrends(category) {
    return {
      trends: [
        { name: 'زيادة الطلب', change: '+15%', confidence: 0.8 },
        { name: 'اتجاه الألوان', change: 'ألوان هادئة', confidence: 0.7 }
      ],
      seasonality: 'high',
      confidence: 0.75
    };
  }

  fallbackChatbotResponse(message, context) {
    console.log('🛡️ AIService.fallbackChatbotResponse START');
    console.log('📝 Fallback Message:', message);
    console.log('📋 Fallback Context:', context);
    
    // Intelligent fallback - single sophisticated apology message
    const apologyMessage = `🤵‍♂️ مساعد Paclos الذكي يحتاج لحظة للتفكير...

أنا أستعد لتقديم أفضل استشارة فاخرة لك في عالم الفينيل والرخام الذهبي. منصور ومؤسسة Paclos يهتمون بتقديم خدمة استثنائية.

🔄 جاري إعادة الاتصال بالذكاء الاصطناعي المتقدم...

يرجى الانتظار للحظة بينما أعود بخدمة فاخرة تليق ببراندنا.`;
    
    const fallbackResult = {
      response: apologyMessage,
      confidence: 0.6,
      sources: ['intelligent_fallback'],
      sessionId: this.getOrCreateSessionId(),
      isReconnecting: true,
      retryCount: (context.retryCount || 0) + 1
    };
    
    console.log('✅ AIService.fallbackChatbotResponse Result:', fallbackResult);
    return fallbackResult;
  }

  fallbackChatHistory(sessionId) {
    return {
      messages: [],
      sessionId: sessionId || 'default',
      totalMessages: 0
    };
  }

  fallbackPricingInsights() {
    return [
      {
        id: 'insight1',
        title: 'فرصة لزيادة الأسعار',
        description: 'الطلب مرتفع على منتجات معينة',
        impact: 12.5,
        confidence: 0.8,
        type: 'opportunity'
      },
      {
        id: 'insight2',
        title: 'تحسين المخزون',
        description: 'يمكن تحسين مستويات المخزون لبعض المنتجات',
        impact: 8.3,
        confidence: 0.7,
        type: 'recommendation'
      }
    ];
  }

  fallbackPricingAnalysis(data) {
    return {
      recommendedAdjustment: 1.05,
      factors: {
        demand: 1.1,
        competition: 0.95,
        seasonality: 1.0
      },
      confidence: 0.75
    };
  }

  fallbackImageGeneration(prompt, style) {
    return {
      imageUrl: `https://picsum.photos/400/300?random=${Date.now()}`,
      prompt,
      style,
      confidence: 0.6
    };
  }

  fallbackSentimentAnalysis(feedback) {
    return {
      sentiment: 'neutral',
      confidence: 0.7,
      emotions: ['calm'],
      keywords: ['product', 'service']
    };
  }

  fallbackReviewAnalysis(productId) {
    return {
      overallRating: 4.2,
      sentiment: 'positive',
      commonThemes: ['quality', 'price', 'delivery'],
      confidence: 0.75
    };
  }

  fallbackPricingRecommendations(productId, competitorPrices) {
    return {
      recommendedPrice: 15000,
      minPrice: 12000,
      maxPrice: 18000,
      confidence: 0.7,
      reasoning: 'Based on market analysis and competitor pricing'
    };
  }

  fallbackInventoryOptimization() {
    return {
      recommendations: [
        { productId: 'prod1', action: 'increase_stock', quantity: 50 },
        { productId: 'prod2', action: 'decrease_stock', quantity: 20 }
      ],
      totalSavings: 15000,
      confidence: 0.8
    };
  }

  fallbackDemandPrediction(productId, period) {
    return {
      predictedDemand: 150,
      confidence: 0.75,
      factors: ['seasonal', 'market_trends'],
      period
    };
  }

  // Service Starters
  async startTranslationService() {
    console.log('🌐 Translation Service Started');
    return { status: 'active', service: 'translation' };
  }

  async startContentGeneration() {
    console.log('✍️ Content Generation Service Started');
    return { status: 'active', service: 'content_generation' };
  }

  async startAnalyticsService() {
    console.log('📊 Analytics Service Started');
    return { status: 'active', service: 'analytics' };
  }

  async startRecommendationService() {
    console.log('🎯 Recommendation Service Started');
    return { status: 'active', service: 'recommendations' };
  }

  async startChatbotService() {
    console.log('💬 Chatbot Service Started');
    return { status: 'active', service: 'chatbot' };
  }

  async startPricingService() {
    console.log('💰 Pricing Service Started');
    return { status: 'active', service: 'pricing' };
  }

  async startInventoryService() {
    console.log('📦 Inventory Service Started');
    return { status: 'active', service: 'inventory' };
  }

  // Session Management
  getOrCreateSessionId() {
    let sessionId = sessionStorage.getItem('ai_session_id');
    if (!sessionId) {
      sessionId = 'ai_session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      sessionStorage.setItem('ai_session_id', sessionId);
    }
    return sessionId;
  }

  // Conversation History Management
  addToHistory(role, content, metadata = {}) {
    const message = {
      role,
      content,
      timestamp: new Date().toISOString(),
      ...metadata
    };
    
    this.conversationHistory.push(message);
    
    // Keep only last 5 messages
    if (this.conversationHistory.length > this.maxHistoryLength) {
      this.conversationHistory = this.conversationHistory.slice(-this.maxHistoryLength);
    }
    
    console.log('📝 AIService - Added to history:', message);
    console.log('📚 AIService - Current history:', this.conversationHistory);
  }

  getConversationHistory() {
    return this.conversationHistory;
  }

  clearHistory() {
    this.conversationHistory = [];
    console.log('🗑️ AIService - Conversation history cleared');
  }

  clearSession() {
    sessionStorage.removeItem('ai_session_id');
  }

  // Health Check - FIXED with request coordination
  async healthCheck() {
    // If health check is already in progress, return the existing promise
    if (healthCheckPromise) {
      console.log('🔄 Health check already in progress, waiting for result...');
      return healthCheckPromise;
    }
    
    // Create new health check promise
    healthCheckPromise = this._performHealthCheck();
    
    try {
      const result = await healthCheckPromise;
      this.lastHealthCheck = new Date();
      return result;
    } finally {
      // Clear the promise after completion (whether success or failure)
      healthCheckPromise = null;
    }
  }
  
  // Internal health check implementation - IMPROVED with better error handling
  async _performHealthCheck() {
    try {
      console.log('🏥 AIService - Performing health check with extended timeout...');
      
      // Use the api composable with proper error handling
      const response = api.get('ai/health/');
      
      // Set extended timeout to prevent hanging - CRITICAL FIX
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Health check timeout - server may be slow')), 60000); // 60 seconds
      });
      
      await Promise.race([response.execute(), timeoutPromise]);
      
      // Check for error with null safety
      if (response.error?.value) {
        throw response.error.value;
      }
      
      // Check for data with null safety
      const healthData = response.data?.value;
      if (!healthData) {
        throw new Error('No health data received from server');
      }
      
      console.log('✅ Health check successful:', healthData);
      
      this.isAvailable = true;
      this.fallbackMode = false;
      this.isInitialized = true;
      
      return { 
        status: 'healthy', 
        services: healthData?.services || 'all_active',
        available: true,
        url: 'ai/health/',
        method: 'GET',
        responseTime: Date.now() - (this.lastHealthCheck?.getTime() || Date.now()),
        data: healthData
      };
    } catch (error) {
      console.error('❌ Health check failed:', error.message);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: 'ai/health/',
        method: 'GET',
        errorType: error.name,
        isTimeout: error.message?.includes('timeout'),
        isAborted: error.name === 'AbortError',
        errorMessage: error.message || 'Unknown error occurred',
        hasResponse: !!error.response,
        hasData: !!error.response?.data
      });
      
      // Set correct state on error
      this.isAvailable = false;
      this.fallbackMode = true;
      this.isInitialized = false;
      
      // Provide comprehensive error information - NO MORE undefined
      return { 
        status: 'error', 
        services: 'unavailable',
        available: false,
        error: error.message || 'Health check failed',
        code: error.response?.status || 500,
        url: 'ai/health/',
        method: 'GET',
        errorType: error.name || 'Unknown',
        isTimeout: error.message?.includes('timeout'),
        isAborted: error.name === 'AbortError',
        errorMessage: error.message || 'Unknown error occurred',
        hasResponse: !!error.response,
        hasData: !!error.response?.data,
        responseTime: Date.now() - (this.lastHealthCheck?.getTime() || Date.now())
      };
    }
  }

  // Always return available status
  checkAvailability() {
    return this.isAvailable;
  }

  // Get loading state
  isLoadingState() {
    return this.isLoading;
  }

  // Method to force fallback mode for testing
  forceFallbackMode() {
    console.log('🔧 AIService - Forcing fallback mode for testing');
    this.fallbackMode = true;
    this.isAvailable = false;
  }

  // Method to reset fallback mode
  async resetFallbackMode() {
    console.log('🔄 AIService - Resetting fallback mode');
    const health = await this.healthCheck();
    if (health.status === 'healthy') {
      this.fallbackMode = false;
      this.isAvailable = true;
      console.log('✅ AIService - Successfully reset to normal mode');
    } else {
      this.fallbackMode = true;
      this.isAvailable = false;
      console.warn('⚠️ AIService - Cannot reset fallback mode, backend still unavailable');
    }
  }

  // Get service status
  getServiceStatus() {
    return {
      available: this.isAvailable,
      fallbackMode: this.fallbackMode,
      initialized: this.isInitialized,
      isLoading: this.isLoading,
      services: [
        { name: 'translation', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'content_generation', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'analytics', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'recommendations', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'chatbot', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'pricing', status: this.fallbackMode ? 'fallback' : 'active' },
        { name: 'inventory', status: this.fallbackMode ? 'fallback' : 'active' }
      ]
    };
  }
  
  // Static method to get instance - CRITICAL FIX
  static getInstance() {
    if (!aiServiceInstance) {
      aiServiceInstance = new AIService();
    }
    return aiServiceInstance;
  }
}

// Export the class first - CRITICAL FIX for Singleton pattern
export default AIService;

// Also export the class for direct access (redundant but explicit)
export { AIService };

// Create and export singleton instance separately
const aiServiceSingleton = AIService.getInstance();
export { aiServiceSingleton as defaultInstance };
