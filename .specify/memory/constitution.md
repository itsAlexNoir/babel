<!--
SYNC IMPACT REPORT
===================
Version Change: Initial → 1.0.0
Rationale: Initial constitution establishment for existing project

Modified Principles: N/A (Initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Technical Stack
  - Development Workflow
  - Governance

Removed Sections: N/A

Templates Status:
  ✅ plan-template.md - No constitution-specific gates found, compatible
  ✅ spec-template.md - User story prioritization aligns with CRUD Operations principle
  ✅ tasks-template.md - Task organization compatible with principles
  ✅ checklist-template.md - Generic structure, no conflicts
  ✅ agent-file-template.md - Generic structure, no conflicts

Follow-up TODOs: None
===================
-->

# Babel Constitution

## Core Principles

### I. Simplicity

The application MUST provide an intuitive interface for managing a personal book collection. All features MUST be discoverable without documentation. The user interface MUST present actions clearly, with explicit buttons for all critical operations.

**Rationale**: Personal library management should be accessible to non-technical users. Complexity creates barriers to consistent usage.

### II. Data Integrity

The system MUST automatically create timestamped backups before any data modification. The system MUST preserve at least the most recent backup. Users MUST have explicit control over backup management through clear UI actions.

**Rationale**: Book catalog data is irreplaceable. Automatic backups prevent data loss while explicit controls prevent accidental operations.

### III. Search & Discovery

The application MUST enable flexible searching across all database fields. Searches MUST be case-insensitive. Results MUST update dynamically as users type.

**Rationale**: Users remember books by different attributes (author, title, tags). Flexible search ensures discoverability.

### IV. CRUD Operations

The system MUST support complete entry lifecycle management:
- Create: Add new book entries with all relevant fields
- Read: View entire library or search results
- Update: Edit existing entries with validation
- Delete: Remove single or multiple entries with confirmation

**Rationale**: Complete lifecycle support ensures the system adapts to collection changes over time.

### V. User Control

All critical operations (save, reload, clear backups) MUST be triggered by explicit user actions via buttons. The system MUST NOT perform destructive operations automatically without user confirmation.

**Rationale**: Explicit control prevents accidental data loss and gives users confidence in system behavior.

### VI. Minimal Dependencies

The project MUST use only essential libraries. Dependencies MUST be pinned to specific versions. Any new dependency MUST be justified by demonstrable value that cannot be achieved with existing tools.

Current approved dependencies:
- `streamlit` - Web UI framework
- `pandas` - Data manipulation
- `rich` - Terminal logging

**Rationale**: Fewer dependencies reduce maintenance burden, security surface, and installation complexity.

### VII. Spanish-First UX

The user interface MUST be in Spanish. Code, documentation, and technical artifacts MUST be in English. Comments explaining domain logic MAY be in Spanish when clarifying business context.

**Rationale**: The application serves Spanish-speaking users. English technical artifacts ensure broader maintainability.

## Technical Stack

**Language**: Python 3.13+  
**Framework**: Streamlit (>=1.48.1)  
**Data Storage**: CSV files with pandas  
**Logging**: Rich console  
**Testing**: pytest (when applicable)  
**Package Management**: uv / pip

**Architecture Pattern**: Single-file Streamlit app with modular Library class

## Development Workflow

### Adding Features

1. Features MUST be documented in user-facing terms (what users can do)
2. Changes affecting data schema MUST be backward compatible or include migration
3. UI changes MUST maintain Spanish language for user-facing text
4. All CRUD operations MUST create backups automatically

### Code Organization

- Main application logic resides in `main.py`
- Library business logic in `src/library.py`
- Database files in `databases/`
- Automatic backups in `databases/backups/`

### Quality Gates

- Code MUST run without errors on Python 3.13+
- Database operations MUST preserve data integrity
- UI actions MUST provide clear feedback to users
- Backup system MUST function before any write operation

## Governance

This constitution establishes the foundational principles for Babel development. All features, refactors, and changes MUST align with these principles.

### Amendment Process

1. Propose changes with rationale documenting which principle is being modified or added
2. Document impact on existing features and templates
3. Update version number following semantic versioning:
   - MAJOR: Removing/redefining principles (backward incompatible)
   - MINOR: Adding new principles or sections
   - PATCH: Clarifications, wording improvements
4. Update constitution file and propagate changes to dependent templates

### Compliance

- All feature specifications MUST reference relevant principles
- Implementation plans MUST demonstrate principle adherence
- Complexity that violates principles MUST be explicitly justified

**Version**: 1.0.0 | **Ratified**: 2026-01-31 | **Last Amended**: 2026-01-31
