from __future__ import annotations

import subprocess


def audit_prompt(context: str) -> str:
    return f"""You are a read-only debugging auditor. Do not modify files.
Analyze the repeated failure below and return exactly these sections:
FACTS
ASSUMPTIONS
LIKELY WRONG ASSUMPTION
EVIDENCE
NEXT DISCRIMINATING CHECK

Failure context:
{context}
"""


def run_codex_audit(context: str, timeout: int = 90) -> str:
    prompt = audit_prompt(context)
    cmd = [
        "codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
        "--ephemeral", prompt,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "codex audit failed").strip())
    return result.stdout.strip()
