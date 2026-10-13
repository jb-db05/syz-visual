"""Goldman Sachs Q3 2026 Research Comment: data (figures quoted in the text) -> charts -> 3-page PDF.
Next update: edit DATA / TEXT below and re-run. Requires /home/claude/{fonts,syz_charts.py,syz_logo_hq.png,template.html}."""
import sys, os
sys.path.insert(0, "/home/claude")
from syz_charts import *
import syz_charts
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
setup_fonts()

def geom(h):
    """Header/margin fractions that keep the 6.4in-canvas geometry in inches when the canvas height is h."""
    return dict(title_y=1-0.352/h, sub_y=1-0.60/h, bar_y=1-0.73/h, foot_y=0.205/h)
def adj(fig, h, left, right=0.96):
    fig.subplots_adjust(top=1-1.02/h, bottom=0.77/h, left=left, right=right)
H = {"c1": 5.6, "c2": 4.8, "c3": 4.8}
for k, h in H.items():
    syz_charts.CROPS[k] = (0.78/h, 0.333/h)
SRC = source_line("company reports", "13 October 2026")

# ---- Chart 1: year-on-year revenue growth (all values quoted in the text) -------------------------
G1 = [("Equities financing", 96, "m"), ("Equities", 72, "m"), ("Equity underwriting", 43, "b"),
      ("Global Banking & Markets", 32, "m"), ("Group revenues", 23, "b"), ("AWM management fees", 22, "b"),
      ("Investment banking fees", 21, "b"), ("Advisory", 18, "b"), ("Debt underwriting", 15, "b"),
      ("Asset & Wealth Management", 14, "b")]

def hbars_growth(path):
    fig, ax = plt.subplots(figsize=(12.5, H["c1"]), dpi=200)
    adj(fig, H["c1"], 0.22)
    style_ax(ax, "x")
    for i, (n, v, k) in enumerate(G1[::-1]):
        ax.barh(i, v, height=0.62, color=ORANGE if k == "m" else BLUEB, zorder=3)
        ax.text(v + 1.2, i, f"+{v}%", va="center", fontsize=10.5, fontweight="bold", color=NAVY)
    ax.set_yticks(range(len(G1))); ax.set_yticklabels([g[0] for g in G1[::-1]], fontsize=10.5, color=NAVY)
    ax.set_xlim(0, 108); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.axvline(0, color=NAVY, linewidth=1)
    from matplotlib.patches import Patch
    leg = ax.legend(handles=[Patch(color=ORANGE, label="Markets"), Patch(color=BLUEB, label="Banking, wealth & group")],
                    loc="lower right", frameon=False, fontsize=10.5)
    for t in leg.get_texts(): t.set_color(NAVY); t.set_fontweight("bold")
    header(fig, "Goldman Sachs — Revenue Growth by Business",
           "Q3 2026 vs. Q3 2025, % change · Markets in orange",
           source_line("company reports", "13 October 2026", "Year-on-year growth as quoted in Q3 2026 results"), **geom(H["c1"]))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

# ---- Chart 2: results vs consensus ---------------------------------------------------------------
G2 = [("EPS", 33), ("Equities", 25), ("Revenues", 12), ("IB fees", 12), ("FICC", -7)]

def bars_surprise(path):
    fig, ax = plt.subplots(figsize=(12.5, H["c2"]), dpi=200)
    adj(fig, H["c2"], 0.07)
    style_ax(ax)
    for i, (n, v) in enumerate(G2):
        ax.bar(i, v, width=0.55, color=BLUEB if v >= 0 else MULB, zorder=3)
        ax.text(i, v + (1.2 if v >= 0 else -1.2), f"{v:+d}%", ha="center", va="bottom" if v >= 0 else "top",
                fontsize=11.5, fontweight="bold", color=BLUEB if v >= 0 else MULB)
    ax.axhline(0, color=NAVY, linestyle=DASH, linewidth=1.2, alpha=0.85, zorder=4)
    ax.set_xticks(range(len(G2))); ax.set_xticklabels([g[0] for g in G2], fontsize=11, color=NAVY, fontweight="bold")
    ax.set_ylim(-14, 40); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.tick_params(axis="x", length=0)
    header(fig, "Goldman Sachs — Q3 2026 vs. Consensus",
           "Actual vs. consensus expectation, % surprise · Dashed line = in line",
           source_line("company reports", "13 October 2026", "Surprise vs. consensus as quoted in the text"), **geom(H["c2"]))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

# ---- Chart 3: Q3 revenues by source, recurring vs. cyclical --------------------------------------
G3 = [("Equities", [("Financing", 3.4, BLUEB), ("Trading & other", 3.0, ORANGE)]),
      ("Asset & Wealth Mgmt", [("Management fees", 3.6, BLUEB), ("Incentive fees & other", 1.5, ORANGE)]),
      ("Fixed Income (FICC)", [("Trading", 3.5, ORANGE)]),
      ("Investment banking fees", [("Fees", 3.2, ORANGE)])]

def stacked_revenues(path):
    fig, ax = plt.subplots(figsize=(12.5, H["c3"]), dpi=200)
    adj(fig, H["c3"], 0.20)
    style_ax(ax, "x")
    for i, (n, segs) in enumerate(G3[::-1]):
        left = 0
        for lab, v, c in segs:
            ax.barh(i, v, left=left, height=0.62, color=c, edgecolor="white", linewidth=1.5, zorder=3)
            ax.text(left + v / 2, i, f"{lab}\n${v:.1f}bn", ha="center", va="center", fontsize=9.5,
                    fontweight="bold", color="white", zorder=4)
            left += v
        ax.text(left + 0.1, i, f"${left:.1f}bn", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_yticks(range(len(G3))); ax.set_yticklabels([g[0] for g in G3[::-1]], fontsize=10.5, color=NAVY)
    ax.set_xlim(0, 7.6); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:.0f}bn"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    leg = ax.legend(handles=[Patch(color=BLUEB, label="Recurring-type (financing balances, management fees)"),
                             Patch(color=ORANGE, label="Activity-sensitive")], loc="lower right", frameon=False, fontsize=10)
    for t in leg.get_texts(): t.set_color(NAVY); t.set_fontweight("bold")
    header(fig, "Goldman Sachs — Q3 2026 Revenues by Source",
           "$bn · Equities and AWM split into recurring-type and activity-sensitive components",
           source_line("company reports", "13 October 2026",
                       "Equities trading & other and AWM incentive & other derived as segment total minus quoted component"), **geom(H["c3"]))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

if __name__ == "__main__":
    for f, k, fn in [("c1", "c1", hbars_growth), ("c2", "c2", bars_surprise), ("c3", "c3", stacked_revenues)]:
        fn(f"{OUT}/{f}.png"); crop_for_pdf(f"{OUT}/{f}.png", f"/home/claude/{f}_crop.png", k)
    os.rename(f"{OUT}/c1.png", f"{OUT}/Chart1_GS_Q3_2026_Growth.png")
    os.rename(f"{OUT}/c2.png", f"{OUT}/Chart2_GS_Q3_2026_vs_Consensus.png")
    os.rename(f"{OUT}/c3.png", f"{OUT}/Chart3_GS_Q3_2026_Revenue_Mix.png")
