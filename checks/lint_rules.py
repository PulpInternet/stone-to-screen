# checks/lint_rules.py
# Static checks for DESIGN_RULES.md. Usage: python3 checks/lint_rules.py index.html
# Style blocks tagged /* v10 */ or later are held to every CSS rule. Earlier blocks are
# reported as legacy warnings so they can be folded in over time without blocking a commit.
import re, sys, html
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
src = open(path, encoding="utf-8").read()
s = re.sub(r"data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]+", "DATA", src)
fails, warns = [], []

# ---------- CSS ----------
RAW_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)")
for n, block in enumerate(re.findall(r"<style[^>]*>(.*?)</style>", s, flags=re.S), 1):
    tag = re.search(r"/\*\s*v(\d+)", block)
    ver = int(tag.group(1)) if tag else 0
    strict = ver >= 10
    where = f"style block {n} (v{ver or '?'})"
    body = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    problems = []
    for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", body):
        sel, decls = rule.group(1).strip(), rule.group(2)
        for d in decls.split(";"):
            if ":" not in d: continue
            prop, val = [x.strip() for x in d.split(":", 1)]
            if prop.startswith("--"): continue                       # token definitions may hold raw values
            if RAW_COLOR.search(val) and "forced-colors" not in sel:
                problems.append(f"raw color in `{sel[:40]}` {prop}: {val[:40]}")
            if "!important" in val: problems.append(f"!important in `{sel[:40]}`")
            if prop == "z-index" and not val.startswith("var(--z-"): problems.append(f"raw z-index {val} in `{sel[:40]}`")
            if prop == "font-style" and "italic" in val: problems.append(f"italic in `{sel[:40]}`")
    for p in problems:
        (fails if strict else warns).append(f"{where}: {p}")

# ---------- markup ----------
text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
visible = html.unescape(re.sub(r"<[^>]+>", " ", text))
js_strings = " ".join(re.findall(r'"(?:t|d|text|label)":\s*"([^"]*)"', s))
for ch, name in (("—", "em dash"), ("–", "en dash")):
    c = visible.count(ch) + js_strings.count(ch)
    if c: fails.append(f"{c} {name}(es) in visible text")
for m in re.finditer(r"<h[1-6][^>]*>(.*?)</h[1-6]>", text, flags=re.S):
    if re.search(r"<(em|i)\b(?![^>]*class=)", m.group(1)): fails.append("italic tag inside a heading: " + re.sub("<[^>]+>", "", m.group(1))[:50])

# the page ships Part I and Part II together and removes the other part on load, so check each view
for keep, drop in (("1", "2"), ("2", "1")):
    view = re.sub(r'<(header|section)\b[^>]*data-page="%s"[^>]*>.*?</\1>' % drop, " ", text, flags=re.S)
    ids = Counter(re.findall(r'\sid="([^"]+)"', view))
    dupes = [i for i, c in ids.items() if c > 1]
    if dupes: fails.append(f"duplicate ids on Part {keep}: " + ", ".join(dupes[:10]))
for img in re.findall(r"<img\b[^>]*>", text):
    if 'alt="' not in img: fails.append("image without alt text")

# ---------- data visualizations ----------
for fig in re.findall(r'<figure class="viz[^"]*">(.*?)</figure>', text, flags=re.S):
    if "<figcaption" not in fig: fails.append("chart without a caption")
    for bar in re.findall(r'<div class="vbar"[^>]*>', fig):
        if 'role="img"' not in bar or "aria-label=" not in bar: fails.append("bar without role=img and aria-label")
    for line in re.findall(r'<div class="eline"[^>]*>', fig):
        if 'role="img"' not in line or "aria-label=" not in line: fails.append("pictogram row without role=img and aria-label")
if re.search(r"\.drop|--aqua", s) and re.search(r'\[data-page="2"\][^{]*\{[^}]*background:var\(--aqua\)', s.split("/* v14")[-1]):
    fails.append("cyan used for something other than water after v14")

# ---------- content ----------
for bad in ("icp_roi", "pure_per_M_usd", "Never show Pulp"):
    if bad in s: fails.append(f"internal research content on the page: {bad}")
for ext in re.findall(r'<script[^>]+src="([^"]+)"', s):
    fails.append(f"external script: {ext}")

print(f"lint_rules: {len(fails)} failure(s), {len(warns)} legacy warning(s)")
for f in fails: print("  FAIL", f)
if warns:
    print("  legacy (pre-v10 blocks, fold in over time):")
    for w in warns[:12]: print("    warn", w)
    if len(warns) > 12: print(f"    ... and {len(warns) - 12} more")
sys.exit(1 if fails else 0)
