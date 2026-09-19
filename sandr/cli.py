from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sandr.adapters.codex import parse_hook_payload
from sandr.config import expand_path, load_config
from sandr.core.events import OperationEvent
from sandr.doctor import run_checks
from sandr.guard.loop_guard import LoopGuard
from sandr.guard.state import load_state
from sandr.install import install_codex_guard, install_config, install_skills
from sandr.memory.index import update_index
from sandr.memory.search import get_document, search, status
from sandr.project import ingest_project, init_project

ROOT = Path(__file__).resolve().parent.parent


def _paths(cfg: dict) -> tuple[Path, Path]:
    knowledge = expand_path(cfg["memory"]["knowledge_dir"], base=Path.cwd())
    db = expand_path(cfg["memory"]["db_path"])
    return knowledge, db


def _guard(cfg: dict) -> LoopGuard:
    g = cfg["guard"]
    return LoopGuard(
        expand_path(g["state_path"]),
        warning_after=int(g["warning_after"]),
        reset_after=int(g["reset_after"]),
        audit_after=int(g["audit_after"]),
    )


def cmd_doctor(args) -> int:
    checks = run_checks(args.config)
    for c in checks:
        label = "OK" if c["ok"] else ("WARN" if c["severity"] == "warn" else "ERROR")
        print(f"[{label}] {c['name']}: {c['detail']}")
    return 0 if all(c["ok"] or c["severity"] == "warn" for c in checks) else 1


def cmd_memory(args) -> int:
    cfg = load_config(args.config)
    knowledge, db = _paths(cfg)
    if args.memory_cmd in {"build", "update"}:
        result = update_index(knowledge, db, rebuild=args.memory_cmd == "build", tokenizer=cfg["memory"].get("tokenizer", "unicode61"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.memory_cmd == "search":
        print(json.dumps(search(db, args.query, args.limit), ensure_ascii=False, indent=2))
    elif args.memory_cmd == "get":
        print(json.dumps(get_document(db, args.id), ensure_ascii=False, indent=2))
    elif args.memory_cmd == "status":
        print(json.dumps(status(db), ensure_ascii=False, indent=2))
    return 0


def cmd_guard(args) -> int:
    cfg = load_config(args.config)
    guard = _guard(cfg)
    if args.guard_cmd == "reset":
        guard.reset()
        print("LoopGuard state reset")
        return 0
    if args.guard_cmd == "status":
        state = load_state(guard.state_path)
        if not args.history:
            state["history"] = state.get("history", [])[-10:]
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    event = OperationEvent(args.type, args.command, args.exit_code, args.output)
    decision = guard.record(event)
    print(json.dumps(decision.__dict__, ensure_ascii=False, indent=2))
    return 2 if decision.level >= 2 else 0


def cmd_skills(args) -> int:
    source = ROOT / "skills"
    if args.skills_cmd == "list":
        names = sorted(p.name for p in source.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
        print("\n".join(names))
        return 0
    result = install_skills(args.host, source=source, selected=args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_project(args) -> int:
    cfg = load_config(args.config)
    knowledge, _db = _paths(cfg)
    if args.project_cmd == "init":
        result = init_project(knowledge, args.slug, args.title)
    else:
        result = ingest_project(knowledge, args.slug, args.source)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_guard_hook(args) -> int:
    cfg = load_config(args.config)
    if not cfg["guard"].get("enabled", True):
        return 0
    try:
        payload = json.load(sys.stdin)
        normalized = parse_hook_payload(payload)
        if normalized["exit_code"] is None:
            return 0
        event = OperationEvent(**normalized)
        decision = _guard(cfg).record(event)
        if decision.level:
            print(f"<sandr-loopguard level=\"{decision.level}\">\n{decision.message}\n</sandr-loopguard>")
    except Exception:
        return 0  # host hook is fail-open
    return 0


def cmd_install(args) -> int:
    report = {"skills": [], "guard": None, "config": None}
    config_target = Path(args.config).expanduser() if args.config else Path.home() / ".config" / "sandr-dev-stack" / "config.toml"
    report["config"] = install_config(ROOT / "config.example.toml", config_target)
    hosts = [args.host] if args.host != "all" else ["codex", "claude"]
    for host in hosts:
        report["skills"].extend(install_skills(host))
    if args.guard and args.host in {"codex", "all"}:
        report["guard"] = install_codex_guard(event=args.hook_event)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sandr")
    p.add_argument("--config", help="Path to config.toml")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor")
    d.set_defaults(func=cmd_doctor)

    m = sub.add_parser("memory")
    ms = m.add_subparsers(dest="memory_cmd", required=True)
    for name in ("build", "update", "status"):
        x = ms.add_parser(name)
        x.set_defaults(func=cmd_memory)
    s = ms.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=5)
    s.set_defaults(func=cmd_memory)
    g = ms.add_parser("get")
    g.add_argument("id", type=int)
    g.set_defaults(func=cmd_memory)

    guard = sub.add_parser("guard")
    gs = guard.add_subparsers(dest="guard_cmd", required=True)
    rec = gs.add_parser("record")
    rec.add_argument("--type", default="shell")
    rec.add_argument("--command", required=True)
    rec.add_argument("--exit-code", type=int, required=True)
    rec.add_argument("--output", default="")
    rec.set_defaults(func=cmd_guard)
    reset = gs.add_parser("reset")
    reset.set_defaults(func=cmd_guard)
    gst = gs.add_parser("status")
    gst.add_argument("--history", action="store_true", help="Show full retained history")
    gst.set_defaults(func=cmd_guard)

    sk = sub.add_parser("skills")
    sks = sk.add_subparsers(dest="skills_cmd", required=True)
    skl = sks.add_parser("list")
    skl.set_defaults(func=cmd_skills)
    ski = sks.add_parser("install")
    ski.add_argument("name")
    ski.add_argument("--host", choices=("codex", "claude"), default="codex")
    ski.set_defaults(func=cmd_skills)

    project = sub.add_parser("project")
    ps = project.add_subparsers(dest="project_cmd", required=True)
    pi = ps.add_parser("init")
    pi.add_argument("slug")
    pi.add_argument("--title")
    pi.set_defaults(func=cmd_project)
    pg = ps.add_parser("ingest")
    pg.add_argument("slug")
    pg.add_argument("source")
    pg.set_defaults(func=cmd_project)

    gh = sub.add_parser("guard-hook")
    gh.set_defaults(func=cmd_guard_hook)

    ins = sub.add_parser("install")
    ins.add_argument("--host", choices=("codex", "claude", "all"), default="codex")
    ins.add_argument("--guard", action="store_true", help="Also install experimental Codex LoopGuard hook")
    ins.add_argument("--hook-event", default="PostToolUse")
    ins.set_defaults(func=cmd_install)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
