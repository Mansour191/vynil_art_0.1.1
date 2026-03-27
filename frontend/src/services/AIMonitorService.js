import AIService from './AIService';
import PricingService from './PricingService';
import ERPNextService from './ERPNextService';

class AIMonitorService {
  constructor() {
    this.isMonitoring = false;
    this.serviceStatus = {
      ai: 'unknown',
      pricing: 'unknown',
      erpnext: 'unknown'
    };
    this.healthCheckInterval = null;
    this.retryAttempts = 0;
    this.maxRetries = 3;
    this.lastHealthCheck = null;
    
    // Initialize singleton instances immediately
    this.aiService = AIService.getInstance();
    this.pricingService = PricingService.getInstance();
    this.erpService = ERPNextService.getInstance();
    
    console.log('🔍 AIMonitorService initialized with singleton instances');
    
    // Start monitoring immediately - but with coordination
    this.startMonitoring();
  }

  async startMonitoring() {
    if (this.isMonitoring) {
      console.log('🔄 AIMonitorService already monitoring');
      return;
    }
    
    console.log('🔍 Starting AI Systems Monitoring...');
    this.isMonitoring = true;
    this.retryAttempts = 0;
    
    // Wait for singleton instances to be ready
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Initial health check
    await this.performHealthCheck();
    
    // Start continuous monitoring
    this.startContinuousMonitoring();
    
    // Start service initialization - but check if already initialized
    await this.initializeAllServices();
  }

  async initializeAllServices() {
    console.log('🚀 Initializing all AI services...');
    
    try {
      // AI Service should already be initializing via singleton
      if (this.aiService.isInitialized) {
        this.serviceStatus.ai = 'active';
        console.log('✅ AI Services already initialized');
      } else {
        // Wait a bit for initialization to complete
        await new Promise(resolve => setTimeout(resolve, 3000));
        this.serviceStatus.ai = this.aiService.isAvailable ? 'active' : 'failed';
        console.log('✅ AI Services initialization completed');
      }
    } catch (error) {
      console.warn('⚠️ AI Services initialization warning:', error);
      this.serviceStatus.ai = 'failed';
    }
    
    // Ensure pricing service is active
    try {
      await this.checkPricingService();
      console.log('✅ Pricing Service active');
    } catch (error) {
      console.warn('⚠️ Pricing Service warning:', error);
      this.serviceStatus.pricing = 'failed';
    }
    
    // Check ERPNext integration
    try {
      await this.checkERPNextIntegration();
      console.log('✅ ERPNext Integration active');
    } catch (error) {
      console.warn('⚠️ ERPNext Integration warning:', error);
      this.serviceStatus.erpnext = 'failed';
    }
    
    this.logServiceStatus();
  }

  startContinuousMonitoring() {
    // Clear any existing interval
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }
    
    // Check health every 30 seconds
    this.healthCheckInterval = setInterval(async () => {
      await this.performHealthCheck();
    }, 30000);
    
