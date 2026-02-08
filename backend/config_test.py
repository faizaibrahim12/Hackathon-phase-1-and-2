import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import settings
print(f"JWT_SECRET from settings: '{settings.JWT_SECRET}'")

# Also test the actual token creation and validation
from src.auth.jwt import create_access_token, get_user_id_from_token

# Create a test token
token = create_access_token(1, "test@example.com")
print(f"Created token: {token}")

# Try to validate it
user_id = get_user_id_from_token(token)
print(f"Validated user_id: {user_id}")