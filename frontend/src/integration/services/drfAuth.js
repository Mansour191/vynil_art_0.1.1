// DRF Auth Kit Integration for Frontend
import { gql } from '@apollo/client/core';

// GraphQL Mutations for DRF Auth Kit
export const DRF_LOGIN_MUTATION = gql`
  mutation Login($email_or_username: String!, $password: String!) {
    login(emailOrUsername: $email_or_username, password: $password) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        phone
        isStaff
        dateJoined
      }
      tokens
      errors
    }
  }
`;

export const DRF_REGISTER_MUTATION = gql`
  mutation Register($username: String!, $email: String!, $password: String!, $password_confirm: String!, $first_name: String!, $last_name: String, $phone: String) {
    register(username: $username, email: $email, password: $password, passwordConfirm: $password_confirm, firstName: $first_name, lastName: $last_name, phone: $phone) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        phone
        isStaff
        dateJoined
      }
      tokens
      errors
    }
  }
`;

export const DRF_CHANGE_PASSWORD_MUTATION = gql`
  mutation ChangePassword($old_password: String!, $new_password: String!, $new_password_confirm: String!) {
    changePassword(oldPassword: $old_password, newPassword: $new_password, newPasswordConfirm: $new_password_confirm) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        phone
        isStaff
        dateJoined
      }
      errors
    }
  }
`;

export const DRF_UPDATE_PROFILE_MUTATION = gql`
  mutation UpdateProfile($first_name: String, $last_name: String, $email: String, $phone: String) {
    updateProfile(firstName: $first_name, lastName: $last_name, email: $email, phone: $phone) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        phone
        isStaff
        dateJoined
      }
      errors
    }
  }
`;

export const DRF_ME_QUERY = gql`
  query Me {
    me {
      id
      username
      email
      firstName
      lastName
      phone
      isStaff
      dateJoined
    }
  }
`;

// REST API endpoints for DRF Auth Kit
export const DRF_AUTH_ENDPOINTS = {
  login: '/api/auth/login/',
  register: '/api/auth/register/',
  changePassword: '/api/auth/change-password/',
  resetPassword: '/api/auth/reset-password/',
  confirmResetPassword: '/api/auth/confirm-reset-password/',
  profile: '/api/auth/profile/',
  updateProfile: '/api/auth/profile/update/',
};

// Helper functions for REST API calls
export const drfAuthRequest = async (endpoint, data = {}, method = 'POST') => {
  const url = `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}${endpoint}`;
  
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  // Add auth token if available
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  if (method !== 'GET' && data) {
    config.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(url, config);
    const responseData = await response.json();
    
    if (!response.ok) {
      throw new Error(responseData.message || 'Request failed');
    }
    
    return responseData;
  } catch (error) {
    throw new Error(error.message || 'Network error');
  }
};

// DRF Auth Kit service class
export class DRFAuthService {
  static async login(emailOrUsername, password) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.login, {
      email_or_username: emailOrUsername,
      password,
    });
  }
  
  static async register(userData) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.register, userData);
  }
  
  static async changePassword(oldPassword, newPassword, newPasswordConfirm) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.changePassword, {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
  }
  
  static async resetPassword(email) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.resetPassword, { email });
  }
  
  static async confirmResetPassword(token, newPassword, newPasswordConfirm) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.confirmResetPassword, {
      token,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
  }
  
  static async getProfile() {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.profile, {}, 'GET');
  }
  
  static async updateProfile(userData) {
    return drfAuthRequest(DRF_AUTH_ENDPOINTS.updateProfile, userData, 'PATCH');
  }
  
  // Token management
  static setTokens(tokens) {
    if (tokens.access) {
      localStorage.setItem('token', tokens.access);
    }
    if (tokens.refresh) {
      localStorage.setItem('refreshToken', tokens.refresh);
    }
  }
  
  static getAccessToken() {
    return localStorage.getItem('token');
  }
  
  static getRefreshToken() {
    return localStorage.getItem('refreshToken');
  }
  
  static clearTokens() {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  }
  
  // Token refresh
  static async refreshToken() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/api/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error('Token refresh failed');
      }
      
      this.setTokens(data);
      return data.access;
    } catch (error) {
      this.clearTokens();
      throw error;
    }
  }
  
  // Check if token is expired and refresh if needed
  static async ensureValidToken() {
    const token = this.getAccessToken();
    if (!token) {
      return null;
    }
    
    try {
      // Decode JWT token to check expiration
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      
      // If token expires in less than 5 minutes, refresh it
      if (payload.exp - currentTime < 300) {
        return await this.refreshToken();
      }
      
      return token;
    } catch (error) {
      // If token is invalid, clear it and return null
      this.clearTokens();
      return null;
    }
  }
}

// Export default service
export default DRFAuthService;
