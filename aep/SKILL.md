---
name: aep
description: API design system in the AEP (API Enhancement Proposals) collection. AEPs provide high-level, concise documentation for API development, serving as the source of truth for consistent, intuitive, and machine-readable API designs. Use this skill when designing, reviewing, or implementing APIs to ensure compliance with these established standards.
---

# AEP (API Enhancement Proposals) Skill

## Overview

AEPs (API Enhancement Proposals) are the authoritative design standards for APIs. They ensure consistency, intuitiveness, and long-term stability across all services.

**Rule of Thumb:** AEPs are numbered by importance. **Lower numbers are more fundamental.**
- **< 100:** Meta-policies and governance.
- **100-199:** **CORE STANDARDS.** Every API developer must know these.
- **200+:** Specific patterns and edge cases.

## AEP Index

### 📌 Core Resource Design (Start Here)
*Defines the fundamental shape of the API.*
- **AEP-121:** Resource-oriented design (The data model: Resources vs Collections)
- **AEP-122:** Resource names (URL structure, formatting)
- **AEP-124:** Resource association (Relationships between resources)
- **AEP-101:** OpenAPI (Specification standards)
- **AEP-102:** APIs and API terminology
- **AEP-126:** Enumerations
- **AEP-127:** HTTP and gRPC Transcoding

### 🛠️ Standard Methods (The "CRUD")
*Every resource should support these standard interactions unless impossible.*
- **AEP-130:** Methods (General guidance)
- **AEP-131:** **Get** (Retrieving a single resource)
- **AEP-132:** **List** (Listing collections, includes pagination)
- **AEP-133:** **Create** (Creating new resources)
- **AEP-134:** **Update** (Updating resources, `update_mask`)
- **AEP-135:** **Delete** (Deleting resources)

### ⚡ Advanced Methods
- **AEP-136:** Custom methods (Verbs beyond CRUD, e.g., `Cancel`, `Undelete`)
- **AEP-137:** Apply (Declarative configuration updates)

### 📋 Fields & Data Types
*Naming conventions and data formats.*
- **AEP-140:** Field names (Snake_case, reserved words)
- **AEP-141:** Quantities (Units, measurements)
- **AEP-142:** Time and duration (Timestamp formats)
- **AEP-143:** Standardized codes (IETF/ISO standards)
- **AEP-144:** Array fields (Repeated fields)
- **AEP-145:** Ranges (Start/end intervals)
- **AEP-146:** Generic fields (Any, Struct)
- **AEP-148:** Standard fields (`name`, `create_time`, `update_time`, `display_name`)

### 🧩 Common Patterns & Features
- **AEP-158:** **Pagination** (Page tokens, page size)
- **AEP-151:** Long-running operations (Async tasks)
- **AEP-193:** **Errors** (Status codes, error details)
- **AEP-154:** Preconditions (ETags, concurrency)
- **AEP-155:** Idempotency (Request IDs)
- **AEP-156:** Singleton resources (Config, Settings)
- **AEP-157:** Partial responses (Field selection)
- **AEP-159:** Reading across collections ("List all books in all libraries")
- **AEP-160:** Filtering (Filter syntax)
- **AEP-161:** Field masks (Partial updates)
- **AEP-162:** Resource Revisions
- **AEP-164:** Soft delete

### 📚 Documentation & Compatibility
- **AEP-180:** Protobuf Backwards compatibility
- **AEP-191:** File and directory structure
- **AEP-192:** Documentation (Comments, formatting)

### 🔍 Specific Patterns (200+)
- **AEP-203:** Field behavior documentation (Required, Output Only)
- **AEP-210:** Unicode
- **AEP-211:** Authorization checks
- **AEP-213:** Common components
- **AEP-214:** Resource expiration (TTL)
- **AEP-216:** States (Enums for lifecycle)
- **AEP-217:** Unreachable resources

### 📦 Batch Operations
- **AEP-231:** Batch Get
- **AEP-233:** Batch Create
- **AEP-234:** Batch Update
- **AEP-235:** Batch Delete

### 🏛️ Meta & Governance
- **AEP-1:** Purpose and Guidelines
- **AEP-5:** Designing an API (The process)
- **AEP-300:** AEP Editions

## How to Use

1.  **Identify the Requirement:** e.g., "I need to add a 'status' field."
2.  **Find the Rule:** Search the index above. "AEP-216: States" looks relevant.
3.  **Read the Standard:**
    - The content is located in: `references/aep/general/<NUMBER>/aep.md.j2`
    - *Example:* To read about Standard Fields, check `references/aep/general/0148/aep.md.j2`
4.  **Verify:** Ensure your implementation matches the spec exactly (naming, behavior, types).

**Pro Tip:** Use `grep` to search across all AEPs if the index isn't enough:
`grep -r "my search term" .agents/skills/aep/references/aep/general`
