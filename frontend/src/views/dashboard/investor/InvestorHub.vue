<template>
  <div class="investor-hub p-6">
    <header class="hub-header mb-8 text-center">
      <h1 class="text-4xl font-bold gold-text mb-2">ركن الممولين | Paclos Hub</h1>
      <p class="text-dim">مؤشرات الأداء الحية والنمو الاستراتيجي للمشروع</p>
    </header>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div v-for="(val, key) in kpiCards" :key="key" class="glass-card kpi-card">
        <div class="kpi-icon mb-4">
          <i :class="val.icon"></i>
        </div>
        <div class="kpi-info">
          <span class="text-dim text-sm block mb-1">{{ $t(key) }}</span>
          <h3 class="text-2xl font-bold">{{ val.prefix }}{{ val.value }}{{ val.suffix }}</h3>
          <div class="progress-bar mt-2" v-if="val.target">
            <div class="progress-fill" :style="{ width: (val.value / val.target * 100) + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Sales Growth Chart -->
      <div class="glass-card chart-container p-6">
        <h3 class="text-xl font-bold gold-text mb-6">نمو المبيعات الشهرية</h3>
        <Line :data="salesChartData" :options="chartOptions" />
      </div>

      <!-- Regional Distribution Map -->
      <div class="glass-card map-container p-6">
        <h3 class="text-xl font-bold gold-text mb-6">التوزيع الجغرافي للمبيعات (خريطة الجزائر)</h3>
        <div id="map" class="algeria-map"></div>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-8">
      <!-- Regional Bar Chart -->
      <div class="glass-card chart-container p-6">
        <h3 class="text-xl font-bold gold-text mb-6">تحليل الولايات بالأرقام</h3>
        <Bar :data="regionalChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useInvestorStore } from '@/store/investor';
import { Line, Bar } from 'vue-chartjs';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import DashboardService from '@/services/DashboardService';
import AIService from '@/services/AIService';
import ERPNextService from '@/services/ERPNextService';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler
} from 'chart.js';

ChartJS.register(
  Title, Tooltip, Legend, LineElement, BarElement, 
  CategoryScale, LinearScale, PointElement, Filler
);

const investorStore = useInvestorStore();
const map = ref(null);
const loading = ref(true);
const error = ref(null);

const wilayaCoords = {
  'الجزائر': [36.7538, 3.0588],
  'وهران': [35.6971, -0.6308],
  'قسنطينة': [36.3650, 6.6147],
  'سطيف': [36.1911, 5.4133],
  'عنابة': [36.9000, 7.7667],
  'تلمسان': [34.8817, -1.3167],
  'بجاية': [36.7511, 5.0567],
  'تيزي وزو': [36.7119, 4.0458],
  'ورقلة': [31.9492, 5.3250],
  'بشار': [31.6167, -2.2167],
};

// Methods
const fetchInvestorData = async () => {
  try {
    loading.value = true;
    error.value = null;

    // Use GraphQL API instead of multiple services
    const { default: GraphQLService } = await import('@/services/GraphQLService');
    const graphQLService = new GraphQLService();

    // Fetch real investor data from backend
    const [
      dashboardStats,
      salesForecast,
      marketTrends,
      customerInsights
    ] = await Promise.all([
        graphQLService.getDashboardStats('monthly'),
        graphQLService.getSalesForecasts(),
        graphQLService.getRegionalAnalytics(),
        graphQLService.getInvestorMetrics('monthly')
      ]);

    // Update investor store with real data
    investorStore.updateKPIs({
      totalRevenue: dashboardStats[0]?.totalSales || 0,
      catalogProgress: 35, // This should come from a separate API
      salesGrowth: salesForecast[0]?.confidenceScore * 100 || 0,
      activeInvestors: customerInsights[0]?.uniqueCustomers || 0
    });

    investorStore.updateRegionalStats(marketTrends.map(trend => ({
      state: trend.wilaya,
      value: trend.totalSales
    })));

    investorStore.updateSalesData(salesForecast.map(forecast => ({
      month: forecast.forecastDate,
      sales: forecast.predictedSales
    })));

    console.log('Investor data loaded successfully:', {
      dashboardStats,
      salesForecast,
      marketTrends,
      customerInsights
    });

  } catch (err) {
    console.error('Error fetching investor data:', err);
    error.value = 'فشل في تحميل بيانات الممول';
    
    // Fallback to mock data if backend fails
    investorStore.updateKPIs({
      totalRevenue: 1250000,
      catalogProgress: 35,
      salesGrowth: 18.5,
      activeInvestors: 47
    });
  } finally {
    loading.value = false;
  }
};

const syncWithERPNext = async () => {
  try {
    await ERPNextService.startRealTimeSync();
    
    // Sync investor data
    await ERPNextService.migrateFinancialData('investor_data', 'last_30_days');
    
    console.log('ERPNext sync started successfully');
  } catch (err) {
    console.error('Error syncing with ERPNext:', err);
  }
};

