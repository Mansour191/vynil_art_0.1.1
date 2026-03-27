<template>
  <div class="royal-ai-dashboard marble-bg min-h-screen p-6">
    <!-- Header -->
    <div
      class="dashboard-header bg-white/80 backdrop-blur-md rounded-2xl shadow-marble p-6 mb-6"
      v-motion="fadeUpVariants"
    >
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-royal-600 to-gold-500 bg-clip-text text-transparent">
            <i class="fas fa-brain mr-3"></i>
            لوحة تحكم الذكاء الاصطناعي
          </h1>
          <p class="text-marble-600 mt-2">مراقبة وإدارة جميع أنظمة الذكاء الاصطناعي والتدريب</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <Button
            icon="fas fa-sync"
            label="تحديث"
            class="p-button-outlined p-button-royal"
            @click="refreshData"
          />
          <Button
            icon="fas fa-download"
            label="تصدير التقرير"
            class="p-button-gold"
            @click="exportReport"
          />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="isLoading"
      class="flex flex-col items-center justify-center py-20"
      v-motion="fadeUpVariants"
    >
      <div class="relative">
        <div class="w-16 h-16 border-4 border-royal-200 border-t-royal-600 rounded-full animate-spin"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-gold-200 border-b-gold-500 rounded-full animate-spin" style="animation-delay: 0.15s"></div>
      </div>
      <p class="text-marble-600 mt-4 font-medium">جاري تحميل بيانات الذكاء الاصطناعي...</p>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6">
      <!-- Quick Stats -->
      <div class="dashboard-grid">
        <div
          v-for="(stat, index) in quickStats"
          :key="index"
          class="card-marble"
          v-motion="{
            initial: { opacity: 0, y: 20 },
            enter: {
              opacity: 1,
              y: 0,
              transition: {
                delay: index * 100,
                duration: 500
              }
            }
          }"
        >
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-bold text-marble-900">{{ stat.value }}</h3>
              <p class="text-marble-600 text-sm mt-1">{{ stat.label }}</p>
            </div>
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center"
              :class="stat.iconBg"
            >
              <i :class="stat.icon" class="text-white text-lg"></i>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-center justify-between text-sm">
              <span class="text-marble-500">{{ stat.changeLabel }}</span>
              <span :class="stat.changeColor">{{ stat.change }}</span>
            </div>
            <div class="mt-2 bg-marble-200 rounded-full h-2">
              <div
                class="h-2 rounded-full"
                :class="stat.progressColor"
                :style="{ width: stat.progress }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Services Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- AI Service Status -->
        <div
          class="card-royal"
          v-motion="fadeUpVariants"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-marble-900">
              <i class="fas fa-brain mr-2 text-royal-600"></i>
              خدمة الذكاء الاصطناعي
            </h3>
            <div
              class="w-3 h-3 rounded-full"
              :class="aiStatus.overall === 'healthy' ? 'bg-green-500 pulse-live' : 'bg-yellow-500'"
            ></div>
          </div>
          
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-marble-600">الخدمات الفرعية</span>
              <span class="font-medium text-marble-900">{{ aiStatus.services?.length || 0 }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-marble-600">نظام التشغيل</span>
              <span class="font-medium text-marble-900">
                {{ aiStatus.fallbackMode ? 'احتياطي' : 'أساسي' }}
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-marble-600">وقت التشغيل</span>
              <span class="font-medium text-marble-900">{{ aiStatus.uptime || '0s' }}</span>
            </div>
          </div>

          <div class="mt-4 flex gap-2">
            <Button
              icon="fas fa-flask"
              label="اختبار"
              class="p-button-outlined p-button-sm p-button-royal"
              @click="testAIService"
            />
            <Button
              icon="fas fa-sync"
              label="إعادة تشغيل"
              class="p-button-outlined p-button-sm p-button-royal"
              @click="restartAIService"
            />
          </div>
        </div>

        <!-- Learning System Status -->
        <div
          class="card-royal"
          v-motion="fadeUpVariants"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-marble-900">
              <i class="fas fa-graduation-cap mr-2 text-gold-500"></i>
              نظام التعلم
            </h3>
            <div
              class="w-3 h-3 rounded-full"
              :class="learningStats.isActive ? 'bg-green-500 pulse-live' : 'bg-charcoal/60'"
            ></div>
          </div>
          
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-marble-600">معدل التعلم</span>
              <span class="font-medium text-marble-900">{{ learningStats.learningRate || 0 }}%</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-marble-600">التحسين</span>
              <span class="font-medium text-marble-900">{{ learningStats.improvementRate || 0 }}%</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-marble-600">النماذج</span>
              <span class="font-medium text-marble-900">{{ learningStats.totalModels || 0 }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-marble-600">آخر تحديث</span>
              <span class="font-medium text-marble-900 text-sm">
                {{ formatTime(learningStats.lastUpdate) }}
              </span>
            </div>
          </div>

          <div class="mt-4 flex gap-2">
            <Button
              icon="fas fa-chart-bar"
              label="التفاصيل"
              class="p-button-outlined p-button-sm p-button-royal"
              @click="viewTrainingDetails"
            />
            <Button
              icon="fas fa-play"
              label="تدريب سريع"
              class="p-button-outlined p-button-sm p-button-gold"
              @click="startQuickTraining"
            />
          </div>
        </div>

        <!-- Performance Monitor -->
        <div
          class="card-royal"
          v-motion="fadeUpVariants"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-marble-900">
              <i class="fas fa-tachometer-alt mr-2 text-royal-600"></i>
              مراقبة الأداء
            </h3>
            <div
              class="w-3 h-3 rounded-full"
              :class="systemStatus.healthy ? 'bg-green-500 pulse-live' : 'bg-yellow-500'"
            ></div>
          </div>
          
          <div class="space-y-3">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-marble-600 text-sm">استخدام المعالج</span>
                <span class="font-medium text-marble-900 text-sm">{{ performanceMetrics.cpuUsage || 0 }}%</span>
              </div>
              <div class="bg-marble-200 rounded-full h-2">
                <div
                  class="bg-gradient-to-r from-royal-500 to-gold-500 h-2 rounded-full"
                  :style="{ width: (performanceMetrics.cpuUsage || 0) + '%' }"
                ></div>
              </div>
            </div>
            
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-marble-600 text-sm">استخدام الذاكرة</span>
                <span class="font-medium text-marble-900 text-sm">{{ performanceMetrics.memoryUsage || 0 }}%</span>
              </div>
              <div class="bg-marble-200 rounded-full h-2">
                <div
                  class="bg-gradient-to-r from-royal-500 to-gold-500 h-2 rounded-full"
                  :style="{ width: (performanceMetrics.memoryUsage || 0) + '%' }"
                ></div>
              </div>
            </div>
            
            <div class="flex justify-between items-center">
              <span class="text-marble-600 text-sm">وقت الاستجابة</span>
              <span class="font-medium text-marble-900 text-sm">{{ performanceMetrics.responseTime || 0 }}ms</span>
            </div>
            
            <div class="flex justify-between items-center">
              <span class="text-marble-600 text-sm">معدل الخطأ</span>
              <span class="font-medium text-marble-900 text-sm">{{ performanceMetrics.errorRate || 0 }}%</span>
            </div>
          </div>

          <div class="mt-4">
            <Button
              icon="fas fa-chart-line"
              label="عرض الرسوم البيانية"
              class="p-button-outlined p-button-sm p-button-royal w-full"
              @click="showPerformanceCharts"
            />
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div
        class="card-royal"
        v-motion="fadeUpVariants"
      >
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-marble-900">
            <i class="fas fa-clock mr-2 text-royal-600"></i>
            النشاط الأخير
          </h3>
          <Button
            icon="fas fa-sync"
            class="p-button-outlined p-button-sm p-button-royal"
            @click="refreshActivity"
          />
        </div>
        
        <div class="space-y-3">
          <div
            v-for="(activity, index) in recentActivities"
            :key="activity.id"
            class="flex items-center justify-between p-3 rounded-xl bg-marble-50/50 border border-marble-200"
            v-motion="{
              initial: { opacity: 0, x: -20 },
              enter: {
                opacity: 1,
                x: 0,
                transition: {
                  delay: index * 50,
                  duration: 300
                }
              }
            }"
          >
            <div class="flex items-center space-x-3">
              <div
                class="w-10 h-10 rounded-lg flex items-center justify-center"
                :class="getActivityIconBg(activity.type)"
              >
                <i :class="getActivityIcon(activity.type)" class="text-white"></i>
              </div>
              <div>
                <p class="font-medium text-marble-900">{{ activity.title }}</p>
                <p class="text-sm text-marble-600">{{ activity.description }}</p>
              </div>
            </div>
            <div class="text-left">
              <span class="text-sm text-marble-500">{{ formatTime(activity.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div
        class="card-royal"
        v-motion="fadeUpVariants"
      >
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-marble-900">
            <i class="fas fa-bolt mr-2 text-gold-500"></i>
            الإجراءات السريعة
          </h3>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <Button
            v-for="action in quickActions"
            :key="action.id"
            :icon="action.icon"
            :label="action.label"
            class="p-button-outlined p-button-royal flex flex-col items-center justify-center h-20 space-y-2"
            :class="action.class"
            @click="action.handler"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useFadeInUp } from '@/composables/useAnimations';
import AIService from '@/services/AIService';
import AIMonitorService from '@/services/AIMonitorService';
import AILearningService from '@/services/AILearningService';

const { variants: fadeUpVariants } = useFadeInUp();

// State
const isLoading = ref(true);
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

const recentActivities = ref([
  {
    id: 1,
    type: 'training',
    title: 'تدريب نموذج المساعد',
    description: 'تم تدريب نموذج المساعد الذكي بدقة 92%',
    timestamp: new Date(Date.now() - 1000 * 60 * 5)
  },
  {
    id: 2,
    type: 'optimization',
    title: 'تحسين الخوارزميات',
    description: 'تم تحسين خوارزمية التسعير بنسبة 15%',
    timestamp: new Date(Date.now() - 1000 * 60 * 15)
  },
  {
    id: 3,
    type: 'monitoring',
    title: 'فحص النظام',
    description: 'اكتمل فحص صحة جميع الخدمات بنجاح',
    timestamp: new Date(Date.now() - 1000 * 60 * 30)
  }
]);

// Computed
const quickStats = computed(() => [
  {
    label: 'حالة الذكاء الاصطناعي',
    value: aiStatus.value.overall === 'healthy' ? 'نشط' : 'محدود',
    icon: 'fas fa-brain',
    iconBg: 'bg-gradient-to-r from-royal-600 to-royal-700',
    changeLabel: 'معدل الاستجابة',
    change: '+2.3%',
    changeColor: 'text-green-600',
    progress: '85%',
    progressColor: 'bg-gradient-to-r from-royal-500 to-royal-600'
  },
  {
    label: 'جلسات التدريب',
    value: learningStats.value.totalSessions || 0,
    icon: 'fas fa-graduation-cap',
    iconBg: 'bg-gradient-to-r from-gold-500 to-gold-600',
    changeLabel: 'هذا الأسبوع',
    change: '+12',
    changeColor: 'text-green-600',
    progress: '72%',
    progressColor: 'bg-gradient-to-r from-gold-500 to-gold-600'
  },
  {
    label: 'متوسط دقة النماذج',
    value: `${learningStats.value.averageAccuracy || 0}%`,
    icon: 'fas fa-chart-line',
    iconBg: 'bg-gradient-to-r from-royal-600 to-gold-500',
    changeLabel: 'تحسن',
    change: '+5.2%',
    changeColor: 'text-green-600',
    progress: '91%',
    progressColor: 'bg-gradient-to-r from-royal-500 to-gold-500'
  },
  {
    label: 'الخدمات النشطة',
    value: `${systemStatus.value.activeServices || 0}/${systemStatus.value.totalServices || 0}`,
    icon: 'fas fa-cogs',
    iconBg: 'bg-gradient-to-r from-green-500 to-green-600',
    changeLabel: 'التشغيل',
    change: '100%',
    changeColor: 'text-green-600',
    progress: '100%',
    progressColor: 'bg-gradient-to-r from-green-500 to-green-600'
  }
]);

const quickActions = [
  {
    id: 1,
    icon: 'fas fa-magic',
    label: 'تحسين النماذج',
    handler: optimizeAllModels
  },
  {
    id: 2,
    icon: 'fas fa-download',
    label: 'نسخ احتياطي',
    handler: backupAllData
  },
  {
    id: 3,
    icon: 'fas fa-stethoscope',
    label: 'تشخيص',
    handler: runDiagnostics
  },
  {
    id: 4,
    icon: 'fas fa-broom',
    label: 'مسح الكاش',
    handler: clearAllCaches
  },
  {
    id: 5,
    icon: 'fas fa-exclamation-triangle',
    label: 'وضع الطوارئ',
    handler: emergencyMode,
    class: 'p-button-danger'
  },
  {
    id: 6,
    icon: 'fas fa-power-off',
    label: 'إيقاف الخدمات',
    handler: shutdownAllServices,
    class: 'p-button-danger'
  }
];

// Methods
const loadStatusData = async () => {
  try {
    const aiServiceStatus = AIService.getServiceStatus();
    aiStatus.value = aiServiceStatus || {
      overall: 'unknown',
      services: [],
      fallbackMode: false,
      uptime: '0s'
    };
    
    const learningAnalytics = AILearningService.getLearningAnalytics();
    learningStats.value = {
      totalSessions: learningAnalytics.totalTrainingSessions || 0,
      averageAccuracy: Math.round((learningAnalytics.averageAccuracy || 0) * 100),
      learningRate: Math.round((learningAnalytics.learningRate || 0) * 100),
      improvementRate: Math.round((learningAnalytics.learningRate || 0) * 100),
      totalModels: learningAnalytics.modelVersions ? Object.keys(learningAnalytics.modelVersions).length : 0,
      lastUpdate: learningAnalytics.lastUpdate,
      isActive: true
    };
    
    const monitorStatus = AIMonitorService.getServiceStatus();
    systemStatus.value = monitorStatus || {
      healthy: false,
      activeServices: 0,
      totalServices: 0,
      uptime: '0s'
    };
    
    performanceMetrics.value = {
      cpuUsage: Math.random() * 30 + 20,
      memoryUsage: Math.random() * 40 + 30,
      responseTime: Math.random() * 100 + 50,
      errorRate: Math.random() * 2
    };
    
  } catch (error) {
    console.error('Error loading AI dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const refreshData = async () => {
  isLoading.value = true;
  await loadStatusData();
};

const formatTime = (timestamp) => {
  if (!timestamp) return '--:--';
  return new Intl.DateTimeFormat('ar-DZ', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(timestamp));
};

const getActivityIcon = (type) => {
  const icons = {
    training: 'fas fa-graduation-cap',
    optimization: 'fas fa-chart-line',
    monitoring: 'fas fa-heartbeat',
    error: 'fas fa-exclamation-triangle'
  };
  return icons[type] || 'fas fa-info-circle';
};

const getActivityIconBg = (type) => {
  const backgrounds = {
    training: 'bg-gradient-to-r from-gold-500 to-gold-600',
    optimization: 'bg-gradient-to-r from-royal-500 to-royal-600',
    monitoring: 'bg-gradient-to-r from-green-500 to-green-600',
    error: 'bg-gradient-to-r from-red-500 to-red-600'
  };
  return backgrounds[type] || 'bg-gradient-to-r from-charcoal to-charcoal/80';
};

// Action handlers
const testAIService = () => {
  console.log('Testing AI Service...');
};

const restartAIService = () => {
  console.log('Restarting AI Service...');
};

const viewTrainingDetails = () => {
  console.log('Viewing training details...');
};

const startQuickTraining = () => {
  console.log('Starting quick training...');
};

const showPerformanceCharts = () => {
  console.log('Showing performance charts...');
};

const refreshActivity = () => {
  console.log('Refreshing activity...');
};

const optimizeAllModels = () => {
  console.log('Optimizing all models...');
};

const backupAllData = () => {
  console.log('Backing up all data...');
};

const runDiagnostics = () => {
  console.log('Running diagnostics...');
};

const clearAllCaches = () => {
  console.log('Clearing all caches...');
};

const emergencyMode = () => {
  console.log('Entering emergency mode...');
};

const shutdownAllServices = () => {
  console.log('Shutting down all services...');
};

const exportReport = () => {
  console.log('Exporting report...');
};

onMounted(() => {
  loadStatusData();
});
</script>

<style scoped>
.royal-ai-dashboard {
  font-family: 'Inter', system-ui, sans-serif;
}

.pulse-live {
  animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.6);
  }
  50% {
    opacity: 0.8;
    box-shadow: 0 0 40px rgba(34, 197, 94, 0.8);
  }
}

:deep(.p-button) {
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.p-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

:deep(.p-button-royal) {
  background: linear-gradient(135deg, #4f46e5, #4338ca);
  border: 1px solid #4f46e5;
  color: white;
}

:deep(.p-button-royal:hover) {
  background: linear-gradient(135deg, #4338ca, #3730a3);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
}

:deep(.p-button-gold) {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border: 1px solid #f59e0b;
  color: white;
}

:deep(.p-button-gold:hover) {
  background: linear-gradient(135deg, #d97706, #b45309);
  box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);
}

:deep(.p-button-danger) {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: 1px solid #ef4444;
  color: white;
}

:deep(.p-button-danger:hover) {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);
}

:deep(.p-button-outlined) {
  background: transparent;
  border: 2px solid;
}

:deep(.p-button-outlined.p-button-royal) {
  border-color: #4f46e5;
  color: #4f46e5;
}

:deep(.p-button-outlined.p-button-royal:hover) {
  background: #4f46e5;
  color: white;
}

:deep(.p-button-outlined.p-button-gold) {
  border-color: #f59e0b;
  color: #f59e0b;
}

:deep(.p-button-outlined.p-button-gold:hover) {
  background: #f59e0b;
  color: white;
}
</style>
