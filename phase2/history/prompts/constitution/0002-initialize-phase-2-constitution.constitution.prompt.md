---
id: 2
title: Initialize Phase 2 Constitution
stage: constitution
date: 2026-01-01
surface: agent
model: opus-4.5
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: [constitution, initialization, sdd]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

You are working on Phase 2 of a Todo App using Spec-Driven Development.

Scope:

- Full-stack web application

Tech stack (fixed):
- Frontend: Next.js (React already install)
- Backend: FastAPI (Python)
- Database: Neon PostgreSQL
- Authentication: Better Auth
- Environment variables already set in backend .env
- Project structure:
  phase2/
    frontend/
    backend/

Rules:
- Multi-user system is mandatory
- Each user can only access their own tasks
- Backend must be stateless
- Database is the source of truth
- Specs must drive implementation (no coding yet)
- Keep specs clear, and implementation-ready


Acknowledge when ready.

## Response snapshot

I have initialized the Project Constitution for Phase 2.

**Success Criteria:** Provide helpful guidance and execute tasks based on your intent while adhering to SDD principles.
**Current Surface:** Agent
**Working Directory:** `C:\Users\Com Plus\Desktop\todo\phase2`

## Outcome

- ✅ Impact: Established the core governing principles and tech stack for Phase 2.
- 🧪 Tests: n/a
- 📁 Files: `.specify/memory/constitution.md`
- 🔁 Next prompts: Start defining the initial feature spec.
- 🧠 Reflection: Successfully encoded user requirements into a formal constitution document.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
