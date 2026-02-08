#!/usr/bin/env python3
import sys
import traceback
from src.main import app

def test_register_endpoint():
    """Test the register endpoint directly"""
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Test the register endpoint
    response = client.post("/api/auth/register", json={
        "email": "test_new@example.com",
        "password": "testpassword123"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Headers: {dict(response.headers)}")

if __name__ == "__main__":
    try:
        print("Testing register endpoint...")
        test_register_endpoint()
    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()