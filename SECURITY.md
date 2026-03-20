# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Reporting a Vulnerability

Email: **64996768+mcp-tool-shop@users.noreply.github.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Version affected
- Potential impact

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge report | 48 hours |
| Assess severity | 7 days |
| Release fix | 30 days |

## Scope

Portlight is a **local-only CLI game**. It does not connect to the internet during gameplay.

- **Data touched:** Local save files (`saves/` directory), local balance/stress report artifacts (`artifacts/`). All data is JSON on the local filesystem.
- **Data NOT touched:** No network connections, no remote servers, no cloud storage, no user analytics.
- **No secrets handling** — does not read, store, or transmit credentials, tokens, or keys.
- **No telemetry** is collected or sent. Zero network egress.
- **Permissions required:** Read/write access to the game directory for save files and report artifacts. No elevated permissions needed.