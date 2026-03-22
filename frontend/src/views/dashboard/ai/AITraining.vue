<template>
  <div class="ai-training">
    <!-- Header -->
    <header class="training-header">
      <div class="header-content">
        <h1 class="text-3xl font-bold gold-text mb-2">
          <i class="fa-solid fa-brain me-3"></i>
          منصة تدريب الذكاء الاصطناعي
        </h1>
        <p class="text-dim">تدريب وتحسين نماذج الذكاء الاصطناعي لتصبح أكثر ذكاءً وتعلماً</p>
      </div>
      <div class="header-actions">
        <button class="btn-primary" @click="startAllTraining" :disabled="isTraining">
          <i :class="isTraining ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-play'"></i>
          تدريب جميع النماذج
        </button>
        <button class="btn-secondary" @click="exportData">
          <i class="fa-solid fa-download"></i>
          تصدير البيانات
        </button>
      </div>
    </header>

    <!-- Training Overview -->
    <div class="training-overview mb-8">
      <div class="overview-cards">
        <div class="overview-card">
          <div class="card-icon">
            <i class="fa-solid fa-graduation-cap"></i>
          </div>
          <div class="card-info">
            <h3>{{ totalTrainingSessions }}</h3>
            <p>جلسات التدريب</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="card-icon">
            <i class="fa-solid fa-chart-line"></i>
          </div>
          <div class="card-info">
            <h3>{{ averageAccuracy }}%</h3>
            <p>متوسط الدقة</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="card-icon">
            <i class="fa-solid fa-trophy"></i>
          </div>
          <div class="card-info">
            <h3>{{ learningRate }}%</h3>
            <p>معدل التعلم</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="card-icon">
            <i class="fa-solid fa-clock"></i>
          </div>
          <div class="card-info">
            <h3>{{ lastUpdate }}</h3>
            <p>آخر تحديث</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Models Grid -->
    <div class="models-section mb-8">
      <div class="section-header">
        <h2 class="text-2xl font-bold">
          <i class="fa-solid fa-cube me-2"></i>
          نماذج الذكاء الاصطناعي
        </h2>
      </div>
      
      <div class="models-grid">
        <div v-for="(model, modelName) in aiModels" :key="modelName" class="model-card">
          <div class="model-header">
            <div class="model-info">
              <h3>{{ getModelName(modelName) }}</h3>
              <span class="model-version">v{{ model.version }}</span>
              <span class="model-status" :class="getModelStatusClass(model)">
                {{ getModelStatus(model) }}
              </span>
            </div>
            <div class="model-icon">
              <i :class="getModelIcon(modelName)"></i>
            </div>
          </div>
          
          <div class="model-metrics">
            <div class="metric">
              <span class="metric-label">الدقة:</span>
              <div class="metric-bar">
                <div class="metric-fill" :style="{ width: (model.accuracy * 100) + '%' }"></div>
              </div>
              <span class="metric-value">{{ Math.round(model.accuracy * 100) }}%</span>
            </div>
            
            <div class="metric">
              <span class="metric-label">الأداء:</span>
              <div class="performance-indicators">
                <div class="indicator">
                  <span>D Precision:</span>
                  <span>{{ Math.round((model.performance?.precision || 0) * 100) }}%</span>
                </div>
                <div class="indicator">
                  <span>Recall:</span>
                  <span>{{ Math.round((model.performance?.recall || 0) * 100) }}%</span>
                </div>
                <div class="indicator">
                  <span>F1 Score:</span>
                  <span>{{ Math.round((model.performance?.f1Score || 0) * 100) }}%</span>
                </div>
              </div>
            </div>
            
            <div class="metric">
              <span class="metric-label">آخر تدريب:</span>
              <span class="metric-value">{{ formatDate(model.lastTrained) }}</span>
            </div>
            
            <div class="metric">
              <span class="metric-label">بيانات التدريب:</span>
              <span class="metric-value">{{ model.trainingData?.length || 0 }}</span>
            </div>
          </div>
          
          <div class="model-actions">
            <button class="btn-sm" @click="trainModel(modelName)" :disabled="isTraining">
              <i :class="isTraining ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-dumbbell'"></i>
              تدريب
            </button>
            <button class="btn-sm btn-secondary" @click="viewModelDetails(modelName)">
              <i class="fa-solid fa-eye"></i>
              تفاصيل
            </button>
            <button class="btn-sm btn-warning" @click="resetModel(modelName)">
              <i class="fa-solid fa-undo"></i>
              إعادة تعيين
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Training Progress -->
    <div v-if="currentTrainingSession" class="training-progress mb-8">
      <div class="glass-card">
        <div class="progress-header">
          <h3 class="text-xl font-bold">
            <i class="fa-solid fa-cogs me-2"></i>
            جاري التدريب
          </h3>
          <span class="training-model">{{ getModelName(currentTrainingSession.modelName) }}</span>
        </div>
        
        <div class="progress-content">
          <div class="progress-bar-container">
            <div class="progress-info">
              <span>الخطوة الحالية: {{ getStepName(currentTrainingSession.currentStep) }}</span>
              <span>{{ currentTrainingSession.progress }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: currentTrainingSession.progress + '%' }"></div>
            </div>
          </div>
          
          <div class="training-details">
            <div class="detail-item">
              <span>وقت البدء:</span>
              <span>{{ formatTime(currentTrainingSession.startTime) }}</span>
            </div>
            <div class="detail-item">
              <span>الحالة:</span>
              <span class="status-badge" :class="currentTrainingSession.status">
                {{ getStatusText(currentTrainingSession.status) }}
              </span>
            </div>
            <div class="detail-item" v-if="currentTrainingSession.result">
              <span>النتيجة:</span>
              <span class="result-summary">
                الدقة: {{ Math.round(currentTrainingSession.result.accuracy * 100) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Training History -->
    <div class="training-history mb-8">
      <div class="glass-card">
        <div class="history-header">
          <h3 class="text-xl font-bold">
            <i class="fa-solid fa-history me-2"></i>
            سجل التدريب
          </h3>
          <div class="history-controls">
            <button class="btn-sm" @click="clearHistory">
              <i class="fa-solid fa-trash"></i>
              مسح السجل
            </button>
            <button class="btn-sm btn-secondary" @click="exportHistory">
              <i class="fa-solid fa-download"></i>
              تصدير السجل
            </button>
          </div>
        </div>
        
        <div class="history-list">
          <div v-for="(session, index) in recentSessions" :key="session.id" class="history-item">
            <div class="session-info">
              <div class="session-model">
                <i :class="getModelIcon(session.modelName)"></i>
                <span>{{ getModelName(session.modelName) }}</span>
              </div>
              <div class="session-details">
                <span class="session-time">{{ formatTime(session.startTime) }}</span>
                <span class="session-duration">{{ calculateDuration(session) }}</span>
              </div>
            </div>
            <div class="session-status">
              <span class="status-badge" :class="session.status">
                {{ getStatusText(session.status) }}
              </span>
              <div v-if="session.result" class="session-result">
                <span>الدقة: {{ Math.round(session.result.accuracy * 100) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Learning Analytics -->
    <div class="learning-analytics">
      <div class="glass-card">
        <h3 class="text-xl font-bold mb-4">
          <i class="fa-solid fa-chart-bar me-2"></i>
          تحليلات التعلم
        </h3>
        
        <div class="analytics-grid">
          <div class="analytics-card">
            <h4>معدل التحسن</h4>
            <div class="analytics-chart">
              <canvas ref="improvementChart"></canvas>
            </div>
          </div>
          
          <div class="analytics-card">
            <h4>دقة النماذج</h4>
            <div class="analytics-chart">
              <canvas ref="accuracyChart"></canvas>
            </div>
          </div>
          
          <div class="analytics-card">
            <h4>بيانات التدريب</h4>
            <div class="data-points">
              <div class="point" v-for="(value, key) in trainingDataPoints" :key="key">
                <span class="point-label">{{ key }}</span>
                <span class="point-value">{{ value }}</span>
              </div>
            </div>
          </div>
          
          <div class="analytics-card">
            <h4>أداء النظام</h4>
            <div class="performance-metrics">
              <div class="metric">
                <span>سرعة الاستجابة:</span>
                <span>{{ systemPerformance.responseTime }}ms</span>
              </div>
              <div class="metric">
                <span>معدل الخطأ:</span>
                <span>{{ systemPerformance.errorRate }}%</span>
              </div>
              <div class="metric">
                <span>استخدام الذاكرة:</span>
                <span>{{ systemPerformance.memoryUsage }}MB</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Advanced Settings -->
    <div class="advanced-settings">
      <div class="glass-card">
        <h3 class="text-xl font-bold mb-4">
          <i class="fa-solid fa-cog me-2"></i>
          إعدادات متقدمة
        </h3>
        
        <div class="settings-grid">
          <div class="setting-group">
            <h4>إعدادات التدريب</h4>
            <div class="setting-item">
              <label>تكرار التدريب التلقائي:</label>
              <select v-model="trainingSettings.autoTrainingInterval" class="form-control">
                <option value="3600000">كل ساعة</option>
                <option value="21600000">كل 6 ساعات</option>
                <option value="86400000">كل 24 ساعة</option>
                <option value="604800000">كل أسبوع</option>
              </select>
            </div>
            <div class="setting-item">
              <label>دقة التدريب المطلوبة:</label>
              <input type="range" v-model="trainingSettings.targetAccuracy" min="0.8" max="0.99" step="0.01" class="form-range">
              <span>{{ trainingSettings.targetAccuracy }}</span>
            </div>
            <div class="setting-item">
              <label>الحد الأقصى لبيانات التدريب:</label>
              <input type="number" v-model="trainingSettings.maxTrainingData" min="100" max="10000" step="100" class="form-control">
            </div>
          </div>
          
          <div class="setting-group">
            <h4>إعدادات التعلم</h4>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="learningSettings.continuousLearning">
                التعلم المستمر
              </label>
            </div>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="learningSettings.adaptiveLearning">
                التعلم التكيفي
              </label>
            </div>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="learningSettings.realTimeAdaptation">
                التكيف في الوقت الحقيقي
              </label>
            </div>
          </div>
          
          <div class="setting-group">
            <h4>إعدادات النظام</h4>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="systemSettings.autoBackup">
                نسخ احتياطي تلقائي
              </label>
            </div>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="systemSettings.performanceMonitoring">
                مراقبة الأداء
              </label>
            </div>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="systemSettings.errorRecovery">
                استرداد الأخطاء التلقائي
              </label>
            </div>
          </div>
        </div>
        
        <div class="settings-actions">
          <button class="btn-primary" @click="saveSettings">
            <i class="fa-solid fa-save"></i>
            حفظ الإعدادات
          </button>
          <button class="btn-secondary" @click="resetSettings">
            <i class="fa-solid fa-undo"></i>
            إعادة تعيين الإعدادات
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import AILearningService from '@/services/AILearningService';
import Chart from 'chart.js/auto';

// State
const isTraining = ref(false);
const currentTrainingSession = ref(null);
const aiModels = ref({});
const trainingSessions = ref([]);
const learningData = ref({});
const systemPerformance = ref({
  responseTime: 150,
  errorRate: 0.5,
  memoryUsage: 256
});

const trainingSettings = ref({
  autoTrainingInterval: 21600000, // 6 hours
  targetAccuracy: 0.95,
  maxTrainingData: 5000
});

const learningSettings = ref({
  continuousLearning: true,
  adaptiveLearning: true,
  realTimeAdaptation: true
});

const systemSettings = ref({
  autoBackup: true,
  performanceMonitoring: true,
  errorRecovery: true
});

// Chart refs
const improvementChart = ref(null);
const accuracyChart = ref(null);

// Computed
const totalTrainingSessions = computed(() => trainingSessions.value.length);
const averageAccuracy = computed(() => {
  const models = Object.values(aiModels.value);
  if (models.length === 0) return 0;
  const totalAccuracy = models.reduce((sum, model) => sum + (model.accuracy || 0), 0);
  return Math.round((totalAccuracy / models.length) * 100);
});
const learningRate = computed(() => {
  const recentSessions = trainingSessions.value.slice(-10);
  if (recentSessions.length === 0) return 0;
  const totalImprovement = recentSessions.reduce((sum, session) => {
    return sum + (session.result?.improvements?.accuracyImprovement || 0);
  }, 0);
  return Math.round((totalImprovement / recentSessions.length) * 100);
});
const lastUpdate = computed(() => {
  const lastSession = trainingSessions.value[trainingSessions.value.length - 1];
  return lastSession ? formatDate(lastSession.endTime) : 'N/A';
});
const recentSessions = computed(() => trainingSessions.value.slice(-10).reverse());
const trainingDataPoints = computed(() => {
  return {
    'المحادثات': learningData.value.conversationContexts?.length || 0,
    'التسعير': learningData.value.pricingPatterns?.length || 0,
    'التفاعلات': learningData.value.userInteractions?.length || 0,
    'الرؤى': learningData.value.productInsights?.length || 0
  };
});

// Methods
const getModelName = (modelName) => {
  const names = {
    chatbot: 'مساعد الدردشة',
    pricing: 'نظام التسعير',
    recommendations: 'نظام التوصيات',
    sentiment: 'تحليل المشاعر'
  };
  return names[modelName] || modelName;
};

const getModelIcon = (modelName) => {
  const icons = {
    chatbot: 'fa-solid fa-comments',
    pricing: 'fa-solid fa-chart-line',
    recommendations: 'fa-solid fa-lightbulb',
    sentiment: 'fa-solid fa-heart'
  };
  return icons[modelName] || 'fa-solid fa-cube';
};

const getModelStatus = (model) => {
  if (!model.lastTrained) return 'not_trained';
  const daysSinceTraining = (Date.now() - new Date(model.lastTrained).getTime()) / (1000 * 60 * 60 * 24);
  return daysSinceTraining > 7 ? 'needs_update' : 'active';
};

const getModelStatusClass = (status) => {
  const classes = {
    active: 'status-active',
    needs_update: 'status-warning',
    not_trained: 'status-inactive'
  };
  return classes[status] || 'status-unknown';
};

const getStepName = (step) => {
  const stepNames = {
    data_preprocessing: 'معالجة البيانات',
    feature_extraction: 'استخراج الميزات',
    model_training: 'تدريب النموذج',
    validation: 'التحقق من الصحة',
    finalization: 'الإنهاء'
  };
  return stepNames[step] || step;
};

const getStatusText = (status) => {
  const statusTexts = {
    training: 'جاري التدريب',
    completed: 'مكتمل',
    failed: 'فشل'
  };
  return statusTexts[status] || status;
};

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Intl.DateTimeFormat('ar-DZ', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date));
};

const formatTime = (date) => {
  if (!date) return 'N/A';
  return new Intl.DateTimeFormat('ar-DZ', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date));
};

const calculateDuration = (session) => {
  if (!session.startTime || !session.endTime) return 'N/A';
  const duration = new Date(session.endTime) - new Date(session.startTime);
  const minutes = Math.floor(duration / 60000);
  const hours = Math.floor(minutes / 60);
  return hours > 0 ? `${hours}h ${minutes % 60}m` : `${minutes}m`;
};

const trainModel = async (modelName) => {
  isTraining.value = true;
  
  try {
    const result = await AILearningService.startTraining(modelName);
    if (result) {
      await loadTrainingData();
      updateCharts();
    }
  } catch (error) {
    console.error(`Error training ${modelName}:`, error);
  } finally {
    isTraining.value = false;
  }
};

const startAllTraining = async () => {
  isTraining.value = true;
  
  try {
    const results = await AILearningService.forceRetraining();
    await loadTrainingData();
    updateCharts();
  } catch (error) {
    console.error('Error in batch training:', error);
  } finally {
    isTraining.value = false;
  }
};

const resetModel = async (modelName) => {
  if (confirm(`هل أنت متأكد من إعادة تعيين نموذج ${getModelName(modelName)}؟`)) {
    // Reset model logic would go here
    console.log(`Reset ${modelName} model`);
  }
};

const viewModelDetails = (modelName) => {
  // Show detailed model information
  console.log(`View details for ${modelName} model`);
};

const clearHistory = () => {
  if (confirm('هل أنت متأكد من مسح سجل التدريب؟')) {
    trainingSessions.value = [];
    console.log('Training history cleared');
  }
};

const exportHistory = () => {
  const historyData = {
    sessions: trainingSessions.value,
    exportDate: new Date().toISOString()
  };
  
  const blob = new Blob([JSON.stringify(historyData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `training-history-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

const exportData = () => {
  AILearningService.exportLearningData();
};

const saveSettings = () => {
  const settings = {
    training: trainingSettings.value,
    learning: learningSettings.value,
    system: systemSettings.value
  };
  
  localStorage.setItem('ai_training_settings', JSON.stringify(settings));
  console.log('Settings saved');
};

const resetSettings = () => {
  trainingSettings.value = {
    autoTrainingInterval: 21600000,
    targetAccuracy: 0.95,
    maxTrainingData: 5000
  };
  
  learningSettings.value = {
    continuousLearning: true,
    adaptiveLearning: true,
    realTimeAdaptation: true
  };
  
  systemSettings.value = {
    autoBackup: true,
    performanceMonitoring: true,
    errorRecovery: true
  };
  
  localStorage.removeItem('ai_training_settings');
  console.log('Settings reset');
};

const loadTrainingData = async () => {
  try {
    aiModels.value = AILearningService.getAllModels();
    trainingSessions.value = AILearningService.getTrainingStatus().completedSessions;
    learningData.value = AILearningService.getLearningAnalytics();
    
    // Update current training session
    const status = AILearningService.getTrainingStatus();
    currentTrainingSession.value = status.currentSession;
    isTraining.value = status.isTraining;
    
  } catch (error) {
    console.error('Error loading training data:', error);
  }
};

const updateCharts = () => {
  nextTick(() => {
    // Update improvement chart
    if (improvementChart.value) {
      new Chart(improvementChart.value, {
        type: 'line',
        data: {
          labels: ['الجلسة 1', 'الجلسة 2', 'الجلسة 3', 'الجلسة 4', 'الجلسة 5'],
          datasets: [{
            label: 'معدل التحسن (%)',
            data: [2.1, 3.5, 2.8, 4.2, 3.9],
            borderColor: '#d4af37',
            backgroundColor: 'rgba(212, 175, 55, 0.1)',
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
    
    // Update accuracy chart
    if (accuracyChart.value) {
      new Chart(accuracyChart.value, {
        type: 'doughnut',
        data: {
          labels: ['مساعد الدردشة', 'التسعير', 'التوصيات', 'تحليل المشاعر'],
          datasets: [{
            data: [
              aiModels.value.chatbot?.accuracy || 0,
              aiModels.value.pricing?.accuracy || 0,
              aiModels.value.recommendations?.accuracy || 0,
              aiModels.value.sentiment?.accuracy || 0
            ],
            backgroundColor: [
              '#4caf50',
              '#d4af37',
              '#ff9800',
              '#f44336'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: '#fff' }
            }
          }
        }
      });
    }
  });
};

// Lifecycle
onMounted(async () => {
  await loadTrainingData();
  updateCharts();
  
  // Load settings
  const savedSettings = localStorage.getItem('ai_training_settings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    trainingSettings.value = { ...trainingSettings.value, ...settings.training };
    learningSettings.value = { ...learningSettings.value, ...settings.learning };
    systemSettings.value = { ...systemSettings.value, ...settings.system };
  }
  
  // Monitor training status
  setInterval(async () => {
    await loadTrainingData();
  }, 5000);
});
</script>

<style scoped>
.ai-training {
  padding: 20px;
  min-height: 100vh;
}

.training-header {
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

.training-overview {
  margin-bottom: 30px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.overview-card {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-2px);
  border-color: #d4af37;
}

.card-icon {
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

.card-info h3 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 1.8rem;
  font-weight: 700;
}

.card-info p {
  margin: 0;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.models-section {
  margin-bottom: 30px;
}

.section-header {
  margin-bottom: 20px;
  padding: 15px;
  background: var(--bg-card);
  border-radius: 10px;
  border: 1px solid var(--border-light);
}

.section-header h2 {
  margin: 0;
  color: #fff;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.model-card {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
  transition: all 0.3s ease;
}

.model-card:hover {
  transform: translateY(-2px);
  border-color: #d4af37;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.model-info h3 {
  margin: 0;
  color: #fff;
  font-size: 1.2rem;
}

.model-version {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: 10px;
}

.model-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-warning {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.status-inactive {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.model-icon {
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

.model-metrics {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 15px;
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

.metric-bar {
  width: 100px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-right: 10px;
}

.metric-fill {
  height: 100%;
  background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.performance-indicators {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.indicator {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.model-actions {
  display: flex;
  gap: 10px;
}

.training-progress {
  margin-bottom: 30px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-header h3 {
  margin: 0;
  color: #fff;
}

.training-model {
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.progress-bar-container {
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: var(--text-dim);
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50 0%, #d4af37 100%);
  border-radius: 5px;
  transition: width 0.3s ease;
}

.training-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.status-badge {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.result-summary {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.training-history {
  margin-bottom: 30px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  margin: 0;
  color: #fff;
}

.history-controls {
  display: flex;
  gap: 10px;
}

.history-list {
  max-height: 400px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.session-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.session-model {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  font-weight: 600;
}

.session-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.9rem;
  color: var(--text-dim);
}

.session-status {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.session-result {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.learning-analytics {
  margin-bottom: 30px;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.analytics-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
}

.analytics-card h4 {
  margin: 0 0 15px 0;
  color: #fff;
  text-align: center;
}

.analytics-chart {
  height: 200px;
  position: relative;
}

.data-points {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.point {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.point-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.point-value {
  color: #d4af37;
  font-weight: 600;
}

.performance-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.advanced-settings {
  margin-bottom: 30px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.setting-group {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
}

.setting-group h4 {
  margin: 0 0 15px 0;
  color: #fff;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.setting-item label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.form-control {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 6px;
  padding: 6px 10px;
  color: #fff;
  font-size: 0.9rem;
}

.form-range {
  width: 100px;
}

.settings-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .models-grid {
    grid-template-columns: 1fr;
  }
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .training-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .model-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .training-details {
    grid-template-columns: 1fr;
  }
  
  .history-item {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
