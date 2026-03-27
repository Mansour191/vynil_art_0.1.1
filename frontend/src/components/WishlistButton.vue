<template>
  <v-btn
    :icon="isInWishlist ? 'mdi-heart' : 'mdi-heart-outline'"
    :variant="isInWishlist ? 'elevated' : 'outlined'"
    :color="isInWishlist ? 'primary' : 'default'"
    @click="toggleWishlist"
    :title="$t(isInWishlist ? 'removeFromWishlist' : 'addToWishlist')"
    class="wishlist-btn"
  >
    <span v-if="showText">{{ $t(isInWishlist ? 'removeFromWishlist' : 'addToWishlist') }}</span>
  </v-btn>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  showText: {
    type: Boolean,
    default: false,
  },
});

const store = useStore();
const { t } = useI18n();

const isInWishlist = computed(() => {
  return store.getters['user/isInWishlist'](props.item.id);
});

const toggleWishlist = () => {
  if (isInWishlist.value) {
    store.dispatch('user/removeFromWishlist', props.item.id);
    showNotification('removed');
  } else {
    store.dispatch('user/addToWishlist', props.item);
    showNotification('added');
  }
};

const showNotification = (action) => {
  // إشعار للمستخدم
  const message = action === 'added' ? t('itemAddedToWishlist') : t('itemRemovedFromWishlist');
  
  // يمكنك استخدام Vuex لإضافة إشعار
  store.dispatch('user/addNotification', {
    type: action === 'added' ? 'success' : 'info',
    title: t('wishlist'),
    message: `${message}: ${props.item.title}`,
    icon: action === 'added' ? 'mdi-heart' : 'mdi-heart-broken',
  });
};
</script>

