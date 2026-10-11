# Keycap math

Whether a keycap set actually covers your layout, what each used key really costs, and how many boards one set can dress at once - so the group buy stops being a gamble. Exact counting in the browser, every layout assumption labeled.

Live site: https://ilanis-agent.github.io/keycapmath/

## The three tools

- **Coverage plan** - `coveragePlan(boardKeys, specialNeeded, setKeys, specialInSet)`: covered keys, shortage, missing specials and a verdict.
- **Price plan** - `pricePlan(priceDollars, setKeys, coveredKeys)`: cents per key in the box versus per key used, and the idle share.
- **Layout plan** - `layoutPlan(setKeys, boardA, boardB)`: leftover keys and a both/one/neither verdict.

## Labeled norms (illustrative references, not recommendations)

- Board: 68 keys (a 65%). Set: 140 keys with 2 special sizes. Price: $120. Key counts ignore profile and row sculpt - check the kitting diagram before any buy.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (12 cases, 60 checks)

Regenerate the oracle expectations: `python3 oracle.py`
