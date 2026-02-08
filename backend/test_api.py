import requests
import json

def test_api():
    # Login first
    login_data = {
        "email": "faiza@test.com",
        "password": "password123"
    }
    
    try:
        login_resp = requests.post("http://127.0.0.1:8000/api/auth/login", json=login_data)
        print(f"Login response: {login_resp.status_code}")
        print(f"Login data: {login_resp.json()}")
        
        if login_resp.status_code == 200:
            token = login_resp.json()["access_token"]
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Create task
            task_data = {
                "title": "Test task after fix",
                "description": "Testing if the internal server error is fixed"
            }
            
            task_resp = requests.post("http://127.0.0.1:8000/api/tasks", json=task_data, headers=headers)
            print(f"Task creation response: {task_resp.status_code}")
            print(f"Task creation data: {task_resp.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()