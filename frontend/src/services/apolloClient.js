import { ApolloClient, InMemoryCache, createHttpLink, from } from '@apollo/client/core';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';
import { useStorage } from '@vueuse/core';

const getAuthToken = () => {
  const authToken = useStorage('authToken', '');
  const accessToken = useStorage('accessToken', '');
  return authToken.value || accessToken.value || null;
}

const httpLink = createHttpLink({
  uri: '/graphql/',
});

const authLink = setContext((_, { headers }) => {
  const token = getAuthToken();
  if (token) {
    return {
      headers: {
        ...headers,
        authorization: `Bearer ${token}`,
      }
    }
  }
  return { headers };
});

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (networkError) {
    console.error('[Network error]:', networkError);
  }
  
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, extensions }) => {
      console.error(`[GraphQL error]: Message: ${message}`);
    });
  }
});

// Create Apollo Client instance for services
export const apolloClient = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    possibleTypes: {
      // Add possible types to prevent FIELD errors
      ProductType: ['ProductType'],
      Query: ['Query'],
      Mutation: ['Mutation'],
      AIHealthType: ['AIHealthType']
    }
  }),
  devtools: {
    enabled: true
  },
  defaultOptions: {
    query: {
      errorPolicy: 'all',
      fetchPolicy: 'cache-and-network'
    }
  }
});

export default apolloClient;
