"""Generate the analysis figures used in the PestLand manual (Click 6 - Results).

Reads data/incident_reports_anonymized.csv and writes PNGs to docs/images/analysis/.

PestLand Risk Index (PRI), per H3-like hex cell (here: matplotlib hexbin):
    severity score  LOW=1, MEDIUM=2, HIGH=3
    PRI = 100 * (mean_score - 1) / 2 * min(1, n / 5)
The confidence term down-weights cells with fewer than 5 reports.
Classes: Low < 25 <= Moderate < 50 <= High < 75 <= Very high.
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

OUT = "docs/images/analysis/"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
RISK = ["#fbd3c1", "#f29a73", "#d9542f", "#8e2413"]  # one warm hue, light -> dark
RISK_LABELS = ["Low (<25)", "Moderate (25-50)", "High (50-75)", "Very high (75+)"]
SEV = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": SURF, "axes.facecolor": SURF,
    "axes.spines.top": False, "axes.spines.right": False,
})

df = pd.read_csv("data/incident_reports_anonymized.csv", low_memory=False)
df["score"] = df["infestation_level"].map(SEV)
df["created_at"] = pd.to_datetime(df["created_at"])

# ---- data-quality: GPS far from the county's own median centre (boundary mismatch) ----
main = df[df.county_name.isin(["KAKAMEGA", "KILIFI", "NYERI"])].copy()
ctr = main.groupby("county_name")[["latitude", "longitude"]].transform("median")
km = np.hypot(main.latitude - ctr.latitude, (main.longitude - ctr.longitude) * np.cos(np.radians(ctr.latitude))) * 111
main["gps_mismatch"] = km > 80
stats = {
    "rows": int(len(df)),
    "pest_disease": int((df.report_type == "PEST/DISEASE").sum()),
    "weed": int((df.report_type == "WEED").sum()),
    "gps_mismatch_main_counties": int(main.gps_mismatch.sum()),
    "gps_mismatch_pct": float(round(100 * main.gps_mismatch.mean(), 1)),
    "unknown_disease": int((df.pest_name == "UNKNOWN DISEASE").sum()),
    "missing_pest_photo_pct": float(round(100 * df.pest_photo.isna().mean(), 1)),
    "missing_rainfall_pct": float(round(100 * df.rainfall.isna().mean(), 1)),
    "level_counts": df.infestation_level.value_counts().to_dict(),
}
json.dump(stats, open(OUT + "summary.json", "w"), indent=2)
print(stats)


def pri(scores):
    s = np.asarray(scores, float)
    return 100 * (s.mean() - 1) / 2 * min(1, len(s) / 5)


# ---- Figure 1: hex risk maps for the three most-surveyed counties ----
cmap, norm = ListedColormap(RISK), BoundaryNorm([0, 25, 50, 75, 100], 4)
fig, axes = plt.subplots(1, 3, figsize=(15, 5.6))
for ax, county in zip(axes, ["KAKAMEGA", "NYERI", "KILIFI"]):
    d = main[(main.county_name == county) & ~main.gps_mismatch & main.score.notna()]
    hb = ax.hexbin(d.longitude, d.latitude, C=d.score, reduce_C_function=pri, gridsize=22,
                   cmap=cmap, norm=norm, linewidths=0.6, edgecolors=SURF, mincnt=1)
    top = d[d.infestation_level == "HIGH"].pest_name.value_counts().head(3)
    ax.set_title(f"{county.title()}  ·  {len(d):,} reports", loc="left", fontsize=12, fontweight="bold")
    ax.text(0.0, -0.13, "Top HIGH-level problems: " + ", ".join(p.title() for p in top.index),
            transform=ax.transAxes, fontsize=8.5, color=INK2)
    ax.set_aspect(1 / np.cos(np.radians(d.latitude.median())))
    ax.grid(color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.tick_params(labelsize=8)
fig.legend(handles=[Patch(color=c, label=l) for c, l in zip(RISK, RISK_LABELS)], title="PestLand Risk Index",
           loc="upper right", ncol=4, frameon=False, fontsize=9, title_fontsize=9)
fig.suptitle("Risk map - hexagon cells coloured by PestLand Risk Index (severity x confidence)",
             x=0.01, ha="left", fontsize=14, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig(OUT + "risk_map_counties.png", dpi=150)
plt.close(fig)

# ---- Figure 2: top problems by infestation level (stacked horizontal bars) ----
lv = ["LOW", "MEDIUM", "HIGH"]
pd_ = df[df.report_type == "PEST/DISEASE"]
top = pd_.pest_name.value_counts().head(12).index[::-1]
t = pd_[pd_.pest_name.isin(top)].groupby(["pest_name", "infestation_level"]).size().unstack(fill_value=0).reindex(index=top, columns=lv, fill_value=0)
fig, ax = plt.subplots(figsize=(10, 6))
left = np.zeros(len(t))
for c, col in zip(lv, [RISK[0], RISK[1], RISK[3]]):
    ax.tick_params(axis="y", labelcolor=INK2)
    ax.barh([p.title() for p in t.index], t[c], left=left, color=col, height=0.62, edgecolor=SURF, linewidth=2, label=c.title())
    left += t[c].values
for y, v in enumerate(left):
    ax.text(v + 40, y, f"{int(v):,}", va="center", fontsize=8.5, color=INK2)
ax.set_xlabel("Reports"); ax.grid(axis="x", color=GRID, lw=0.5); ax.set_axisbelow(True)
ax.legend(title="Infestation level", frameon=False, loc="lower right")
ax.set_title("Top 12 pest/disease problems by infestation level", loc="left", fontsize=13, fontweight="bold")
fig.tight_layout(); fig.savefig(OUT + "top_problems_by_level.png", dpi=150); plt.close(fig)

# ---- Figure 3: weekly reports during the main 2024 campaign ----
c = df[(df.created_at >= "2024-06-01") & (df.created_at < "2024-09-01")].copy()
c["kind"] = np.where(c.report_type == "WEED", "Weed", c.category.fillna("Pest/Disease"))
w = c.groupby([pd.Grouper(key="created_at", freq="W-MON"), "kind"]).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(10, 4.6))
for k, col in zip(["Disease", "Pest", "Weed"], ["#2a78d6", "#eb6834", "#1baf7a"]):
    if k in w:
        ax.plot(w.index, w[k], color=col, lw=2, marker="o", ms=5, label=k)
        ax.annotate(k, (w.index[-1], w[k].iloc[-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color=INK2)
ax.set_ylabel("Reports per week"); ax.grid(axis="y", color=GRID, lw=0.5)
ax.legend(frameon=False, loc="upper left")
ax.set_title("Weekly reports, June-August 2024 surveillance campaign", loc="left", fontsize=13, fontweight="bold")
fig.tight_layout(); fig.savefig(OUT + "weekly_trend.png", dpi=150); plt.close(fig)
