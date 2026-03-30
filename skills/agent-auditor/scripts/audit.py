#!/usr/bin/env python3
"""
Agent Auditor - Audits and optimizes Claude Code agents in a multi-agent pipeline.

Analyzes CLAUDE.md files, measures token costs, finds duplication, checks delegation
patterns, verifies consistency, and suggests lazy-loading opportunities.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import tiktoken

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PROJECTS_DIR = r"c:\Users\Privat\Documents\Claude Code\claude-projects"
ENCODING_NAME = "cl100k_base"
TOKEN_WARNING_THRESHOLD = 4000
TOKEN_CRITICAL_THRESHOLD = 8000
LAZY_LOAD_TOKEN_THRESHOLD = 500
MIN_PARAGRAPH_WORDS = 50
SIMILARITY_THRESHOLD = 0.85

# Severity levels
CRITICAL = "CRITICAL"
WARNING = "WARNING"
INFO = "INFO"
OK = "OK"

# Directories to skip when scanning for reference files
SKIP_DIRS = {".venv", "node_modules", "__pycache__", ".git", ".cache", "backup", "data"}

# Extensions to count as reference files
REFERENCE_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".ts",
    ".csv", ".toml", ".cfg", ".ini", ".sh", ".bat",
}


# ---------------------------------------------------------------------------
# Token Counting
# ---------------------------------------------------------------------------

def count_tokens(text: str, encoding) -> int:
    """Count tokens in text using tiktoken."""
    try:
        return len(encoding.encode(text))
    except Exception:
        # Fallback: rough estimate (1 token ~ 4 chars)
        return len(text) // 4


def read_file_safe(path: Path) -> str:
    """Read a file, handling encoding issues gracefully."""
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""


# ---------------------------------------------------------------------------
# Agent Discovery
# ---------------------------------------------------------------------------

def discover_agents(target: str) -> list[dict]:
    """
    Discover agents to audit.
    Returns list of dicts: { 'name': str, 'path': Path, 'claude_md': Path }
    """
    agents = []

    if target.lower() == "all" or target == "":
        projects_dir = Path(DEFAULT_PROJECTS_DIR)
        if not projects_dir.exists():
            print(f"Projects directory not found: {projects_dir}")
            sys.exit(1)

        for entry in sorted(projects_dir.iterdir()):
            if entry.is_dir():
                claude_md = entry / "CLAUDE.md"
                if claude_md.exists():
                    agents.append({
                        "name": entry.name,
                        "path": entry,
                        "claude_md": claude_md,
                    })
    else:
        target_path = Path(target)
        if not target_path.exists():
            print(f"Path not found: {target_path}")
            sys.exit(1)

        claude_md = target_path / "CLAUDE.md"
        if not claude_md.exists():
            print(f"No CLAUDE.md found in: {target_path}")
            sys.exit(1)

        agents.append({
            "name": target_path.name,
            "path": target_path,
            "claude_md": claude_md,
        })

    return agents


# ---------------------------------------------------------------------------
# Reference File Discovery
# ---------------------------------------------------------------------------

def find_referenced_paths(claude_md_text: str) -> set[str]:
    """Extract file paths referenced in CLAUDE.md (backtick paths and markdown links)."""
    refs = set()

    # Identify code block ranges to skip backticks inside them
    code_block_ranges = []
    for m in re.finditer(r'```[\w]*\n.*?```', claude_md_text, re.DOTALL):
        code_block_ranges.append((m.start(), m.end()))

    # Backtick paths: `path/to/file.ext` or `../agent/file.md`
    for match in re.finditer(r'`([^`\n]{3,80})`', claude_md_text):
        candidate = match.group(1)
        # Skip backticks inside code blocks
        in_code_block = any(start <= match.start() < end for start, end in code_block_ranges)
        if in_code_block:
            continue
        # Skip backticks inside markdown table rows (documentation examples)
        line_start = claude_md_text.rfind('\n', 0, match.start()) + 1
        line_end = claude_md_text.find('\n', match.end())
        if line_end == -1:
            line_end = len(claude_md_text)
        line = claude_md_text[line_start:line_end]
        if line.strip().startswith('|') and line.strip().endswith('|'):
            continue
        # Must look like a file path (has extension or slash)
        if ('/' in candidate or '\\' in candidate or '.' in candidate):
            # Filter out code snippets, URLs, commands, non-path content
            if not candidate.startswith(('http', 'npm ', 'pip ', 'git ', 'python ', '/')):
                if not candidate.startswith('{') and not candidate.startswith('['):
                    # Skip template patterns with braces like {NN}, {product}
                    if '{' in candidate:
                        continue
                    # Skip bare extensions like .json, .txt, .md, .nbflow
                    if re.match(r'^\.\w+$', candidate):
                        continue
                    # Skip quoted strings (contain spaces + quotes)
                    if '"' in candidate:
                        continue
                    # Skip property-like strings (contain colons)
                    if ':' in candidate:
                        continue
                    # Skip strings that are clearly code/config, not file paths
                    if '=' in candidate or '(' in candidate or ')' in candidate:
                        continue
                    # Skip API endpoints and HTTP methods
                    if candidate.upper().startswith(('GET ', 'POST ', 'PUT ', 'DELETE ', 'PATCH ')):
                        continue
                    # Skip JSON-style dot notation (e.g., graphData.links, output.links)
                    if re.match(r'^[a-zA-Z_]+\.[a-zA-Z_]+$', candidate) and '/' not in candidate:
                        continue
                    # Must have a recognizable file extension or directory slash
                    has_extension = bool(re.search(r'\.\w{1,6}$', candidate))
                    has_slash = '/' in candidate or '\\' in candidate
                    if has_extension or has_slash:
                        # Skip namespace-style identifiers (e.g., nanobanana/Prompt)
                        # that have a slash but no extension (not real file paths)
                        if has_slash and not has_extension:
                            # Only include if it looks like a directory path (no uppercase after slash)
                            parts = candidate.replace('\\', '/').split('/')
                            last_part = parts[-1] if parts else ""
                            if last_part and last_part[0].isupper() and '.' not in last_part:
                                continue
                        refs.add(candidate)

    # Markdown links: [text](path)
    for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', claude_md_text):
        path = match.group(2)
        if not path.startswith(('http', 'mailto:', '#')):
            # Skip template patterns
            if '{' not in path:
                refs.add(path)

    return refs


def find_agent_files(agent_path: Path) -> list[Path]:
    """Find all non-CLAUDE.md files in the agent directory that could be references."""
    files = []
    for root, dirs, filenames in os.walk(agent_path):
        root_path = Path(root)
        # Skip uninteresting directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in filenames:
            fpath = root_path / fname
            if fpath.name == "CLAUDE.md":
                continue
            if fpath.suffix.lower() in REFERENCE_EXTENSIONS:
                files.append(fpath)
    return files


def check_reference_files(agent: dict, claude_md_text: str, encoding) -> tuple[list[dict], list[dict]]:
    """
    Check referenced files and find orphans.
    Returns (findings, ref_file_stats).
    """
    findings = []
    ref_file_stats = []
    agent_path = agent["path"]

    referenced_paths = find_referenced_paths(claude_md_text)
    actual_files = find_agent_files(agent_path)
    actual_relative = set()

    for f in actual_files:
        try:
            rel = f.relative_to(agent_path)
            actual_relative.add(str(rel).replace("\\", "/"))
        except ValueError:
            pass

    # Check if referenced files exist
    for ref in sorted(referenced_paths):
        # Try resolving relative to agent path
        resolved = agent_path / ref.replace("/", os.sep)
        if resolved.exists() and resolved.is_file():
            text = read_file_safe(resolved)
            tokens = count_tokens(text, encoding)
            ref_file_stats.append({
                "path": str(resolved),
                "relative": ref,
                "tokens": tokens,
            })
        elif resolved.exists() and resolved.is_dir():
            # Directory reference -- valid, just skip (no token counting for dirs)
            pass
        else:
            # Could be a relative path like ../other-agent/
            # Only flag files that look like they should be in this agent's tree
            if not ref.startswith("..") and not ref.startswith("~/"):
                # Skip directory-style references (ending in /)
                if ref.endswith("/"):
                    continue
                findings.append({
                    "severity": WARNING,
                    "check": "Reference Files",
                    "message": f"Referenced path does not exist: `{ref}`",
                    "fix": f"Remove the reference or create the file at {ref}",
                })

    # Find orphaned files (exist but not referenced)
    referenced_normalized = set()
    for ref in referenced_paths:
        # Normalize: strip leading ./ and convert slashes
        normalized = ref.lstrip("./").replace("\\", "/")
        referenced_normalized.add(normalized)

    # Directories that contain working artifacts, not agent references
    ORPHAN_SKIP_PREFIXES = (
        "projects/", "output/", "research/", "content-plans/",
        "scripts/", "data/", "backup/", "temp/", "tmp/",
    )

    for f in actual_files:
        try:
            rel = str(f.relative_to(agent_path)).replace("\\", "/")
        except ValueError:
            continue

        # Skip common non-reference files
        if any(part.startswith(".") for part in Path(rel).parts):
            continue
        if any(rel.startswith(prefix) for prefix in ORPHAN_SKIP_PREFIXES):
            continue

        if rel not in referenced_normalized:
            text = read_file_safe(f)
            tokens = count_tokens(text, encoding)
            if tokens > 100:  # Only flag files with meaningful content
                findings.append({
                    "severity": INFO,
                    "check": "Reference Files",
                    "message": f"Orphaned file ({tokens} tokens): {rel}",
                    "fix": f"Reference it in CLAUDE.md or remove if unused",
                })

    return findings, ref_file_stats


# ---------------------------------------------------------------------------
# Token Cost Analysis
# ---------------------------------------------------------------------------

def check_token_cost(agent: dict, claude_md_text: str, ref_file_stats: list[dict], encoding) -> list[dict]:
    """Analyze token costs for the agent."""
    findings = []
    claude_md_tokens = count_tokens(claude_md_text, encoding)
    ref_tokens = sum(r["tokens"] for r in ref_file_stats)
    total_tokens = claude_md_tokens + ref_tokens

    if claude_md_tokens >= TOKEN_CRITICAL_THRESHOLD:
        findings.append({
            "severity": CRITICAL,
            "check": "Token Cost",
            "message": f"CLAUDE.md is {claude_md_tokens:,} tokens (threshold: {TOKEN_CRITICAL_THRESHOLD:,})",
            "fix": "Move large sections (tables, examples, detailed instructions) to separate reference files",
        })
    elif claude_md_tokens >= TOKEN_WARNING_THRESHOLD:
        findings.append({
            "severity": WARNING,
            "check": "Token Cost",
            "message": f"CLAUDE.md is {claude_md_tokens:,} tokens (threshold: {TOKEN_WARNING_THRESHOLD:,})",
            "fix": "Consider moving infrequently-used sections to reference files for lazy loading",
        })

    return findings


# ---------------------------------------------------------------------------
# Duplication Detection
# ---------------------------------------------------------------------------

def extract_paragraphs(text: str) -> list[str]:
    """Extract meaningful paragraphs (50+ words) from text."""
    paragraphs = []
    # Split on double newlines or heading boundaries
    blocks = re.split(r'\n\s*\n', text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Skip headings, tables, code blocks
        if block.startswith('#') or block.startswith('|') or block.startswith('```'):
            continue
        # Normalize whitespace
        normalized = " ".join(block.split())
        words = normalized.split()
        if len(words) >= MIN_PARAGRAPH_WORDS:
            paragraphs.append(normalized)

    return paragraphs


def normalize_for_comparison(text: str) -> str:
    """Normalize text for comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join(text.split())
    return text


