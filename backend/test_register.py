import requests
import json

url = 'http://127.0.0.1:8000/graphql/'
query = '''
mutation Register($username: String!, $email: String!, $password: String!, $firstName: String!, $lastName: String!) {
  register(username: $username, email: $email, password: $password, firstName: $firstName, lastName: $lastName) {
    register {
      success
      errors {
        message
        field
      }
    }
  }
}
'''

variables = {
  'username': 'testuser123',
  'email': 'test@example.com',
  'password': 'Test123456',
  'firstName': 'Test User',
  'lastName': ''
}

try:
    response = requests.post(url, json={'query': query, 'variables': variables})
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
