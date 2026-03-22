import { defineStore } from 'pinia';
import { DRF_LOGIN_MUTATION, DRF_REGISTER_MUTATION, DRF_CHANGE_PASSWORD_MUTATION, DRF_UPDATE_PROFILE_MUTATION, DRF_ME_QUERY, graphqlMutation, graphqlQuery } from '@/integration/services/graphql';
import DRFAuthService from '@/integration/services/drfAuth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    refreshToken: null,
    role: 'guest',
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin' || Boolean(state.user && (state.user.isStaff || state.user.is_staff)),
    isInvestor: (state) => state.role === 'investor',
    isCustomer: (state) => state.role === 'customer' || Boolean(state.user && !(state.user.isStaff || state.user.is_staff)),
    userDisplayName: (state) => {
      if (state.user) {
        return state.user.firstName || state.user.username || 'مستخدم';
      }
      return 'ضيف';
    },
  },
  actions: {
    async initializeAuth() {
      try {
        const token = localStorage.getItem('token');
        const refreshToken = localStorage.getItem('refreshToken');
        const userData = localStorage.getItem('user');
        const role = localStorage.getItem('role');

        console.log('🔐 Initializing auth with:', { token: !!token, userData: !!userData, role });

        if (token && userData) {
          this.token = token;
          this.refreshToken = refreshToken;
          try {
            this.user = JSON.parse(userData);
          } catch (parseError) {
            console.error('Failed to parse user data:', parseError);
            this.logout();
            return;
          }
          this.role = role || 'guest';
          
          // Ensure token is valid (but don't block initialization if it fails)
          try {
            const validToken = await DRFAuthService.ensureValidToken();
            if (!validToken) {
              console.warn('Token validation failed, logging out');
              this.logout();
            }
          } catch (tokenError) {
            console.error('Token validation error:', tokenError);
            // Don't logout immediately, let the user continue with existing token
            // Token refresh will happen on API calls
          }
        } else {
          console.log('No token or user data found, staying logged out');
          this.logout();
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        this.logout();
      }
    },

    setUser(userData, token, refreshToken = null, role = null) {
      this.user = userData;
      this.token = token;
      this.refreshToken = refreshToken;
      this.role = role || ((userData.isStaff || userData.is_staff) ? 'admin' : 'customer');
      
      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('token', token);
      if (refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
      }
      localStorage.setItem('role', this.role);
    },

    async login(emailOrUsername, password) {
      try {
        this.loading = true;
        this.error = null;
        
        // Try GraphQL first, fallback to REST
        let data;
        try {
          data = await graphqlMutation(DRF_LOGIN_MUTATION, {
            email_or_username: emailOrUsername,
            password,
          });
          
          if (!data?.login?.success) {
            throw new Error(data?.login?.message || 'فشل تسجيل الدخول');
          }
          
          const { user, tokens } = data.login;
          this.setUser(user, tokens.access, tokens.refresh);
          return { success: true, user, role: this.role };
        } catch (graphqlError) {
          // Fallback to REST API
          console.log('GraphQL login failed, trying REST:', graphqlError);
          
          const response = await DRFAuthService.login(emailOrUsername, password);
          
          if (!response.success) {
            throw new Error(response.message || 'فشل تسجيل الدخول');
          }
          
          const { user, tokens } = response.data;
          DRFAuthService.setTokens(tokens);
          this.setUser(user, tokens.access, tokens.refresh);
          return { success: true, user, role: this.role };
        }
      } catch (e) {
        const errorMsg = e.message || 'بيانات الدخول غير صحيحة';
        this.error = errorMsg;
        throw new Error(errorMsg);
      } finally {
        this.loading = false;
      }
    },

    async register(userData) {
      try {
        this.loading = true;
        this.error = null;
        
        // Try GraphQL first, fallback to REST
        let data;
        try {
          data = await graphqlMutation(DRF_REGISTER_MUTATION, userData);
          
          if (!data?.register?.success) {
            throw new Error(data?.register?.message || 'فشل إنشاء الحساب');
          }
          
          const { user, tokens } = data.register;
          this.setUser(user, tokens.access, tokens.refresh);
          return data.register;
        } catch (graphqlError) {
          // Fallback to REST API
          console.log('GraphQL register failed, trying REST:', graphqlError);
          
          const response = await DRFAuthService.register(userData);
          
          if (!response.success) {
            throw new Error(response.message || 'فشل إنشاء الحساب');
          }
          
          const { user, tokens } = response.data;
          DRFAuthService.setTokens(tokens);
          this.setUser(user, tokens.access, tokens.refresh);
          return response;
        }
      } catch (e) {
        const errorMsg = e.message || 'حدث خطأ أثناء التسجيل';
        this.error = errorMsg;
        throw new Error(errorMsg);
      } finally {
        this.loading = false;
      }
    },

    async changePassword(oldPassword, newPassword, newPasswordConfirm) {
      try {
        this.loading = true;
        this.error = null;
        
        // Try GraphQL first, fallback to REST
        let data;
        try {
          data = await graphqlMutation(DRF_CHANGE_PASSWORD_MUTATION, {
            old_password: oldPassword,
            new_password: newPassword,
            new_password_confirm: newPasswordConfirm,
          });
          
          if (!data?.changePassword?.success) {
            throw new Error(data?.changePassword?.message || 'فشل تغيير كلمة المرور');
          }
          
          return data.changePassword;
        } catch (graphqlError) {
          // Fallback to REST API
          console.log('GraphQL change password failed, trying REST:', graphqlError);
          
          const response = await DRFAuthService.changePassword(oldPassword, newPassword, newPasswordConfirm);
          
          if (!response.success) {
            throw new Error(response.message || 'فشل تغيير كلمة المرور');
          }
          
          return response;
        }
      } catch (e) {
        const errorMsg = e.message || 'حدث خطأ أثناء تغيير كلمة المرور';
        this.error = errorMsg;
        throw new Error(errorMsg);
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(userData) {
      try {
        this.loading = true;
        this.error = null;
        
        // Try GraphQL first, fallback to REST
        let data;
        try {
          data = await graphqlMutation(DRF_UPDATE_PROFILE_MUTATION, userData);
          
          if (!data?.updateProfile?.success) {
            throw new Error(data?.updateProfile?.message || 'فشل تحديث الملف الشخصي');
          }
          
          this.user = data.updateProfile.user;
          localStorage.setItem('user', JSON.stringify(this.user));
          return data.updateProfile;
        } catch (graphqlError) {
          // Fallback to REST API
          console.log('GraphQL update profile failed, trying REST:', graphqlError);
          
          const response = await DRFAuthService.updateProfile(userData);
          
          if (!response.success) {
            throw new Error(response.message || 'فشل تحديث الملف الشخصي');
          }
          
          this.user = response.data.user;
          localStorage.setItem('user', JSON.stringify(this.user));
          return response;
        }
      } catch (e) {
        const errorMsg = e.message || 'حدث خطأ أثناء تحديث الملف الشخصي';
        this.error = errorMsg;
        throw new Error(errorMsg);
      } finally {
        this.loading = false;
      }
    },

    async fetchProfile() {
      try {
        this.loading = true;
        this.error = null;
        
        // Try GraphQL first, fallback to REST
        let data;
        try {
          data = await graphqlQuery(DRF_ME_QUERY);
          
          if (data?.me) {
            this.user = data.me;
            localStorage.setItem('user', JSON.stringify(this.user));
            return this.user;
          }
        } catch (graphqlError) {
          // Fallback to REST API
          console.log('GraphQL fetch profile failed, trying REST:', graphqlError);
          
          const response = await DRFAuthService.getProfile();
          
          if (response.success) {
            this.user = response.data.user;
            localStorage.setItem('user', JSON.stringify(this.user));
            return this.user;
          }
        }
      } catch (e) {
        const errorMsg = e.message || 'حدث خطأ أثناء جلب الملف الشخصي';
        this.error = errorMsg;
        throw new Error(errorMsg);
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      this.role = 'guest';
      this.error = null;
      
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('role');
      
      DRFAuthService.clearTokens();
    },

    async refreshToken() {
      try {
        const newToken = await DRFAuthService.refreshToken();
        this.token = newToken;
        localStorage.setItem('token', newToken);
        return newToken;
      } catch (error) {
        this.logout();
        throw error;
      }
    },

    clearError() {
      this.error = null;
    },
  },
});
