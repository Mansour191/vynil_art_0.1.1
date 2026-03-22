<template>
  <div class="pricing-manager">
    <!-- Header -->
    <header class="pricing-header">
      <div class="header-content">
        <h1 class="text-3xl font-bold gold-text mb-2">
          <i class="fa-solid fa-chart-line me-3"></i>
          مدير التسعير الذكي
        </h1>
        <p class="text-dim">نظام تسعير دينامي مدعوم بالذكاء الاصطناعي وتحليلات السوق</p>
      </div>
      <div class="header-actions">
        <button class="btn-primary" @click="runPricingOptimization">
          <i class="fa-solid fa-robot me-2"></i>
          تحسين التسعير بالذكاء الاصطناعي
        </button>
        <button class="btn-secondary" @click="exportPricingReport">
          <i class="fa-solid fa-download me-2"></i>
          تصدير تقرير
        </button>
      </div>
    </header>

    <!-- KPI Cards -->
    <div class="kpi-grid mb-8">
      <div v-for="kpi in kpiData" :key="kpi.title" class="kpi-card glass-card">
        <div class="kpi-icon">
          <i :class="kpi.icon"></i>
        </div>
        <div class="kpi-info">
          <h3>{{ kpi.value }}</h3>
          <p>{{ kpi.title }}</p>
          <div class="kpi-trend" :class="kpi.trendType">
            <i :class="kpi.trendIcon"></i>
            <span>{{ kpi.trend }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Pricing Rules -->
      <div class="glass-card pricing-rules">
        <div class="card-header">
          <h3 class="text-xl font-bold">
            <i class="fa-solid fa-gavel me-2"></i>
            قواعد التسعير
          </h3>
          <button class="btn-sm btn-primary" @click="showCreateRuleModal = true">
            <i class="fa-solid fa-plus me-1"></i>
            قاعدة جديدة
          </button>
        </div>
        
        <div class="rules-list">
          <div v-for="rule in pricingRules" :key="rule.id" class="rule-item">
            <div class="rule-info">
              <h4>{{ rule.name }}</h4>
              <p>{{ rule.description }}</p>
              <div class="rule-conditions">
                <span v-for="condition in rule.conditions" :key="condition" class="condition-tag">
                  {{ condition }}
                </span>
              </div>
            </div>
            <div class="rule-actions">
              <button class="btn-sm" @click="editRule(rule)">
                <i class="fa-solid fa-edit"></i>
              </button>
              <button class="btn-sm btn-danger" @click="deleteRule(rule.id)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Price Testing -->
      <div class="glass-card price-testing">
        <div class="card-header">
          <h3 class="text-xl font-bold">
            <i class="fa-solid fa-flask me-2"></i>
            اختبار التسعير
          </h3>
        </div>
        
        <div class="test-form">
          <div class="form-group">
            <label>اختر المنتج</label>
            <select v-model="testConfig.productId" class="form-control">
              <option value="">اختر منتج...</option>
              <option v-for="product in availableProducts" :key="product.id" :value="product.id">
                {{ product.name }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>نوع الاختبار</label>
            <select v-model="testConfig.testType" class="form-control">
              <option value="competitor">تحليل المنافسين</option>
              <option value="demand">تحليل الطلب</option>
              <option value="seasonality">تحليل الموسمية</option>
              <option value="customer">تحليل شريحة العملاء</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>الفترة الزمنية</label>
            <select v-model="testConfig.period" class="form-control">
              <option value="7days">7 أيام</option>
              <option value="30days">30 يوم</option>
              <option value="90days">90 يوم</option>
              <option value="1year">سنة</option>
            </select>
          </div>
          
          <button class="btn-primary w-100" @click="runPriceTest" :disabled="testLoading">
            <i :class="testLoading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-play'"></i>
            {{ testLoading ? 'جاري الاختبار...' : 'تشغيل الاختبار' }}
          </button>
        </div>
        
        <!-- Test Results -->
        <div v-if="testResults" class="test-results">
          <h4>نتائج الاختبار</h4>
          <div class="result-item">
            <span class="label">السعر الحالي:</span>
            <span class="value">{{ formatCurrency(testResults.currentPrice) }}</span>
          </div>
          <div class="result-item">
            <span class="label">السعر المقترح:</span>
            <span class="value recommended">{{ formatCurrency(testResults.recommendedPrice) }}</span>
          </div>
          <div class="result-item">
            <span class="label">التأثير المتوقع:</span>
            <span class="value" :class="testResults.expectedImpact > 0 ? 'positive' : 'negative'">
              {{ testResults.expectedImpact > 0 ? '+' : '' }}{{ testResults.expectedImpact }}%
            </span>
          </div>
          <div class="result-item">
            <span class="label">مستوى الثقة:</span>
            <div class="confidence-bar">
              <div class="confidence-fill" :style="{ width: testResults.confidence + '%' }"></div>
            </div>
            <span class="confidence-value">{{ testResults.confidence }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Dashboard -->
    <div class="glass-card analytics-dashboard">
      <div class="card-header">
        <h3 class="text-xl font-bold">
          <i class="fa-solid fa-chart-bar me-2"></i>
          تحليلات التسعير
        </h3>
        <div class="period-selector">
          <select v-model="analyticsPeriod" @change="loadAnalytics" class="form-control">
            <option value="7days">آخر 7 أيام</option>
            <option value="30days">آخر 30 يوم</option>
            <option value="90days">آخر 90 يوم</option>
            <option value="1year">آخر سنة</option>
          </select>
        </div>
      </div>
      
      <div class="analytics-grid">
        <!-- Price Performance Chart -->
        <div class="chart-container">
          <h4>أداء التسعير</h4>
          <canvas ref="pricePerformanceChart"></canvas>
        </div>
        
        <!-- Price Distribution -->
        <div class="chart-container">
          <h4>توزيع الأسعار</h4>
          <canvas ref="priceDistributionChart"></canvas>
        </div>
        
        <!-- Competitor Analysis -->
        <div class="chart-container">
          <h4>تحليل المنافسين</h4>
          <canvas ref="competitorAnalysisChart"></canvas>
        </div>
        
        <!-- ROI Analysis -->
        <div class="chart-container">
          <h4>تحليل العائد على الاستثمار</h4>
          <canvas ref="roiAnalysisChart"></canvas>
        </div>
      </div>
    </div>

    <!-- AI Insights -->
    <div class="glass-card ai-insights">
      <div class="card-header">
        <h3 class="text-xl font-bold">
          <i class="fa-solid fa-brain me-2"></i>
          رؤى الذكاء الاصطناعي
        </h3>
        <button class="btn-sm btn-primary" @click="generateAIInsights" :disabled="aiLoading">
          <i :class="aiLoading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync'"></i>
          تحديث الرؤى
        </button>
      </div>
      
      <div class="insights-grid">
        <div v-for="insight in aiInsights" :key="insight.id" class="insight-card">
          <div class="insight-header">
            <i :class="insight.icon"></i>
            <h4>{{ insight.title }}</h4>
            <span class="insight-type" :class="insight.type">{{ insight.typeLabel }}</span>
          </div>
          <p>{{ insight.description }}</p>
          <div class="insight-metrics">
            <div class="metric">
              <span class="metric-label">الأثر المتوقع:</span>
              <span class="metric-value" :class="insight.impact > 0 ? 'positive' : 'negative'">
                {{ insight.impact > 0 ? '+' : '' }}{{ insight.impact }}%
              </span>
            </div>
            <div class="metric">
              <span class="metric-label">الثقة:</span>
              <span class="metric-value">{{ insight.confidence }}%</span>
            </div>
          </div>
          <div class="insight-actions">
            <button class="btn-sm" @click="applyInsight(insight)">
              <i class="fa-solid fa-check me-1"></i>
              تطبيق
            </button>
            <button class="btn-sm btn-secondary" @click="dismissInsight(insight.id)">
              <i class="fa-solid fa-times me-1"></i>
              تجاهل
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <CreateRuleModal 
      v-if="showCreateRuleModal"
      @close="showCreateRuleModal = false"
      @created="handleRuleCreated"
    />
    
    <EditRuleModal
      v-if="showEditRuleModal"
      :rule="selectedRule"
      @close="showEditRuleModal = false"
      @updated="handleRuleUpdated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import PricingService from '@/services/PricingService';
import AIService from '@/services/AIService';
import ERPNextService from '@/services/ERPNextService';
import DashboardService from '@/services/DashboardService';
import CreateRuleModal from './components/CreateRuleModal.vue';
import EditRuleModal from './components/EditRuleModal.vue';

// State
const loading = ref(true);
const testLoading = ref(false);
const aiLoading = ref(false);
const showCreateRuleModal = ref(false);
const showEditRuleModal = ref(false);
const selectedRule = ref(null);
const analyticsPeriod = ref('30days');

const pricingRules = ref([]);
const availableProducts = ref([]);
const testResults = ref(null);
const aiInsights = ref([]);

const testConfig = ref({
  productId: '',
  testType: 'competitor',
  period: '30days'
});

// Charts
const pricePerformanceChart = ref(null);
const priceDistributionChart = ref(null);
const competitorAnalysisChart = ref(null);
const roiAnalysisChart = ref(null);

// Computed
const kpiData = computed(() => [
  {
    title: 'متوسط هامش الربح',
    value: '28.5%',
    icon: 'fa-solid fa-percentage',
    trend: '+2.3%',
    trendType: 'positive',
    trendIcon: 'fa-solid fa-arrow-up'
  },
  {
    title: 'دقة التسعير',
    value: '94.2%',
    icon: 'fa-solid fa-bullseye',
    trend: '+1.8%',
    trendType: 'positive',
    trendIcon: 'fa-solid fa-arrow-up'
  },
  {
    title: 'تحسين الإيرادات',
    value: '+15.7%',
    icon: 'fa-solid fa-chart-line',
    trend: '+5.2%',
    trendType: 'positive',
    trendIcon: 'fa-solid fa-arrow-up'
  },
  {
    title: 'عدد التعديلات',
    value: '1,247',
    icon: 'fa-solid fa-sync',
    trend: '-3.1%',
    trendType: 'negative',
    trendIcon: 'fa-solid fa-arrow-down'
  }
]);

// Methods
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ar-DZ', {
    style: 'currency',
    currency: 'DZD',
    minimumFractionDigits: 0
  }).format(amount);
};

