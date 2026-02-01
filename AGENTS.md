# Agent Instructions

## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: (the agent model's name and attribution byline)
```

## Key Conventions
- **Skill Creation**: ALWAYS load `skill-creator` skill. See `.agents/skills/skill-creator/SKILL.md`
- **Templates**: Clean up unused template example files when creating new skills.
- **Docs Maintenance**: ALWAYS load `agents-md` skill when:
  - Maintaining *this* `AGENTS.md`
  - Writing skills that need to modify or interact with `AGENTS.md` files.

## Skill Design Standards
- **Self-Registration**: Every skill MUST be designed to insert an entry into the target project's `AGENTS.md`.
  - **Required**: Announce existence and specific use cases (e.g., "Use `db-migrate` for schema changes").
  - **Optional**: Include critical context/rules that must always be loaded when the skill is present.

## Local Skills
- **Skill Creator**: Create/update skills. See `.agents/skills/skill-creator/SKILL.md`
- **Agents Docs**: Maintain `AGENTS.md` and guide skill documentation logic. See `.agents/skills/agents-md/SKILL.md`