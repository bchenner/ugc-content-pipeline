---
name: agent-auditor
description: "Use when someone asks to audit agents, optimize CLAUDE.md files, reduce token usage, check agent quality, find duplication across agents, or improve agent instructions. Also trigger for 'audit my agents', 'optimize the pipeline', 'check agent health'."
argument-hint: "[agent-path or 'all']"
---

# Agent Auditor

Audits and optimizes Claude Code agents in a multi-agent pipeline. Analyzes CLAUDE.md files, measures token costs, finds duplication, checks delegation patterns, verifies consistency, and suggests lazy-loading opportunities.

## When to Use This Skill

Trigger when user:
- Asks to audit, review, or optimize agents
- Wants to reduce token usage or context costs
- Asks about duplication across agents
- Wants to check agent health, quality, or consistency
- Mentions CLAUDE.md optimization
- Asks to find orphaned files or broken references

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

All commands must be run from the skill directory:

```bash
SKILL_DIR="$HOME/.claude/skills/agent-auditor"
cd "$SKILL_DIR"
```

## Commands

### Audit All Agents
```bash
python scripts/run.py audit.py all
```

### Audit a Specific Agent
```bash
python scripts/run.py audit.py /path/to/agent-directory
```

### Audit with Auto-Fix
```bash
python scripts/run.py audit.py all --fix
```

### Save a Markdown Report
```bash
python scripts/run.py audit.py all --report
```

### Machine-Readable JSON Output
```bash
python scripts/run.py audit.py all --json
```

### Combine Flags
```bash
python scripts/run.py audit.py all --report --fix
python scripts/run.py audit.py /path/to/agent --json --fix
```

## Workflow

### Step 1: Discover Agents

If the argument is `all` or empty, the script scans `c:\Users\Privat\Documents\Claude Code\claude-projects\` for all directories containing a CLAUDE.md file. If a specific path is given, it audits only that agent.

Run the audit:
```bash
cd "$HOME/.claude/skills/agent-auditor"
python scripts/run.py audit.py $ARGUMENTS
```

### Step 2: Review Findings

The script outputs findings organized by severity:

| Severity | Meaning |
|----------|---------|
| **CRITICAL** | Must fix. Context bloat, broken references, major issues |
| **WARNING** | Should fix. Duplication, delegation violations, large sections |
| **INFO** | Nice to fix. Orphaned files, lazy-load opportunities, quality tips |
| **OK** | Checks that passed cleanly |

Each finding shows the agent name, the issue, and the recommended fix.

### Step 3: Apply Fixes (if --fix was used)

When `--fix` is passed, the script auto-fixes simple issues:
- Removes trailing whitespace
- Normalizes line endings
- Flags (but does not auto-fix) content issues that need human review

### Step 4: Act on Recommendations

After reviewing the audit output, help the user:
- Move large sections to reference files (lazy loading)
- Extract duplicated content to shared references
- Fix broken file references
- Improve vague instructions
- Remove orphaned files

## Audit Checks

| Check | What It Does |
|-------|-------------|
| **Token Cost** | Counts tokens in CLAUDE.md and reference files. Flags >4000 (warning) and >8000 (critical) |
| **Duplication** | Finds identical or near-identical paragraphs across agents |
| **Reference Files** | Checks that referenced files exist, finds orphaned files |
| **Delegation** | Detects agents doing work they should delegate (prompt blocks, scripts in wrong agents) |
| **Consistency** | Checks product names, IDs, URLs are consistent across agents |
| **Lazy Loading** | Identifies large sections (>500 tokens) that could be moved to reference files |
| **Quality** | Flags vague instructions, missing output formats, missing "what NOT to do" sections |

## Output

Reports are saved to `data/reports/` with timestamp filenames when `--report` is used.

## Tips

- Run `all` first to get a pipeline-wide view before drilling into individual agents
- The `--report` flag saves a markdown file you can share or track over time
- Use `--json` when you want to process results programmatically
- Token counts use tiktoken with cl100k_base encoding (same tokenizer Claude uses)
- The skill auto-creates its virtual environment on first run
