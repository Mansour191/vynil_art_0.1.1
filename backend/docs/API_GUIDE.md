# VynilArt GraphQL API Guide

## 📋 **Table of Contents**

1. [Authentication](#authentication)
2. [Core Queries](#core-queries)
3. [Product Management](#product-management)
4. [Order Management](#order-management)
5. [Pricing Engine](#pricing-engine)
6. [AI Services](#ai-services)
7. [ERPNext Integration](#erpnext-integration)
8. [Real-time Subscriptions](#real-time-subscriptions)
9. [Error Handling](#error-handling)
10. [Rate Limiting & Best Practices](#rate-limiting--best-practices)

---

## 🔐 **Authentication**

### JWT Authentication
All API endpoints (except health check) require JWT authentication.

#### Login Mutation
```graphql
mutation Login($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    token
    refreshToken
    user {
      id
      username
      email
      isStaff
    }
  }
}
```

**Request Example:**
```json
{
  "query": "mutation Login($username: String!, $password: String!) { login(username: $username, password: $password) { token refreshToken user { id username email isStaff } } }",
  "variables": {
    "username": "admin@example.com",
    "password": "your-password"
  }
}
```

**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN",
  "Content-Type": "application/json"
}
```

---

## 🔍 **Core Queries**

### Get Current User
```graphql
query GetMe {
  me {
    id
    username
    email
    firstName
    lastName
    isStaff
    dateJoined
    profile {
      phone
      address
      city
      country
    }
  }
}
```

### Categories
```graphql
query GetCategories {
  categories {
    id
    name
    slug
    description
    image
    wastePercent
    children {
      id
      name
      slug
    }
  }
}
```

### Materials
```graphql
query GetMaterials {
  materials {
    id
    name
    slug
    description
    pricePerSqm
    inStock
    properties
  }
}
```

---

## 📦 **Product Management**

### Get Products (with Pagination & Filtering)
```graphql
query GetProducts(
  $categorySlug: String
  $search: String
  $limit: Int = 20
  $offset: Int = 0
  $priceMin: Float
  $priceMax: Float
  $inStock: Boolean = true
) {
  products(
    categorySlug: $categorySlug
    search: $search
    limit: $limit
    offset: $offset
    priceMin: $priceMin
    priceMax: $priceMax
    inStock: $inStock
  ) {
    id
    name
    slug
    description
    basePrice
    category {
      name
      slug
    }
    materials {
      name
      slug
      pricePerSqm
    }
    images {
      id
      imageUrl
      isMain
      altText
    }
    variants {
      name
      sku
      price
      inStock
    }
    inStock
    isActive
    createdAt
    updatedAt
  }
}
```

**Request Example:**
```json
{
  "query": "query GetProducts($categorySlug: String, $search: String, $limit: Int, $offset: Int) { products(categorySlug: $categorySlug, search: $search, limit: $limit, offset: $offset) { id name slug description basePrice category { name slug } materials { name slug pricePerSqm } images { id imageUrl isMain altText } inStock isActive } }",
  "variables": {
    "categorySlug": "marble",
    "search": "white",
    "limit": 10,
    "offset": 0
  }
}
```

### Get Single Product
```graphql
query GetProduct($slug: String!) {
  product(slug: $slug) {
    id
    name
    slug
    description
    basePrice
    category {
      name
      slug
      wastePercent
    }
    materials {
      id
      name
      slug
      description
      pricePerSqm
      inStock
    }
    images {
      id
      imageUrl
      isMain
      altText
      order
    }
    variants {
      id
      name
      sku
      price
      inStock
      attributes
    }
    specifications
    careInstructions
    inStock
    isActive
    seoTitle
    seoDescription
    createdAt
    updatedAt
  }
}
```

---

## 🛒 **Order Management**

### Get My Orders
```graphql
query GetMyOrders($limit: Int = 10, $offset: Int = 0) {
  myOrders(limit: $limit, offset: $offset) {
    id
    orderNumber
    status
    subtotal
    taxAmount
    shippingCost
    totalAmount
    currency
    createdAt
    updatedAt
    items {
      id
      product {
        name
        slug
      }
      material {
        name
      }
      quantity
      width
      height
      unitPrice
      totalPrice
    }
    shippingAddress {
      fullName
      address
      city
      country
      postalCode
      phone
    }
    payments {
      id
      amount
      status
      paymentMethod
      transactionId
      createdAt
    }
    timeline {
      id
      status
      message
      timestamp
      isPublic
    }
  }
}
```

### Create Order
```graphql
mutation CreateOrder($input: OrderInput!) {
  createOrder(input: $input) {
    id
    orderNumber
    status
    totalAmount
    items {
      id
      product {
        name
      }
      quantity
      totalPrice
    }
  }
}
```

**Order Input Example:**
```json
{
  "input": {
    "items": [
      {
        "productId": "1",
        "materialId": "1",
        "quantity": 2,
        "width": 100,
        "height": 50
      }
    ],
    "shippingAddress": {
      "fullName": "John Doe",
      "address": "123 Main St",
      "city": "New York",
      "country": "USA",
      "postalCode": "10001",
      "phone": "+1234567890"
    },
    "paymentMethod": "credit_card"
  }
}
```

---

## 💰 **Pricing Engine**

### Calculate Price (Complex Pricing)
```graphql
query CalculatePrice($input: PriceCalculationInput!) {
  calculatePrice(input: $input) {
    basePrice
    materialPrice
    laborCost
    wasteCost
    subtotal
    taxAmount
    totalPrice
    currency
    breakdown {
      material {
        name
        pricePerSqm
        totalCost
      }
      waste {
        percentage
        cost
      }
      labor {
        hourlyRate
        hours
        cost
      }
      tax {
        rate
        amount
      }
    }
    appliedRules {
      ruleName
      discount
      reason
    }
  }
}
```

**Request Example:**
```json
{
  "query": "query CalculatePrice($input: PriceCalculationInput!) { calculatePrice(input: $input) { basePrice materialPrice laborCost wasteCost subtotal taxAmount totalPrice currency breakdown { material { name pricePerSqm totalCost } waste { percentage cost } labor { hourlyRate hours cost } tax { rate amount } } appliedRules { ruleName discount reason } } }",
  "variables": {
    "input": {
      "productId": "1",
      "materialId": "1",
      "width": 120,
      "height": 80,
      "quantity": 3,
      "categorySlug": "marble"
    }
  }
}
```

### Validate Coupon
```graphql
mutation ValidateCoupon($code: String!, $orderValue: Float!) {
  validateCoupon(code: $code, orderValue: $orderValue) {
    valid
    discountType
    discountValue
    finalAmount
    message
    coupon {
      id
      code
      discountType
      discountValue
      minOrderValue
      maxUses
      usedCount
      validUntil
    }
  }
}
```

---

## 🤖 **AI Services**

### Semantic Search
```graphql
query SemanticSearch($query: String!, $filters: SearchFilters, $limit: Int = 10) {
  semanticSearch(query: $query, filters: $filters, limit: $limit) {
    products {
      id
      name
      slug
      description
      basePrice
      relevanceScore
      category {
        name
        slug
      }
      images {
        id
        imageUrl
        isMain
      }
    }
    suggestions
    totalResults
    searchTime
    filters {
      categories {
        name
        slug
        count
      }
      priceRanges {
        min
        max
        count
      }
      materials {
        name
        slug
        count
      }
    }
  }
}
```

**Request Example:**
```json
{
  "query": "query SemanticSearch($query: String!, $filters: SearchFilters, $limit: Int) { semanticSearch(query: $query, filters: $filters, limit: $limit) { products { id name slug description basePrice relevanceScore category { name slug } images { id imageUrl isMain } } suggestions totalResults searchTime } }",
  "variables": {
    "query": "white marble for kitchen countertop",
    "filters": {
      "categorySlug": "marble",
      "priceMax": 500,
      "inStock": true
    },
    "limit": 5
  }
}
```

### AI Chat (Streaming)
```graphql
subscription AIChatStream($message: String!, $context: String) {
  aiChatStream(message: $message, context: $context) {
    content
    type
    progress
    timestamp
    userId
  }
}
```

### Market Trends
```graphql
query MarketTrends($category: String, $period: String = "30d") {
  marketTrends(category: $category, period: $period) {
    category
    period
    trends {
      date
      demand
      averagePrice
      competition
      recommendations
    }
    insights {
      trend
      confidence
      factors
    }
  }
}
```

---

## 🔄 **ERPNext Integration**

### Sync with ERPNext
```graphql
mutation SyncWithERPNext($syncType: String!, $dryRun: Boolean = false) {
  syncWithERPNext(syncType: $syncType, dryRun: $dryRun) {
    success
    message
    recordsSynced
    errors
    syncId
    timestamp
  }
}
```

### Push to ERPNext
```graphql
mutation PushToERPNext($entityType: String!, $entityId: ID!) {
  pushToERPNext(entityType: $entityType, entityId: $entityId) {
    success
    message
    erpnextId
    errors
    timestamp
  }
}
```

### ERPNext Health Check
```graphql
query ERPNextHealth {
  erpnextHealth {
    status
    message
    responseTime
    lastSync
    version
  }
}
```

---

## 📡 **Real-time Subscriptions**

### Order Updates
```graphql
subscription OrderUpdates($orderId: ID!) {
  orderUpdates(orderId: $orderId) {
    orderId
    status
    message
    timestamp
    userId
  }
}
```

### Notifications
```graphql
subscription Notifications($userId: ID) {
  notifications(userId: $userId) {
    id
    title
    message
    type
    isRead
    userId
  }
}
```

### ERPNext Sync Status
```graphql
subscription ERPNextSyncStatus {
  erpnextSyncStatus {
    syncId
    status
    message
    recordsSynced
    timestamp
    errorMessage
  }
}
```

---

## ⚠️ **Error Handling**

### Error Response Format
```json
{
  "errors": [
    {
      "message": "Authentication credentials were not provided.",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "me"
      ],
      "extensions": {
        "code": "UNAUTHENTICATED",
        "exception": {
          "stacktrace": ["..."]
        }
      }
    }
  ],
  "data": {
    "me": null
  }
}
```

### Common Error Codes
- `UNAUTHENTICATED` - Authentication required
- `PERMISSION_DENIED` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `VALIDATION_ERROR` - Input validation failed
- `RATE_LIMITED` - Too many requests
- `INTERNAL_SERVER_ERROR` - Server error
- `ERPNEXT_CONNECTION_ERROR` - ERPNext connection failed
- `AI_SERVICE_ERROR` - AI service unavailable

### ERPNext Error Handling
```graphql
query ERPNextHealth {
  erpnextHealth {
    status
    message
    responseTime
    lastSync
    version
    errorDetails {
      code
      message
      timestamp
    }
  }
}
```

---

## 🚀 **Rate Limiting & Best Practices**

### Rate Limiting
- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Staff users**: 5000 requests/hour
- **AI queries**: 50 requests/hour
- **ERPNext sync**: 10 requests/hour

### Best Practices

#### 1. Pagination
Always use pagination for large datasets:
```graphql
query GetProducts($limit: Int = 20, $offset: Int = 0) {
  products(limit: $limit, offset: $offset) {
    id
    name
    # ... other fields
  }
}
```

#### 2. Field Selection
Request only the fields you need:
```graphql
query GetProduct($slug: String!) {
  product(slug: $slug) {
    id
    name
    basePrice
    # Don't request unnecessary fields
  }
}
```

#### 3. Caching
- Use GraphQL cache headers
- Implement client-side caching
- Cache static data (categories, materials)

#### 4. Error Handling
Always handle errors gracefully:
```javascript
try {
  const result = await client.query({ query: GET_PRODUCT });
  // Handle success
} catch (error) {
  if (error.networkError) {
    // Handle network errors
  } else if (error.graphQLErrors) {
    // Handle GraphQL errors
  }
}
```

#### 5. Real-time Updates
Use subscriptions for real-time data:
```javascript
const subscription = client.subscribe({
  query: ORDER_UPDATES_SUBSCRIPTION,
  variables: { orderId: '123' }
}).subscribe({
  next: (data) => {
    // Handle real-time updates
  },
  error: (error) => {
    // Handle subscription errors
  }
});
```

---

## 📊 **Performance Tips**

### 1. Use Selective Field Queries
```graphql
# Good - Only requested fields
query GetProductBasic($slug: String!) {
  product(slug: $slug) {
    id
    name
    basePrice
  }
}

# Avoid - Requesting everything
query GetProductFull($slug: String!) {
  product(slug: $slug) {
    id
    name
    description
    basePrice
    category { ... }
    materials { ... }
    images { ... }
    variants { ... }
    specifications
    careInstructions
    # ... potentially large fields
  }
}
```

### 2. Batch Operations
```graphql
# Good - Single query for multiple items
query GetMultipleProducts($slugs: [String!]!) {
  products: getProductsBySlugs(slugs: $slugs) {
    id
    name
    basePrice
  }
}

# Avoid - Multiple queries
query GetProduct1 { product(slug: "product-1") { id name } }
query GetProduct2 { product(slug: "product-2") { id name } }
```

### 3. Use Subscriptions for Real-time Data
```graphql
# For real-time updates
subscription OrderUpdates($orderId: ID!) {
  orderUpdates(orderId: $orderId) {
    status
    message
    timestamp
  }
}
```

---

## 🔧 **Development Tools**

### GraphQL Playground
Access at: `http://localhost:8000/graphql/` (when DEBUG=True)

### Health Check
```bash
curl http://localhost:8000/health/
```

### Schema Introspection
```graphql
query IntrospectionQuery {
  __schema {
    types {
      name
      kind
      description
    }
  }
}
```

---

## 📞 **Support**

For API support and questions:
- Check the error messages for specific guidance
- Review the GraphQL Playground for schema documentation
- Contact the development team for complex issues

---

**Last Updated:** March 28, 2026  
**API Version:** v1.0.0  
**GraphQL Endpoint:** `/graphql/`  
**WebSocket Endpoint:** `ws://localhost:8000/ws/graphql/subscriptions/`
