# Example Runs

Three structured sample arcs showing different captain types and commercial strategies. These aren't fiction — they represent realistic play patterns based on the game's economy and systems.

## Merchant: Lawful Scaling

A disciplined Mediterranean trader building toward Lawful Trade House.

**Days 1-10: Route discovery**
```
portlight new "Elena" --type merchant
portlight market                          # Grain is cheap at Porto Novo (high stock)
portlight buy grain 15
portlight sail al_manar                   # Al-Manar consumes grain
portlight advance                         # 3-day voyage
portlight advance
portlight advance
portlight sell grain 15                   # ~1,600 silver profit per unit margin
portlight market                          # Check what's cheap here — spice
portlight buy spice 5                     # Luxury, but small quantities
portlight sail porto_novo
portlight advance
portlight advance
portlight sell spice 5                    # Higher per-unit margin
```

**Days 10-25: Infrastructure and contracts**
```
portlight warehouse lease depot           # Stage cargo at Porto Novo
portlight office open                     # Broker for Mediterranean contracts
portlight contracts                       # Check the board
portlight accept <grain_delivery_offer>   # Aligns with existing route
portlight buy grain 20
portlight warehouse deposit grain 10      # Store half for timing
portlight sail al_manar
portlight advance
portlight advance
portlight advance
portlight sell grain 10                   # Deliver contract obligation
portlight obligations                     # Check remaining requirements
```

**Days 25-50: Trust growth and license acquisition**
```
portlight reputation                      # Trust growing from completed contracts
portlight license buy med_trade_charter   # Unlock premium Mediterranean contracts
portlight milestones                      # Check: Regional Foothold milestones earned
                                          # Profile: "Lawful House" emerging
```

**Outcome:** Steady silver growth, rising trust, clean reputation. Lawful Trade House candidacy building. Brigantine upgrade around day 20. Career profile shows Lawful House as primary, Contract Specialist as secondary.

---

## Smuggler: Shadow Network

A West African operator trading luxury goods under customs pressure.

**Days 1-10: Luxury margin discovery**
```
portlight new "Kojo" --type smuggler
portlight market                          # Sun Harbor — cotton cheap, silk/spice valuable
portlight buy cotton 10                   # Safe early cargo
portlight sail iron_point                 # Short West African route
portlight advance
portlight sell cotton 10
portlight buy iron 10
portlight sail sun_harbor
portlight advance
portlight sell iron 10                    # Return leg profitable
```

**Days 10-25: Heat management**
```
portlight reputation                      # Heat rising from luxury region trades
portlight market                          # Check for silk/spice availability
portlight buy silk 5                      # Higher margins, but attracts attention
portlight sail palm_cove
portlight advance
portlight advance
portlight sell silk 5                     # Large per-unit margin
portlight status                          # Silver growing fast
                                          # But inspections increasing
```

**Days 25-45: Profitable under pressure**
```
portlight reputation                      # Heat at 15-20 in West Africa
                                          # Inspections happening every few voyages
portlight milestones                      # Shadow Operator tag emerging
                                          # "Profitable under heat" evidence
portlight insure buy hull_basic           # Protect against storm losses
portlight credit open                     # Leverage for bigger cargo runs
portlight credit draw 200
portlight buy silk 8
portlight sail sun_harbor
```

**Outcome:** High margins but constant pressure. Heat management becomes a real skill — knowing when to switch to staples for cooldown, when to push luxury runs. Shadow Network candidacy building. Career profile shows Shadow Operator as primary.

---

## Navigator: Oceanic Reach

A long-haul operator pushing into the East Indies.

**Days 1-15: Mediterranean profit base**
```
portlight new "Yara" --type navigator
portlight market                          # Porto Novo starting port
portlight buy grain 15                    # Build capital with safe trades
portlight sail silva_bay                  # Short Mediterranean route
portlight advance
portlight advance
portlight sell grain 15
portlight buy timber 10                   # Timber from Silva Bay
portlight sail porto_novo
portlight advance
portlight advance
portlight sell timber 10
```

**Days 15-30: Brigantine and range expansion**
```
portlight shipyard buy brigantine         # Speed + cargo upgrade
portlight provision 20                    # Stock up for longer voyages
portlight routes                          # Now longer routes are viable
portlight sail sun_harbor                 # Cross into West Africa
portlight advance
portlight advance
portlight advance
portlight advance
portlight market                          # New region, new opportunities
portlight sell grain 10                   # Mediterranean goods sell well here
portlight buy cotton 15                   # Cotton is cheap in West Africa
```

**Days 30-60: East Indies push**
```
portlight routes                          # East Indies routes visible with brigantine
portlight provision 25                    # Long voyage ahead
portlight sail <east_indies_port>
portlight advance                         # Multi-day voyage
...
portlight market                          # East Indies prices — porcelain cheap
portlight buy porcelain 10
portlight warehouse lease depot           # EI staging warehouse
portlight office open                     # EI broker for premium contracts
portlight milestones                      # Oceanic Carrier tag emerging
```

**Outcome:** Slower start but eventually the most profitable routes. East Indies porcelain and spice back to Mediterranean or West Africa create the highest margins in the game. Oceanic Reach candidacy building. Career profile shows Oceanic Carrier as primary, Infrastructure Builder as secondary.

---

## Reading these examples

These arcs show different strategies, not different difficulty levels. Each captain type has a natural commercial identity, but the game doesn't force you into it. A merchant can push into the East Indies. A smuggler can build legitimate trust. A navigator can work luxury margins.

The career profile and victory paths reflect what you actually did, not what your captain type suggests. That's the design: the game interprets your commercial history, and two runs that end rich in different ways are distinguishable.
