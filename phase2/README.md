# Phase 2 Todo Application

A full-stack, multi-user Todo application with secure authentication and advanced task management features.

## Features

- Secure user authentication (signup/login)
- Task CRUD with Multi-User Isolation
- Task priorities (Low, Medium, High)
- Task categories
- Real-time search
- Advanced filtering (status, priority, category)
- Sorting (date, title, priority)
- Toast notifications
- Fully responsive mobile design
- Pakistan flag green theme

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL (Neon)
- **Frontend**: Next.js 16, React 19, TailwindCSS
- **Auth**: JWT tokens with bcrypt
- **Database**: Neon PostgreSQL

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python init_db.py

# Run backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-better-auth-secret
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

**Auth**
- POST `/api/v1/auth/signup` - Create account
- POST `/api/v1/auth/login` - Login

**Tasks**
- GET `/api/v1/tasks/` - List tasks (supports filters)
- POST `/api/v1/tasks/` - Create task
- PUT `/api/v1/tasks/{id}` - Update task
- DELETE `/api/v1/tasks/{id}` - Delete task

## Usage

1. **Signup**: Navigate to `/auth/signup` and create an account
2. **Login**: Go to `/auth/login` with your credentials
3. **Dashboard**: Access `/dashboard` to manage your tasks
4. **Create Tasks**: Use the form to add tasks with priority and category
5. **Search & Filter**: Use the filter panel to find specific tasks
6. **Sort**: Change sorting to organize tasks your way

## Project Structure

See `IMPLEMENTATION_SUMMARY.md` for detailed implementation notes.

## Specifications

All specifications are in the `specs/core-features/` directory:
- `spec.md` - Functional requirements
- `plan.md` - Architecture and design
- `tasks.md` - Implementation tasks

## Development History

Prompt History Records (PHRs) are maintained in `history/prompts/core-features/`:
1. Backend infrastructure implementation
2. Frontend infrastructure implementation
3. Task priorities and categories
4. Complete implementation with all features

---

Built with Claude Code following Spec-Driven Development (SDD) principles.
