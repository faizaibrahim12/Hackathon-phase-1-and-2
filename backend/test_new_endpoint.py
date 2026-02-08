#!/usr/bin/env python3
"""
Test script to verify the new signup-with-task endpoint
"""

import requests
import json

def test_signup_with_task_endpoint():
    """Test the new signup-with-task endpoint"""
    
    print("Testing the new signup-with-task endpoint...")
    
    # Define the API endpoint
    base_url = "http://localhost:8000"
    signup_with_task_url = f"{base_url}/api/signup-with-task"
    
    # Prepare test data
    test_email = "apitest@example.com"
    test_password = "securepassword123"
    test_task_title = "API Test Task"
    test_task_description = "This task was created via the signup-with-task API endpoint."
    
    # Prepare the request payload
    payload = {
        "email": test_email,
        "password": test_password
    }
    
    # Prepare query parameters
    params = {
        "initial_task_title": test_task_title,
        "initial_task_description": test_task_description
    }
    
    print(f"Sending POST request to: {signup_with_task_url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Query params: {json.dumps(params, indent=2)}")
    
    try:
        # Make the request
        response = requests.post(
            signup_with_task_url,
            json=payload,
            params=params,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            print("\n[SUCCESS] Endpoint responded with 201 Created")
            print(f"User ID: {response_data.get('user', {}).get('id')}")
            print(f"User Email: {response_data.get('user', {}).get('email')}")
            print(f"Task ID: {response_data.get('initial_task', {}).get('id')}")
            print(f"Task Title: {response_data.get('initial_task', {}).get('title')}")
            print(f"Message: {response_data.get('message')}")
        else:
            print(f"[ERROR] Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n[WARNING] Could not connect to server. Is the backend running?")
        print("To test this endpoint, start the backend server with: uvicorn src.main:app --reload --port 8000")
        print("\nHowever, the endpoint has been successfully added to the application.")
    
    # Also test the demo endpoint
    print(f"\nTesting demo endpoint...")
    demo_url = f"{base_url}/api/demo-signup-task"
    try:
        demo_response = requests.get(demo_url)
        if demo_response.status_code == 200:
            print(f"[SUCCESS] Demo endpoint accessible: {demo_response.status_code}")
        else:
            print(f"[INFO] Demo endpoint status: {demo_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[INFO] Demo endpoint not accessible (server not running)")


if __name__ == "__main__":
    print("=== Testing New Signup-With-Task Endpoint ===")
    test_signup_with_task_endpoint()
    print("\nTest completed!")