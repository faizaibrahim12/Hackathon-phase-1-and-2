from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.auth.jwt import get_user_id_from_token


PUBLIC_ROUTES = [
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/refresh",
    "/api/signup-with-task",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/"
]

async def verify_token_middleware(request: Request, call_next):
    # ✅ Allow CORS preflight requests (OPTIONS)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    # ✅ Allow public routes
    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "unauthorized", "detail": "Authorization header missing"},
        )

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "invalid_token", "detail": "Invalid authorization format"},
        )

    user_id = get_user_id_from_token(token)
    if not user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "invalid_token", "detail": "Token expired or invalid"},
        )

    request.state.user_id = user_id
    return await call_next(request)
