<template>
  <div class="investor-ai-insights">
    <header class="ai-header mb-8">
      <div class="header-content">
        <h1 class="text-4xl font-bold gold-text">تحليلات الذكاء الاصطناعي</h1>
        <p class="text-dim">رؤى استراتيجية مبنية على تعلم الآلة والنمذجة التنبؤية</p>
      </div>
      <div class="ai-status">
        <span class="pulse"></span>
        <span>النظام متصل | معالجة البيانات الحية</span>
      </div>
    </header>

    <!-- AI Prediction Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
      <div class="glass-card ai-card prediction">
        <div class="ai-icon-wrapper">
          <i class="fa-solid fa-chart-line"></i>
          <div class="icon-glow"></div>
        </div>
        <div class="ai-info">
          <span class="label">توقعات النمو الاستراتيجي</span>
          <h3 class="value">+{{ aiStats.growthPrediction }}%</h3>
          <p class="desc">تحليل خوارزمي للاتجاهات المستقبلية</p>
        </div>
      </div>

      <div class="glass-card ai-card risk">
        <div class="ai-icon-wrapper">
          <i class="fa-solid fa-user-shield"></i>
          <div class="icon-glow"></div>
        </div>
        <div class="ai-info">
          <span class="label">مؤشر أمان الاستثمار</span>
          <h3 class="value">{{ 100 - aiStats.riskScore }}/100</h3>
          <p class="desc">تقييم المخاطر التشغيلية والمالية</p>
        </div>
      </div>

      <div class="glass-card ai-card roi">
        <div class="ai-icon-wrapper">
          <i class="fa-solid fa-gem"></i>
          <div class="icon-glow"></div>
        </div>
        <div class="ai-info">
          <span class="label">العائد السنوي المتوقع (ROI)</span>
          <h3 class="value">{{ aiStats.expectedROI }}%</h3>
          <p class="desc">تقدير الأرباح بناءً على كفاءة الأصول</p>
        </div>
      </div>
    </div>

    <!-- AI Detailed Analysis -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-10">
      <div class="glass-card analysis-panel p-8">
        <h3 class="text-2xl font-bold gold-text mb-6"><i class="fa-solid fa-vials"></i> محاكي السيناريوهات الذكي</h3>
        <div class="simulator-controls mb-8">
          <div class="control-item">
            <label>زيادة ميزانية التسويق (%)</label>
            <input type="range" v-model="simParams.marketing" min="0" max="100" />
            <span class="val">{{ simParams.marketing }}%</span>
          </div>
          <div class="control-item">
            <label>تعديل السعر (%)</label>
            <input type="range" v-model="simParams.prices" min="-20" max="20" />
            <span class="val">{{ simParams.prices }}%</span>
          </div>
          <div class="control-item checkbox">
            <input type="checkbox" v-model="simParams.newBranch" id="newBranch" />
            <label for="newBranch">افتتاح فرع جديد في ولاية كبرى</label>
          </div>
        </div>

        <div class="simulation-result p-6 rounded-xl bg-dark border-gold">
          <div class="res-grid">
            <div class="res-item">
              <span class="label">النمو المتوقع</span>
              <span class="val green-text">{{ simResult.projectedGrowth }}%</span>
            </div>
            <div class="res-item">
              <span class="label">إجمالي العائد</span>
              <span class="val gold-text">{{ simResult.estimatedRevenue }} دج</span>
            </div>
            <div class="res-item">
              <span class="label">تأثير المخاطر</span>
              <span class="val" :class="simResult.riskImpact === 'عالي' ? 'red-text' : 'yellow-text'">{{ simResult.riskImpact }}</span>
            </div>
          </div>
          <div class="confidence-bar mt-4">
            <div class="flex justify-between text-xs mb-1">
              <span>نسبة الثقة في التوقعات</span>
              <span>{{ simResult.confidenceScore }}%</span>
            </div>
            <div class="progress-bar mini">
              <div class="progress-fill green" :style="{ width: simResult.confidenceScore + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card analysis-panel p-8">
        <h3 class="text-2xl font-bold gold-text mb-6"><i class="fa-solid fa-trophy"></i> الجدارة الاستثمارية للأصول</h3>
        <div class="asset-list">
          <div v-for="asset in assetPerformance" :key="asset.category" class="asset-item mb-4 p-4 rounded-lg bg-dark border-light">
            <div class="flex justify-between items-center mb-2">
              <span class="font-bold">{{ asset.category }}</span>
              <span class="roi-badge"><i class="fa-solid fa-arrow-up text-xs mr-1"></i> {{ asset.roi }}% ROI</span>
            </div>
            <div class="flex gap-4 text-xs text-dim">
              <span><i class="fa-solid fa-sync-alt"></i> الدوران: {{ asset.turnOver }}</span>
              <span><i class="fa-solid fa-shield-virus"></i> مخاطر المخزون: {{ asset.inventoryRisk }}</span>
            </div>
          </div>
        </div>
        <div class="strategic-recommendation mt-6">
          <h4 class="font-bold mb-4"><i class="fa-solid fa-bolt gold-text"></i> توصية استراتيجية (AI Recommended):</h4>
          <p class="bg-dark p-4 rounded-lg border-gold">
            {{ strategicRecommendation }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-10">
      <div class="glass-card analysis-panel p-8">
        <h3 class="text-2xl font-bold gold-text mb-6"><i class="fa-solid fa-satellite-dish"></i> فرص السوق الضائعة (Untapped Markets)</h3>
        <div class="market-list">
          <div v-for="market in untappedMarkets" :key="market.region" class="market-item mb-4 p-5 rounded-xl bg-dark border-gold flex items-center gap-6">
            <div class="market-score">
              <svg class="progress-circle" viewBox="0 0 36 36">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path class="circle" :stroke-dasharray="market.score + ', 100'" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <text x="18" y="20.35" class="percentage">{{ market.score }}%</text>
              </svg>
            </div>
            <div class="market-info">
              <h4 class="font-bold text-lg mb-1">{{ market.region }}</h4>
              <p class="text-xs text-dim"><i class="fa-solid fa-info-circle mr-1"></i> {{ market.reason }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card analysis-panel p-8">
        <h3 class="text-2xl font-bold gold-text mb-6"><i class="fa-solid fa-user-tie"></i> تحليل القيمة الحياتية للعملاء (Strategic CLV)</h3>
        <div class="clv-insights mt-4">
          <div v-for="clv in clvInsights" :key="clv.segment" class="clv-item mb-6">
            <div class="flex justify-between items-center mb-2">
              <span class="segment-name font-bold">{{ clv.segment }}</span>
              <span class="clv-value gold-text">{{ clv.avgClv.toLocaleString() }} دج <i class="fa-solid fa-coins text-xs ml-1"></i></span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: clv.potential + '%' }"></div>
            </div>
            <div class="flex justify-between text-xs text-dim mt-2">
              <span><i class="fa-solid fa-expand-alt mr-1"></i> إمكانية التوسع: {{ clv.potential }}%</span>
              <span :class="clv.trend === 'up' ? 'green-text' : 'red-text'">
                <i :class="clv.trend === 'up' ? 'fa-solid fa-chart-line' : 'fa-solid fa-arrow-down'"></i>
                {{ clv.trend === 'up' ? 'نمو مستمر' : 'انخفاض طفيف' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { Line } from 'vue-chartjs';
import AIService from '@/services/AIService';
import ERPNextService from '@/services/ERPNextService';
import DashboardService from '@/services/DashboardService';

const loading = ref(true);
const error = ref(null);
const aiStats = ref({
  growthPrediction: 0,
  riskScore: 15,
  expectedROI: 0,
  marketSentiment: 0,
  competitorAnalysis: {},
  demandForecast: []
});

const marketTrends = ref([]);
const customerInsights = ref({});
const recommendations = ref([]);

// Methods
const fetchAIInsights = async () => {
  try {
    loading.value = true;
    error.value = null;

    // Fetch AI insights from backend
    const [
      salesForecast,
      marketTrendData,
      customerData,
      productRecommendations,
      demandPrediction
    ] = await Promise.all([
      AIService.getSalesForecast('90days'),
      AIService.getMarketTrends(),
      AIService.getCustomerInsights(),
      AIService.getProductRecommendations(),
      AIService.predictDemand()
    ]);

    // Update AI stats with real data
    aiStats.value = {
      growthPrediction: salesForecast.growthRate || 0,
      riskScore: salesForecast.riskAssessment?.score || 15,
      expectedROI: salesForecast.expectedROI || 0,
      marketSentiment: marketTrendData.sentiment || 0,
      competitorAnalysis: marketTrendData.competitorAnalysis || {},
      demandForecast: demandPrediction.demand || []
    };

    marketTrends.value = marketTrendData.trends || [];
    customerInsights.value = customerData;
    recommendations.value = productRecommendations;

    console.log('AI Insights loaded:', {
      salesForecast,
      marketTrendData,
      customerData,
      productRecommendations,
      demandPrediction
    });

  } catch (err) {
    console.error('Error fetching AI insights:', err);
    error.value = 'فشل في تحميل بيانات الذكاء الاصطناعي';
    
    // Fallback to mock data if backend fails
    aiStats.value = {
      growthPrediction: 23.5,
      riskScore: 15,
      expectedROI: 28.3,
      marketSentiment: 0.75,
      competitorAnalysis: {
        topCompetitors: ['منافس 1', 'منافس 2'],
        marketShare: 12.5
      },
      demandForecast: [
        { month: 'يناير', demand: 1200 },
        { month: 'فبراير', demand: 1350 },
        { month: 'مارس', demand: 1100 }
      ]
    };
  } finally {
    loading.value = false;
  }
};

const generateAIReport = async () => {
  try {
    const report = await AIService.analyzeCustomerFeedback('overall_performance');
    console.log('AI Report generated:', report);
    
    // Sync report with ERPNext
    await ERPNextService.syncToERPNext('ai_reports', {
      report,
      timestamp: new Date().toISOString(),
      type: 'performance_analysis'
    });
  } catch (err) {
    console.error('Error generating AI report:', err);
  }
};

const optimizeInventory = async () => {
  try {
    const optimization = await AIService.getInventoryOptimization();
    console.log('Inventory optimization:', optimization);
    
    // Apply optimization recommendations
    for (const item of optimization.recommendations) {
      await DashboardService.updateProduct(item.productId, {
        stock_level: item.recommendedStock,
        reorder_point: item.reorderPoint
      });
    }
  } catch (err) {
    console.error('Error optimizing inventory:', err);
  }
};

const analyzeSentiment = async (feedback) => {
  try {
    const analysis = await AIService.analyzeCustomerFeedback(feedback);
    return analysis;
  } catch (err) {
    console.error('Error analyzing sentiment:', err);
    return null;
  }
};

const getPricingRecommendations = async (productId) => {
  try {
    const recommendations = await AIService.getPricingRecommendations(productId);
    return recommendations;
  } catch (err) {
    console.error('Error getting pricing recommendations:', err);
    return null;
  }
};

// Computed
const riskLevel = computed(() => {
  const score = aiStats.value.riskScore;
  if (score <= 20) return 'منخفض';
  if (score <= 40) return 'متوسط';
  if (score <= 60) return 'مرتفع';
  return 'عالي';
});

const riskColor = computed(() => {
  const score = aiStats.value.riskScore;
  if (score <= 20) return '#4CAF50';
  if (score <= 40) return '#FF9800';
  if (score <= 60) return '#F44336';
  return '#D32F2F';
});

const roiLevel = computed(() => {
  const roi = aiStats.value.expectedROI;
  if (roi >= 30) return 'ممتاز';
  if (roi >= 20) return 'جيد';
  if (roi >= 10) return 'متوسط';
  return 'ضعيف';
});

// Lifecycle
onMounted(() => {
  fetchAIInsights();
  
  // Refresh AI data every 5 minutes
  setInterval(fetchAIInsights, 300000);
});
import {
  Chart as ChartJS,
  Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler);

// State
const simParams = ref({
  marketing: 10,
  prices: 0,
  newBranch: false
});

const assetPerformance = ref([]);
const untappedMarkets = ref([]);
const clvInsights = ref([]);

// Simulation Logic
const simResult = computed(() => {
  return InvestorAIService.simulateScenario({
    marketingIncrease: simParams.value.marketing,
    priceAdjustment: simParams.value.prices,
    newBranchOpening: simParams.value.newBranch
  });
});

const strategicRecommendation = computed(() => {
  if (simParams.value.newBranch) {
    return "افتتاح فرع جديد سيزيد من حصتك السوقية بنسبة كبيرة، لكن تأكد من توفير سيولة كافية لتغطية التكاليف التشغيلية في أول 6 أشهر.";
  }
  return "نقترح زيادة ميزانية البحث والتطوير (R&D) بنسبة 5% للتركيز على 'الرخام الذكي'، حيث يتوقع الذكاء الاصطناعي أن يكون هذا الاتجاه هو الرائد في عام 2026.";
});

const loadAIData = async () => {
  assetPerformance.value = await InvestorAIService.getAssetPerformance();
  untappedMarkets.value = await InvestorAIService.getMarketOpportunities();
  clvInsights.value = await InvestorAIService.calculateCLVInsights();
};

onMounted(() => {
  loadAIData();
});

const forecastChartData = {
  labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
  datasets: [
    {
      label: 'الأداء الفعلي',
      data: [30, 45, 42, 60, 75, 90],
      borderColor: '#d4af37',
      backgroundColor: 'rgba(212, 175, 55, 0.1)',
      fill: true,
      tension: 0.4
    },
    {
      label: 'توقعات الذكاء الاصطناعي',
      data: [90, 110, 125, 140, 160, 185],
      borderColor: '#2ecc71',
      borderDash: [5, 5],
      backgroundColor: 'transparent',
      tension: 0.4
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: '#ffffff' } } },
  scales: {
    y: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.1)' } },
    x: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.1)' } }
  }
};
</script>

