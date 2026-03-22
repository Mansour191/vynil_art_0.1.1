import AIService from '@/services/AIService';

const API_BASE = (import.meta.env.VUE_APP_API_URL || '').replace(/\/+$/, '');

class ChatService {
  constructor() {
    this.sessionId = this.generateSessionId();
    this.isAvailable = true;
    this.fallbackResponses = [
      'أنا مساعد Paclos الذكي، يمكنني مساعدتك في:',
      'لدي معلومات شاملة عن منتجات الفينيل والتصاميم',
      'يمكنني تحليل الأسعار وتقديم توصيات ذكية',
      'أستطيع مساعدتك في اختيار المنتجات المناسبة',
      'لدي إمكانية تحليل السوق والمنافسين',
      'يمكنني توفير معلومات عن حالة الطلبات والشحن'
    ];
  }

  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  async ask(message) {
    try {
      // Always try to use AI service first
      const aiResponse = await AIService.sendMessage(message, {
        sessionId: this.sessionId,
        context: {
          service: 'paclos_assistant',
          language: 'ar',
          region: 'algeria'
        }
      });

      this.isAvailable = true;
      return {
        answer: aiResponse.response,
        confidence: aiResponse.confidence || 0.8,
        sources: aiResponse.sources || [],
        sessionId: this.sessionId
      };

    } catch (error) {
      console.warn('AI Service unavailable, using fallback:', error);
      
      // Fallback to intelligent responses
      const fallbackResponse = this.generateIntelligentResponse(message);
      this.isAvailable = true;
      
      return {
        answer: fallbackResponse,
        confidence: 0.6,
        sources: ['fallback'],
        sessionId: this.sessionId
      };
    }
  }

  generateIntelligentResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Product-related queries
    if (lowerMessage.includes('منتج') || lowerMessage.includes('فينيل') || lowerMessage.includes('تصميم')) {
      return this.getProductResponse(lowerMessage);
    }
    
    // Pricing-related queries
    if (lowerMessage.includes('سعر') || lowerMessage.includes('تكلفة') || lowerMessage.includes('خصم')) {
      return this.getPricingResponse(lowerMessage);
    }
    
    // Order-related queries
    if (lowerMessage.includes('طلب') || lowerMessage.includes('شحن') || lowerMessage.includes('توصيل')) {
      return this.getOrderResponse(lowerMessage);
    }
    
    // General help
    if (lowerMessage.includes('مساعدة') || lowerMessage.includes('كيف') || lowerMessage.includes('ماذا')) {
      return this.getHelpResponse();
    }
    
    // Default intelligent response
    return this.getDefaultResponse();
  }

  getProductResponse(message) {
    const responses = [
      'لدينا مجموعة واسعة من منتجات الفينيل عالية الجودة. هل تبحث عن نوع معين مثل فينيل الجدران، الأبواب، أو الأرضيات؟',
      'يمكنني مساعدتك في اختيار المنتج المناسب حسب احتياجاتك وميزانيتك. ما هو استخدامك المتوقع؟',
      'جميع منتجاتنا مدعومة بضمان الجودة ويمكن تخصيصها حسب طلبك. هل تريد معرفة المزيد عن نوع معين؟',
      'أسعارنا تنافسية وجودتنا عالية. يمكنني تحليل المنتج الأنسب لميزانيتك وميزانيتك.'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  getPricingResponse(message) {
    const responses = [
      'نظام التسعير لدينا ذكي ويعتمد على تحليل السوق والطلب. يمكنني تزويدك بأفضل الأسعار المتاحة.',
      'أسعارنا ديناميكية وتتغير حسب العرض والطلب والمنافسة. هل تريد معرفة سعر منتج معين؟',
      'يمكنني تحليل أفضل سعر لك بناءً على السوق والميزانية. ما هو المنتج الذي تهتم به؟',
      'لدينا عروض وخصومات متنوعة. يمكنني مساعدتك في العثور على أفضل صفقة.'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  getOrderResponse(message) {
    const responses = [
      'يمكنني تتبع حالة طلبك وتزويدك بمعلومات الشحن. ما هو رقم طلبك؟',
      'نظام الشحن لدينا سريع وموثوق. التوصيل في جميع أنحاء الجزائر خلال 3-5 أيام عمل.',
      'يمكنني مساعدتك في معرفة حالة طلبك وتقدير وقت التوصيل. هل لديك رقم الطلب؟',
      'لدينا خيارات شحن متعددة تناسب احتياجاتك. يمكنني مساعدتك في اختيار الأنسب.'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  getHelpResponse() {
    return `أنا مساعد Paclos الذكي المطور خصيصاً لهذا المتجر. يمكنني:
    
🎯 تحليل الأسعار والتوصيات
📦 مساعدة في اختيار المنتجات
📊 تتبع الطلبات والشحن
🤖 توفير رؤى ذكية للسوق
💡 الإجابة على استفساراتك

كيف يمكنني مساعدتك اليوم؟`;
  }

  getDefaultResponse() {
    const responses = [
      'أنا هنا لمساعدتك! يمكنني تحليل المنتجات والأسعار وتقديم توصيات ذكية. ما الذي يهمك؟',
      'مرحباً بك في Paclos! أنا مساعدك الذكي. اسألني عن أي شيء يتعلق بمنتجاتنا أو خدماتنا.',
      'يمكنني مساعدتك في العثور على أفضل المنتجات والأسعار. ما هو احتياجك؟',
      'أنا جاهز لمساعدتك! لدي معلومات شاملة عن منتجات الفينيل والخدمات المتاحة.'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  async getChatHistory() {
    try {
      const history = await AIService.getChatHistory(this.sessionId);
      return history;
    } catch (error) {
      console.warn('Could not load chat history:', error);
      return [];
    }
  }

  clearSession() {
    this.sessionId = this.generateSessionId();
  }

  checkAvailability() {
    return this.isAvailable;
  }
}

export default new ChatService();
