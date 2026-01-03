# Todo App Phase 2 Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All features, fixes, and refactors must follow the Spec-Plan-Task-Implement cycle. Specifications drive the development process, and no code should be written until the implementation plan is approved.

### II. Multi-User Isolation (MUI)
The system MUST support multiple users where data isolation is strictly enforced at both the application and database layers. A user must never be able to access, modify, or delete tasks belonging to another user.

### III. Stateless Backend Architecture
The FastAPI backend must remain stateless. Authentication and session state should be handled via standard patterns (Better Auth) with the database as the primary persistent store.

### IV. Single Source of Truth
The Neon PostgreSQL database is the definitive source of truth for all application state.

### V. Smallest Viable Diff
Implementation should favor small, testable, and focused changes. Avoid unrelated refactors or feature creep.

## Project Vision
To build a secure, full-stack personal task management system that scales to multiple users using modern web technologies.

## Technology Stack
- **Frontend**: Next.js (React)
- **Backend**: FastAPI (Python)
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth

## Development Workflow
1. **Spec**: Define the feature and requirements in `specs/<feature>/spec.md`.
2. **Plan**: Design the architecture and interfaces in `specs/<feature>/plan.md`.
3. **Tasks**: Create a dependency-ordered task list in `specs/<feature>/tasks.md`.
4. **Implementation**: Execute tasks, maintaining a PHR for every interaction.
5. **Review**: Verify implementation against the spec and tests.

## Governance
This constitution is the primary governing document for Phase 2 development. Amendments must be documented and updated here before being applied to the implementation.

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