def simple_similarity(a: str, b: str) -> float:
    """
    Simple word-overlap similarity (Jaccard-like).
    Returns float 0.0..1.0.
    """
    words_a = set(a.split())
    words_b = set(b.split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


def check_duplication(agents: list[dict], agent_texts: dict[str, str]) -> list[dict]:
    """Find duplicated paragraphs across agents."""
    findings = []

    # Extract paragraphs per agent
    agent_paragraphs = {}
    for agent in agents:
        name = agent["name"]
        text = agent_texts.get(name, "")
        agent_paragraphs[name] = extract_paragraphs(text)

    # Compare all pairs
    # Track: normalized_paragraph -> set of agent names
    paragraph_locations = defaultdict(set)

    for name, paragraphs in agent_paragraphs.items():
        for para in paragraphs:
            normalized = normalize_for_comparison(para)
            paragraph_locations[normalized].add(name)

    # Also check near-duplicates via similarity
    all_normalized = []
    for name, paragraphs in agent_paragraphs.items():
        for para in paragraphs:
            normalized = normalize_for_comparison(para)
            all_normalized.append((name, para, normalized))

    # Check cross-agent similarity (only compare across different agents)
    seen_pairs = set()
    for i, (name_a, para_a, norm_a) in enumerate(all_normalized):
        for j, (name_b, para_b, norm_b) in enumerate(all_normalized):
            if i >= j or name_a == name_b:
                continue
            pair_key = (min(name_a, name_b), max(name_a, name_b), min(norm_a[:50], norm_b[:50]))
            if pair_key in seen_pairs:
                continue

            sim = simple_similarity(norm_a, norm_b)
            if sim >= SIMILARITY_THRESHOLD:
                seen_pairs.add(pair_key)
                paragraph_locations[norm_a].add(name_a)
                paragraph_locations[norm_a].add(name_b)

    # Report paragraphs in 2+ agents
    reported = set()
    for normalized, agent_names in paragraph_locations.items():
        if len(agent_names) >= 2:
            preview = normalized[:100] + "..." if len(normalized) > 100 else normalized
            if preview in reported:
                continue
            reported.add(preview)

            severity = WARNING if len(agent_names) >= 3 else INFO
            findings.append({
                "severity": severity,
                "check": "Duplication",
                "message": f'Duplicate content in {len(agent_names)} agents ({", ".join(sorted(agent_names))}): "{preview}"',
                "fix": "Move shared content to a common reference file and link from each agent",
            })

    return findings


# ---------------------------------------------------------------------------
# Delegation Pattern Check
# ---------------------------------------------------------------------------

def check_delegation(agent: dict, claude_md_text: str) -> list[dict]:
    """Check for delegation violations: agents doing work they should delegate."""
    findings = []
    name = agent["name"].lower()

    # Detect JSON prompt blocks in non-prompter agents
    if "prompter" not in name:
        # Look for JSON-like prompt structures
        json_blocks = re.findall(
            r'```json\s*\n\s*\{[^}]*(?:subject|photography|background|face|hair|clothing)[^}]*\}',
            claude_md_text,
            re.IGNORECASE | re.DOTALL,
        )
        if json_blocks:
            findings.append({
                "severity": WARNING,
                "check": "Delegation",
                "message": f"Found {len(json_blocks)} JSON prompt block(s) in a non-prompter agent",
                "fix": "Delegate prompt creation to the appropriate Prompter agent instead",
            })

    # Detect script/dialogue in non-script-writer agents
    if "script" not in name and "writer" not in name:
        dialogue_patterns = re.findall(
            r'(?:^|\n)(?:HOOK|SCENE|CTA|OPENER|CLOSER)\s*[:]\s*.{20,}',
            claude_md_text,
            re.IGNORECASE,
        )
        if dialogue_patterns:
            findings.append({
                "severity": WARNING,
                "check": "Delegation",
                "message": f"Found {len(dialogue_patterns)} script/dialogue block(s) in a non-script agent",
                "fix": "Delegate script writing to the Script Writer agent",
            })

    # Detect strategy content in non-strategist agents
    if "strateg" not in name:
        strategy_patterns = re.findall(
            r'(?:audience\s+research|competitor\s+analysis|market\s+positioning|content\s+strategy)',
            claude_md_text,
            re.IGNORECASE,
        )
        # Only flag if there are detailed strategy sections, not just references
        if len(strategy_patterns) >= 3:
            findings.append({
                "severity": INFO,
                "check": "Delegation",
                "message": f"Found {len(strategy_patterns)} strategy-related sections in a non-strategist agent",
                "fix": "Consider whether this content belongs in the Strategist agent",
            })

    if not findings:
        findings.append({
            "severity": OK,
            "check": "Delegation",
            "message": "Delegation patterns look clean",
            "fix": "",
        })

    return findings


# ---------------------------------------------------------------------------
# Consistency Check
# ---------------------------------------------------------------------------

def extract_key_terms(text: str) -> dict[str, list[str]]:
    """Extract key terms: spreadsheet IDs, URLs, product names, brand names."""
    terms = {}

    # Spreadsheet IDs (long alphanumeric strings)
    sheet_ids = re.findall(r'[A-Za-z0-9_-]{30,60}', text)
    if sheet_ids:
        terms["spreadsheet_ids"] = sheet_ids

    # URLs
    urls = re.findall(r'https?://[^\s\)]+', text)
    if urls:
        terms["urls"] = urls

    # Product/brand names: capitalized multi-word names near "product", "brand"
    product_matches = re.findall(
        r'(?:product|brand)[:\s]+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)',
        text,
    )
    if product_matches:
        terms["products"] = product_matches

    return terms


def check_consistency(agents: list[dict], agent_texts: dict[str, str]) -> list[dict]:
    """Check consistency of key terms across agents."""
    findings = []

    all_terms = {}
    for agent in agents:
        name = agent["name"]
        text = agent_texts.get(name, "")
        all_terms[name] = extract_key_terms(text)

    # Check spreadsheet IDs consistency
    all_sheet_ids = defaultdict(set)
    for name, terms in all_terms.items():
        for sid in terms.get("spreadsheet_ids", []):
            all_sheet_ids[sid].add(name)

    # If a spreadsheet ID appears in some agents but not others that reference sheets
    sheet_agents = {name for name, terms in all_terms.items() if terms.get("spreadsheet_ids")}
    if len(sheet_agents) > 1:
        id_sets = defaultdict(set)
        for name in sheet_agents:
            for sid in all_terms[name].get("spreadsheet_ids", []):
                id_sets[name].add(sid)
        # Check for mismatches (different IDs for same purpose)
        unique_ids = set()
        for name, ids in id_sets.items():
            unique_ids.update(ids)
        if len(unique_ids) > len(sheet_agents):
            findings.append({
                "severity": INFO,
                "check": "Consistency",
                "message": f"Multiple spreadsheet IDs found across agents: {len(unique_ids)} unique IDs in {len(sheet_agents)} agents",
                "fix": "Verify all agents reference the correct spreadsheet IDs",
            })

    if not findings:
        findings.append({
            "severity": OK,
            "check": "Consistency",
            "message": "Key terms appear consistent across the pipeline",
            "fix": "",
        })

    return findings


# ---------------------------------------------------------------------------
# Lazy Loading Opportunities
# ---------------------------------------------------------------------------

def check_lazy_loading(agent: dict, claude_md_text: str, encoding) -> list[dict]:
    """Identify large sections in CLAUDE.md that could be moved to reference files."""
    findings = []

    # Split into sections by headings
    sections = re.split(r'(^#{1,3}\s+.+$)', claude_md_text, flags=re.MULTILINE)

    current_heading = None
    current_content = ""
    line_offset = 0

    for part in sections:
        if re.match(r'^#{1,3}\s+', part):
            # Process previous section
            if current_heading and current_content.strip():
                tokens = count_tokens(current_content, encoding)
                if tokens >= LAZY_LOAD_TOKEN_THRESHOLD:
                    findings.append({
                        "severity": INFO,
                        "check": "Lazy Loading",
                        "message": f'Section "{current_heading.strip()}" is {tokens:,} tokens',
                        "fix": f"Move to a reference file (e.g., reference/{current_heading.strip().lower().replace(' ', '-')}.md) and link from CLAUDE.md",
                    })
            current_heading = part.strip().lstrip('#').strip()
            current_content = ""
        else:
            current_content += part

    # Check last section
    if current_heading and current_content.strip():
        tokens = count_tokens(current_content, encoding)
        if tokens >= LAZY_LOAD_TOKEN_THRESHOLD:
            findings.append({
                "severity": INFO,
                "check": "Lazy Loading",
                "message": f'Section "{current_heading.strip()}" is {tokens:,} tokens',
                "fix": f"Move to a reference file and link from CLAUDE.md",
            })

    # Check for large tables
    table_blocks = re.finditer(
        r'((?:^\|.+\|$\n?){4,})',
        claude_md_text,
        re.MULTILINE,
    )
    for match in table_blocks:
        table_text = match.group(1)
        tokens = count_tokens(table_text, encoding)
        if tokens >= LAZY_LOAD_TOKEN_THRESHOLD:
            line_num = claude_md_text[:match.start()].count('\n') + 1
            findings.append({
                "severity": INFO,
                "check": "Lazy Loading",
                "message": f"Large table at line ~{line_num} ({tokens:,} tokens)",
                "fix": "Consider moving this table to a reference file if it is not always needed",
            })

    # Check for large code blocks
    code_blocks = re.finditer(
        r'```[\w]*\n(.+?)```',
        claude_md_text,
        re.DOTALL,
    )
    for match in code_blocks:
        code_text = match.group(1)
        tokens = count_tokens(code_text, encoding)
        if tokens >= LAZY_LOAD_TOKEN_THRESHOLD:
            line_num = claude_md_text[:match.start()].count('\n') + 1
            findings.append({
                "severity": INFO,
                "check": "Lazy Loading",
                "message": f"Large code block at line ~{line_num} ({tokens:,} tokens)",
                "fix": "Move to a separate reference/example file if not always needed",
            })

    return findings


# ---------------------------------------------------------------------------
# Instruction Quality
# ---------------------------------------------------------------------------

VAGUE_PATTERNS = [
    (r'\bdo\s+good\s+work\b', "do good work"),
    (r'\bbe\s+careful\b', "be careful"),
    (r'\buse\s+best\s+practices\b', "use best practices"),
    (r'\bfollow\s+standards\b', "follow standards"),
    (r'\bdo\s+your\s+best\b', "do your best"),
    (r'\bensure\s+quality\b', "ensure quality"),
    (r'\bmake\s+sure\s+it\s*(?:\'s|is)\s+good\b', "make sure it's good"),
    (r'\bhandle\s+(?:it|this)\s+appropriately\b', "handle it appropriately"),
    (r'\buse\s+common\s+sense\b', "use common sense"),
    (r'\bdo\s+what\s*(?:\'s|is)\s+right\b', "do what's right"),
]


def check_quality(agent: dict, claude_md_text: str) -> list[dict]:
    """Check instruction quality in CLAUDE.md."""
    findings = []

    # Check for vague instructions
    for pattern, label in VAGUE_PATTERNS:
        matches = re.findall(pattern, claude_md_text, re.IGNORECASE)
        if matches:
            findings.append({
                "severity": INFO,
                "check": "Quality",
                "message": f'Vague instruction found: "{label}"',
                "fix": "Replace with specific, measurable instructions",
            })

    # Check for output format specifications
    has_output_format = bool(re.search(
        r'(?:output\s+format|response\s+format|return\s+format|file\s+naming|folder\s+structure)',
        claude_md_text,
        re.IGNORECASE,
    ))
    if not has_output_format:
        findings.append({
            "severity": INFO,
            "check": "Quality",
            "message": "No output format specification found",
            "fix": "Add a section specifying expected output formats, file naming, or response structure",
        })

    # Check for "What NOT to do" sections
    has_not_section = bool(re.search(
        r'(?:what\s+not\s+to|do\s+not|don\'t|never|avoid|important\s*:?\s*(?:never|do\s+not))',
        claude_md_text,
        re.IGNORECASE,
    ))
    if not has_not_section:
        findings.append({
            "severity": INFO,
            "check": "Quality",
            "message": 'No "what NOT to do" guardrails found',
            "fix": 'Add explicit boundaries: what the agent should NOT do, common mistakes to avoid',
        })

    # Check for delegation rules (in non-leaf agents)
    has_delegation = bool(re.search(
        r'(?:delegat|handoff|pass\s+to|send\s+to|forward\s+to)',
        claude_md_text,
        re.IGNORECASE,
    ))
    # Only flag if the agent seems to be a coordinator (references other agents)
    references_other_agents = bool(re.search(
        r'(?:agent|prompter|writer|planner|scanner|strategist)',
        claude_md_text,
        re.IGNORECASE,
    ))
    if references_other_agents and not has_delegation:
        findings.append({
            "severity": WARNING,
            "check": "Quality",
            "message": "References other agents but has no delegation rules",
            "fix": "Add explicit delegation rules: what to pass, what to expect back",
        })

    if not findings:
        findings.append({
            "severity": OK,
            "check": "Quality",
            "message": "Instruction quality checks passed",
            "fix": "",
        })

    return findings


# ---------------------------------------------------------------------------
# Auto-Fix
# ---------------------------------------------------------------------------

def apply_fixes(agent: dict, claude_md_text: str) -> tuple[str, list[str]]:
    """Apply auto-fixes to CLAUDE.md. Returns (fixed_text, list_of_changes)."""
    changes = []
    fixed = claude_md_text

    # Fix 1: Remove trailing whitespace on lines
    lines = fixed.split('\n')
    new_lines = []
    trailing_count = 0
    for line in lines:
        stripped = line.rstrip()
        if stripped != line:
            trailing_count += 1
        new_lines.append(stripped)

    if trailing_count > 0:
        fixed = '\n'.join(new_lines)
        changes.append(f"Removed trailing whitespace from {trailing_count} lines")

    # Fix 2: Normalize multiple blank lines to max 2
    original_fixed = fixed
    fixed = re.sub(r'\n{4,}', '\n\n\n', fixed)
    if fixed != original_fixed:
        changes.append("Normalized excessive blank lines")

    # Fix 3: Ensure file ends with single newline
    if not fixed.endswith('\n'):
        fixed += '\n'
        changes.append("Added missing trailing newline")
    elif fixed.endswith('\n\n'):
        fixed = fixed.rstrip('\n') + '\n'
        changes.append("Normalized trailing newlines")

    return fixed, changes


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_report(
    agents: list[dict],
    all_findings: dict[str, list[dict]],
    agent_stats: dict[str, dict],
    pipeline_stats: dict,
) -> str:
    """Generate a markdown report."""
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("# Agent Audit Report")
    lines.append(f"\nDate: {now}")
    lines.append(f"Agents scanned: {len(agents)}")
    lines.append(f"Total pipeline tokens: {pipeline_stats['total_tokens']:,}")
    lines.append("")

    for agent in agents:
        name = agent["name"]
        stats = agent_stats.get(name, {})
        findings = all_findings.get(name, [])

        lines.append(f"## {name}")
        lines.append(f"\n- **Path**: `{agent['path']}`")
        lines.append(f"- **CLAUDE.md tokens**: {stats.get('claude_md_tokens', 0):,}")
        lines.append(f"- **Reference files**: {stats.get('ref_file_count', 0)} files, {stats.get('ref_tokens', 0):,} tokens")
        lines.append(f"- **Total context cost**: {stats.get('total_tokens', 0):,} tokens")
        lines.append("")

        severity_order = {CRITICAL: 0, WARNING: 1, INFO: 2, OK: 3}
        sorted_findings = sorted(findings, key=lambda f: severity_order.get(f["severity"], 99))

        for finding in sorted_findings:
            sev = finding["severity"]
            marker = {"CRITICAL": "!!!", "WARNING": "!!", "INFO": "i", "OK": "+"}[sev]
            lines.append(f"- **[{sev}]** {finding['message']}")
            if finding.get("fix"):
                lines.append(f"  - Fix: {finding['fix']}")

        lines.append("")

    # Pipeline-wide findings
    pipeline_findings = all_findings.get("__pipeline__", [])
    if pipeline_findings:
        lines.append("## Pipeline-Wide Findings")
        lines.append("")
        for finding in pipeline_findings:
            lines.append(f"- **[{finding['severity']}]** {finding['message']}")
            if finding.get("fix"):
                lines.append(f"  - Fix: {finding['fix']}")
        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total tokens**: {pipeline_stats['total_tokens']:,} across {len(agents)} agents")

    dup_count = pipeline_stats.get("duplication_count", 0)
    if dup_count:
        lines.append(f"- **Duplication**: {dup_count} instances of shared content found")

    critical_count = sum(
        1 for name_findings in all_findings.values()
        for f in name_findings
        if f["severity"] == CRITICAL
    )
    warning_count = sum(
        1 for name_findings in all_findings.values()
        for f in name_findings
        if f["severity"] == WARNING
    )
    info_count = sum(
        1 for name_findings in all_findings.values()
        for f in name_findings
        if f["severity"] == INFO
    )

    lines.append(f"- **Critical**: {critical_count}")
    lines.append(f"- **Warnings**: {warning_count}")
    lines.append(f"- **Info**: {info_count}")

    # Top optimization suggestion
    if pipeline_stats.get("top_optimization"):
        lines.append(f"\n**Top optimization**: {pipeline_stats['top_optimization']}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Console Output
# ---------------------------------------------------------------------------

def print_header(text: str):
    width = max(len(text) + 4, 60)
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def print_agent_header(name: str, path: str):
    print(f"\n--- Agent: {name} ({path}) ---")


def print_finding(finding: dict):
    sev = finding["severity"]
    markers = {
        CRITICAL: "\033[91m[CRITICAL]\033[0m",
        WARNING: "\033[93m[WARNING]\033[0m",
        INFO: "\033[94m[INFO]\033[0m",
        OK: "\033[92m[OK]\033[0m",
    }
    # Fall back to plain text if terminal doesn't support ANSI
    try:
        marker = markers.get(sev, f"[{sev}]")
    except Exception:
        marker = f"[{sev}]"

    print(f"  {marker} {finding['message']}")
    if finding.get("fix") and sev != OK:
        print(f"           Fix: {finding['fix']}")


# ---------------------------------------------------------------------------
# Main Audit Logic
# ---------------------------------------------------------------------------

def run_audit(target: str, do_fix: bool = False, do_report: bool = False, do_json: bool = False):
    """Run the full audit."""

    # Initialize tiktoken
    try:
        encoding = tiktoken.get_encoding(ENCODING_NAME)
    except Exception as e:
        print(f"Failed to initialize tiktoken: {e}")
        sys.exit(1)

    # Discover agents
    agents = discover_agents(target)
    if not agents:
        print("No agents found to audit.")
        sys.exit(1)

    print_header("AGENT AUDIT REPORT")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Date: {now}")
    print(f"Agents scanned: {len(agents)}")

    # Read all CLAUDE.md texts
    agent_texts = {}
    for agent in agents:
        agent_texts[agent["name"]] = read_file_safe(agent["claude_md"])

    # Per-agent audit
    all_findings = {}
    agent_stats = {}
    total_pipeline_tokens = 0
    largest_agent = ("", 0)

    for agent in agents:
        name = agent["name"]
        claude_md_text = agent_texts[name]
        claude_md_tokens = count_tokens(claude_md_text, encoding)
        findings = []

        # Reference files check
        ref_findings, ref_file_stats = check_reference_files(agent, claude_md_text, encoding)
        findings.extend(ref_findings)

        ref_tokens = sum(r["tokens"] for r in ref_file_stats)
        total_agent_tokens = claude_md_tokens + ref_tokens

        # Token cost check
        findings.extend(check_token_cost(agent, claude_md_text, ref_file_stats, encoding))

        # Delegation check
        findings.extend(check_delegation(agent, claude_md_text))

        # Lazy loading check
        findings.extend(check_lazy_loading(agent, claude_md_text, encoding))

        # Quality check
        findings.extend(check_quality(agent, claude_md_text))

        # Auto-fix if requested
        fix_changes = []
        if do_fix:
            fixed_text, fix_changes = apply_fixes(agent, claude_md_text)
            if fix_changes:
                agent["claude_md"].write_text(fixed_text, encoding="utf-8")
                for change in fix_changes:
                    findings.append({
                        "severity": OK,
                        "check": "Auto-Fix",
                        "message": f"Fixed: {change}",
                        "fix": "",
                    })

        # Store results
        all_findings[name] = findings
        agent_stats[name] = {
            "claude_md_tokens": claude_md_tokens,
            "ref_file_count": len(ref_file_stats),
            "ref_tokens": ref_tokens,
            "total_tokens": total_agent_tokens,
        }
        total_pipeline_tokens += total_agent_tokens

        if total_agent_tokens > largest_agent[1]:
            largest_agent = (name, total_agent_tokens)

        # Console output (unless JSON mode)
        if not do_json:
            print_agent_header(name, str(agent["path"]))
            print(f"  CLAUDE.md tokens: {claude_md_tokens:,}")
            print(f"  Reference files: {len(ref_file_stats)} files, {ref_tokens:,} tokens")
            print(f"  Total context cost: {total_agent_tokens:,} tokens")
            print()

            severity_order = {CRITICAL: 0, WARNING: 1, INFO: 2, OK: 3}
            sorted_findings = sorted(findings, key=lambda f: severity_order.get(f["severity"], 99))
            for finding in sorted_findings:
                print_finding(finding)

    # Pipeline-wide checks
    pipeline_findings = []

    # Duplication check (cross-agent)
    if len(agents) > 1:
        dup_findings = check_duplication(agents, agent_texts)
        pipeline_findings.extend(dup_findings)

    # Consistency check
    if len(agents) > 1:
        consistency_findings = check_consistency(agents, agent_texts)
        pipeline_findings.extend(consistency_findings)

    all_findings["__pipeline__"] = pipeline_findings

    # Pipeline stats
    dup_count = sum(1 for f in pipeline_findings if f["check"] == "Duplication" and f["severity"] != OK)
    top_opt = ""
    if largest_agent[1] > TOKEN_WARNING_THRESHOLD:
        top_opt = f"{largest_agent[0]} has the highest context cost ({largest_agent[1]:,} tokens)"

    pipeline_stats = {
        "total_tokens": total_pipeline_tokens,
        "duplication_count": dup_count,
        "top_optimization": top_opt,
    }

    # Print pipeline-wide findings
    if not do_json:
        if pipeline_findings:
            print(f"\n--- Pipeline-Wide Findings ---")
            for finding in pipeline_findings:
                print_finding(finding)

        # Summary
        print(f"\n{'=' * 60}")
        print(f"  SUMMARY")
        print(f"{'=' * 60}")
        print(f"  Total tokens: {total_pipeline_tokens:,} across {len(agents)} agents")

        if dup_count:
            print(f"  Duplication: {dup_count} instances of shared content")

        critical_count = sum(
            1 for nf in all_findings.values() for f in nf if f["severity"] == CRITICAL
        )
        warning_count = sum(
            1 for nf in all_findings.values() for f in nf if f["severity"] == WARNING
        )
        info_count = sum(
            1 for nf in all_findings.values() for f in nf if f["severity"] == INFO
        )

        print(f"  Critical: {critical_count}")
        print(f"  Warnings: {warning_count}")
        print(f"  Info: {info_count}")

        if top_opt:
            print(f"\n  Top optimization: {top_opt}")

        print()

    # JSON output
    if do_json:
        output = {
            "date": now,
            "agents_scanned": len(agents),
            "pipeline_stats": pipeline_stats,
            "agents": {},
            "pipeline_findings": [
                {"severity": f["severity"], "check": f["check"], "message": f["message"], "fix": f["fix"]}
                for f in pipeline_findings
            ],
        }
        for agent in agents:
            name = agent["name"]
            output["agents"][name] = {
                "path": str(agent["path"]),
                "stats": agent_stats[name],
                "findings": [
                    {"severity": f["severity"], "check": f["check"], "message": f["message"], "fix": f["fix"]}
                    for f in all_findings.get(name, [])
                ],
            }
        print(json.dumps(output, indent=2))

    # Save report
    if do_report:
        report_text = generate_report(agents, all_findings, agent_stats, pipeline_stats)
        skill_dir = Path(__file__).parent.parent
        reports_dir = skill_dir / "data" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = reports_dir / f"audit-{timestamp}.md"
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\nReport saved to: {report_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Audit and optimize Claude Code agents in a multi-agent pipeline.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help='Path to agent directory, or "all" to scan the default projects directory (default: all)',
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix simple issues (trailing whitespace, line endings)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Save a markdown report to data/reports/",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON (machine-readable)",
    )

    args = parser.parse_args()
    run_audit(
        target=args.target,
        do_fix=args.fix,
        do_report=args.report,
        do_json=args.json_output,
    )


if __name__ == "__main__":
    main()
