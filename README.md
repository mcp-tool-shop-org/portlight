# Portlight

Trade-first maritime strategy game with living port economy, ship progression, and verifiable trade receipts.

## Install

```bash
pip install -e ".[dev]"
```

## Play

```bash
portlight new "Captain Hawk"
portlight market
portlight buy grain 10
portlight sail al_manar
portlight sell grain 10
portlight ledger
```

## Test

```bash
pytest
```

## Architecture

```
src/portlight/
  engine/    — economy, voyage, events, progression rules
  content/   — ports, goods, ships, captains (game data)
  app/       — Typer CLI + Rich rendering
  receipts/  — trade receipt schema, hashing, export
  xrpl/      — optional XRPL adapter (not core runtime)
```

## License

MIT
