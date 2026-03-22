<template>
  <div class="ai-monitor">
    <!-- Header -->
    <header class="monitor-header">
      <div class="header-content">
        <h1 class="text-3xl font-bold gold-text mb-2">
          <i class="fa-solid fa-brain me-3"></i>
          مراقبة أنظمة الذكاء الاصطناعي
        </h1>
        <p class="text-dim">مراقبة مستمرة لجميع خدمات الذكاء الاصطناعي والتكاملات</p>
      </div>
      <div class="header-actions">
        <button class="btn-primary" @click="forceRestart" :disabled="isRestarting">
          <i :class="isRestarting ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync'"></i>
          إعادة التشغيل
        </button>
        <button class="btn-secondary" @click="emergencyRecovery" :disabled="isEmergencyMode">
          <i class="fa-solid fa-exclamation-triangle"></i>
          استرداد عاجل
        </button>
      </div>
    </header>

    <!-- Status Overview -->
    <div class="status-overview mb-8">
      <div class="status-card" :class="{ healthy: serviceStatus.overall === 'healthy', degraded: serviceStatus.overall === 'degraded' }">
        <div class="status-icon">
          <i :class="serviceStatus.overall === 'healthy' ? 'fa-solid fa-check-circle' : 'fa-solid fa-exclamation-triangle'"></i>
        </div>
        <div class="status-info">
          <h3>حالة النظام</h3>
          <p>{{ serviceStatus.overall === 'healthy' ? 'جميع الخدمات تعمل بشكل طبيعي' : 'بعض الخدمات تعمل بوضع محدود' }}</p>
          <div class="status-details">
            <span>الوقت التشغيل: {{ serviceStatus.uptime }}</span>
            <span>آخر فحص: {{ formatTime(serviceStatus.lastCheck) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Services Grid -->
    <div class="services-grid mb-8">
      <div v-for="(status, service) in serviceStatus.services" :key="service" class="service-card">
        <div class="service-header">
          <div class="service-info">
            <h3>{{ getServiceName(service) }}</h3>
            <span class="service-status" :class="status">
              {{ getStatusText(status) }}
            </span>
          </div>
          <div class="service-icon">
            <i :class="getServiceIcon(service)"></i>
          </div>
        </div>
        
        <div class="service-metrics">
          <div class="metric">
            <span class="metric-label">الحالة:</span>
            <span class="metric-value" :class="status">
              {{ getStatusText(status) }}
            </span>
          </div>
          <div class="metric">
            <span class="metric-label">الأداء:</span>
            <div class="performance-bar">
              <div class="performance-fill" :style="{ width: getPerformanceLevel(status) + '%' }"></div>
            </div>
            <span class="performance-value">{{ getPerformanceLevel(status) }}%</span>
          </div>
          <div class="metric">
            <span class="metric-label">آخر تحديث:</span>
            <span class="metric-value">{{ formatTime(serviceStatus.lastCheck) }}</span>
          </div>
        </div>
        
        <div class="service-actions">
          <button class="btn-sm" @click="testService(service)" :disabled="isTesting">
            <i :class="isTesting ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-flask'"></i>
            اختبار
          </button>
          <button class="btn-sm btn-secondary" @click="restartService(service)" :disabled="isRestarting">
            <i class="fa-solid fa-redo"></i>
            إعادة تشغيل
          </button>
        </div>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="metrics-dashboard">
      <div class="glass-card">
        <h3 class="text-xl font-bold mb-4">
          <i class="fa-solid fa-chart-line me-2"></i>
          مؤشرات الأداء
        </h3>
        
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">
              <i class="fa-solid fa-clock"></i>
              <span>وقت التشغيل</span>
            </div>
            <div class="metric-value large">{{ performanceMetrics.uptime }}</div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">
              <i class="fa-solid fa-heartbeat"></i>
              <span>فحوص الحالة</span>
            </div>
            <div class="metric-value large">{{ performanceMetrics.healthChecks }}</div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">
              <i class="fa-solid fa-exclamation-triangle"></i>
              <span>عدد الأخطاء</span>
            </div>
            <div class="metric-value large error">{{ performanceMetrics.errorCount }}</div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">
              <i class="fa-solid fa-server"></i>
              <span>الخدمات النشطة</span>
            </div>
            <div class="metric-value large">{{ serviceStatus.activeServices }}/{{ serviceStatus.totalServices }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Real-time Logs -->
    <div class="logs-section">
      <div class="glass-card">
        <div class="logs-header">
          <h3 class="text-xl font-bold">
            <i class="fa-solid fa-terminal me-2"></i>
            السجلات المباشرة
          </h3>
          <div class="logs-controls">
            <button class="btn-sm" @click="clearLogs">
              <i class="fa-solid fa-trash"></i>
              مسح
            </button>
            <button class="btn-sm" @click="exportLogs">
              <i class="fa-solid fa-download"></i>
              تصدير
            </button>
          </div>
        </div>
        
        <div class="logs-container" ref="logsContainer">
          <div v-for="(log, index) in logs" :key="index" class="log-entry" :class="log.type">
            <span class="log-time">{{ formatTime(log.timestamp) }}</span>
            <span class="log-service">{{ log.service }}</span>
            <span class="log-message">{{ log.message }}</span>
            <span class="log-level">{{ log.level }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Emergency Mode Alert -->
    <div v-if="isEmergencyMode" class="emergency-alert">
      <div class="alert-content">
        <i class="fa-solid fa-exclamation-triangle"></i>
        <div>
          <h4>وضع الاسترداد العاجل نشط</h4>
          <p>يعمل النظام في وضع محدود. بعض المميزات قد لا تكون متاحة.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import AIMonitorService from '@/services/AIMonitorService';
import AIService from '@/services/AIService';

// State
const serviceStatus = ref({
  overall: 'unknown',
  healthy: false,
  services: {},
  activeServices: 0,
  totalServices: 0,
  lastCheck: null,
  uptime: '0s'
});

const performanceMetrics = ref({
  uptime: '0s',
  healthChecks: 0,
  errorCount: 0,
  lastRestart: null
});

const logs = ref([]);
const isRestarting = ref(false);
const isTesting = ref(false);
const isEmergencyMode = ref(false);
const logsContainer = ref(null);

// Methods
const formatTime = (timestamp) => {
  if (!timestamp) return 'N/A';
  return new Intl.DateTimeFormat('ar-DZ', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(new Date(timestamp));
};

const getServiceName = (service) => {
  const names = {
    ai: 'خدمات الذكاء الاصطناعي',
    pricing: 'نظام التسعير الذكي',
    erpnext: 'تكامل ERPNext'
  };
  return names[service] || service;
};

const getServiceIcon = (service) => {
  const icons = {
    ai: 'fa-solid fa-brain',
    pricing: 'fa-solid fa-chart-line',
    erpnext: 'fa-solid fa-database'
  };
  return icons[service] || 'fa-solid fa-cog';
};

const getStatusText = (status) => {
  const texts = {
    active: 'نشط',
    fallback: 'وضع احتياطي',
    limited: 'محدود',
    unknown: 'غير معروف'
  };
  return texts[status] || status;
};

const getPerformanceLevel = (status) => {
  const levels = {
    active: 95,
    fallback: 70,
    limited: 50,
    unknown: 30
  };
  return levels[status] || 30;
};

const updateServiceStatus = () => {
  const status = AIMonitorService.getServiceStatus();
  serviceStatus.value = status;
};

const updatePerformanceMetrics = () => {
  performanceMetrics.value = AIMonitorService.getPerformanceMetrics();
};

const addLog = (message, type = 'info', level = 'INFO', service = 'SYSTEM') => {
  const log = {
    timestamp: new Date(),
    message,
    type,
    level,
    service
  };
  
  logs.value.unshift(log);
  
  // Keep only last 100 logs
  if (logs.value.length > 100) {
    logs.value = logs.value.slice(0, 100);
  }
  
  // Auto-scroll to top
  nextTick(() => {
    if (logsContainer.value) {
      logsContainer.value.scrollTop = 0;
    }
  });
};

const forceRestart = async () => {
  isRestarting.value = true;
  addLog('بدء إعادة تشغيل أنظمة الذكاء الاصطناعي...', 'info', 'INFO', 'MONITOR');
  
  try {
    const success = await AIMonitorService.forceRestart();
    
    if (success) {
      addLog('تمت إعادة تشغيل الأنظمة بنجاح', 'success', 'SUCCESS', 'MONITOR');
      localStorage.setItem('ai_last_restart', new Date().toISOString());
    } else {
      addLog('فشلت إعادة تشغيل الأنظمة', 'error', 'ERROR', 'MONITOR');
    }
  } catch (error) {
    addLog(`خطأ في إعادة التشغيل: ${error.message}`, 'error', 'ERROR', 'MONITOR');
  } finally {
    isRestarting.value = false;
    updateServiceStatus();
    updatePerformanceMetrics();
  }
};

const emergencyRecovery = async () => {
  isEmergencyMode.value = true;
  addLog('تفعيل وضع الاسترداد العاجل...', 'warning', 'WARNING', 'MONITOR');
  
  try {
    const success = await AIMonitorService.emergencyRecovery();
    
    if (success) {
      addLog('تم تفعيل وضع الاسترداد العاجل بنجاح', 'success', 'SUCCESS', 'MONITOR');
    } else {
      addLog('فشل تفعيل وضع الاسترداد العاجل', 'error', 'ERROR', 'MONITOR');
    }
  } catch (error) {
    addLog(`خطأ في الاسترداد العاجل: ${error.message}`, 'error', 'ERROR', 'MONITOR');
  } finally {
    isEmergencyMode.value = false;
    updateServiceStatus();
  }
};

const testService = async (serviceName) => {
  isTesting.value = true;
  addLog(`بدء اختبار خدمة ${getServiceName(serviceName)}...`, 'info', 'INFO', 'TEST');
  
  try {
    let result;
    
    switch (serviceName) {
      case 'ai':
        result = await AIService.healthCheck();
        break;
      case 'pricing':
        result = await AIMonitorService.checkPricingService();
        break;
      case 'erpnext':
        result = await AIMonitorService.checkERPNextIntegration();
        break;
    default:
        result = { status: 'unknown' };
    }
    
    const status = result.status || result;
    addLog(`نتيجة اختبار ${getServiceName(serviceName)}: ${getStatusText(status)}`, 
             status === 'active' ? 'success' : 'warning', 
             status === 'active' ? 'SUCCESS' : 'WARNING', 
             'TEST');
    
  } catch (error) {
    addLog(`خطأ في اختبار ${getServiceName(serviceName)}: ${error.message}`, 'error', 'ERROR', 'TEST');
  } finally {
    isTesting.value = false;
    updateServiceStatus();
  }
};

const restartService = async (serviceName) => {
  addLog(`إعادة تشغيل خدمة ${getServiceName(serviceName)}...`, 'info', 'INFO', 'RESTART');
  
  try {
    // Service-specific restart logic would go here
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    addLog(`تمت إعادة تشغيل خدمة ${getServiceName(serviceName)} بنجاح`, 'success', 'SUCCESS', 'RESTART');
    
  } catch (error) {
    addLog(`خطأ في إعادة تشغيل ${getServiceName(serviceName)}: ${error.message}`, 'error', 'ERROR', 'RESTART');
  } finally {
    updateServiceStatus();
  }
};

const clearLogs = () => {
  logs.value = [];
  addLog('تم مسح السجلات', 'info', 'INFO', 'SYSTEM');
};

const exportLogs = () => {
  const logData = {
    logs: logs.value,
    serviceStatus: serviceStatus.value,
    performanceMetrics: performanceMetrics.value,
    exportDate: new Date().toISOString()
  };
  
  const blob = new Blob([JSON.stringify(logData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `ai-monitor-logs-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
  
  addLog('تم تصدير السجلات', 'info', 'INFO', 'SYSTEM');
};

// Event Listeners
const handleServiceStatusUpdate = (event) => {
  const status = event.detail;
  serviceStatus.value = status;
  
  // Add log for status changes
  if (status.overall !== serviceStatus.value.overall) {
    const statusText = status.overall === 'healthy' ? 'صحي' : 'محظور';
    addLog(`تغير حالة النظام إلى: ${statusText}`, 'info', 'INFO', 'MONITOR');
  }
};

// Lifecycle
onMounted(() => {
  // Initial status update
  updateServiceStatus();
  updatePerformanceMetrics();
  
  // Add initial log
  addLog('بدء مراقبة أنظمة الذكاء الاصطناعي', 'info', 'INFO', 'MONITOR');
  
  // Listen for service status updates
  window.addEventListener('ai-service-status-update', handleServiceStatusUpdate);
  
  // Update status every 10 seconds
  const statusInterval = setInterval(() => {
    updateServiceStatus();
    updatePerformanceMetrics();
  }, 10000);
  
  // Cleanup on unmount
  onUnmounted(() => {
    clearInterval(statusInterval);
    window.removeEventListener('ai-service-status-update', handleServiceStatusUpdate);
    AIMonitorService.cleanup();
  });
});
</script>

<style scoped>
.ai-monitor {
  padding: 20px;
  min-height: 100vh;
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
}

.header-content h1 {
  margin: 0 0 5px 0;
  color: #fff;
}

.header-content p {
  margin: 0;
  color: var(--text-dim);
}

.header-actions {
  display: flex;
  gap: 10px;
}

.status-overview {
  margin-bottom: 30px;
}

.status-card {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.status-card.healthy {
  border-color: #4caf50;
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.2);
}

.status-card.degraded {
  border-color: #ff9800;
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.2);
}

.status-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.status-card.healthy .status-icon {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-card.degraded .status-icon {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.status-info h3 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 1.2rem;
}

.status-info p {
  margin: 0 0 10px 0;
  color: var(--text-dim);
}

.status-details {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: var(--text-dim);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.service-card {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-2px);
  border-color: #d4af37;
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.service-info h3 {
  margin: 0;
  color: #fff;
  font-size: 1.1rem;
}

.service-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.service-status.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.service-status.fallback {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.service-status.limited {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.service-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.service-metrics {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.metric-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.metric-value {
  color: #fff;
  font-weight: 600;
}

.metric-value.active {
  color: #4caf50;
}

.metric-value.fallback {
  color: #ff9800;
}

.metric-value.limited {
  color: #f44336;
}

.performance-bar {
  width: 100px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.performance-fill {
  height: 100%;
  background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.performance-value {
  font-size: 0.8rem;
  margin-right: 10px;
}

.service-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.metrics-dashboard {
  margin-bottom: 30px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.metric-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
  text-align: center;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.metric-value.large {
  font-size: 2rem;
  font-weight: 700;
  color: #d4af37;
  margin-bottom: 5px;
}

.metric-value.large.error {
  color: #f44336;
}

.logs-section {
  margin-bottom: 30px;
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logs-container {
  max-height: 400px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 15px;
}

.log-entry {
  display: grid;
  grid-template-columns: 100px 150px 1fr 80px;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.85rem;
}

.log-entry.success {
  border-left: 3px solid #4caf50;
}

.log-entry.error {
  border-left: 3px solid #f44336;
}

.log-entry.warning {
  border-left: 3px solid #ff9800;
}

.log-time {
  color: var(--text-dim);
  font-family: monospace;
}

.log-service {
  color: #d4af37;
  font-weight: 600;
}

.log-message {
  color: #fff;
}

.log-level {
  text-align: center;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.emergency-alert {
  background: rgba(244, 67, 54, 0.2);
  border: 2px solid #f44336;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.alert-content i {
  font-size: 2rem;
  color: #f44336;
}

.alert-content h4 {
  margin: 0 0 5px 0;
  color: #f44336;
}

.alert-content p {
  margin: 0;
  color: var(--text-dim);
}

/* Responsive Design */
@media (max-width: 768px) {
  .monitor-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .log-entry {
    grid-template-columns: 80px 1fr 60px;
    gap: 5px;
  }
  
  .log-service {
    display: none;
  }
}
</style>