const loadPricingRules = async () => {
  try {
    const rules = await PricingService.getPricingRules();
    pricingRules.value = rules;
  } catch (error) {
    console.error('Error loading pricing rules:', error);
  }
};

const loadAvailableProducts = async () => {
  try {
    const products = await DashboardService.getProducts({ limit: 100 });
    availableProducts.value = products.products || [];
  } catch (error) {
    console.error('Error loading products:', error);
  }
};

const runPriceTest = async () => {
  if (!testConfig.value.productId) {
    alert('يرجى اختيار منتج للاختبار');
    return;
  }

  try {
    testLoading.value = true;
    const results = await PricingService.runPriceTest(testConfig.value);
    testResults.value = results;
    
    console.log('Price test results:', results);
  } catch (error) {
    console.error('Error running price test:', error);
    alert('فشل في تشغيل اختبار التسعير');
  } finally {
    testLoading.value = false;
  }
};

const runPricingOptimization = async () => {
  try {
    await PricingService.optimizeAllPrices();
    await loadAnalytics();
    alert('تم تحسين جميع الأسعار بنجاح');
  } catch (error) {
    console.error('Error running pricing optimization:', error);
    alert('فشل في تحسين التسعير');
  }
};

const generateAIInsights = async () => {
  try {
    aiLoading.value = true;
    const insights = await AIService.getPricingInsights();
    aiInsights.value = insights;
    
    console.log('AI Insights:', insights);
  } catch (error) {
    console.error('Error generating AI insights:', error);
  } finally {
    aiLoading.value = false;
  }
};

