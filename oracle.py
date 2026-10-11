import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(n) + " " + (word if n == 1 else (form or word + "s"))
def money(c): return "$" + str(c // 100) + "." + str(c % 100).zfill(2)
def fmt(x): return str(jsnum(x))
def rnd(x): return math.floor(x + 0.5)

def coverage_plan(boardKeys, specialNeeded, setKeys, specialInSet):
    if not (boardKeys > 0) or not (specialNeeded > 0) or not (setKeys > 0) or not (specialInSet > 0):
        return {"error": "board, specials, set and set specials must be positive"}
    covered = setKeys if setKeys >= boardKeys and False else (boardKeys if setKeys >= boardKeys else setKeys)
    shortage = boardKeys - covered
    missing_special = 0 if specialInSet >= specialNeeded else specialNeeded - specialInSet
    verdict = "short" if shortage > 0 else ("gaps" if missing_special > 0 else "full")
    return {"covered": covered, "shortage": shortage, "missingSpecial": missing_special, "verdict": verdict}

def price_plan(priceDollars, setKeys, coveredKeys):
    if not (priceDollars > 0) or not (setKeys > 0) or not (coveredKeys > 0):
        return {"error": "price, set and covered keys must be positive"}
    return {"perKeyCents": rnd(priceDollars * 100 / setKeys),
            "perCoveredCents": rnd(priceDollars * 100 / coveredKeys),
            "idlePct": rnd((setKeys - coveredKeys) / setKeys * 100)}

def layout_plan(setKeys, boardA, boardB):
    if not (setKeys > 0) or not (boardA > 0) or not (boardB > 0):
        return {"error": "set and both boards must be positive"}
    leftover = setKeys - boardA
    verdict = "short" if setKeys < boardA else ("both" if leftover >= boardB else "one")
    return {"leftover": leftover, "verdict": verdict}

def render_coverage(r, boardKeys, specialNeeded, setKeys, specialInSet):
    if r["verdict"] == "full":
        detail, word = "every key covered, all specials in the box", "full cover"
    elif r["verdict"] == "gaps":
        detail, word = "every base key covered, " + plural(r["missingSpecial"], "special key") + " missing", "cover with gaps"
    else:
        detail, word = plural(r["shortage"], "key") + " short before specials even enter it", "short"
    return ("A set of " + fmt(setKeys) + " keys against a board of " + fmt(boardKeys) + " keys needing "
            + plural(specialNeeded, "special key") + ": " + detail + " - " + word + ".")

def render_price(r, priceDollars, setKeys, coveredKeys):
    return ("At $" + fmt(priceDollars) + " for a set of " + fmt(setKeys) + " keys: " + money(r["perKeyCents"])
            + " a key in the box, " + money(r["perCoveredCents"]) + " for each of the " + plural(coveredKeys, "key")
            + " your board uses - " + fmt(r["idlePct"]) + "% of the set rides along unused.")

def render_layout(r, setKeys, boardA, boardB):
    if r["verdict"] == "short":
        detail, word = plural(0 - r["leftover"], "key") + " short on the first board", "neither board dressed"
    else:
        detail = plural(r["leftover"], "key") + " left after the first"
        word = "both boards dressed" if r["verdict"] == "both" else "only the first board dressed"
    return ("A set of " + fmt(setKeys) + " keys, a first board of " + fmt(boardA) + " keys and a second of "
            + fmt(boardB) + " keys: " + detail + " - " + word + ".")

cases = []
for a in [(68, 3, 140, 2), (104, 2, 150, 2), (87, 2, 80, 2), (0, 3, 140, 2)]:
    r = coverage_plan(*a)
    cases.append({"fn": "coveragePlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_coverage(r, *a)})
for a in [(120, 140, 68), (90, 120, 87), (150, 160, 104), (0, 140, 68)]:
    r = price_plan(*a)
    cases.append({"fn": "pricePlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_price(r, *a)})
for a in [(150, 68, 61), (120, 87, 68), (60, 68, 61), (0, 68, 61)]:
    r = layout_plan(*a)
    cases.append({"fn": "layoutPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_layout(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
