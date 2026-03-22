// src\views\dashboard\forecasting\components\ForecastChart.vue
<template>
  <div class="forecast-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'ForecastChart',
  props: {
    data: {
      type: Array,
      default: () => [],
    },
    predictions: {
      type: Array,
      default: () => [],
    },
    historical: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  watch: {
    data: {
      handler() {
        this.$nextTick(() => {
          this.initChart();
        });
      },
      deep: true,
    },
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
  methods: {
    initChart() {
      if (!this.$refs.chartCanvas) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = this.$refs.chartCanvas.getContext('2d');

      // تجهيز البيانات
      const labels = this.generateLabels();
      const historicalData = this.historical.length
        ? this.historical
        : this.generateMockHistorical();
      const predictionData = this.predictions.length
        ? this.predictions
        : this.generateMockPredictions();

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'المبيعات الفعلية',
              data: historicalData,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              borderWidth: 2,
              pointBackgroundColor: '#2196F3',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              tension: 0.4,
              fill: true,
            },
            {
              label: 'التوقعات',
              data: predictionData,
              borderColor: '#d4af37',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              borderWidth: 2,
              borderDash: [5, 5],
              pointBackgroundColor: '#d4af37',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              backgroundColor: 'rgba(26, 26, 46, 0.9)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#d4af37',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                label: (context) => {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  label += new Intl.NumberFormat('ar-SA', {
                    style: 'currency',
                    currency: 'SAR',
                    minimumFractionDigits: 0,
                  }).format(context.raw);
                  return label;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(255, 255, 255, 0.1)',
                drawBorder: false,
              },
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)',
                callback: (value) => {
                  return new Intl.NumberFormat('ar-SA', {
                    style: 'currency',
                    currency: 'SAR',
                    minimumFractionDigits: 0,
                    notation: 'compact',
                  }).format(value);
                },
              },
            },
            x: {
              grid: {
                display: false,
              },
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)',
                maxRotation: 45,
                minRotation: 45,
              },
            },
          },
          elements: {
            line: {
              tension: 0.4,
            },
          },
          animations: {
            tension: {
              duration: 1000,
              easing: 'linear',
              from: 0.8,
              to: 0.4,
              loop: false,
            },
          },
        },
      });
    },

    generateLabels() {
      const labels = [];
      const totalDays = Math.max(this.historical.length, this.predictions.length, 30);

      for (let i = 1; i <= totalDays; i++) {
        if (i === 1) {
          labels.push('اليوم 1');
        } else if (i === totalDays) {
          labels.push(`اليوم ${i}`);
        } else if (i % 5 === 0) {
          labels.push(`يوم ${i}`);
        } else {
          labels.push('');
        }
      }

      return labels;
    },

    generateMockHistorical() {
      return Array(30)
        .fill(0)
        .map(() => Math.floor(Math.random() * 800 + 400));
    },

    generateMockPredictions() {
      return Array(30)
        .fill(0)
        .map((_, i) => Math.floor(Math.random() * 600 + 500 + i * 10));
    },
  },
};
</script>

<style scoped>
.forecast-chart {
  width: 100%;
  height: 100%;
  min-height: 300px;
  position: relative;
}
</style>
