import requests
import json

# Test the task creation endpoint
def test_task_creation():
    # First, let's login to get a token
    login_data = {
        "email": "faiza@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post("http://127.0.0.1:8000/api/auth/login", json=login_data)
        print(f"Login Status Code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"Access Token received: {access_token[:20]}..." if access_token else "No token")
            
            # Now try to create a task with the token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            task_data = {
                "title": "Test task after fix",
                "description": "Testing if the internal server error is fixed"
            }
            
            task_response = requests.post(
                "http://127.0.0.1:8000/api/tasks", 
                json=task_data, 
                headers=headers
            )
            
            print(f"Task Creation Status Code: {task_response.status_code}")
            print(f"Task Creation Response: {task_response.text}")
            
        else:
            print(f"Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_task_creation()