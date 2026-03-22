# Ship Gate

> No repo is "done" until every applicable line is checked.
> Copy this into your repo root. Check items off per-release.

**Tags:** `[all]` every repo · `[npm]` `[pypi]` `[vsix]` `[desktop]` `[container]` published artifacts · `[mcp]` MCP servers · `[cli]` CLI tools

**Detected:** `[all]` `[pypi]` `[cli]`

---

## A. Security Baseline

- [x] `[all]` SECURITY.md exists (report email, supported versions, response timeline) (2026-03-20)
- [x] `[all]` README includes threat model paragraph (data touched, data NOT touched, permissions required) (2026-03-20)
- [x] `[all]` No secrets, tokens, or credentials in source or diagnostics output (2026-03-20)
- [x] `[all]` No telemetry by default — state it explicitly even if obvious (2026-03-20)

### Default safety posture

- [ ] `[cli|mcp|desktop]` SKIP: no dangerous actions — game commands only (buy, sell, sail); no delete/kill/restart operations
- [x] `[cli|mcp|desktop]` File operations constrained to known directories (2026-03-20) — saves/ and artifacts/ only
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server

## B. Error Handling

- [ ] `[all]` SKIP: game CLI — errors are Rich-formatted user messages, not structured API responses. No external consumers.
- [x] `[cli]` Exit codes: 0 ok · 1 user error (2026-03-20) — Typer handles exit codes via typer.Exit(1)
- [x] `[cli]` No raw stack traces without `--debug` (2026-03-20) — Typer catches exceptions, no traceback in app layer
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[desktop]` SKIP: not a desktop app
- [ ] `[vscode]` SKIP: not a VS Code extension

## C. Operator Docs

- [x] `[all]` README is current: what it does, install, usage, supported platforms + runtime versions (2026-03-20)
- [x] `[all]` CHANGELOG.md (Keep a Changelog format) (2026-03-20)
- [x] `[all]` LICENSE file present and repo states support status (2026-03-20)
- [x] `[cli]` `--help` output accurate for all commands and flags (2026-03-20)
- [ ] `[cli|mcp|desktop]` SKIP: single-player game — no logging levels needed; no secrets to redact
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[complex]` SKIP: not a daemon or service — single-player game with auto-save

## D. Shipping Hygiene

- [x] `[all]` `verify` script exists (test + build + smoke in one command) (2026-03-20) — verify.sh
- [x] `[all]` Version in manifest matches git tag (2026-03-22) — v2.0.0 in pyproject.toml, tag at release
- [ ] `[all]` SKIP: no CI configured — local-only development, manual verification
- [ ] `[all]` SKIP: no CI configured — dependency updates handled manually
- [ ] `[npm]` SKIP: not an npm package
- [x] `[pypi]` `python_requires` set (2026-03-20) — `>=3.11` in pyproject.toml
- [x] `[pypi]` Clean wheel + sdist build (2026-03-22) — `portlight-2.0.0-py3-none-any.whl` builds clean
- [ ] `[vsix]` SKIP: not a VS Code extension
- [ ] `[desktop]` SKIP: not a desktop app

## E. Identity (soft gate — does not block ship)

- [x] `[all]` Logo in README header (2026-03-20)
- [x] `[all]` Translations (polyglot-mcp, 7 languages) (2026-03-20)
- [x] `[org]` Landing page (@mcptoolshop/site-theme) (2026-03-20)
- [x] `[all]` GitHub repo metadata: description, homepage, topics (2026-03-20)

---

## Gate Rules

**Hard gate (A–D):** Must pass before any version is tagged or published.
If a section doesn't apply, mark `SKIP:` with justification — don't leave it unchecked.

**Soft gate (E):** Should be done. Product ships without it, but isn't "whole."

**Checking off:**
```
- [x] `[all]` SECURITY.md exists (2026-03-20)
```

**Skipping:**
```
- [ ] `[mcp]` SKIP: not an MCP server
```
