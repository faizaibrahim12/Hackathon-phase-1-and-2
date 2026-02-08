import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import settings
from src.auth.jwt import create_access_token, verify_token
from src.middleware.auth import verify_token_middleware
from fastapi import Request
from datetime import datetime

print("=== Configuration Test ===")
print(f"JWT_SECRET: {settings.JWT_SECRET}")
print(f"JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
print(f"JWT_EXPIRATION_HOURS: {settings.JWT_EXPIRATION_HOURS}")

print("\n=== Token Creation Test ===")
token = create_access_token(123, "test@example.com")
print(f"Created token: {token}")

print("\n=== Token Verification Test ===")
payload = verify_token(token)
print(f"Verified payload: {payload}")

print("\n=== Manual JWT Decode Test ===")
from jose import jwt
try:
    decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    print(f"Manually decoded: {decoded}")
    
    # Check expiration
    exp_timestamp = decoded.get('exp', 0)
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp) if exp_timestamp else None
    current_time = datetime.utcnow()
    
    print(f"Token expires at: {exp_datetime}")
    print(f"Current time: {current_time}")
    print(f"Token expired: {current_time > exp_datetime if exp_datetime else True}")
    
except Exception as e:
    print(f"Manual decode error: {e}")