    console.log('🔄 Continuous monitoring started (30-second intervals)');
  }

  async performHealthCheck() {
    try {
      this.lastHealthCheck = new Date();
      
      console.log('🔍 Performing coordinated health check...');
      
      // Use cached singleton instances to prevent concurrent health checks
      // Check AI Service with proper error handling
      try {
        const aiHealth = await this.aiService.healthCheck();
        this.serviceStatus.ai = aiHealth.status === 'healthy' ? 'active' : 'failed';
        console.log('✅ AI Service health check:', this.serviceStatus.ai);
      } catch (error) {
        this.serviceStatus.ai = 'failed';
        console.error('❌ AI Service health check failed:', error.message);
      }
      
      // Check Pricing Service with proper error handling
      try {
        const pricingStatus = await this.checkPricingService();
        this.serviceStatus.pricing = pricingStatus;
        console.log('✅ Pricing Service health check:', this.serviceStatus.pricing);
      } catch (error) {
        this.serviceStatus.pricing = 'failed';
        console.error('❌ Pricing Service health check failed:', error.message);
      }
      
      // Check ERPNext with proper error handling
      try {
        const erpStatus = await this.checkERPNextIntegration();
        this.serviceStatus.erpnext = erpStatus;
        console.log('✅ ERPNext Service health check:', this.serviceStatus.erpnext);
      } catch (error) {
        this.serviceStatus.erpnext = 'failed';
        console.error('❌ ERPNext Service health check failed:', error.message);
      }
      
      // Reset retry attempts on success
      if (this.isHealthy()) {
        this.retryAttempts = 0;
      }
      
      // Log comprehensive status
      console.group('📊 System Health Status');
      console.log('AI Service:', this.serviceStatus.ai);
      console.log('Pricing Service:', this.serviceStatus.pricing);
      console.log('ERPNext Service:', this.serviceStatus.erpnext);
      console.log('Overall Status:', this.getOverallStatus());
      console.log('Last Check:', this.lastHealthCheck.toISOString());
      console.groupEnd();
      
    } catch (error) {
      console.error('❌ Health check failed:', error);
      this.handleHealthCheckFailure(error);
    }
  }

  async checkPricingService() {
    try {
      // Use cached singleton instance to prevent concurrent calls
      console.log('💰 Checking Pricing Service health...');
      
      // Test pricing service functionality with timeout
      const testResult = await Promise.race([
        this.pricingService.calculateDynamicPrice('test', {
          customerSegment: 'test',
          quantity: 1
        }),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Pricing service timeout')), 8000)
        )
      ]);
      
      return testResult ? 'active' : 'failed';
    } catch (error) {
      console.warn('Pricing service check failed:', error.message);
      return 'failed';
    }
  }

  async checkERPNextIntegration() {
    try {
      // Use cached singleton instance to prevent concurrent calls
      console.log('🏥 Checking ERPNext Service health...');
      
      // Test ERPNext connectivity with timeout
      const healthCheck = await Promise.race([
        this.erpService.checkIntegrationHealth(),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('ERPNext service timeout')), 8000)
        )
      ]);
      
      return healthCheck.status === 'healthy' ? 'active' : 'failed';
    } catch (error) {
      console.warn('ERPNext integration check failed:', error.message);
      return 'failed';
    }
  }

  handleHealthCheckFailure(error) {
    this.retryAttempts++;
    
    if (this.retryAttempts <= this.maxRetries) {
      console.warn(`⚠️ Health check failed, retrying (${this.retryAttempts}/${this.maxRetries})...`);
      
      // Attempt to reinitialize services
      setTimeout(async () => {
        await this.initializeAllServices();
      }, 5000 * this.retryAttempts); // Exponential backoff
      
    } else {
      console.error('❌ Max retries reached, services may be degraded');
      this.serviceStatus = {
        ai: 'fallback',
        pricing: 'fallback',
        erpnext: 'limited'
      };
    }
  }

  // Get overall system status - FIXED
  getOverallStatus() {
    const services = this.serviceStatus;
    const activeCount = Object.values(services).filter(s => s === 'active').length;
    const totalCount = Object.keys(services).length;
    
    if (activeCount === totalCount) {
      return 'healthy';
    } else if (activeCount >= 2) {
      return 'degraded';
    } else {
      return 'critical';
    }
  }

  isHealthy() {
    return Object.values(this.serviceStatus).every(status => 
      status === 'active' || status === 'fallback'
    );
  }

  logServiceStatus() {
    const status = this.getServiceStatus();
    console.log('📊 Service Status:', {
      timestamp: new Date().toISOString(),
      overall: status.overall,
      services: status.services,
      health: status.healthy ? 'healthy' : 'degraded'
    });
    
    // Dispatch custom event for UI updates
    window.dispatchEvent(new CustomEvent('ai-service-status-update', {
      detail: status
    }));
  }

  getServiceStatus() {
    const services = this.serviceStatus;
    const activeCount = Object.values(services).filter(s => s === 'active').length;
    const totalCount = Object.keys(services).length;
    
    return {
      overall: activeCount === totalCount ? 'healthy' : 'degraded',
      healthy: activeCount >= 2, // At least 2 services active
      services: services,
      activeServices: activeCount,
      totalServices: totalCount,
      lastCheck: this.lastHealthCheck,
      uptime: this.calculateUptime()
    };
  }

  calculateUptime() {
    // Simple uptime calculation (would be more sophisticated in production)
    const startTime = localStorage.getItem('ai_monitor_start_time');
    if (!startTime) {
      localStorage.setItem('ai_monitor_start_time', new Date().toISOString());
      return '0s';
    }
    
    const uptime = Date.now() - new Date(startTime).getTime();
    const seconds = Math.floor(uptime / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes % 60}m`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    } else {
      return `${seconds}s`;
    }
  }

  async forceRestart() {
    console.log('🔄 Forcing AI services restart...');
    
    try {
      // Stop monitoring
      this.stopMonitoring();
      
      // Clear any cached states
      localStorage.removeItem('ai_monitor_start_time');
      
      // Wait a moment then restart
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Restart everything
      await this.startMonitoring();
      
      console.log('✅ AI services restart completed');
      return true;
      
    } catch (error) {
      console.error('❌ Failed to restart AI services:', error);
      return false;
    }
  }

  stopMonitoring() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
    
    this.isMonitoring = false;
    console.log('⏹️ AI monitoring stopped');
  }

  // Emergency recovery methods
  async emergencyRecovery() {
    console.log('🚨 Emergency recovery mode activated...');
    
    try {
      // Force all services into fallback mode
      this.serviceStatus = {
        ai: 'fallback',
        pricing: 'fallback',
        erpnext: 'limited'
      };
      
      // Clear all intervals and timeouts
      this.stopMonitoring();
      
      // Reinitialize with minimal services
      await this.initializeAllServices();
      
      // Restart monitoring with shorter intervals
      this.healthCheckInterval = setInterval(async () => {
        await this.performHealthCheck();
      }, 15000); // 15 seconds in emergency mode
      
      console.log('🆘 Emergency recovery completed');
      return true;
      
    } catch (error) {
      console.error('❌ Emergency recovery failed:', error);
      return false;
    }
  }

  // Performance monitoring
  getPerformanceMetrics() {
    return {
      uptime: this.calculateUptime(),
      healthChecks: this.getHealthCheckCount(),
      serviceStatus: this.getServiceStatus(),
      lastRestart: localStorage.getItem('ai_last_restart'),
      errorCount: this.getErrorCount()
    };
  }

  getHealthCheckCount() {
    const count = localStorage.getItem('ai_health_checks');
    return count ? parseInt(count) : 0;
  }

  getErrorCount() {
    const count = localStorage.getItem('ai_error_count');
    return count ? parseInt(count) : 0;
  }

  incrementHealthCheckCount() {
    const current = this.getHealthCheckCount();
    localStorage.setItem('ai_health_checks', (current + 1).toString());
  }

  incrementErrorCount() {
    const current = this.getErrorCount();
    localStorage.setItem('ai_error_count', (current + 1).toString());
  }

  // Cleanup
  cleanup() {
    this.stopMonitoring();
    console.log('🧹 AI Monitor Service cleaned up');
  }
}

// Create singleton instance
const aiMonitorService = new AIMonitorService();

// Auto-start on import
aiMonitorService.startMonitoring();

// Export singleton
export default aiMonitorService;
