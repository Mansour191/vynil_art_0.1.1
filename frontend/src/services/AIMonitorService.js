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
    
    // Start monitoring immediately
    this.startMonitoring();
  }

  async startMonitoring() {
    if (this.isMonitoring) return;
    
    console.log('🔍 Starting AI Systems Monitoring...');
    this.isMonitoring = true;
    this.retryAttempts = 0;
    
    // Initial health check
    await this.performHealthCheck();
    
    // Start continuous monitoring
    this.startContinuousMonitoring();
    
    // Start service initialization
    await this.initializeAllServices();
  }

  async initializeAllServices() {
    console.log('🚀 Initializing all AI services...');
    
    try {
      // Force AI services to start
      await AIService.initializeAISystems();
      this.serviceStatus.ai = 'active';
      console.log('✅ AI Services initialized');
    } catch (error) {
      console.warn('⚠️ AI Services initialization warning:', error);
      this.serviceStatus.ai = 'fallback';
    }
    
    // Ensure pricing service is active
    try {
      await this.checkPricingService();
      this.serviceStatus.pricing = 'active';
      console.log('✅ Pricing Service active');
    } catch (error) {
      console.warn('⚠️ Pricing Service warning:', error);
      this.serviceStatus.pricing = 'fallback';
    }
    
    // Check ERPNext integration
    try {
      await this.checkERPNextIntegration();
      this.serviceStatus.erpnext = 'active';
      console.log('✅ ERPNext Integration active');
    } catch (error) {
      console.warn('⚠️ ERPNext Integration warning:', error);
      this.serviceStatus.erpnext = 'limited';
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
      
      // Check AI Service
      const aiHealth = await AIService.healthCheck();
      this.serviceStatus.ai = aiHealth.status === 'healthy' ? 'active' : 'fallback';
      
      // Check Pricing Service
      const pricingStatus = await this.checkPricingService();
      this.serviceStatus.pricing = pricingStatus;
      
      // Check ERPNext
      const erpStatus = await this.checkERPNextIntegration();
      this.serviceStatus.erpnext = erpStatus;
      
      // Reset retry attempts on success
      if (this.isHealthy()) {
        this.retryAttempts = 0;
      }
      
      this.logServiceStatus();
      
    } catch (error) {
      console.error('❌ Health check failed:', error);
      this.handleHealthCheckFailure(error);
    }
  }

  async checkPricingService() {
    try {
      // Test pricing service functionality
      const testResult = await PricingService.calculateDynamicPrice('test', {
        customerSegment: 'test',
        quantity: 1
      });
      
      return testResult ? 'active' : 'fallback';
    } catch (error) {
      console.warn('Pricing service check failed:', error);
      return 'fallback';
    }
  }

  async checkERPNextIntegration() {
    try {
      // Test ERPNext connectivity
      const healthCheck = await ERPNextService.checkIntegrationHealth();
      return healthCheck ? 'active' : 'limited';
    } catch (error) {
      console.warn('ERPNext integration check failed:', error);
      return 'limited';
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
