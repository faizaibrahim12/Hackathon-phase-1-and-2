from src.auth.jwt import verify_token, get_user_id_from_token
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoiYW5vdGhlcnRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3Njg5MjQ5Mzl9.nku0t1Ca5ZKPs275V9UicVGUcrsy3s313k5UC61bYHw"

print("Testing verify_token function:")
result = verify_token(token)
print(f"verify_token result: {result}")

print("\nTesting get_user_id_from_token function:")
user_id = get_user_id_from_token(token)
print(f"get_user_id_from_token result: {user_id}")