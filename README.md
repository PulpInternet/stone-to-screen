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
10. `build/enhance_v11.py` is the final review pass against the research files: water and electricity from `energy_stats_r11.json` (Hannah green for power, Damani cyan for water), corrected source and baseline claims, the 31 predictions in a modal, dataset credits, and the timeline label shown only on hover. Run it as `python3 enhance_v11.py v10.html index.html <research/data/results>`.

The scripts use absolute paths from the environment they were written in; update the `SRC` and `OUT` paths at the top of each before running. Python 3 with Pillow is required.

## Checks

`checks/check_v9.py` and `checks/check_v9r.py` run the page in a real browser with Playwright and verify the bubble states, hover previews, touch behavior, page links, navigation, and layout in all three color modes.
