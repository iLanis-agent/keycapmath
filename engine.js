(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function money(c) { return "$" + Math.floor(c / 100) + "." + ("0" + (c % 100)).slice(-2); }

  function coveragePlan(boardKeys, specialNeeded, setKeys, specialInSet) {
    if (!(boardKeys > 0) || !(specialNeeded > 0) || !(setKeys > 0) || !(specialInSet > 0)) return { error: "board, specials, set and set specials must be positive" };
    var covered = setKeys >= boardKeys ? boardKeys : setKeys;
    var shortage = boardKeys - covered;
    var missingSpecial = specialInSet >= specialNeeded ? 0 : specialNeeded - specialInSet;
    var verdict = shortage > 0 ? "short" : (missingSpecial > 0 ? "gaps" : "full");
    return { covered: covered, shortage: shortage, missingSpecial: missingSpecial, verdict: verdict };
  }

  function pricePlan(priceDollars, setKeys, coveredKeys) {
    if (!(priceDollars > 0) || !(setKeys > 0) || !(coveredKeys > 0)) return { error: "price, set and covered keys must be positive" };
    var perKey = Math.round(priceDollars * 100 / setKeys);
    var perCovered = Math.round(priceDollars * 100 / coveredKeys);
    var idlePct = Math.round((setKeys - coveredKeys) / setKeys * 100);
    return { perKeyCents: perKey, perCoveredCents: perCovered, idlePct: idlePct };
  }

  function layoutPlan(setKeys, boardA, boardB) {
    if (!(setKeys > 0) || !(boardA > 0) || !(boardB > 0)) return { error: "set and both boards must be positive" };
    var leftover = setKeys - boardA;
    var verdict = setKeys < boardA ? "short" : (leftover >= boardB ? "both" : "one");
    return { leftover: leftover, verdict: verdict };
  }

  function renderCoverage(r, boardKeys, specialNeeded, setKeys, specialInSet) {
    var detail, word;
    if (r.verdict === "full") { detail = "every key covered, all specials in the box"; word = "full cover"; }
    else if (r.verdict === "gaps") { detail = "every base key covered, " + plural(r.missingSpecial, "special key") + " missing"; word = "cover with gaps"; }
    else { detail = plural(r.shortage, "key") + " short before specials even enter it"; word = "short"; }
    return "A set of " + setKeys + " keys against a board of " + boardKeys + " keys needing " + plural(specialNeeded, "special key") + ": " + detail + " - " + word + ".";
  }

  function renderPrice(r, priceDollars, setKeys, coveredKeys) {
    return "At $" + priceDollars + " for a set of " + setKeys + " keys: " + money(r.perKeyCents) + " a key in the box, " + money(r.perCoveredCents) + " for each of the " + plural(coveredKeys, "key") + " your board uses - " + r.idlePct + "% of the set rides along unused.";
  }

  function renderLayout(r, setKeys, boardA, boardB) {
    var detail, word;
    if (r.verdict === "short") { detail = plural(0 - r.leftover, "key") + " short on the first board"; word = "neither board dressed"; }
    else { detail = plural(r.leftover, "key") + " left after the first"; word = r.verdict === "both" ? "both boards dressed" : "only the first board dressed"; }
    return "A set of " + setKeys + " keys, a first board of " + boardA + " keys and a second of " + boardB + " keys: " + detail + " - " + word + ".";
  }

  var api = { coveragePlan: coveragePlan, pricePlan: pricePlan, layoutPlan: layoutPlan, renderCoverage: renderCoverage, renderPrice: renderPrice, renderLayout: renderLayout };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.KeycapMath = api;
})(this);