const loadAnalytics = async () => {
  try {
    const analytics = await PricingService.getPricingAnalytics(null, analyticsPeriod.value);
    
    // Update charts with new data
    await nextTick();
    updateCharts(analytics);
    
    console.log('Pricing analytics loaded:', analytics);
  } catch (error) {
    console.error('Error loading analytics:', error);
  }
};

const updateCharts = (analytics) => {
  // Price Performance Chart
  if (pricePerformanceChart.value) {
    new Chart(pricePerformanceChart.value, {
      type: 'line',
      data: {
        labels: analytics.pricePerformance?.labels || [],
        datasets: [{
          label: 'الأداء',
          data: analytics.pricePerformance?.data || [],
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

  // Price Distribution Chart
  if (priceDistributionChart.value) {
    new Chart(priceDistributionChart.value, {
      type: 'doughnut',
      data: {
        labels: analytics.priceDistribution?.labels || [],
        datasets: [{
          data: analytics.priceDistribution?.data || [],
          backgroundColor: [
            '#d4af37',
            '#4caf50',
            '#ff9800',
            '#f44336',
            '#2196f3'
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

  // Competitor Analysis Chart
  if (competitorAnalysisChart.value) {
    new Chart(competitorAnalysisChart.value, {
      type: 'bar',
      data: {
        labels: analytics.competitorAnalysis?.labels || [],
        datasets: [{
          label: 'أسعارنا',
          data: analytics.competitorAnalysis?.ourPrices || [],
          backgroundColor: '#d4af37'
        }, {
          label: 'متوسط المنافسين',
          data: analytics.competitorAnalysis?.competitorPrices || [],
          backgroundColor: '#4caf50'
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

  // ROI Analysis Chart
  if (roiAnalysisChart.value) {
    new Chart(roiAnalysisChart.value, {
      type: 'line',
      data: {
        labels: analytics.roiAnalysis?.labels || [],
        datasets: [{
          label: 'العائد على الاستثمار',
          data: analytics.roiAnalysis?.data || [],
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

const editRule = (rule) => {
  selectedRule.value = rule;
  showEditRuleModal.value = true;
};

const deleteRule = async (ruleId) => {
  if (!confirm('هل أنت متأكد من حذف هذه القاعدة؟')) return;
  
  try {
    await PricingService.deletePricingRule(ruleId);
    await loadPricingRules();
    alert('تم حذف القاعدة بنجاح');
  } catch (error) {
    console.error('Error deleting rule:', error);
    alert('فشل في حذف القاعدة');
  }
};

const handleRuleCreated = async (rule) => {
  try {
    await PricingService.createPricingRule(rule);
    await loadPricingRules();
    showCreateRuleModal.value = false;
    alert('تم إنشاء القاعدة بنجاح');
  } catch (error) {
    console.error('Error creating rule:', error);
    alert('فشل في إنشاء القاعدة');
  }
};

const handleRuleUpdated = async (rule) => {
  try {
    await PricingService.updatePricingRule(rule.id, rule);
    await loadPricingRules();
    showEditRuleModal.value = false;
    alert('تم تحديث القاعدة بنجاح');
  } catch (error) {
    console.error('Error updating rule:', error);
    alert('فشل في تحديث القاعدة');
  }
};

const applyInsight = async (insight) => {
  try {
    await PricingService.applyAIInsight(insight);
    alert('تم تطبيق الرؤية بنجاح');
  } catch (error) {
    console.error('Error applying insight:', error);
    alert('فشل في تطبيق الرؤية');
  }
};

const dismissInsight = (insightId) => {
  aiInsights.value = aiInsights.value.filter(insight => insight.id !== insightId);
};

const exportPricingReport = async () => {
  try {
    const report = await PricingService.generatePricingReport();
    
    // Create download link
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pricing-report-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    // Sync with ERPNext
    await ERPNextService.syncToERPNext('pricing_reports', {
      report,
      timestamp: new Date().toISOString(),
      type: 'pricing_analysis'
    });
    
    alert('تم تصدير التقرير بنجاح');
  } catch (error) {
    console.error('Error exporting report:', error);
    alert('فشل في تصدير التقرير');
  }
};

// Lifecycle
onMounted(async () => {
  try {
    loading.value = true;
    
    // Load initial data
    await Promise.all([
      loadPricingRules(),
      loadAvailableProducts(),
      loadAnalytics(),
      generateAIInsights()
    ]);
    
    // Initialize charts
    await nextTick();
    
    // Subscribe to real-time pricing updates
    PricingService.subscribeToPriceUpdates((data) => {
      console.log('Real-time pricing update:', data);
      // Refresh analytics when prices change
      loadAnalytics();
    });
    
  } catch (error) {
    console.error('Error initializing pricing manager:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.pricing-manager {
  padding: 20px;
  min-height: 100vh;
}

.pricing-header {
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
  margin: 0;
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

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.kpi-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.kpi-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(212, 175, 55, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #d4af37;
}

.kpi-info h3 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 1.5rem;
}

.kpi-info p {
  margin: 0 0 10px 0;
  color: var(--text-dim);
}

.kpi-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9rem;
}

.kpi-trend.positive {
  color: #4caf50;
}

.kpi-trend.negative {
  color: #f44336;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.pricing-rules,
.price-testing {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-light);
}

.card-header h3 {
  margin: 0;
  color: #fff;
}

.rules-list {
  max-height: 400px;
  overflow-y: auto;
}

.rule-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  margin-bottom: 10px;
}

.rule-info h4 {
  margin: 0 0 8px 0;
  color: #fff;
}

.rule-info p {
  margin: 0 0 10px 0;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.rule-conditions {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.condition-tag {
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
}

.rule-actions {
  display: flex;
  gap: 5px;
}

.test-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #fff;
  font-weight: 500;
}

.form-control {
  padding: 10px;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-primary);
  color: #fff;
}

.test-results {
  margin-top: 20px;
  padding: 15px;
  background: rgba(76, 175, 80, 0.1);
  border-radius: 10px;
  border-left: 3px solid #4caf50;
}

.test-results h4 {
  margin: 0 0 15px 0;
  color: #fff;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.result-item .label {
  color: var(--text-dim);
}

.result-item .value {
  font-weight: 600;
  color: #fff;
}

.result-item .value.positive {
  color: #4caf50;
}

.result-item .value.negative {
  color: #f44336;
}

.result-item .value.recommended {
  color: #d4af37;
}

.confidence-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin: 0 10px;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
  border-radius: 3px;
}

.confidence-value {
  color: #d4af37;
  font-weight: 600;
  min-width: 50px;
}

.analytics-dashboard,
.ai-insights {
  background: var(--bg-card);
  border-radius: 15px;
  border: 1px solid var(--border-light);
  padding: 20px;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
}

.chart-container h4 {
  margin: 0 0 15px 0;
  color: #fff;
  text-align: center;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.insight-card {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  padding: 15px;
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.insight-header h4 {
  margin: 0;
  color: #fff;
  font-size: 1.1rem;
}

.insight-type {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.insight-type.opportunity {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.insight-type.warning {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.insight-type.risk {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.insight-card p {
  margin: 0 0 15px 0;
  color: var(--text-dim);
  line-height: 1.5;
}

.insight-metrics {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.metric-label {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.metric-value {
  font-weight: 600;
  color: #fff;
}

.insight-actions {
  display: flex;
  gap: 10px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .pricing-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
