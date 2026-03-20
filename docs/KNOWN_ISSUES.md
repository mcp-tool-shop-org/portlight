# Known Issues

Active issues identified through the balance harness, stress testing, and manual play. This is not a bug list — these are tuning targets and design limitations acknowledged for the alpha.

## Balance

### Smuggler ship progression
**Severity:** Medium
**Status:** Under investigation

The smuggler captain does not reach brigantine in the current balance simulation (105 runs, mixed_volatility scenario). Merchant reaches it by day 20, navigator by day 11. Smuggler's luxury margins should be sufficient but the automated policy bots don't accumulate silver fast enough for the upgrade.

**Likely cause:** Smuggler's higher inspection rate and seizure risk erodes margins faster than the luxury pricing advantage compensates. The bot strategy also doesn't optimize for the smuggler's specific advantages.

### Mediterranean route concentration
**Severity:** Medium
**Status:** Known, tuning planned

Porto Novo to Silva Bay accounts for 31% of all route traffic in simulated play. This is partly structural (Mediterranean ports have the best early-game margin on staples) and partly because policy bots don't explore West Africa or East Indies aggressively enough.

**Impact:** Feels narrow. Players who discover West African cotton/iron routes and East Indies porcelain will find good margins, but the game doesn't push them there.

### Contract completion rates
**Severity:** Medium
**Status:** Strategy gap, not engine gap

Zero contracts completed across all 105 automated runs. The contract engine works correctly — offers generate, acceptance works, provenance validates, deadlines resolve. The gap is that policy bots don't prioritize carrying the right goods to the right destination within the deadline.

**Impact:** Human players who read the contract board and plan routes accordingly will complete contracts normally. This is a bot strategy limitation, not a game bug.

### Insurance adoption
**Severity:** Low
**Status:** Expected for alpha

Zero insurance purchases across all automated runs. Policies are available and functional. Policy bots don't evaluate risk well enough to decide when insurance is worth the premium.

**Impact:** Human players will discover insurance when they lose valuable cargo to storms or fail a contract. The system works; the incentive clarity could be improved.

## UX

### No save migration
**Severity:** Medium
**Status:** By design for alpha

Save files may break across alpha versions if the data format changes. There is no migration path. Players should expect to start fresh runs when updating.

### Limited error messages for infrastructure
**Severity:** Low
**Status:** Known

Some infrastructure commands (warehouse, office, license, credit) return terse error messages when requirements aren't met. The requirements are documented in the command help, but inline explanations could be clearer.

### No undo
**Severity:** Low
**Status:** By design

There is no undo for trades, contract acceptance, or infrastructure purchases. This is intentional — decisions have consequences. But it means a mistyped command can cost silver or time.

## Performance

### Balance harness speed
**Severity:** Low
**Status:** Acceptable for alpha

Running the full balance harness (105 simulations across 7 scenarios, 3 captains, 5 seeds) takes approximately 20 seconds. Stress test suite (9 scenarios) takes approximately 2 seconds. Both are fast enough for development iteration.

## Feedback

If you're testing Portlight, the most useful feedback is:

- **Route discoveries** — which routes did you find profitable that aren't Porto Novo / Silva Bay?
- **Contract experience** — were contracts worth taking? Were deadlines realistic?
- **Infrastructure timing** — when did you first feel ready for a warehouse or broker?
- **Ship upgrade timing** — did the brigantine feel achievable at a reasonable point?
- **Victory path clarity** — did you understand what the game was recognizing about your career?
- **Balance notes** — did any captain type feel significantly weaker or stronger?

Save files, trade ledger exports, and milestone screenshots are all helpful for tuning.
