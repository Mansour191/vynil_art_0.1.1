import AIServiceGraphQL from './AIServiceGraphQL';

// Export the new GraphQL-based AIService as default
export default AIServiceGraphQL;

// Also export a class for backward compatibility
export { AIServiceGraphQL };

// Create singleton instance
const aiServiceInstance = AIServiceGraphQL.getInstance();

export default aiServiceInstance;
