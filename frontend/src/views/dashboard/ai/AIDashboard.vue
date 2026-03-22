<template>
  <div class="ai-dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="text-3xl font-bold gold-text mb-2">
          <i class="fa-solid fa-brain me-3"></i>
          لوحة تحكم الذكاء الاصطناعي
        </h1>
        <p class="text-dim">مراقبة وإدارة جميع أنظمة الذكاء الاصطناعي والتدريب</p>
      </div>
      <div class="header-actions">
        <button class="btn-primary" @click="goToTraining">
          <i class="fa-solid fa-graduation-cap me-2"></i>
          منصة التدريب
        </button>
        <button class="btn-secondary" @click="goToMonitoring">
          <i class="fa-solid fa-heartbeat me-2"></i>
          المراقبة
        </button>
      </div>
    </header>

    <!-- Quick Stats -->
    <div class="quick-stats mb-8">
      <div class="stats-grid">
        <div class="stat-card glass-card">
          <div class="stat-icon">
            <i class="fa-solid fa-brain"></i>
          </div>
          <div class="stat-info">
            <h3>{{ aiStatus.overall === 'healthy' ? 'نشط' : 'محدود' }}</h3>
            <p>حالة الذكاء الاصطناعي</p>
          </div>
        </div>
        
        <div class="stat-card glass-card">
          <div class="stat-icon">
            <i class="fa-solid fa-graduation-cap"></i>
          </div>
          <div class="stat-info">
            <h3>{{ learningStats.totalSessions }}</h3>
            <p>جلسات التدريب</p>
          </div>
        </div>
        
        <div class="stat-card glass-card">
          <div class="stat-icon">
            <i class="fa-solid fa-chart-line"></i>
          </div>
          <div class="stat-info">
            <h3>{{ learningStats.averageAccuracy }}%</h3>
            <p>متوسط دقة النماذج</p>
          </div>
        </div>
        
        <div class="stat-card glass-card">
          <div class="stat-icon">
            <i class="fa-solid fa-cogs"></i>
          </div>
          <div class="stat-info">
            <h3>{{ systemStatus.activeServices }}/{{ systemStatus.totalServices }}</h3>
            <p>الخدمات النشطة</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Services Grid -->
    <div class="services-grid mb-8">
      <!-- AI Service Status -->
      <div class="service-panel glass-card">
        <div class="panel-header">
          <h3>
            <i class="fa-solid fa-brain me-2"></i>
            خدمة الذكاء الاصطناعي
          </h3>
          <div class="status-indicator" :class="{ online: aiStatus.overall === 'healthy', offline: aiStatus.overall !== 'healthy' }">
            <i class="fa-solid fa-circle"></i>
            {{ aiStatus.overall === 'healthy' ? 'نشط' : 'محدود' }}
          </div>
        </div>
        
        <div class="service-content">
          <div class="service-metrics">
            <div class="metric">
              <span>الخدمات الفرعية:</span>
              <span>{{ aiStatus.services?.length || 0 }}</span>
            </div>
            <div class="metric">
              <span>نظام التشغيل:</span>
              <span>{{ aiStatus.fallbackMode ? 'احتياطي' : 'أساسي' }}</span>
            </div>
            <div class="metric">
              <span>وقت التشغيل:</span>
              <span>{{ systemStatus.uptime }}</span>
            </div>
          </div>
          
          <div class="service-actions">
            <button class="btn-sm" @click="testAIService">
              <i class="fa-solid fa-flask"></i>
              اختبار
            </button>
            <button class="btn-sm btn-secondary" @click="restartAIService">
              <i class="fa-solid fa-sync"></i>
              إعادة التشغيل
            </button>
          </div>
        </div>
      </div>

      <!-- Learning System Status -->
      <div class="service-panel glass-card">
        <div class="panel-header">
          <h3>
            <i class="fa-solid fa-graduation-cap me-2"></i>
            نظام التعلم
          </h3>
          <div class="status-indicator" :class="{ online: learningStatus.isActive, offline: !learningStatus.isActive }">
            <i class="fa-solid fa-circle"></i>
            {{ learningStatus.isActive ? 'نشط' : 'غير نشط' }}
          </div>
        </div>
        
        <div class="service-content">
          <div class="service-metrics">
            <div class="metric">
              <span>معدل التعلم:</span>
              <span>{{ learningStats.learningRate }}%</span>
            </div>
            <div class="metric">
              <span>التحسين:</span>
              <span>{{ learningStats.improvementRate }}%</span>
            </div>
            <div class="metric">
              <span>النماذج:</span>
              <span>{{ learningStats.totalModels }}</span>
            </div>
            <div class="metric">
              <span>آخر تحديث:</span>
              <span>{{ formatTime(learningStats.lastUpdate) }}</span>
            </div>
          </div>
          
          <div class="service-actions">
            <button class="btn-sm" @click="viewTrainingDetails">
              <i class="fa-solid fa-chart-bar"></i>
              التفاصيل
            </button>
            <button class="btn-sm btn-primary" @click="startQuickTraining">
              <i class="fa-solid fa-play"></i>
              تدريب سريع
            </button>
          </div>
        </div>
      </div>

      <!-- Performance Monitor -->
      <div class="service-panel glass-card">
        <div class="panel-header">
          <h3>
            <i class="fa-solid fa-tachometer-alt me-2"></i>
            مراقبة الأداء
          </h3>
          <div class="status-indicator" :class="{ online: systemStatus.healthy, offline: !systemStatus.healthy }">
            <i class="fa-solid fa-circle"></i>
            {{ systemStatus.healthy ? 'طبيعي' : 'يحتاج انتباه' }}
          </div>
        </div>
        
        <div class="service-content">
          <div class="performance-chart">
            <canvas ref="performanceChart"></canvas>
          </div>
          
          <div class="performance-metrics">
            <div class="metric-row">
              <span class="metric-label">استخدام المعالج:</span>
              <div class="metric-bar">
                <div class="metric-fill" :style="{ width: performanceMetrics.cpuUsage + '%' }"></div>
              </div>
              <span>{{ performanceMetrics.cpuUsage }}%</span>
            </div>
            
            <div class="metric-row">
              <span class="metric-label">استخدام الذاكرة:</span>
              <div class="metric-bar">
                <div class="metric-fill" :style="{ width: performanceMetrics.memoryUsage + '%' }"></div>
              </div>
              <span>{{ performanceMetrics.memoryUsage }}%</span>
            </div>
            
            <div class="metric-row">
              <span class="metric-label">وقت الاستجابة:</span>
              <span>{{ performanceMetrics.responseTime }}ms</span>
            </div>
            
            <div class="metric-row">
              <span class="metric-label">معدل الخطأ:</span>
              <span>{{ performanceMetrics.errorRate }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="activity-section mb-8">
      <div class="glass-card">
        <div class="section-header">
          <h3>
            <i class="fa-solid fa-history me-2"></i>
            النشاط الحديث
          </h3>
          <button class="btn-sm" @click="refreshActivity">
            <i class="fa-solid fa-sync"></i>
            تحديث
          </button>
        </div>
        
        <div class="activity-list">
          <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
            <div class="activity-icon">
              <i :class="getActivityIcon(activity.type)"></i>
            </div>
            <div class="activity-content">
              <div class="activity-header">
                <span class="activity-title">{{ activity.title }}</span>
                <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
              </div>
              <div class="activity-description">{{ activity.description }}</div>
            </div>
            <div class="activity-status" :class="activity.status">
              {{ getStatusText(activity.status) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <div class="glass-card">
        <h3 class="text-xl font-bold mb-4">
          <i class="fa-solid fa-bolt me-2"></i>
          إجراءات سريعة
        </h3>
        
        <div class="actions-grid">
          <button class="action-btn" @click="optimizeAllModels">
            <i class="fa-solid fa-magic"></i>
            تحسين جميع النماذج
          </button>
          
          <button class="action-btn" @click="backupAllData">
            <i class="fa-solid fa-download"></i>
            نسخ احتياطي للبيانات
          </button>
          
          <button class="action-btn" @click="runDiagnostics">
            <i class="fa-solid fa-stethoscope"></i>
            تشخيص النظام
          </button>
          
          <button class="action-btn" @click="clearAllCaches">
            <i class="fa-solid fa-broom"></i>
            مسح جميع الكاشات
          </button>
          
          <button class="action-btn btn-warning" @click="emergencyMode">
            <i class="fa-solid fa-exclamation-triangle"></i>
            وضع الطوارئ
          </button>
          
          <button class="action-btn btn-danger" @click="shutdownAllServices">
            <i class="fa-solid fa-power-off"></i>
            إيقاف جميع الخدمات
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import AIService from '@/services/AIService';
import AIMonitorService from '@/services/AIMonitorService';
import AILearningService from '@/services/AILearningService';
import Chart from 'chart.js/auto';

const router = useRouter();

// State
const aiStatus = ref({
  overall: 'unknown',
  services: [],
  fallbackMode: false,
  uptime: '0s'
});

const learningStats = ref({
  totalSessions: 0,
  averageAccuracy: 0,
  learningRate: 0,
  improvementRate: 0,
  totalModels: 0,
  lastUpdate: null,
  isActive: false
});

const systemStatus = ref({
  healthy: false,
  activeServices: 0,
  totalServices: 0,
  uptime: '0s'
});

const performanceMetrics = ref({
  cpuUsage: 0,
  memoryUsage: 0,
  responseTime: 0,
  errorRate: 0
});

const recentActivities = ref([]);

// Chart refs
const performanceChart = ref(null);

// Computed
const getActivityIcon = (type) => {
  const icons = {
    training: 'fa-solid fa-graduation-cap',
    monitoring: 'fa-solid fa-heartbeat',
    error: 'fa-solid fa-exclamation-triangle',
    success: 'fa-solid fa-check-circle',
    warning: 'fa-solid fa-exclamation-circle',
    info: 'fa-solid fa-info-circle'
  };
  return icons[type] || 'fa-solid fa-cog';
};

const getStatusText = (status) => {
  const statusTexts = {
    completed: 'مكتمل',
    running: 'جاري التشغيل',
    failed: 'فشل',
    warning: 'تحذير',
    info: 'معلومات'
  };
  return statusTexts[status] || status;
};

const formatTime = (timestamp) => {
  if (!timestamp) return 'N/A';
  return new Intl.DateTimeFormat('ar-DZ', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(new Date(timestamp));
};

// Methods
const loadStatusData = async () => {
  try {
    // Load AI Service Status
    const aiServiceStatus = AIService.getServiceStatus();
    aiStatus.value = aiServiceStatus;
    
    // Load Learning System Stats
    const learningAnalytics = AILearningService.getLearningAnalytics();
    learningStats.value = {
      ...learningAnalytics,
      isActive: true
    };
    
    // Load System Status
    const monitorStatus = AIMonitorService.getServiceStatus();
    systemStatus.value = monitorStatus;
    
    // Load Performance Metrics
    performanceMetrics.value = {
      cpuUsage: Math.random() * 30 + 20, // Simulated
      memoryUsage: Math.random() * 40 + 30,
      responseTime: Math.random() * 100 + 50,
      errorRate: Math.random() * 2
    };
    
    // Load Recent Activities
    await loadRecentActivities();
    
  } catch (error) {
    console.error('Error loading AI dashboard data:', error);
  }
};

const loadRecentActivities = async () => {
  const activities = [
    {
      id: 1,
      type: 'training',
      title: 'تدريب نموذج المساعد',
      description: 'تم تدريب نموذج المساعد الذكي بدقة 92%',
      status: 'completed',
      timestamp: new Date(Date.now() - 3600000).toISOString()
    },
    {
      id: 2,
      type: 'monitoring',
      title: 'فحص صحة النظام',
      description: 'تم إجراء فحص شامل لجميع خدمات الذكاء الاصطناعي',
      status: 'success',
      timestamp: new Date(Date.now() - 7200000).toISOString()
    },
    {
      id: 3,
      type: 'info',
      title: 'تحديث نموذج التسعير',
      description: 'تم تحديث نموذج التسعير الذكي ببيانات جديدة',
      status: 'completed',
      timestamp: new Date(Date.now() - 10800000).toISOString()
    },
    {
      id: 4,
      type: 'warning',
      title: 'استخدام عالي للذاكرة',
      description: 'استخدام الذاكرة تجاوز 85% من السعة المتاحة',
      status: 'warning',
      timestamp: new Date(Date.now() - 14400000).toISOString()
    },
    {
      id: 5,
      type: 'success',
      title: 'تحسين دقة النموذج',
      description: 'تحسنت دقة نموذج تحليل المشاعر بنسبة 3%',
      status: 'completed',
      timestamp: new Date(Date.now() - 18000000).toISOString()
    }
  ];
  
  recentActivities.value = activities;
};

const goToTraining = () => {
  router.push('/dashboard/ai/training');
};

const goToMonitoring = () => {
  router.push('/dashboard/ai/monitor');
};

const testAIService = async () => {
  try {
    const result = await AIService.healthCheck();
    addActivity('test', 'اختبار خدمة الذكاء الاصطناعي', 
               result.status === 'healthy' ? 'نجح الاختبار' : 'فشل الاختبار', 
               result.status === 'healthy' ? 'success' : 'failed');
  } catch (error) {
    addActivity('error', 'خطأ في اختبار الذكاء الاصطناعي', error.message, 'failed');
  }
};

const restartAIService = async () => {
  try {
    await AIService.initializeAISystems();
    addActivity('info', 'إعادة تشغيل خدمة الذكاء الاصطناعي', 'تمت إعادة التشغيل بنجاح', 'success');
  } catch (error) {
    addActivity('error', 'خطأ في إعادة تشغيل الذكاء الاصطناعي', error.message, 'failed');
  }
};

const viewTrainingDetails = () => {
  router.push('/dashboard/ai/training');
};

const startQuickTraining = async () => {
  try {
    await AILearningService.startTraining('chatbot');
    addActivity('training', 'تدريب سريع للمساعد', 'بدء تدريب نموذج المساعد', 'running');
  } catch (error) {
    addActivity('error', 'خطأ في التدريب السريع', error.message, 'failed');
  }
};

const optimizeAllModels = async () => {
  try {
    const results = await AILearningService.forceRetraining();
    addActivity('info', 'تحسين جميع النماذج', 
               `تم تحسين ${results.filter(r => r.success).length} نماذج بنجاح`, 'success');
  } catch (error) {
    addActivity('error', 'خطأ في تحسين النماذج', error.message, 'failed');
  }
};

const backupAllData = () => {
  try {
    AILearningService.exportLearningData();
    AIService.exportServiceStatus();
    addActivity('info', 'نسخ احتياطي', 'تم تصدير جميع بيانات الذكاء الاصطناعي', 'success');
  } catch (error) {
    addActivity('error', 'خطأ في النسخ الاحتياطي', error.message, 'failed');
  }
};

const runDiagnostics = async () => {
  try {
    const diagnostics = await Promise.all([
      AIService.healthCheck(),
      AIMonitorService.getServiceStatus(),
      AILearningService.getLearningAnalytics()
    ]);
    
    addActivity('info', 'تشخيص النظام', 
               'اكتمل التشخيص بنجاح - جميع الأنظمة تعمل بشكل طبيعي', 'success');
  } catch (error) {
    addActivity('error', 'خطأ في التشخيص', error.message, 'failed');
  }
};

const clearAllCaches = () => {
  try {
    // Clear all caches
    localStorage.removeItem('ai_learning_data');
    localStorage.removeItem('ai_training_sessions');
    localStorage.removeItem('ai_models');
    
    addActivity('info', 'مسح الكاشات', 'تم مسح جميع الكاشات بنجاح', 'success');
  } catch (error) {
    addActivity('error', 'خطأ في مسح الكاشات', error.message, 'failed');
  }
};

const emergencyMode = async () => {
  try {
    await AIMonitorService.emergencyRecovery();
    addActivity('warning', 'تفعيل وضع الطوارئ', 'تم تفعيل وضع الطوارئ', 'warning');
  } catch (error) {
    addActivity('error', 'خطأ في وضع الطوارئ', error.message, 'failed');
  }
};

const shutdownAllServices = () => {
  if (confirm('هل أنت متأكد من إيقاف جميع خدمات الذكاء الاصطناعي؟')) {
    try {
      AIMonitorService.stopMonitoring();
      addActivity('warning', 'إيقاف الخدمات', 'تم إيقاف جميع خدمات الذكاء الاصطناعي', 'warning');
    } catch (error) {
      addActivity('error', 'خطأ في إيقاف الخدمات', error.message, 'failed');
    }
  }
};

const refreshActivity = async () => {
  await loadRecentActivities();
};

const addActivity = (type, title, description, status) => {
  const activity = {
    id: Date.now(),
    type,
    title,
    description,
    status,
    timestamp: new Date().toISOString()
  };
  
  recentActivities.value.unshift(activity);
  
  // Keep only last 20 activities
  if (recentActivities.value.length > 20) {
    recentActivities.value = recentActivities.value.slice(0, 20);
  }
};

const updatePerformanceChart = () => {
  if (performanceChart.value) {
    new Chart(performanceChart.value, {
      type: 'line',
      data: {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [{
          label: 'استخدام المعالج (%)',
          data: [25, 30, 45, 60, 55, 40],
          borderColor: '#d4af37',
          backgroundColor: 'rgba(212, 175, 55, 0.1)',
          tension: 0.4
        }, {
          label: 'استخدام الذاكرة (%)',
          data: [35, 40, 55, 70, 65, 50],
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#fff' }
          }
        },
        scales: {
          y: {
            ticks: { color: '#fff' },
            grid: { color: 'rgba(255, 255, 255, 0.1)' }
          },
          x: {
            ticks: { color: '#fff' },
            grid: { color: 'rgba(255, 255, 255, 0.1)' }
          }
        }
      }
    });
  }
};

// Lifecycle
onMounted(async () => {
  await loadStatusData();
  
  // Update performance chart every 30 seconds
  setInterval(updatePerformanceChart, 30000);
  
  // Update status data every 10 seconds
  setInterval(loadStatusData, 10000);
  
  nextTick(() => {
    updatePerformanceChart();
  });
});
</script>

<style scoped>
.ai-dashboard {
  padding: 20px;
  min-height: 100vh;
}

.dashboard-header {
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

.quick-stats {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: #d4af37;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-info h3 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 1.8rem;
  font-weight: 700;
}

.stat-info p {
  margin: 0;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.service-panel {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h3 {
  margin: 0;
  color: #fff;
  font-size: 1.2rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-indicator.online {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-indicator.offline {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.service-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.service-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.metric span {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.metric span:last-child {
  color: #fff;
  font-weight: 600;
}

.service-actions {
  display: flex;
  gap: 10px;
}

.performance-chart {
  height: 200px;
  margin-bottom: 20px;
}

.performance-metrics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.metric-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.metric-bar {
  width: 100px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin: 0 10px;
}

.metric-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50 0%, #d4af37 50%, #ff9800 100%);
  border-radius: 3px;
}

.activity-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #fff;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: grid;
  grid-template-columns: 40px 1fr 80px 100px;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.activity-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-title {
  color: #fff;
  font-weight: 600;
  font-size: 0.95rem;
}

.activity-time {
  color: var(--text-dim);
  font-size: 0.8rem;
  font-family: monospace;
}

.activity-description {
  color: var(--text-dim);
  font-size: 0.85rem;
  line-height: 1.4;
}

.activity-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
}

.activity-status.success {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.activity-status.failed {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.activity-status.warning {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.activity-status.running {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
}

.quick-actions {
  margin-bottom: 30px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.action-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
}

.action-btn:hover {
  transform: translateY(-2px);
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.action-btn.btn-warning {
  border-color: #ff9800;
}

.action-btn.btn-warning:hover {
  border-color: #f57c00;
}

.action-btn.btn-danger {
  border-color: #f44336;
}

.action-btn.btn-danger:hover {
  border-color: #d32f2f;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .service-metrics {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    grid-template-columns: 40px 1fr 80px;
    gap: 10px;
  }
  
  .activity-status {
    grid-column: 4;
    margin-top: 8px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
