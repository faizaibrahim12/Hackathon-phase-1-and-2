# Todo Backend API

FastAPI backend for full-stack todo application (Phase II).

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- pip

### Installation

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -e .
```

3. **Configure environment**
Copy `.env.example` to `.env` and update with your database URL:
```bash
cp .env.example .env
```

4. **Apply database migrations**
```bash
alembic upgrade head
```

5. **Run development server**
```bash
fastapi run src/main.py
# or: uvicorn src.main:app --reload
```

Server will be available at `http://localhost:8000`

## API Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── exceptions.py        # Custom exceptions
│   ├── auth/                # Authentication module
│   │   ├── __init__.py
│   │   ├── models.py        # User model
│   │   ├── schemas.py       # Request/response schemas
│   │   ├── service.py       # Business logic (TODO)
│   │   ├── routes.py        # API routes (TODO)
│   │   └── jwt.py           # JWT utilities (TODO)
│   ├── tasks/               # Tasks module
│   │   ├── __init__.py
│   │   ├── models.py        # Task model
│   │   ├── schemas.py       # Request/response schemas
│   │   ├── service.py       # Business logic (TODO)
│   │   └── routes.py        # API routes (TODO)
│   └── middleware/          # Middleware
│       └── __init__.py
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   ├── versions/
│   │   └── 001_initial_schema.py
│   └── __init__.py
├── pyproject.toml
├── alembic.ini
├── .env.example
└── .env
```

## Database Migrations

### Create new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback one migration
```bash
alembic downgrade -1
```

### View migration history
```bash
alembic current  # Show current revision
alembic history  # Show all revisions
```

## Testing with curl

### Health check
```bash
curl http://localhost:8000/health
```

### Endpoints (when implemented)

#### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

## Next Steps

- [ ] Phase P2: Implement authentication (JWT, password hashing)
- [ ] Phase P3: Implement task CRUD endpoints
- [ ] Add comprehensive error handling
- [ ] Add rate limiting
- [ ] Add request validation
- [ ] Write unit tests
- [ ] Add logging

## Environment Variables

See `.env.example` for all required variables.

## License

MIT
