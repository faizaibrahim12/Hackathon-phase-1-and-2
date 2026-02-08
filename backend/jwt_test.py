from jose import jwt
from datetime import datetime, timedelta
import os
import sys

# Add the src directory to the path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import settings

# Test token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoiYW5vdGhlcnRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3Njg5MjQ5Mzl9.nku0t1Ca5ZKPs275V9UicVGUcrsy3s313k5UC61bYHw"

print("JWT Secret:", settings.JWT_SECRET)
print("JWT Algorithm:", settings.JWT_ALGORITHM)

try:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    print("Decoded payload:", payload)
    
    # Check if token is expired
    exp_time = datetime.utcfromtimestamp(payload.get("exp", 0))
    current_time = datetime.utcnow()
    print(f"Token expires at: {exp_time}")
    print(f"Current time: {current_time}")
    print(f"Token expired: {current_time > exp_time}")
    
except Exception as e:
    print(f"Error decoding token: {e}")