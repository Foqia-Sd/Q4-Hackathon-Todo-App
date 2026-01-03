---
id: 7
title: Define System Consistency Guardian Skill
stage: general
date: 2026-01-01
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: Com Plus
command: System Consistency Guardian Skills...
labels: [setup, skills, qa, integrity, validation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/system-consistency-guardian.skill.md
tests:
 - none
---

## Prompt

System Consistency Guardian
Skills: Contract Drift Detection

Description:
Detect and prevent mismatches between frontend, backend, database, and auth specifications.

Skills: Spec Integrity Enforcement

Description:
Ensure specifications remain the single source of truth throughout implementation.

Skills: Cross-Layer Validation

Description:
Validate that behavior across layers produces consistent and predictable outcomes.

## Response snapshot

I've documented the `System Consistency Guardian` skill in `.claude/skills/system-consistency-guardian.skill.md`.

## Outcome

- ✅ Impact: Defined the contract drift detection and cross-layer validation capabilities.
- 🧪 Tests: n/a
- 📁 Files: `.claude/skills/system-consistency-guardian.skill.md`
- 🔁 Next prompts: none
- 🧠 Reflection: Finalizing the core audit and validation skill to ensure system-wide consistency.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
