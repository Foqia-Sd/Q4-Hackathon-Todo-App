# Implementation Plan: AI-Powered Natural Language Todo Control

**Branch**: `1-ai-chat-todo-control` | **Date**: 2026-01-14 | **Spec**: [link](../spec.md)
**Input**: Feature specification from `/specs/1-ai-chat-todo-control/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of AI-powered natural language todo control that allows users to manage tasks through conversational interface. The system will integrate OpenAI Agents SDK to interpret user intent and call backend skills for task operations while preserving all existing functionality. The solution includes a new chat interface accessible from the task dashboard with a sidebar navigation.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript, FastAPI
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, React, BetterAuth
**Storage**: PostgreSQL (Neon), existing database schema
**Testing**: pytest, jest
**Target Platform**: Web application (responsive)
**Project Type**: Full-stack web application with existing frontend and backend
**Performance Goals**: <3s response time for 95% of AI requests, 90% intent recognition accuracy
**Constraints**: Must preserve existing functionality, stateless architecture, no hardcoded AI logic in routes
**Scale/Scope**: Single application serving multiple authenticated users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Preserve Existing Functionality**: ✅ Verified - Plan extends existing backend/frontend without modifying current functionality
- **Stateless Backend Architecture**: ✅ Confirmed - /chat endpoint is stateless, retrieves context per request
- **AI-Powered Task Control**: ✅ Incorporated - OpenAI Agents SDK integrated for natural language processing
- **Chat History Persistence**: ✅ Verified - ChatMessage model designed for database storage
- **Separation of Reasoning and Execution**: ✅ Confirmed - AI agent (reasoning) calls backend skills (execution)
- **Database Access Restrictions**: ✅ Verified - AI agent uses backend services/skills, no direct DB access
- **OpenAI Agents SDK Integration**: ✅ Incorporated - Core component of the design
- **MCP Integration**: ⚠️ Planned - Will implement Model Context Protocol for tool orchestration

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-chat-todo-control/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py      # New: ChatMessage model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py  # New: Chat history management
│   │   └── task_skills.py   # New: Backend skills for AI agent
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py      # New: /chat endpoint
│   │   │   └── router.py
│   │   └── deps.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── todo_agent.py    # New: AI agent implementation
│   └── main.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx    # New: AI chat interface
│   │   ├── Sidebar.jsx          # New: Navigation sidebar
│   │   └── Navbar.jsx           # Updated: Add Chat button
│   ├── pages/
│   │   └── Dashboard.jsx        # Updated: Include chat functionality
│   ├── services/
│   │   └── aiService.js         # New: AI service integration
│   └── utils/
└── public/
```

**Structure Decision**: Web application (frontend + backend) with new AI components integrated alongside existing functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New API endpoint | Required for chat functionality | Would require modifying existing routes |
| New database models | Required for chat history persistence | Cannot reuse existing task models for chat messages |