import { useQuery, useMutation } from '@vue/apollo-composable';
import { ref, computed } from 'vue';
import { provideApolloClient } from '@vue/apollo-composable';
import { client } from '@/plugins/apolloPlugin';

// Ensure Apollo Client is available for composables
provideApolloClient(client);

// Import all queries and mutations
import {
  AI_HEALTH_CHECK,
  MARKET_TRENDS,
  DEMAND_FORECAST,
  COMPETITOR_PRICES,
  PRICING_ANALYSIS,
  GET_PRODUCTS,
  GET_PRODUCT,
  GET_CATEGORIES,
  GET_ME,
  GET_SHIPPING_OPTIONS
} from '@/graphql/queries';

import {
  LOGIN_MUTATION,
  REGISTER_MUTATION,
  UPDATE_PROFILE_MUTATION,
  CHAT_WITH_AI_MUTATION,
  CREATE_ORDER_MUTATION
} from '@/graphql/mutations';

// GraphQL Query Composable
export function useGraphQLQuery(query, options = {}) {
  const { 
    loading, 
    error, 
    data, 
    refetch 
  } = useQuery(query, {
    errorPolicy: 'all',
    fetchPolicy: 'cache-and-network',
    ...options
  });

  const isLoading = computed(() => loading.value);
  const hasError = computed(() => !!error.value);
  const errorMessage = computed(() => error.value?.message || 'An error occurred');
  const result = computed(() => data.value || null);

  return {
    loading: isLoading,
    error: hasError,
    errorMessage,
    data: result,
    refetch
  };
}

// GraphQL Mutation Composable
export function useGraphQLMutation(mutation, options = {}) {
  const { 
    loading, 
    error, 
    mutate 
  } = useMutation(mutation, {
    errorPolicy: 'all',
    ...options
  });

  const isLoading = computed(() => loading.value);
  const hasError = computed(() => !!error.value);
  const errorMessage = computed(() => error.value?.message || 'An error occurred');

  const execute = async (variables) => {
    try {
      const result = await mutate({ variables });
      return result.data;
    } catch (err) {
      console.error('GraphQL mutation error:', err);
      throw err;
    }
  };

  return {
    loading: isLoading,
    error: hasError,
    errorMessage,
    execute
  };
}

// AI Service GraphQL Composables
export function useAIHealth(service = 'general') {
  return useGraphQLQuery(AI_HEALTH_CHECK, {
    variables: { service }
  });
}

export function useMarketTrends(category = null, period = '30days') {
  return useGraphQLQuery(MARKET_TRENDS, {
    variables: { category, period }
  });
}

export function useDemandForecast(productId, period = '30days') {
  return useGraphQLQuery(DEMAND_FORECAST, {
    variables: { productId, period },
    skip: !productId
  });
}

export function useCompetitorPrices(productId) {
  return useGraphQLQuery(COMPETITOR_PRICES, {
    variables: { productId },
    skip: !productId
  });
}

export function usePricingAnalysis(productId) {
  return useGraphQLQuery(PRICING_ANALYSIS, {
    variables: { productId },
    skip: !productId
  });
}

// Product GraphQL Composables
export function useProducts(categorySlug = null) {
  return useGraphQLQuery(GET_PRODUCTS, {
    variables: { categorySlug }
  });
}

export function useProduct(id) {
  return useGraphQLQuery(GET_PRODUCT, {
    variables: { id },
    skip: !id
  });
}

export function useCategories() {
  return useGraphQLQuery(GET_CATEGORIES);
}

// Auth GraphQL Composables
export function useLogin() {
  return useGraphQLMutation(LOGIN_MUTATION);
}

export function useRegister() {
  return useGraphQLMutation(REGISTER_MUTATION);
}

export function useUpdateProfile() {
  return useGraphQLMutation(UPDATE_PROFILE_MUTATION);
}

export function useMe() {
  return useGraphQLQuery(GET_ME);
}

// AI Chat GraphQL Composable
export function useChatWithAI() {
  return useGraphQLMutation(CHAT_WITH_AI_MUTATION);
}

// Order GraphQL Composable
export function useCreateOrder() {
  return useGraphQLMutation(CREATE_ORDER_MUTATION);
}

// Shipping GraphQL Composable
export function useShippingOptions() {
  return useGraphQLQuery(GET_SHIPPING_OPTIONS);
}
