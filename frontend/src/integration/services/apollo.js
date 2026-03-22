import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core';
import { setContext } from '@apollo/client/link/context';

const resolveGraphqlUrl = () => {
  const envUrl =
    import.meta.env.VITE_GRAPHQL_URL ||
    import.meta.env.VITE_API_URL ||
    '';
  const normalized = String(envUrl).trim().replace(/\/+$/, '');
  return normalized ? `${normalized}/graphql/` : 'http://127.0.0.1:8000/graphql/';
};

const httpLink = createHttpLink({
  uri: resolveGraphqlUrl(),
  // Add error handling for network issues
  fetch: (uri, options) => {
    return fetch(uri, options).catch(error => {
      console.error('Apollo Client Network Error:', error);
      throw error;
    });
  }
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      Authorization: token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json',
    },
  };
});

const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          products: {
            merge(_, incoming) {
              return incoming;
            },
          },
          categories: {
            merge(_, incoming) {
              return incoming;
            },
          },
        },
      },
    },
  }),
  // Add error handling
  defaultOptions: {
    watchQuery: {
      errorPolicy: 'all',
    },
    query: {
      errorPolicy: 'all',
    },
  },
});

export default apolloClient;
