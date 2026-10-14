"""Morgan Stanley: share price vs. consensus EPS (Bloomberg weekly). Syz Visual chart, standalone PNG + PDF crop."""
import sys, os
sys.path.insert(0, "/home/claude")
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator, NullLocator
import syz_charts as sc
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
sc.setup_fonts()
plt.rcParams["text.parse_math"] = False
d = pd.read_excel(f"{OUT}/data/MS_bloomberg_weekly.xlsx").sort_values("Date")
d.columns = ["date", "px", "eps", "ma40", "pe"]
ASOF = d["date"].iloc[-1].strftime("%-d %B %Y")
PE_ANCHOR = 12            # log axes scaled so price and EPS lines cross where forward P/E = 12x
EPS_LIM = (0.7, 25)
i = d.set_index("date")
PE_AVG = i["pe"].mean()
last = d.iloc[-1]

x = mdates.date2num(d["date"])
fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.07, right=0.92)
sc.style_ax(ax)
ax2 = ax.twinx()
ax2.spines[["top", "left"]].set_visible(False); ax2.spines["right"].set_color(sc.SPINE)
ax2.tick_params(colors=sc.AXIS_TXT, labelsize=9.5, length=3)
ax.plot(x, d["eps"], color=sc.ORANGE, linewidth=1.9, zorder=3, label="Consensus EPS, BEst ($, lhs)")
ax2.plot(x, d["px"], color=sc.BLUEB, linewidth=1.6, zorder=3, label="Share price ($, rhs)")
ax2.plot(x, d["ma40"], color=sc.NAVY, linewidth=1.1, linestyle=sc.DASH, alpha=0.8, zorder=3, label="40-week moving average (rhs)")
for a, lim in ((ax, EPS_LIM), (ax2, (EPS_LIM[0] * PE_ANCHOR, EPS_LIM[1] * PE_ANCHOR))):
    a.set_yscale("log"); a.set_ylim(*lim); a.yaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20]))
ax2.yaxis.set_major_locator(FixedLocator([10, 20, 50, 100, 200]))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.plot(x[-1], last.eps, "o", color=sc.ORANGE, ms=5, zorder=4)
ax.annotate(f"{last.eps:.1f}", (x[-1], last.eps), xytext=(10, -14), textcoords="offset points",
            color=sc.ORANGE, fontsize=10, fontweight="bold")
ax2.plot(x[-1], last.px, "o", color=sc.BLUEB, ms=5, zorder=4)
ax2.annotate(f"{last.px:,.0f}", (x[-1], last.px), xytext=(10, 6), textcoords="offset points",
             color=sc.BLUEB, fontsize=10, fontweight="bold")
ax.text(0.985, 0.04, f"Forward P/E {last.pe:.1f}x (avg. since 2005 {PE_AVG:.1f}x)", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=10, color=sc.NAVY, fontweight="bold",
        bbox=dict(facecolor="white", edgecolor=sc.SPINE, boxstyle="round,pad=0.4"))
ax.set_xlim(x[0] - 40, x[-1] + 620)
ax.xaxis.set_major_locator(FixedLocator(mdates.date2num(pd.date_range("2006", d["date"].iloc[-1], freq="2YS"))))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
leg = ax.legend(h2 + h1, l2 + l1, loc="upper left", frameon=False, fontsize=10.5)
for t in leg.get_texts(): t.set_color(sc.NAVY); t.set_fontweight("bold")
sc.header(fig, "Morgan Stanley — Share Price vs. Consensus Earnings",
          f"Weekly, Apr 2005–Oct 2026 · log scales aligned so the lines cross at {PE_ANCHOR}x forward P/E",
          sc.source_line("Bloomberg", ASOF, "No consensus EPS published Dec 2007–Mar 2009"))
png = f"{OUT}/MS_Share_Price_vs_EPS.png"
fig.savefig(png, dpi=200, facecolor="white"); plt.close(fig)
sc.crop_for_pdf(png, f"{OUT}/MS_Share_Price_vs_EPS_crop.png", "line")
print(png, ASOF, round(PE_AVG, 1))
