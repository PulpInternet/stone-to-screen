# Design and code rules

These rules apply to every change to `index.html`, whether it comes from a person, a build script, or an AI agent. `checks/lint_rules.py` enforces the ones a machine can check. Run it before every commit; it must pass.

## How the code is organized

1. **One build step per change.** Each change is a script in `build/` named `enhance_vNN.py` that reads the previous version and writes the next. Scripts fail loudly when a string they expect is missing (`assert`), so a change never applies silently to the wrong place.
2. **New CSS goes in one `<style>` block per step**, appended before `</body>`, opening with a comment that names the step: `/* v16: ... */`. Never edit an earlier block in place; override it in the new block.
3. **Tokens first.** Colors, spacing, widths, tap size, and z-index come from the tokens on `:root`. A new rule may not contain a raw color, and should not contain a raw spacing value when a token exists.
4. **Fix at the source when a rule keeps being overridden.** If three later blocks override the same selector, fold them into one rule in the next step and say so in its comment.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--col` | 680px | Reading column. Text, figures, and the middle of both bars. |
| `--frame` | 1180px | Fixed bars and wide furniture. Nothing in a bar sits outside it. |
| `--gutter` | 24px, 16px under 560px | Minimum side padding everywhere. |
| `--frame-pad` | computed | Side padding for full-width bars: the gutter, or whatever centers the frame. |
| `--s1` to `--s7` | 4, 8, 12, 16, 24, 32, 48px | Spacing scale. Use `gap` on flex and grid, not margins between siblings. |
| `--tap` | 44px | Minimum height and width of anything you can tap or click. |
| `--z-rail`, `--z-bar`, `--z-modal` | 45, 50, 80 | The only z-index values. |
| `--bg`, `--fg`, `--mut`, `--line`, `--card`, `--band` | per mode | Ground, text, secondary text, rules, raised surfaces, bands. |
| `--btn-bg`, `--btn-fg`, `--link` | per mode | Primary buttons and links. |
| `--yellow` | electric yellow | Part I accent. On Part II it resolves to Hannah green. |
| `--p2acc`, `--sus` | Hannah green | Part II accent and all Part II data. |
| `--aqua`, `--aqua-edge` | Damani cyan | Water only. |

## Color

1. **Light, Dark, and Mono change colors only.** A grayscale screenshot of any mode must match the others shape for shape. Never change size, position, or visibility by mode.
2. **One accent per part.** Part I uses electric yellow; Part II uses Hannah green, starting at the "Next, Part II" teaser. The accent marks the current chapter, the hero word, the speech bubble, and the current page link. It is never used for body text.
3. **Data colors on Part II:** Hannah green for every measured series, gray (`--mut` at reduced opacity) for comparison series, Damani cyan for water and nothing else. Mono turns data gray.
4. **No colored stripe on one edge of a card, modal, callout, or panel.** No gradients, glows, or decorative color.
5. **Text on an accent fill is `--ink`.** Check contrast at 4.5:1 for text and 3:1 for graphical marks; add an edge token (like `--aqua-edge`) rather than darkening a brand color.

## Layout and spacing

1. **Two widths only:** `--col` for reading, `--frame` for bars. Fixed bars use `--frame-pad` on both sides so their contents never pin to the screen edge on wide displays.
2. **The middle of each bar lines up with the reading column** within 2px on screens wider than 1100px. Narrower, the bar puts the part links first and the middle takes the remaining space.
3. **Photos and figures start on the text's left edge.** Never center a figure narrower than the column.
4. **No page-level sideways scroll.** Only the chapter strips scroll sideways, and nothing scrolls inside them.
5. **Respect safe areas.** Fixed bars add `env(safe-area-inset-*)` to their own padding.

## Type

1. Libre Franklin with an Arial fallback. No monospace.
2. **No italics** in any title, headline, label, or display type, including single accent words.
3. American spelling. No em dashes or en dashes in visible text.
4. Uppercase labels get letter spacing (0.1 to 0.14em) and weight 600.

## Interaction

1. Every control works with touch, mouse, trackpad, keyboard, and pen, with and without hover.
2. **Hover-only information must have a non-hover path.** Labels that appear on hover (like the timeline label) also appear on keyboard focus.
3. **Secondary views open as floating modals** over a dimmed page, close on outside click, the close button, and Escape, and return focus to the control that opened them.
4. **Jumps take about 0.4s** and land below the top bar. Reduced motion makes them instant and removes movement, keeping opacity fades at 0.12s.
5. **The scroll timeline stays quiet:** very low opacity while scrolling, gone 1.5s after, full only on hover or focus. Its label never covers the reading column.

## Data visualizations

1. **Build every chart from the shared parts:** `.viz` (figure), `.vrow`/`.vh`/`.vbar` (labeled bars), `.dots` (grids), `.eline`/`.pg` (pictograms), `.vleg` (legend), `.vcap` (caption). Do not hand-roll a new chart type when one of these fits.
2. **Every number on screen comes from a file in `research/`,** and the build script that places it reads it from that file instead of typing it in. Middle estimates are labeled as such, and ranges appear in the caption.
3. **Every chart has a caption** stating the unit, the sample size or source, and whether figures are measured, calculated, or estimated.
4. **Values are printed as text** next to every mark. Color never carries meaning alone, so charts survive Mono and forced colors.
5. **Each mark group has `role="img"` and an `aria-label`** with the label and the value.
6. **Pictograms state their unit** in a key (for example, 1 hour of home electricity, 10 liters of water), and partial icons are clipped, never rounded up.
7. **Comparisons say what they compare.** Simulated and real requests are never mixed in one series. Baselines are shown when a result is compared with guessing.
8. **Labels never collide** with each other, with their marks, or with lines, at 320, 390, 768, 1024, 1440, and 2000px wide, in every mode. `checks/check_layout.py` tests this.

## Content

1. Pulp Corporation, established 2026, Brooklyn, New York. No earlier founding story.
2. Nothing from `research/internal/`: no prices, ROI, customer names, or pipeline.
3. Corrections in `AGENT_NOTES.md` section 4 are used exactly as written, everywhere.
4. Simulated requests are labeled simulated and say they were written for this study.

## Before every commit

1. `python3 checks/lint_rules.py index.html` passes.
2. `python3 checks/check_layout.py index.html` reports no issues and no script errors.
3. Run `build/enhance_v15.py` last, so the build id that keeps visitors on the newest version matches the file.
