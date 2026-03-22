<template>
  <div class="product-reviews mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="mb-0">{{ $t('reviews') || 'المراجعات والتقييمات' }} ({{ reviewsCount }})</h4>
      <div v-if="reviewsCount > 0" class="avg-rating d-flex align-items-center">
        <span class="h4 mb-0 me-2 text-gold">{{ averageRating }}</span>
        <div class="stars me-2">
          <i v-for="i in 5" :key="i" 
             :class="['fa-solid fa-star', { 'text-gold': i <= Math.round(averageRating), 'text-muted': i > Math.round(averageRating) }]">
          </i>
        </div>
      </div>
    </div>

    <!-- Add Review Form -->
    <div class="card shadow-sm border-0 rounded-lg mb-5 bg-light">
      <div class="card-body p-4">
        <h5 class="mb-3">{{ $t('addReview') || 'أضف مراجعتك' }}</h5>
        
        <div v-if="!isAuthenticated" class="text-center py-3">
          <p class="text-muted mb-3">{{ $t('loginToReview') || 'يجب تسجيل الدخول لإضافة تقييمك' }}</p>
          <router-link to="/login" class="btn btn-outline-gold btn-sm px-4">
            {{ $t('login') }}
          </router-link>
        </div>

        <form v-else @submit.prevent="submitReview">
          <div class="mb-3">
            <label class="form-label d-block">{{ $t('rating') || 'تقييمك' }}</label>
            <div class="rating-input h3 mb-0">
              <i v-for="i in 5" :key="i" 
                 class="fa-solid fa-star cursor-pointer transition-scale"
                 :class="i <= newReview.rating ? 'text-gold' : 'text-muted opacity-50'"
                 @click="newReview.rating = i">
              </i>
            </div>
          </div>
          <div class="mb-3">
            <textarea 
              class="form-control border-0 shadow-sm" 
              rows="3" 
              v-model="newReview.comment"
              :placeholder="$t('reviewPlaceholder') || 'اكتب رأيك في المنتج هنا...'"
              required
            ></textarea>
          </div>
          <button type="submit" class="btn btn-gold px-4" :disabled="submitting">
            <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ $t('submitReview') || 'إرسال المراجعة' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Reviews List -->
    <div class="reviews-list">
      <div v-if="reviews.length === 0" class="text-center py-5 opacity-50">
        <i class="fa-solid fa-comment-slash fa-3x mb-3"></i>
        <p>{{ $t('noReviewsYet') || 'لا توجد مراجعات لهذا المنتج بعد.' }}</p>
      </div>

      <div v-else v-for="review in reviews" :key="review.id" class="review-item mb-4 pb-4 border-bottom">
        <div class="d-flex justify-content-between mb-2">
          <div class="user-info">
            <h6 class="mb-1">{{ review.userName }}</h6>
            <div class="stars small">
              <i v-for="i in 5" :key="i" 
                 :class="['fa-solid fa-star', i <= review.rating ? 'text-gold' : 'text-muted opacity-30']">
              </i>
            </div>
          </div>
          <div class="review-meta text-end">
            <small class="text-muted d-block mb-1">{{ formatDate(review.date) }}</small>
            <button 
              v-if="!review.reported"
              class="btn btn-link btn-sm text-muted p-0 text-decoration-none" 
              @click="reportReview(review.id)"
            >
              <i class="fa-solid fa-flag me-1 small"></i> {{ $t('report') || 'إبلاغ' }}
            </button>
            <span v-else class="badge bg-light text-danger border small">
              <i class="fa-solid fa-exclamation-triangle me-1"></i> {{ $t('reported') || 'تم الإبلاغ' }}
            </span>
          </div>
        </div>
        <p class="review-comment mb-0 text-secondary">{{ review.comment }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  productId: {
    type: String,
    required: true
  }
});

const store = useStore();
const submitting = ref(false);

const newReview = ref({
  rating: 5,
  comment: ''
});

// Computed
const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
const reviews = computed(() => store.getters['reviews/getProductReviews'](props.productId));
const averageRating = computed(() => store.getters['reviews/getAverageRating'](props.productId));
const reviewsCount = computed(() => store.getters['reviews/getReviewsCount'](props.productId));

// Methods
const submitReview = async () => {
  if (!newReview.value.comment.trim()) return;
  
  submitting.value = true;
  try {
    await store.dispatch('reviews/submitReview', {
      productId: props.productId,
      rating: newReview.value.rating,
      comment: newReview.value.comment
    });
    newReview.value = { rating: 5, comment: '' };
    // محاكاة تنبيه نجاح
    console.log('✅ تم إضافة التقييم بنجاح');
  } catch (error) {
    alert(error.message);
  } finally {
    submitting.value = false;
  }
};

const reportReview = (reviewId) => {
  const reason = prompt('يرجى كتابة سبب الإبلاغ:');
  if (reason) {
    store.dispatch('reviews/reportReview', {
      productId: props.productId,
      reviewId,
      reason
    });
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ar-DZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>

<style scoped>
.text-gold {
  color: #d4af37;
}

.cursor-pointer {
  cursor: pointer;
}

.transition-scale {
  transition: transform 0.2s;
}

.transition-scale:hover {
  transform: scale(1.2);
}

.btn-gold {
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #f1d592 100%));
  color: #1a1a2e;
  font-weight: 600;
  border: none;
}

.btn-outline-gold {
  color: #d4af37;
  border: 1px solid #d4af37;
}

.btn-outline-gold:hover {
  background: var(--gold-gradient);
  color: #1a1a2e;
}

.review-item:last-child {
  border-bottom: none !important;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
