"""Regenerate coupling-pt1-instability-curves.png from the v6 notebook's setup cell,
with the band names and tick labels matching the article table (Stable / Balanced / Borderline / Unstable; 0.25 / 0.50 / 0.75)."""
import json, re, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src = "".join(json.load(open(Path(__file__).with_name("coupling_notebook_part_1c_matplotlib_v6.ipynb")))["cells"][1]["source"])
src = src.replace("import nbformat\n", "")
src = re.sub(r'"cli"', '"color"', src)
src = src.replace('"xtick.cli"', '"xtick.color"').replace('"ytick.cli"', '"ytick.color"').replace('"text.cli"', '"text.color"')
src = src.replace('.cli"', '.color"')
src = src.replace('"Mostly Stable", "MOSTLY STABLE"', '"Balanced", "BALANCED"')
src = src.replace('"Volatile", "VOLATILE"', '"Unstable", "UNSTABLE"')
# 0.25 and 0.75 were printed as 0.2 and 0.8 by a one-decimal formatter
src = src.replace('f"{x:.1f}"', '(f"{x:.2f}" if abs(x * 10 - round(x * 10)) > 1e-9 else f"{x:.1f}")')
src = src.replace("bbox_to_anchor=(-0.23, 0.45)", "bbox_to_anchor=(-0.29, 0.45)")
src = src[: src.index("def render_md(")]
ns = {}
exec(src, ns)
out = sys.argv[1]
plt.show = lambda *a, **k: plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
ns["render_instability_curves"]()
print("wrote", out)
