# Finance Dashboard Backend

## Overview

This project implements a backend service for a role-based finance dashboard system.

It supports:

- user management
- secure authentication
- financial record storage
- analytics endpoints
- role-based access control using JWT authorization

The system follows a clean and scalable architecture using FastAPI, SQLAlchemy, and SQLite.

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication (python-jose)
- Passlib (bcrypt)
- Pydantic Validation

## Features Implemented

### 1. User & Role Management

Supports:

- Create users
- Assign roles
- Activate role-based access restrictions

#### Roles & Permissions
| Role    | Permissions |
|---------|-------------|
| Viewer  | View dashboard summaries |
| Analyst | View records + analytics |
| Admin   | Full access (users + records management) |

### 2. Authentication

JWT-based login system with:

- password hashing using bcrypt
- token generation
- OAuth2 integration with Swagger
- role embedded inside token payload

#### Endpoint
`POST /login`

Returns:

- access_token
- token_type

### 3. Financial Records Management

Supported operations:

- `POST   /records`
- `GET    /records`
- `PUT    /records/{id}`
- `DELETE /records/{id}`

Includes:

- filtering by category
- filtering by type
- pagination support
- creator tracking
- soft delete support

Example:

`GET /records?page=1&limit=10&type=income`

### 4. Dashboard Summary APIs

Analytics endpoints:

- `GET /dashboard/summary`
- `GET /dashboard/category-summary`
- `GET /dashboard/recent`

Returns:

- total income
- total expenses
- net balance
- category totals
- recent transactions

Example response:

```json
{
  "total_income": 100000,
  "total_expense": 20000,
  "net_balance": 80000
}
```

### 5. Role-Based Access Control (RBAC)

Implemented using dependency injection middleware.

Hierarchy:

viewer < analyst < admin

#### Access Rules
| Endpoint       | Access |
|----------------|--------|
| POST /users    | Admin only |
| POST /records  | Admin only |
| GET /records   | Analyst + Admin |
| Dashboard APIs | Analyst + Admin |

### 6. Soft Delete Support

Records are not permanently removed.

Instead:

- `is_deleted = True`

Deleted records are automatically excluded from queries.

### 7. Pagination Support

Endpoint:

`GET /records?page=1&limit=10`

Response format:

```json
{
  "page": 1,
  "limit": 10,
  "data": []
}
```

## Database Schema

### User Table

Fields:

- id
- name
- email
- password
- role
- is_active

### Record Table

Fields:

- id
- amount
- type
- category
- date
- note
- created_by
- is_deleted

## Project Structure

```
finance-dashboard-backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routes/
│       ├── users.py
│       ├── records.py
│       └── dashboard.py
```

## How to Run Locally

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Server
```bash
uvicorn app.main:app --reload
```

### 4. Open Swagger UI
http://127.0.0.1:8000/docs

## Example Workflow

1. Create admin user
2. Login via `/login`
3. Authorize inside Swagger
4. Create records
5. Access analytics endpoints

## Assumptions Made

- SQLite used for simplicity
- JWT expiration set to 60 minutes
- Soft delete implemented instead of permanent deletion
- Role hierarchy enforced using middleware dependency

## Future Improvements

Possible extensions:

- refresh tokens
- search endpoints
- rate limiting
- audit logging
- unit tests
- PostgreSQL migration support

