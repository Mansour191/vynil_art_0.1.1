import { useAuthStore } from '@/store/auth';

// src/store/modules/cart.js

export default {
  namespaced: true,
  state: {
    items: (() => {
      try {
        const saved = localStorage.getItem('cart');
        return saved ? JSON.parse(saved) : [];
      } catch (e) {
        return [];
      }
    })(),
    loading: false,
    error: null,
  },
  mutations: {
    SET_ITEMS(state, items) {
      state.items = items;
      localStorage.setItem('cart', JSON.stringify(state.items));
    },
    ADD_TO_CART(state, product) {
      const existingItem = state.items.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity += product.quantity || 1;
      } else {
        state.items.push({
          ...product,
          quantity: product.quantity || 1
        });
      }
      localStorage.setItem('cart', JSON.stringify(state.items));
    },
    REMOVE_FROM_CART(state, productId) {
      state.items = state.items.filter(item => item.id !== productId);
      localStorage.setItem('cart', JSON.stringify(state.items));
    },
    UPDATE_QUANTITY(state, { productId, quantity }) {
      const item = state.items.find(item => item.id === productId);
      if (item) {
        item.quantity = Math.max(1, quantity);
        localStorage.setItem('cart', JSON.stringify(state.items));
      }
    },
    CLEAR_CART(state) {
      state.items = [];
      localStorage.removeItem('cart');
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    }
  },
  actions: {
    async fetchCart({ commit }) {
      commit('SET_LOADING', true);
      try {
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
          // محاكاة طلب API لجلب السلة من الخادم
          await new Promise(resolve => setTimeout(resolve, 500));
          // const response = await api.get('/cart');
          // commit('SET_ITEMS', response.data);
        }
      } catch (error) {
        commit('SET_ERROR', error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    addToCart({ commit }, product) {
      commit('ADD_TO_CART', product);
      
      // إرسال إشعار وتوست عند إضافة منتج للسلة
      import('@/integration/services/NotificationService').then(service => {
        service.default.success(
          'تمت الإضافة للسلة', 
          `تم إضافة ${product.name || product.title} بنجاح إلى سلة التسوق الخاصة بك.`
        );
      });

      const authStore = useAuthStore();
      if (authStore.isAuthenticated) {
        // sync with server logic
        console.log('Syncing cart addition with server...');
      }
    },
    removeFromCart({ commit }, productId) {
      commit('REMOVE_FROM_CART', productId);
      
      const authStore = useAuthStore();
      if (authStore.isAuthenticated) {
        // sync with server logic
        console.log('Syncing cart removal with server...');
      }
    },
    updateQuantity({ commit }, payload) {
      commit('UPDATE_QUANTITY', payload);
      
      const authStore = useAuthStore();
      if (authStore.isAuthenticated) {
        // sync with server logic
        console.log('Syncing quantity update with server...');
      }
    },
    clearCart({ commit }) {
      commit('CLEAR_CART');
      
      const authStore = useAuthStore();
      if (authStore.isAuthenticated) {
        // sync with server logic
        console.log('Syncing cart clear with server...');
      }
    },
    async mergeCart({ state, commit }) {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) return;
      
      commit('SET_LOADING', true);
      try {
        // محاكاة جلب السلة من الخادم
        await new Promise(resolve => setTimeout(resolve, 800));
        const serverCart = []; // هب أن السلة في الخادم فارغة حالياً للمحاكاة
        
        const localCart = state.items;
        const mergedCart = [...serverCart];

        localCart.forEach(localItem => {
          const existingItem = mergedCart.find(item => item.id === localItem.id);
          if (existingItem) {
            existingItem.quantity += localItem.quantity;
          } else {
            mergedCart.push(localItem);
          }
        });

        commit('SET_ITEMS', mergedCart);
        // بعد الدمج، نقوم بتحديث الخادم
        console.log('Cart merged and synced with server');
      } catch (error) {
        console.error('Failed to merge cart:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    }
  },
  getters: {
    cartItems: state => state.items,
    cartTotalItems: state => state.items.reduce((total, item) => total + item.quantity, 0),
    cartTotalPrice: state => state.items.reduce((total, item) => total + (item.price * item.quantity), 0),
    isCartEmpty: state => state.items.length === 0
  }
};
