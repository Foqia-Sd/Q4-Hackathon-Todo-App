# Implementation Plan: Phase 2 Core Features

**Branch**: `main` | **Date**: 2026-01-01 | **Spec**: [specs/core-features/spec.md](specs/core-features/spec.md)
**Input**: Create an architectural plan for implementing Phase 2 including folder structure, API routes, Better Auth flow, schema, and data flow.

## Summary
Implement a multi-user Todo application with a Next.js frontend and FastAPI backend. The system uses Better Auth for stateless authentication and Neon PostgreSQL for persistence. Core logic centers on strict multi-user isolation (MUI) ensuring users only interact with their own data.

## Technical Context
- **Language/Version**: Python 3.10+, TypeScript/Node.js 20+
- **Primary Dependencies**: FastAPI (Backend), Next.js (Frontend), Better Auth (Auth), Prisma (or SQLAlchemy for DB), Neon (DB Hosting)
- **Storage**: Neon PostgreSQL
- **Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
- **Target Platform**: Web
- **Project Type**: Full-stack Web Application
- **Performance Goals**: API response time < 200ms p95
- **Constraints**: Stateless backend, Secure isolation, Neon DB usage

## Constitution Check
- **SDD Compliance**: Plan follows Spec.
- **Multi-User Isolation**: Enforced via `user_id` on all task operations.
- **Statelessness**: Using JWT/Session handling via Better Auth (Backend does not store local sessions).

## Project Structure

### Documentation
```text
specs/core-features/
├── spec.md              # Functional specification
├── plan.md              # This file
└── tasks.md             # Implementation tasks (to be created)
```

### Source Code Structure
```text
backend/
├── app/
│   ├── api/            # Route definitions
│   │   ├── auth.py     # Better Auth integration
│   │   └── tasks.py    # Task CRUD
│   ├── core/           # Config, Security, Constants
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic models (request/response)
│   ├── services/       # Business logic / DB access
│   └── main.py         # Entry point
├── tests/
└── .env

frontend/
├── src/
│   ├── app/            # Next.js App Router
│   ├── components/     # UI components
│   ├── hooks/          # Custom React hooks (e.g., useAuth)
│   ├── lib/            # Shared utilities (auth client, api client)
│   └── services/       # API abstraction layer
├── tests/
└── .env.local
```

## Architectural Design

### Database Schema (PostgreSQL)
- **Users Table**: `id` (UUID), `email` (Unique), `password_hash`, `created_at`, `updated_at`.
- **Tasks Table**: `id` (UUID), `user_id` (FK to Users), `title` (String), `status` (Enum: pending, completed), `created_at`, `updated_at`.

### Authentication Flow (Better Auth)
1. **Signup/Login**: Frontend sends credentials to `Better Auth` endpoint.
2. **Session Generation**: `Better Auth` creates a session/token.
3. **API Access**: Frontend includes the token (Cookie or Header) in requests to FastAPI.
4. **Verification**: FastAPI middleware/dependency verifies the token with `Better Auth` or the DB session.
5. **Context**: FastAPI extracts `user_id` from the verified session and injects it into the request handler.

### Backend API Route Structure (FastAPI)
- `POST /api/auth/signup`: User registration.
- `POST /api/auth/login`: User session creation.
- `POST /api/auth/logout`: Session termination.
- `GET /api/tasks`: List all tasks for the *current authenticated user*.
- `POST /api/tasks`: Create a new task for the *current authenticated user*.
- `PUT /api/tasks/{task_id}`: Update a task (check ownership first).
- `DELETE /api/tasks/{task_id}`: Delete a task (check ownership first).

### Data Flow
1. **Trigger**: User interacts with a form/button on the **Frontend**.
2. **Request**: Frontend (Next.js) fetches the appropriate **Backend** (FastAPI) endpoint with Auth token.
3. **Logic**: Backend verifies identity, validates input, and enforces MUI.
4. **Persistence**: Backend interacts with **Database** (Neon) to read/write specific user data.
5. **Response**: Backend returns status/data to Frontend.
6. **Update**: Frontend updates local state/UI based on the result.

## Risks & Mitigations
- **Risk**: Unauthorized data access (MUI failure). **Mitigation**: Implement a centralized FastAPI dependency that automatically filters all DB queries by the authenticated `user_id`.
- **Risk**: Auth sync issues. **Mitigation**: Use Better Auth's standard client-side and server-side libraries to ensure consistent session handling.
- **Risk**: Schema drift. **Mitigation**: Use database migrations (e.g., Alembic for Python) to manage schema changes.

📋 Architectural decision detected: Multi-user isolation pattern using centralized user_id dependency in FastAPI. Document reasoning and tradeoffs? Run `/sp.adr centralized-mui-enforcement`.
📋 Architectural decision detected: Choosing Better Auth for session-based authentication in a stateless FastAPI backend. Document reasoning and tradeoffs? Run `/sp.adr better-auth-integration`.