<style scoped>
.investor-ai-insights {
  color: white;
  animation: fadeIn 0.5s ease;
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-status {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
}

.pulse {
  width: 10px;
  height: 10px;
  background: #2ecc71;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
}

.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  transition: all 0.3s ease;
}

.ai-card {
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.ai-card:hover {
  transform: translateY(-5px);
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.05);
}

.ai-icon-wrapper {
  width: 65px;
  height: 65px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.05));
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: #d4af37;
  position: relative;
  border: 1px solid rgba(212, 175, 55, 0.2);
  transition: all 0.3s ease;
}

.ai-card:hover .ai-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
  background: var(--gold-gradient);
  color: #000;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.4), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.ai-card:hover .icon-glow {
  opacity: 1;
}

.ai-info .label {
  display: block;
  font-size: 0.85rem;
  color: #adb5bd;
  margin-bottom: 5px;
}

.ai-info .value {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.ai-info .desc {
  font-size: 0.75rem;
  color: #6c757d;
}

/* Simulator Styles */
.simulator-controls {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.control-item label {
  font-size: 0.9rem;
  color: #adb5bd;
}

.control-item input[type="range"] {
  accent-color: #d4af37;
}

.control-item .val {
  align-self: flex-end;
  color: #d4af37;
  font-weight: bold;
}

.control-item.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.res-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  text-align: center;
}

.res-item .label {
  display: block;
  font-size: 0.75rem;
  color: #adb5bd;
  margin-bottom: 5px;
}

.res-item .val {
  font-weight: bold;
  font-size: 1.1rem;
}

/* Asset Styles */
.roi-badge {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 0.8rem;
}

/* Market Score Styles */
.market-score {
  width: 60px;
}

.progress-circle {
  width: 100%;
}

.circle-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.05);
  stroke-width: 3.8;
}

.circle {
  fill: none;
  stroke: #d4af37;
  stroke-width: 2.8;
  stroke-linecap: round;
  transition: stroke-dasharray 0.3s ease;
}

.percentage {
  fill: white;
  font-size: 0.5rem;
  text-anchor: middle;
  font-weight: bold;
}

/* Colors */
.green-text { color: #2ecc71; }
.red-text { color: #e74c3c; }
.yellow-text { color: #f1c40f; }

.chart-placeholder {
  height: 300px;
}

.insight-item {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
}

.segmentation-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.segment-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-bar {
  height: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f39c12);
}

.border-gold {
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.bg-dark {
  background: rgba(0, 0, 0, 0.2);
}

.gold-text { color: #d4af37; }
.text-dim { color: #adb5bd; }
</style>
