# Balance Report — mixed_volatility

Total runs: 105

## Executive Summary

- **Brigantine gap**: navigator fastest (day 11), merchant slowest (day 20), gap = 9 days
- **Top route**: silva_bay->porto_novo (432 uses, 31% of all traffic)


## Captain Parity

| Captain | Runs | Brig Day | Galleon Day | NW@40 | Inspections | Seizures | Defaults | Contracts OK | Strongest Path |
|---------|------|----------|-------------|-------|-------------|----------|----------|--------------|----------------|
| merchant  |   35 |       20 |          28 | 12396 |         2.0 |      0.0 |      0.2 |          0.0 | lawful_house   |
| navigator |   35 |       11 |          40 |  8962 |         1.9 |      0.0 |      0.0 |          0.0 | lawful_house   |
| smuggler  |   35 |        - |           - | 13985 |         3.3 |      0.4 |      0.0 |          0.0 | lawful_house   |


## Route Economics

| Route | Uses | Total Profit | Avg Profit | Captain Mix |
|-------|------|-------------|------------|-------------|
| silva_bay->porto_novo          |  432 |     711,156 |       1646 | merchant:272, navigator:160 |
| porto_novo->silva_bay          |  420 |     405,697 |        966 | merchant:241, navigator:179 |
| sun_harbor->iron_point         |  105 |     135,939 |       1295 | smuggler:105 |
| iron_point->sun_harbor         |  101 |     290,293 |       2874 | merchant:1, smuggler:100 |
| palm_cove->iron_point          |   71 |      51,723 |        728 | merchant:1, smuggler:70 |
| sun_harbor->palm_cove          |   67 |      56,866 |        849 | merchant:1, smuggler:66 |
| iron_point->palm_cove          |   53 |      41,120 |        776 | smuggler:53 |
| palm_cove->sun_harbor          |   43 |     114,549 |       2664 | smuggler:43 |
| al_manar->porto_novo           |   23 |      54,281 |       2360 | merchant:5, navigator:18 |
| al_manar->silva_bay            |   22 |      26,952 |       1225 | merchant:15, navigator:7 |


## Victory Path Health

| Path | Candidacy | Completion | Candidacy Rate | Completion Rate | Captain Skew |
|------|-----------|------------|---------------|-----------------|--------------|
| lawful_trade_house   |         0 |          0 |            0% |              0% |  |
| shadow_network       |        29 |          0 |           28% |              0% | merchant:9, navigator:6, smuggler:14 |
| oceanic_reach        |        11 |          0 |           10% |              0% | merchant:1, navigator:10 |
| commercial_empire    |         0 |          0 |            0% |              0% |  |


## Infrastructure & Finance Timing

| Captain | 1st Warehouse | 1st Broker | 1st License | Insurance % | Credit % |
|---------|---------------|------------|-------------|-------------|----------|
| merchant  |         day 2 |      day 2 |           - |          0% |      14% |
| navigator |         day 2 |      day 2 |           - |          0% |       0% |
| smuggler  |         day 2 |      day 2 |           - |          0% |       0% |
