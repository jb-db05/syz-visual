"""Morgan Stanley Q3 2026: Charts 1-2 from figures quoted in the text (Chart 3 = build_chart.py, Bloomberg data)."""
import sys, os
sys.path.insert(0, "/home/claude")
from syz_charts import *
import syz_charts
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = os.path.dirname(os.path.abspath(__file__))
setup_fonts()
plt.rcParams["text.parse_math"] = False
def geom(h): return dict(title_y=1-0.352/h, sub_y=1-0.60/h, bar_y=1-0.73/h, foot_y=0.205/h)
def adj(fig, h, left, right=0.96): fig.subplots_adjust(top=1-1.02/h, bottom=0.77/h, left=left, right=right)
H = {"m1": 5.8, "m2": 4.4}
for k, h in H.items(): syz_charts.CROPS[k] = (0.78/h, 0.333/h)
def leg(ax, handles, loc="lower right"):
    l = ax.legend(handles=handles, loc=loc, frameon=False, fontsize=10.5)
    for t in l.get_texts(): t.set_color(NAVY); t.set_fontweight("bold")
SRC = source_line("company reports", "14 October 2026", "Figures as quoted in Q3 2026 results")

G1 = [("Equities", 41, "i"), ("Advisory", 30, "i"), ("Fee-based client assets", 19, "w"),
      ("Institutional Securities", 18, "i"), ("WM asset management revenues", 16, "w"),
      ("Investment Management assets", 13, "w"), ("Wealth Management revenues", 10, "w"),
      ("Investment banking revenues", 2, "i"), ("Debt underwriting", -3, "i"), ("Fixed Income", -7, "i"),
      ("Investment Management revenues", -12, "w"), ("Equity underwriting", -19, "i")]

def c1(path):
    h = H["m1"]; fig, ax = plt.subplots(figsize=(12.5, h), dpi=200); adj(fig, h, 0.25); style_ax(ax, "x")
    for i, (nm, v, k) in enumerate(G1[::-1]):
        ax.barh(i, v, height=0.62, color=ORANGE if k == "i" else BLUEB, zorder=3)
        ax.text(v + (0.8 if v >= 0 else -0.8), i, f"{v:+d}%", va="center", ha="left" if v >= 0 else "right",
                fontsize=10.5, fontweight="bold", color=NAVY)
    ax.set_yticks(range(len(G1))); ax.set_yticklabels([g[0] for g in G1[::-1]], fontsize=10.5, color=NAVY)
    ax.set_xlim(-26, 48); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0); ax.axvline(0, color=NAVY, linewidth=1)
    leg(ax, [Patch(color=ORANGE, label="Institutional Securities"), Patch(color=BLUEB, label="Wealth & Investment Management")])
    header(fig, "Morgan Stanley — Growth by Business", "Q3 2026 vs. Q3 2025, % change · revenues and client assets",
           SRC, **geom(h))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

G2 = [("Consensus", 113, BLUEB, 0.32), ("Q3 actual", 232, ORANGE, 0.95), (None, 0, None, 0),
      ("Q2", 39, BLUEB, 0.32), ("Q3", 80.5, ORANGE, 0.95)]

def c2(path):
    h = H["m2"]; fig, ax = plt.subplots(figsize=(12.5, h), dpi=200); adj(fig, h, 0.07); style_ax(ax)
    for i, (lab, v, c, a) in enumerate(G2):
        if lab is None: continue
        ax.bar(i, v, width=0.62, color=c, alpha=a, linewidth=0, zorder=3)
        ax.text(i, v + 5, f"${v:g}bn", ha="center", va="bottom", fontsize=11.5, fontweight="bold",
                color=c if a > 0.5 else BLUEB)
    ax.set_xticks([0, 1, 3, 4]); ax.set_xticklabels([g[0] for g in G2 if g[0]], fontsize=11, color=NAVY, fontweight="bold")
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 315); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:.0f}bn"))
    for xc, t in [(0.5, "Net new assets: 2.1x expectations"), (3.5, "Fee-based flows: 2.1x Q2")]:
        ax.text(xc, 308, t, ha="center", va="top", fontsize=11.5, fontweight="bold", color=NAVY)
    ax.axvline(2, color=SPINE, linewidth=1)
    header(fig, "Morgan Stanley — Wealth Management Flows", "$bn · Q3 2026 vs. analysts' expectation and vs. Q2 2026",
           source_line("company reports", "14 October 2026", "Consensus net new assets as quoted in the text · just over half of Q3 net new assets IPO-related"), **geom(h))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

if __name__ == "__main__":
    for k, fn, name in [("m1", c1, "Chart1_MS_Q3_2026_Growth"), ("m2", c2, "Chart2_MS_Q3_2026_WM_Flows")]:
        fn(f"{OUT}/{name}.png"); crop_for_pdf(f"{OUT}/{name}.png", f"/home/claude/{k}_crop.png", k)
