<template>
  <div class="creative-voting p-6">
    <header class="mb-8">
      <h1 class="text-3xl font-bold gold-text mb-2">التصويت الإبداعي | Creative Voting</h1>
      <p class="text-dim">شارك في تشكيل مستقبل 'Paclos' من خلال التصويت على التصاميم القادمة</p>
    </header>

    <div class="designs-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div 
        v-for="design in investorStore.draftDesigns" 
        :key="design.id" 
        class="glass-card design-card overflow-hidden"
      >
        <div class="design-image-container relative">
          <img :src="design.image" :alt="design.title" class="design-image w-full h-64 object-cover" />
          <div class="vote-overlay absolute top-4 right-4 bg-black/60 backdrop-blur px-4 py-2 rounded-full border border-gold">
            <span class="gold-text font-bold"><i class="fa-solid fa-vote-yea mr-2"></i> {{ design.votes }} صوت</span>
          </div>
        </div>
        
        <div class="p-6">
          <h3 class="text-xl font-bold gold-text mb-3">{{ design.title }}</h3>
          <p class="text-dim text-sm mb-6 line-clamp-2">{{ design.description }}</p>
          
          <button 
            class="w-full vote-btn"
            :disabled="investorStore.votedDesignIds.includes(design.id)"
            @click="investorStore.voteForDesign(design.id)"
          >
            <span v-if="investorStore.votedDesignIds.includes(design.id)">
              <i class="fa-solid fa-check mr-2"></i> تم التصويت
            </span>
            <span v-else>
              <i class="fa-solid fa-plus mr-2"></i> تصويت لهذا التصميم
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Future Design Goal Section -->
    <section class="mt-12 glass-card p-8 text-center border-gold">
      <h2 class="text-2xl font-bold gold-text mb-4">هدفنا القادم: 50 تصميماً ملكياً</h2>
      <div class="max-w-2xl mx-auto">
        <div class="catalog-progress-large mb-4">
          <div class="progress-track bg-white/10 h-4 rounded-full overflow-hidden">
            <div 
              class="progress-fill-gold h-full" 
              :style="{ width: (investorStore.kpis.catalogProgress / 50 * 100) + '%' }"
            ></div>
          </div>
        </div>
        <p class="text-dim">تم إنجاز {{ investorStore.kpis.catalogProgress }} من أصل 50 تصميماً مستهدفاً للكتالوج الأساسي</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useInvestorStore } from '@/store/investor';

const investorStore = useInvestorStore();
</script>

<style scoped>
.creative-voting {
  color: white;
}

.gold-text { color: #d4af37; }
.border-gold { border-color: #d4af37; }
.text-dim { color: #adb5bd; }

.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
}

.design-card {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.design-card:hover {
  transform: translateY(-10px);
  border-color: #d4af37;
  box-shadow: 0 15px 35px rgba(212, 175, 55, 0.2);
}

.design-image {
  transition: transform 0.6s ease;
}

.design-card:hover .design-image {
  transform: scale(1.1);
}

.vote-btn {
  background: linear-gradient(135deg, #d4af37 0%, #f1c40f 100%);
  color: #000;
  padding: 12px;
  border-radius: 12px;
  font-weight: 800;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.vote-btn:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
}

.vote-btn:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: #adb5bd;
  cursor: not-allowed;
}

.progress-fill-gold {
  background: linear-gradient(90deg, #d4af37, #f1c40f);
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
}

.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
@media (min-width: 768px) { .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.gap-8 { gap: 2rem; }
.relative { position: relative; }
.absolute { position: absolute; }
.top-4 { top: 1rem; }
.right-4 { right: 1rem; }
.rounded-full { border-radius: 9999px; }
.w-full { width: 100%; }
.h-64 { height: 16rem; }
.object-cover { object-fit: cover; }
</style>
