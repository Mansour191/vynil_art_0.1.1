import requests
import json

url = 'http://127.0.0.1:8000/graphql/'
query = 'mutation { tokenAuth(username: "admin", password: "admin123") { tokenAuth { token payload user { id username isStaff } } } }'

try:
    response = requests.post(url, json={'query': query})
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
