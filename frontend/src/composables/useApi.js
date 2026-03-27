// src/composables/useApi.js
import { useFetch } from '@vueuse/core'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/'

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('authToken') || localStorage.getItem('accessToken') || null
}

// Create default headers with auth token
const getDefaultHeaders = () => {
  const token = getAuthToken()
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  return headers
}

// Main API composable - FIXED with disabled auto-aborting for health checks
export function useApi(url, options = {}) {
  // Fix double slash issue - normalize URL
  const normalizedUrl = url.startsWith('/') ? url.slice(1) : url
  const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${normalizedUrl}`
  
  // Enhanced options with proper abort handling
  const requestOptions = {
    ...options,
    headers: {
      ...getDefaultHeaders(),
      ...options.headers
    },
    // CRITICAL FIX: Extended timeouts for health checks and stability
    timeout: options.timeout || 30000, // 30 second default timeout for health checks
    immediate: options.immediate !== false, // Don't execute immediately by default
    // CRITICAL FIX: Disable VueUse's automatic aborting completely
    abortController: undefined,
    // Add ref to track abort state
    aborted: ref(false),
    // Add unique request ID for debugging
    requestId: `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
  
  const {
    data,
    error,
    isFetching,
    isFinished,
    canAbort,
    aborted,
    abort,
    execute,
    statusCode,
    statusText
  } = useFetch(fullUrl, requestOptions)
  
  // Enhanced execute with NO auto-aborting for health checks
  const enhancedExecute = async (executeOptions = {}) => {
    const requestId = requestOptions.requestId;
    const isHealthCheck = fullUrl.includes('/health/') || fullUrl.includes('/ai/health/');
    
    console.log(`🚀 Starting request ${requestId}: ${fullUrl} (Health Check: ${isHealthCheck})`);
    
    try {
      // Reset abort state before execution
      aborted.value = false
      
      // CRITICAL FIX: Don't create abort controller for health checks to prevent auto-aborting
      let abortController = null;
      let timeoutId = null;
      
      if (!isHealthCheck) {
        // Only create abort controller for non-health check requests
        abortController = new AbortController();
        
        // Set timeout only for non-health check requests
        const timeoutDuration = executeOptions.timeout || 30000;
        timeoutId = setTimeout(() => {
          if (!aborted.value) {
            console.warn(`⏰ Request ${requestId} timeout (${timeoutDuration}ms), aborting:`, fullUrl);
            abortController.abort();
            aborted.value = true;
          }
        }, timeoutDuration);
      } else {
        // For health checks, use a very long timeout but don't abort
        console.log(`🏥 Health check ${requestId} - NO auto-aborting, will wait for response`);
      }
      
      // Execute request with conditional abort controller
      const result = await execute({
        ...executeOptions,
        abortController, // Will be undefined for health checks
        // Prevent automatic aborting from VueUse
        immediate: true,
        // Add retry logic for failed requests
        retry: executeOptions.retry || (isHealthCheck ? 5 : 2),
        retryDelay: executeOptions.retryDelay || 3000
      });
      
      // Clear timeout if it exists
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      
      console.log(`✅ Request ${requestId} completed successfully:`, fullUrl);
      return result;
    } catch (err) {
      console.error(`🔴 Request ${requestId} failed:`, err);
      
      // Enhanced error logging with null checks
      const errorInfo = {
        requestId,
        message: err.message || 'Unknown error',
        status: statusCode?.value || err.status || 'UNKNOWN',
        statusText: statusText?.value || err.statusText || 'No status text',
        url: fullUrl,
        method: options.method || 'GET',
        aborted: aborted?.value || false,
        errorType: err.name || 'Unknown',
        isHealthCheck,
        timestamp: new Date().toISOString()
      };
      
      console.error(`📋 Request ${requestId} Details:`, errorInfo);
      
      // Handle different error types appropriately
      if (err.name === 'AbortError') {
        if (isHealthCheck) {
          console.warn(`⚠️ Health check ${requestId} was aborted (this should not happen with disabled auto-abort):`, fullUrl);
          // Don't treat health check aborts as critical
          throw { ...err, isAborted: true, requestId, isHealthCheck };
        } else {
          console.warn(`⚠️ Request ${requestId} was aborted (normal for non-health checks):`, fullUrl);
          throw { ...err, isAborted: true, requestId };
        }
      } else if (err.status === 20) {
        console.warn(`⚠️ Request ${requestId} received Status 20 (possible network issue):`, fullUrl);
        throw { ...err, isNetworkError: true, requestId };
      } else {
        console.error(`❌ Request ${requestId} critical error:`, err);
        throw { ...err, requestId };
      }
    }
  }
  
  return {
    data,
    error,
    isFetching,
    isFinished,
    canAbort,
    aborted,
    abort,
    execute: enhancedExecute,
    statusCode,
    statusText,
    // Convenience methods
    get: (endpoint, opts = {}) => useApi(`${normalizedUrl}${endpoint}`, { ...opts, method: 'GET' }),
    post: (endpoint, opts = {}) => useApi(`${normalizedUrl}${endpoint}`, { ...opts, method: 'POST' }),
    put: (endpoint, opts = {}) => useApi(`${normalizedUrl}${endpoint}`, { ...opts, method: 'PUT' }),
    delete: (endpoint, opts = {}) => useApi(`${normalizedUrl}${endpoint}`, { ...opts, method: 'DELETE' }),
    patch: (endpoint, opts = {}) => useApi(`${normalizedUrl}${endpoint}`, { ...opts, method: 'PATCH' })
  }
}

// Convenience methods for different HTTP methods
export const api = {
  // GET request
  get(url, options = {}) {
    return useApi(url, {
      method: 'GET',
      ...options
    })
  },
  
  // POST request
  post(url, options = {}) {
    return useApi(url, {
      method: 'POST',
      ...options
    })
  },
  
  // PUT request
  put(url, options = {}) {
    return useApi(url, {
      method: 'PUT',
      ...options
    })
  },
  
  // DELETE request
  delete(url, options = {}) {
    return useApi(url, {
      method: 'DELETE',
      ...options
    })
  },
  
  // PATCH request
  patch(url, options = {}) {
    return useApi(url, {
      method: 'PATCH',
      ...options
    })
  }
}

// Export for direct use
export default api
