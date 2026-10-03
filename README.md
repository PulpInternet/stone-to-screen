# From Stone to Screen

An interactive essay on writing as memory and cost, with Part II on Pulp's research.

`index.html` is the whole site: one self-contained file with all photos, styles, and scripts inside it. Part I opens at `index.html`; Part II opens at `index.html#part-ii`. No server, build step, or dependencies are needed to host it; the only external requests are Google Fonts.

## Rebuilding from source

The page is generated from the Part I source draft by these scripts, run in order:

1. `build/rewrite_part1.py` rewrites Part I under the memory-and-cost frame.
2. `build/build_v3.py` adds Part II and the record of how we check our claims (reads `build/story_data.json`).
3. `build/enhance_v4.py` makes the photos shift-free and adds the chapter bar and scroll timeline.
4. `build/enhance_v5.py` splits Part I and Part II into two pages.
5. `build/enhance_v6.py` moves the timeline left and sizes the photos.
6. `build/enhance_v7.py` adds the centered Antiquity to Today bar and the speech bubble.
7. `build/enhance_v8.py` adds hover previews, collapse on leave, phone flashes, and the Part links.
8. `build/enhance_v9.py` shows the speech bubble only while the bar is hovered, and slims the idle bar.
9. `build/enhance_v10.py` speeds up jumps to about 0.4 s, aligns photos to the text column, quiets the scroll timeline (very low opacity, 1.5 s, full on hover), and redraws the energy chart with sustainability-green power and water pictograms. Run it as `python3 enhance_v10.py <v9 output> v10.html`.
10. `build/enhance_v11.py` is the final review pass against the research files: water and electricity from `energy_stats_r11.json` (Hannah green for power, Damani cyan for water), corrected source and baseline claims, the 31 predictions in a modal, dataset credits, and the timeline label shown only on hover. Run it as `python3 enhance_v11.py v10.html v11.html <research/data/results>`.
11. `build/enhance_v12.py` carries the research palette through every Part II chart: Damani cyan for measured results, Hannah green for efficiency and sustainability, gray for comparison series. Run it as `python3 enhance_v12.py v11.html v12.html`.
12. `build/enhance_v13.py` makes Hannah green Part II's accent in place of electric yellow, starting on "spend" in the Next, Part II teaser at the end of Part I. Run it as `python3 enhance_v13.py v12.html v13.html`.
13. `build/enhance_v14.py` makes Part II all Hannah green; Damani cyan stays only on water. Run it as `python3 enhance_v14.py v13.html v14.html`.
14. `build/enhance_v15.py` adds a fresh-version check for GitHub Pages: on load the page fetches its own URL with a unique query (skipping the browser cache and GitHub's CDN), compares build ids, and reloads once onto a newer build. It does nothing off github.io. Run it last, on the final output: `python3 enhance_v15.py <input> index.html`.
15. `build/enhance_v16.py` adds layout tokens (column, frame, gutter, spacing, tap size, z-index), keeps both fixed bars inside a 1180 px frame, and brings every control to a 44 px tap target. Run it as `python3 enhance_v16.py v15.html v16.html`.
16. `build/enhance_v17.py` adds Part III, Run the numbers, at `index.html#part-iii`: the estimator from the first research page, rebuilt on public data only. Visitors set a traffic mix across the six kinds of requests, a yearly volume, model, reasoning mode, and grid, and see provider spend (at provider list prices), share of model work, electricity with its 80% range, carbon, and water saved. Every input figure is read from `research/data/results`; nothing comes from `research/internal`. Run it as `python3 enhance_v17.py v16.html v17.html <research/data/results>`.
17. `build/enhance_v18.py` is a consolidation pass: legacy raw colors and z-index values folded into tokens, the pre-script page hiding extended to three parts, the hero highlight spacing fixed, one hero text measure, and short part labels in the bottom bar. Run it as `python3 enhance_v18.py v17.html v18.html`, then `python3 enhance_v15.py v18.html index.html`.
18. `build/enhance_v19.py` gives Part III the same navigation as Parts I and II: Chapters 15 to 17 in the chapter bar, scroll timeline, Index, and New here bar. Mouse clicks no longer leave a focus ring. Run it as `python3 enhance_v19.py v18.html v19.html`, then `python3 enhance_v15.py v19.html index.html`.

`enhance_v15.py` (the build id) always runs last, and is safe to run more than once.

## Rules

`DESIGN_RULES.md` holds the CSS, layout, and data visualization rules every change follows. Before committing, run:

- `python3 checks/lint_rules.py index.html` (static rules; must pass)
- `python3 checks/check_layout.py index.html` (layout, overlap, alignment, tap targets at nine widths)
- `python3 checks/check_functional.py index.html` (clicks and types through every control on desktop and phone)

After pushing, confirm the live page's build id matches local and run `check_functional.py` against the live URL. See DESIGN_RULES.md.

## Seeing a new version

After a push, GitHub Pages takes about a minute to publish. Open the page normally; if it is stale, it reloads itself onto the new build within a second. You no longer need a hard refresh or a private window.

The scripts use absolute paths from the environment they were written in; update the `SRC` and `OUT` paths at the top of each before running. Python 3 with Pillow is required.

## Earlier checks

`checks/check_v9.py` and `checks/check_v9r.py` run the page in a real browser with Playwright and verify the bubble states, hover previews, touch behavior, page links, navigation, and layout in all three color modes.
