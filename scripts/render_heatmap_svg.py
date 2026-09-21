import json
import os
from datetime import datetime

colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

json_path = "data/contributions.json"
if not os.path.exists(json_path):
    days_data = []
else:
    with open(json_path, "r", encoding="utf-8") as f:
        days_data = json.load(f)

total_days = len(days_data)
svg_rects = []
x_offset = 44
y_offset = 68
box_size = 12
gap = 3

for i, day in enumerate(days_data[-371:]):
    col = i // 7
    row = i % 7
    x = x_offset + col * (box_size + gap)
    y = y_offset + row * (box_size + gap)
    lvl = day.get("level", 0)
    color = colors[lvl] if lvl < len(colors) else colors[-1]
    svg_rects.append(f'<rect class="c" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2.5" fill="{color}" stroke="#21262d" stroke-width="0.5"><title>{day.get("date")}</title></rect>')

rects_rendered = "\n".join(svg_rects)

svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="250" viewBox="0 0 860 250" role="img" aria-label="Contributions">
<style>
@keyframes drop{{from{{opacity:0;transform:translateY(-9px)}}to{{opacity:1;transform:translateY(0)}}}}
.c{{animation:drop .5s ease-out both}}
@media (prefers-reduced-motion:reduce){{.c{{animation:none}}}}
</style>
<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<rect width="860" height="250" rx="10" fill="#0d1117"/>
<path d="M0 10a10 10 0 0 1 10-10h840a10 10 0 0 1 10 10v28H0z" fill="#161b22"/>
<line x1="0" y1="38" x2="860" y2="38" stroke="#21262d"/>
<circle cx="24" cy="19" r="6" fill="#ff5f56"/>
<circle cx="46" cy="19" r="6" fill="#ffbd2e"/>
<circle cx="68" cy="19" r="6" fill="#27c93f"/>
<text x="430" y="24" text-anchor="middle" font-size="13" fill="#8b949e">sepansarr — contributions, last 12 months</text>
<text x="36" y="93" text-anchor="end" font-size="10" fill="#8b949e">Mon</text>
<text x="36" y="123" text-anchor="end" font-size="10" fill="#8b949e">Wed</text>
<text x="36" y="153" text-anchor="end" font-size="10" fill="#8b949e">Fri</text>
{rects_rendered}
<text x="44" y="220" font-size="12" fill="#c9d1d9">Updated automatically via GitHub Actions</text>
</g>
</svg>"""

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(svg_template)