const getAIRecommendations = async () => {
  try {
    const recommendations = await AIService.getProductRecommendations();
    console.log('AI Recommendations:', recommendations);
    return recommendations;
  } catch (err) {
    console.error('Error getting AI recommendations:', err);
    return [];
  }
};

const initMap = () => {
  // إزالة الخريطة إذا كانت موجودة (لمنع التكرار في HMR)
  if (map.value) {
    map.value.remove();
  }

  // تهيئة الخريطة بمركز الجزائر
  map.value = L.map('map', {
    center: [32.0, 3.0], // مركز تقريبي للجزائر
    zoom: 5,
    zoomControl: false,
    scrollWheelZoom: false
  });

  // إضافة طبقة الخريطة (نمط داكن ليناسب واجهة الممولين)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
  }).addTo(map.value);

  // إضافة علامات الولايات مع بيانات المبيعات
  investorStore.regionalStats.forEach(stat => {
    const coords = wilayaCoords[stat.state];
    if (coords) {
      const radius = Math.sqrt(stat.value) * 1.5; // حجم الدائرة يتناسب مع المبيعات
      
      const circle = L.circle(coords, {
        color: '#d4af37',
        fillColor: '#d4af37',
        fillOpacity: 0.6,
        radius: radius * 1000 // تحويل للتمثيل على الخريطة
      }).addTo(map.value);

      circle.bindPopup(`
        <div class="map-popup">
          <h4 style="color: #d4af37; margin-bottom: 5px;">${stat.state}</h4>
          <p style="margin: 0; font-weight: bold;">المبيعات: ${stat.value} طلب</p>
        </div>
      `);
    }
  });
};

// Lifecycle
onMounted(async () => {
  await fetchInvestorData();
  initMap();
  
  // Start periodic data refresh
  setInterval(fetchInvestorData, 60000); // Refresh every minute
  
  // Get AI recommendations
  getAIRecommendations();
  
  // Check ERPNext sync status
  try {
    const syncStatus = await ERPNextService.getRealTimeSyncStatus();
    if (!syncStatus.isActive) {
      await syncWithERPNext();
    }
  } catch (err) {
    console.error('Error checking ERPNext sync status:', err);
  }
});

const kpiCards = computed(() => ({
  totalRevenue: { value: investorStore.kpis.totalRevenue.toLocaleString(), prefix: 'دج ', icon: 'fa-solid fa-sack-dollar' },
  catalogProgress: { value: investorStore.kpis.catalogProgress, target: 50, suffix: ' / 50', icon: 'fa-solid fa-diagram-project' },
  salesGrowth: { value: investorStore.kpis.salesGrowth, suffix: '%', icon: 'fa-solid fa-arrow-trend-up' },
  activeInvestors: { value: investorStore.kpis.activeInvestors, icon: 'fa-solid fa-users-viewfinder' }
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: '#ffffff' } }
  },
  scales: {
    y: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.1)' } },
    x: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.1)' } }
  }
};

const salesChartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [{
    label: 'المبيعات',
    data: [30, 45, 42, 60, 75, 90],
    borderColor: '#d4af37',
    backgroundColor: 'rgba(212, 175, 55, 0.1)',
    fill: true,
    tension: 0.4
  }]
};

const regionalChartData = computed(() => ({
  labels: investorStore.regionalStats.map(s => s.state),
  datasets: [{
    label: 'عدد الطلبات',
    data: investorStore.regionalStats.map(s => s.value),
    backgroundColor: '#d4af37'
  }]
}));
</script>

<style scoped>
.investor-hub {
  color: white;
}

.gold-text {
  color: #d4af37;
}

.text-dim {
  color: #adb5bd;
}

.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  transition: transform 0.3s ease;
}

.glass-card:hover {
  transform: translateY(-5px);
  border-color: #d4af37;
}

.kpi-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.kpi-icon {
  font-size: 1.5rem;
  color: #d4af37;
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f1c40f);
  border-radius: 3px;
}

.chart-container {
  height: 400px;
}

.map-container {
  height: 400px;
}

.algeria-map {
  height: 300px;
  width: 100%;
  border-radius: 15px;
  background: rgba(0, 0, 0, 0.2);
}

:deep(.leaflet-popup-content-wrapper) {
  background: #1a1a1a;
  color: white;
  border: 1px solid #d4af37;
}

:deep(.leaflet-popup-tip) {
  background: #d4af37;
}

/* Tailwind-like utilities if not available */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
@media (min-width: 768px) { .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .lg\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.gap-6 { gap: 1.5rem; }
.gap-8 { gap: 2rem; }
.p-6 { padding: 1.5rem; }
.mb-8 { margin-bottom: 2rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 1rem; }
.text-2xl { font-size: 1.5rem; }
.text-4xl { font-size: 2.25rem; }
.font-bold { font-weight: 700; }
</style>
