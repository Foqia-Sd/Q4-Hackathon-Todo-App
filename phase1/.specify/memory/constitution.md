<!--
=============================================================================
SYNC IMPACT REPORT
=============================================================================
Version change: 0.0.0 → 1.0.0 (Initial constitution for Phase 1)
Bump rationale: MAJOR - Initial ratification of project constitution

Modified principles: N/A (new constitution)
Added sections:
  - Core Principles (7 principles)
  - Phase 1 Scope & Constraints
  - Mandatory Workflow
  - Governance

Removed sections: N/A

Templates requiring updates:
  ✅ plan-template.md - Constitution Check section will reference these principles
  ✅ spec-template.md - Aligned with functional requirements format
  ✅ tasks-template.md - Aligned with phase-based task organization

Follow-up TODOs: None
=============================================================================
-->

# In-Memory Python Console Todo Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All development MUST follow the strict SDD methodology. No implementation work begins without a completed specification. The workflow is sequential and mandatory:

1. **Constitution** → Establishes project principles and constraints
2. **Specify** → Defines feature requirements and acceptance criteria
3. **Plan** → Documents technical approach and architecture
4. **Tasks** → Breaks down implementation into testable units
5. **Implement** → Executes tasks according to the plan

Skipping or merging steps is prohibited. Each phase produces artifacts that inform the next.

### II. Reusable Intelligence First

Phase 1 work MUST produce reusable artifacts, not throwaway code. Every deliverable serves future phases:

- **Spec templates**: Capture patterns for feature specification
- **Feature patterns**: Document common implementation approaches
- **Agent instructions**: Encode decision-making for AI assistance
- **Architecture decisions**: Record rationale via ADRs

The goal is intelligence capture—knowledge that accelerates future development and reduces rework.

### III. In-Memory Simplicity

Phase 1 operates under intentional constraints to maintain focus:

- **Storage**: In-memory only; no database or file persistence
- **User model**: Single-user; no authentication or authorization
- **Interface**: Python console application; no web or GUI
- **Data lifecycle**: All data exists only for the duration of the session

These constraints are features, not limitations. They enable rapid iteration and clean architecture.

### IV. Minimal Dependencies

The project uses only approved libraries to minimize complexity:

- **Package manager**: `uv` (mandatory for all dependency management)
- **Console output**: `rich` (formatted, colorful terminal output)
- **User input**: `questionary` (interactive CLI prompts and menus)

All dependencies MUST be added via `uv add`. No additional third-party libraries without explicit amendment to this constitution.

### V. Todo Entity Contract

Each todo item MUST conform to this minimal contract:

- **ID**: Unique identifier (system-generated, immutable)
- **Title**: User-provided description (required, non-empty string)
- **Completed**: Boolean status (default: False)

No additional fields in Phase 1. Future phases may extend this contract.

### VI. Complete CRUD Operations

The application MUST support all standard todo management operations:

- **Create**: Add a new todo with a title
- **Read**: View all todos (list) and individual todo details
- **Update**: Modify a todo's title
- **Delete**: Remove a todo permanently
- **Toggle**: Mark a todo as complete or incomplete

Each operation MUST provide clear user feedback and handle edge cases gracefully.

### VII. Clean CLI Experience

The user interface MUST be intuitive and professional:

- Clear menu navigation with `questionary`
- Formatted output using `rich` tables and styling
- Meaningful error messages for invalid operations
- Confirmation prompts for destructive actions (delete)
- Graceful exit handling

## Phase 1 Scope & Constraints

### In Scope

- Python console application with interactive menus
- In-memory todo storage (list or dict)
- Complete CRUD operations for todos
- Clean, formatted console output
- Spec-driven documentation artifacts

### Out of Scope (Deferred to Future Phases)

- Data persistence (database, file storage)
- Multi-user support
- Authentication/authorization
- Web interface or API
- Due dates, priorities, categories, tags
- Search or filtering functionality

### Success Criteria

| Criteria | Measurement |
|----------|-------------|
| Feature completeness | All CRUD operations functional |
| In-memory operation | No file or database I/O |
| CLI quality | Users can complete all operations without confusion |
| SDD compliance | Constitution, spec, plan, tasks artifacts exist |
| Code quality | Clean, readable Python following PEP 8 |

## Mandatory Workflow

### Development Sequence

```
/sp.constitution → /sp.specify → /sp.plan → /sp.tasks → /sp.implement
```

### Phase Gates

Each phase MUST complete before the next begins:

1. **Constitution** (this document) - Ratified and committed
2. **Specification** - Feature spec with user stories and acceptance criteria
3. **Plan** - Technical design with architecture decisions
4. **Tasks** - Ordered task list with dependencies
5. **Implementation** - Code following the task list

### Artifact Locations

```
.specify/memory/constitution.md     # This file
specs/<feature>/spec.md             # Feature specification
specs/<feature>/plan.md             # Implementation plan
specs/<feature>/tasks.md            # Task breakdown
history/prompts/                    # Prompt History Records
history/adr/                        # Architecture Decision Records
```

## Governance

### Amendment Process

1. Propose amendment with rationale
2. Review impact on existing artifacts
3. Update constitution with version increment
4. Propagate changes to dependent templates
5. Commit with descriptive message

### Version Policy

- **MAJOR**: Breaking changes to principles or scope
- **MINOR**: New principles or sections added
- **PATCH**: Clarifications and wording improvements

### Compliance

- All code reviews MUST verify principle adherence
- Deviations require explicit justification in ADR
- Constitution supersedes all other project documentation

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
