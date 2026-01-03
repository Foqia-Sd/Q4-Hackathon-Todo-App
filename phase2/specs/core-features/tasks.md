# Tasks: Phase 2 Core Features

**Input**: Design documents from `/specs/core-features/`
**Prerequisites**: plan.md (required), spec.md (required)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, etc.)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure for backend/ and frontend/ per plan.md
- [ ] T002 Initialize FastAPI project in backend/ and install base dependencies
- [ ] T003 Initialize Next.js project in frontend/ and install base dependencies
- [ ] T004 [P] Configure shared linting and formatting for the workspace
- [ ] T005 Setup environment variable management in backend/.env and frontend/.env.local

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for Authentication and Multi-User Isolation (MUI)

- [ ] T006 [P] Configure Neon PostgreSQL connection in backend/app/core/config.py
- [ ] T007 Initialize database migration framework (Alembic) in backend/
- [ ] T008 [P] Setup Better Auth configuration for Python/FastAPI in backend/app/api/auth.py
- [ ] T009 Create Base Model and Timestamp mixins in backend/app/models/base.py
- [ ] T010 Implement Authentication Middleware/Dependency in backend/app/core/security.py
- [ ] T011 Create centralized user_id dependency for MUI in backend/app/core/mui.py
- [ ] T012 Configure shadcn/ui and primary green theme in frontend/tailwind.config.js
- [ ] T013 Setup API Client and Auth Provider in frontend/src/lib/

---

## Phase 3: User Story 1 - Secure User Authentication (Priority: P1) 🎯 MVP

**Goal**: Allow users to sign up, log in, and log out securely.

**Independent Test**: Register a new user via UI, log out, and log back in successfully.

- [ ] T014 [P] [US1] Create User DB model in backend/app/models/user.py
- [ ] T015 [US1] Implement Signup, Login, and Logout logic in backend/app/api/auth.py
- [ ] T016 [P] [US1] Create Signup and Login UI components in frontend/src/components/auth/
- [ ] T017 [US1] Implement Auth pages (signup/login) in frontend/src/app/auth/
- [ ] T018 [US1] Integrate Frontend Auth services with Backend API in frontend/src/services/auth.ts

---

## Phase 4: User Story 2 - Task CRUD & Ownership (Priority: P1)

**Goal**: Create, Read, Update, and Delete tasks with strict user ownership.

**Independent Test**: Create a task as User A, then verify User B cannot retrieve or modify it via API.

- [ ] T019 [P] [US2] Create Task DB model with user_id FK in backend/app/models/task.py
- [ ] T020 [US2] Implement Task CRUD service with MUI enforcement in backend/app/services/task.py
- [ ] T021 [US2] Create Task API endpoints with MUI dependency in backend/app/api/tasks.py
- [ ] T022 [P] [US2] Create Task List and Task Item UI components in frontend/src/components/tasks/
- [ ] T023 [US2] Implement Task management dashboard in frontend/src/app/dashboard/
- [ ] T024 [US2] Integrate Frontend Task services with Backend API in frontend/src/services/tasks.ts

---

## Phase 5: User Story 3 - Task Priorities & Categories (Priority: P2)

**Goal**: Organise tasks with high/medium/low priority and categories (Work, Home, etc.).

**Independent Test**: Create a task with "High" priority and "Work" category, and verify it persists correctly.

- [ ] T025 [P] [US3] Update Task DB model to include priority and category fields in backend/app/models/task.py
- [ ] T026 [US3] Update Task Pydantic schemas for priorities and categories in backend/app/schemas/task.py
- [ ] T027 [US3] Update Task CRUD logic to handle priorities/categories in backend/app/services/task.py
- [ ] T028 [P] [US3] Add Priority and Category selection to Task creation UI in frontend/src/components/tasks/
- [ ] T029 [US3] Update Task Item UI to display priorities and category tags in frontend/src/components/tasks/

---

## Phase 6: User Story 4 - Search, Filters & Sorting (Priority: P2)

**Goal**: Efficiently find and organize tasks using keyword search, status/priority filters, and sorting.

**Independent Test**: Filter completed tasks and search for a specific keyword; verify results match exactly.

- [ ] T030 [US4] Implement dynamic query filtering (status, priority, tag, search) in backend/app/services/task.py
- [ ] T031 [US4] Update Task API to support filter/search/sort query parameters in backend/app/api/tasks.py
- [ ] T032 [P] [US4] Create SearchBar and FilterPanel UI components in frontend/src/components/dashboard/
- [ ] T033 [US4] Implement sorting logic (alphabetical, priority, due date) in frontend/src/hooks/useTasks.ts
- [ ] T034 [US4] Integrate Search and Filter UI with Task fetching service in frontend/src/app/dashboard/page.tsx

---

## Phase 7: Polish & UX (Priority: P3)

**Purpose**: Enhance the visual appeal, responsiveness, and dark/light theme support.

- [ ] T035 [P] Implement Responsive navigation and mobile-friendly task layout in frontend/src/components/layout/
- [ ] T036 [P] Add Dark/Light mode toggle and theme-specific styling in frontend/src/components/theme-toggle.tsx
- [ ] T037 Refine "Pakistan Flag green" accent styling across all interactive elements
- [ ] T038 Add toast notifications for CRUD and Auth actions in frontend/src/components/ui/use-toast.ts
- [ ] T039 [P] Final API validation and error handling hardening in backend/app/main.py

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 & 2**: MUST complete first to provide structure and authentication foundation.
- **Phase 3 (Auth)**: Pre-requisite for all Dashbord/Task operations.
- **Phase 4 (CRUD)**: Foundation for Phase 5 (Priorities) and Phase 6 (Filter/Search).
- **Phase 7 (Polish)**: Can run concurrently with other phases once core UI is established.

### Parallel Opportunities
- Backend and Frontend development for the same User Story can proceed in parallel once API contracts are defined.
- UI component creation ([P] tasks) can happen concurrently within each phase.
- Setup tasks for Backend and Frontend are independent.
