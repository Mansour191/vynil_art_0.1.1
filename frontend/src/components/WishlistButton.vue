<template>
  <button
    class="wishlist-btn"
    :class="{ active: isInWishlist }"
    @click="toggleWishlist"
    :title="$t(isInWishlist ? 'removeFromWishlist' : 'addToWishlist')"
  >
    <i :class="isInWishlist ? 'fa-solid fa-heart' : 'far fa-heart'"></i>
    <span v-if="showText">{{ $t(isInWishlist ? 'removeFromWishlist' : 'addToWishlist') }}</span>
  </button>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'WishlistButton',
  props: {
    item: {
      type: Object,
      required: true,
    },
    showText: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters('user', ['isInWishlist']),
  },
  methods: {
    ...mapActions('user', ['addToWishlist', 'removeFromWishlist']),

    toggleWishlist() {
      if (this.isInWishlist(this.item.id)) {
        this.removeFromWishlist(this.item.id);
        this.showNotification('removed');
      } else {
        this.addToWishlist(this.item);
        this.showNotification('added');
      }
    },

    showNotification(action) {
      // إشعار للمستخدم
      const message =
        action === 'added' ? this.$t('itemAddedToWishlist') : this.$t('itemRemovedFromWishlist');

      // يمكنك استخدام Vuex لإضافة إشعار
      this.$store.dispatch('user/addNotification', {
        type: action === 'added' ? 'success' : 'info',
        title: this.$t('wishlist'),
        message: `${message}: ${this.item.title}`,
        icon: action === 'added' ? 'fa-solid fa-heart' : 'fa-solid fa-heart-broken',
      });
    },
  },
};
</script>

<style scoped>
.wishlist-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 30px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.wishlist-btn i {
  color: var(--gold-primary);
  transition: all 0.3s;
}

.wishlist-btn:hover {
  border-color: var(--gold-primary);
  transform: translateY(-2px);
}

.wishlist-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.wishlist-btn.active i {
  color: var(--bg-deep);
}

.wishlist-btn:active {
  transform: scale(0.95);
}
</style>
