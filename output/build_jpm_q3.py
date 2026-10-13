"""JPMorgan Chase Q3 2026 Research Comment: charts from figures quoted in the text. Needs /home/claude/{fonts,syz_charts.py}."""
import sys, os
sys.path.insert(0, "/home/claude")
from syz_charts import *
import syz_charts
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = os.path.dirname(os.path.abspath(__file__))
setup_fonts()
plt.rcParams['text.parse_math'] = False
def geom(h): return dict(title_y=1-0.352/h, sub_y=1-0.60/h, bar_y=1-0.73/h, foot_y=0.205/h)
def adj(fig, h, left, right=0.96): fig.subplots_adjust(top=1-1.02/h, bottom=0.77/h, left=left, right=right)
H = {"j1": 5.8, "j2": 3.9, "j3": 4.6}
for k, h in H.items(): syz_charts.CROPS[k] = (0.78/h, 0.333/h)
def leg(ax, handles, loc="lower right"):
    l = ax.legend(handles=handles, loc=loc, frameon=False, fontsize=10.5)
    for t in l.get_texts(): t.set_color(NAVY); t.set_fontweight("bold")

# Chart 1: Q3 growth y/y, figures as quoted
G1 = [("Equities", 49, "m"), ("Advisory", 32, "b"), ("Markets", 15, "m"), ("Investment banking fees", 14, "b"),
      ("Asset & Wealth Management", 14, "b"), ("Payments", 14, "b"), ("Net interest income", 13, "b"),
      ("Average loans", 10, "b"), ("Consumer & Community Banking", 9, "b"), ("Managed revenues", 8, "b"),
      ("Deposits", 8, "b"), ("Fixed Income", -4, "m")]
def c1(path):
    h = H["j1"]; fig, ax = plt.subplots(figsize=(12.5, h), dpi=200); adj(fig, h, 0.24); style_ax(ax, "x")
    n = len(G1)
    for i, (nm, v, k) in enumerate(G1[::-1]):
        ax.barh(i, v, height=0.62, color=ORANGE if k == "m" else BLUEB, zorder=3)
        ax.text(v + (1 if v >= 0 else -1), i, f"{v:+d}%", va="center", ha="left" if v >= 0 else "right",
                fontsize=10.5, fontweight="bold", color=NAVY)
    ax.set_yticks(range(n)); ax.set_yticklabels([g[0] for g in G1[::-1]], fontsize=10.5, color=NAVY)
    ax.set_xlim(-9, 56); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0); ax.axvline(0, color=NAVY, linewidth=1)
    leg(ax, [Patch(color=ORANGE, label="Markets"), Patch(color=BLUEB, label="Banking, wealth, payments & balance sheet")])
    header(fig, "JPMorgan Chase — Growth by Business", "Q3 2026 vs. Q3 2025, % change · Markets in orange",
           source_line("company reports", "13 October 2026", "Growth rates as quoted in Q3 2026 results"), **geom(h))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

# Chart 2: 2027 NII ex-Markets: guidance vs Street
def c2(path):
    h = H["j2"]; fig, ax = plt.subplots(figsize=(12.5, h), dpi=200); adj(fig, h, 0.24); style_ax(ax, "x")
    ax.hlines(2, 94, 107, color=GRID, linewidth=0, zorder=1)
    ax.plot([103, 104.5], [1, 1], color=BLUEB, linewidth=9, solid_capstyle="round", zorder=3)
    ax.text(105.1, 1, "$103–104.5bn", va="center", fontsize=11, fontweight="bold", color=BLUEB)
    ax.plot(97.2, 0, "o", color=BLUEB, ms=14, zorder=3); ax.text(97.9, 0, "$97.2bn", va="center", fontsize=11, fontweight="bold", color=BLUEB)
    ax.plot(107, 2, "o", color=ORANGE, ms=14, zorder=3); ax.text(107.7, 2, "$107bn", va="center", fontsize=11.5, fontweight="bold", color=ORANGE)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["2026 expected", "2027 analysts' estimates", "2027 JPMorgan guidance"], fontsize=10.5, color=NAVY)
    ax.set_ylim(-0.6, 2.6); ax.set_xlim(94, 111.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:.0f}bn"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    header(fig, "JPMorgan Chase — 2027 Net Interest Income Outlook", "NII excluding Markets, $bn · Axis starts at $94bn",
           source_line("company reports", "13 October 2026", "Analyst range as quoted in the text"), **geom(h))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

# Chart 3: Q3 revenues by business, y/y in labels
G3 = [("Consumer & Community Banking", [("+9% y/y", 21.2, BLUEB)]),
      ("Markets", [("Equities +49%", 5.0, ORANGE), ("Fixed Income −4%", 5.3, ORANGE)]),
      ("Asset & Wealth Management", [("+14% y/y", 6.9, BLUEB)]),
      ("Investment banking fees", [("+14% y/y", 3.0, BLUEB)])]
def c3(path):
    h = H["j3"]; fig, ax = plt.subplots(figsize=(12.5, h), dpi=200); adj(fig, h, 0.24); style_ax(ax, "x")
    for i, (n, segs) in enumerate(G3[::-1]):
        left = 0
        for lab, v, c in segs:
            ax.barh(i, v, left=left, height=0.62, color=c, edgecolor="white", linewidth=1.5, zorder=3)
            ax.text(left + v / 2, i, (f"{lab}\n${v:.1f}bn" if len(segs) > 1 else lab),
                    ha="center", va="center", fontsize=9.5, fontweight="bold", color="white", zorder=4)
            left += v
        ax.text(left + 0.3, i, f"${left:.1f}bn", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_yticks(range(len(G3))); ax.set_yticklabels([g[0] for g in G3[::-1]], fontsize=10.5, color=NAVY)
    ax.set_xlim(0, 24); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:.0f}bn"))
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    leg(ax, [Patch(color=ORANGE, label="Markets"), Patch(color=BLUEB, label="Banking & wealth")])
    header(fig, "JPMorgan Chase — Q3 2026 Revenues by Business", "$bn, with year-on-year growth · Markets split into Equities and Fixed Income",
           source_line("company reports", "13 October 2026", "Fixed Income derived as Markets $10.3bn minus Equities $5.0bn"), **geom(h))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

if __name__ == "__main__":
    for f, k, fn, name in [("j1", "j1", c1, "Chart1_JPM_Q3_2026_Growth"), ("j2", "j2", c2, "Chart2_JPM_2027_NII_Outlook"),
                           ("j3", "j3", c3, "Chart3_JPM_Q3_2026_Revenue_Mix")]:
        fn(f"{OUT}/{name}.png"); crop_for_pdf(f"{OUT}/{name}.png", f"/home/claude/{f}_crop.png", k)
