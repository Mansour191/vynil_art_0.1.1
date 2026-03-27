// API Testing Tool - Verify all endpoints are working
import { httpClient } from '@/services/HttpClient.js';
import AIService from '@/services/AIService.js';

class ApiTest {
  static async testAllEndpoints() {
    console.group('🧪 Testing All API Endpoints');
    
    const endpoints = [
      { name: 'AI Health Check', url: '/ai/health/', method: 'GET' },
      { name: 'AI Market Trends', url: '/ai/analytics/market-trends', method: 'GET' },
      { name: 'AI Demand Prediction', url: '/ai/inventory/demand-prediction/test', method: 'GET' },
      { name: 'AI Pricing Analysis', url: '/ai/analyze/pricing-factors', method: 'POST', data: { product: 'test', factors: { price: 100 } } }
    ];
    
    const results = [];
    
    for (const endpoint of endpoints) {
      try {
        console.log(`🔍 Testing: ${endpoint.name}`);
        
        const startTime = Date.now();
        let response;
        
        if (endpoint.method === 'GET') {
          response = await httpClient.get(endpoint.url);
        } else if (endpoint.method === 'POST') {
          response = await httpClient.post(endpoint.url, endpoint.data);
        }
        
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        if (response.ok) {
          console.log(`✅ ${endpoint.name}: ${response.status} (${duration}ms)`);
          results.push({ ...endpoint, status: 'success', duration, responseStatus: response.status });
        } else {
          console.error(`❌ ${endpoint.name}: ${response.status} ${response.statusText} (${duration}ms)`);
          results.push({ ...endpoint, status: 'failed', duration, error: response.statusText, responseStatus: response.status });
        }
        
      } catch (error) {
        console.error(`💥 ${endpoint.name}: Network Error - ${error.message}`);
        results.push({ ...endpoint, status: 'network_error', error: error.message });
      }
    }
    
    console.groupEnd();
    
    // Summary
    const successCount = results.filter(r => r.status === 'success').length;
    const failCount = results.filter(r => r.status !== 'success').length;
    
    console.log(`📊 Test Results: ${successCount}/${results.length} successful`);
    
    if (failCount > 0) {
      console.table('Failed Endpoints:', results.filter(r => r.status !== 'success'));
    }
    
    return results;
  }
  
  static async testDirectAPI(endpoint, data = null) {
    console.log(`🔍 Direct API Test: ${endpoint}`);
    
    try {
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: data ? 'POST' : 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: data ? JSON.stringify(data) : undefined
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Direct API Success:', result);
        return result;
      } else {
        console.error('❌ Direct API Failed:', response.status, response.statusText);
        const errorText = await response.text();
        console.error('Error Body:', errorText);
        return null;
      }
    } catch (error) {
      console.error('💥 Direct API Network Error:', error);
      return null;
    }
  }
  
  static checkProxyConfiguration() {
    console.group('🔧 Proxy Configuration Check');
    
    const config = {
      devMode: import.meta.env.DEV,
      apiBaseUrl: import.meta.env.VITE_API_URL,
      proxyConfig: {
        graphql: '/api/graphql -> http://127.0.0.1:8000/graphql',
        api: '/api -> http://127.0.0.1:8000'
      }
    };
    
    console.log('Environment:', config);
    console.log('Proxy should work in DEV mode:', config.devMode);
    
    // Test which URLs are being generated
    const testUrl = '/ai/health/';
    const httpClientUrl = httpClient.buildURL(testUrl);
    const directUrl = `http://127.0.0.1:8000${testUrl}`;
    
    console.log('HttpClient URL:', httpClientUrl);
    console.log('Direct URL:', directUrl);
    console.log('URLs match:', httpClientUrl === directUrl);
    
    console.groupEnd();
    
    return config;
  }
}

// Make available globally
window.ApiTest = ApiTest;

console.log('🧪 API Test Tool Loaded - Use ApiTest.testAllEndpoints() in console');

export default ApiTest;
