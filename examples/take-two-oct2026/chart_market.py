"""Chart: global games market 2026E by platform (Newzoo). Syz Visual style."""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
D = os.path.dirname(os.path.abspath(__file__))
for w in ["Regular", "SemiBold", "Bold", "ExtraBold"]:
    fm.fontManager.addfont(f"{D}/fonts/Nunito-{w}.ttf")
plt.rcParams["font.family"] = "Nunito"
NAVY, BLUEB, ORANGE, GOLD, AXIS, SPINE, GRID, GREY = "#202945", "#4B5F80", "#FF6C0E", "#FFC545", "#5A5F68", "#D6D9DE", "#EDEFF2", "#8A8F98"
seg = ["Mobile", "Console", "PC"]; rev = [121.1, 46.9, 45.9]; g = [6.8, 5.1, 5.3]
fig, ax = plt.subplots(figsize=(12.5, 3.6), dpi=200)
fig.subplots_adjust(left=0.10, right=0.96, top=0.95, bottom=0.16)
ax.set_facecolor("white"); fig.patch.set_facecolor("white")
y = np.arange(len(seg))[::-1]
cols = [BLUEB, ORANGE, BLUEB]
ax.barh(y, rev, height=0.56, color=cols, zorder=3)
for yi, r, gi, c in zip(y, rev, g, cols):
    ax.text(r + 1.5, yi, f"${r:.1f}bn", va="center", fontsize=12, fontweight="bold", color=c)
    ax.text(r + 17, yi, f"+{gi:.1f}% y/y", va="center", fontsize=10.5, color=AXIS)
ax.set_yticks(y); ax.set_yticklabels(seg, fontsize=12, fontweight="bold", color=NAVY)
ax.set_xlim(0, 150); ax.set_xlabel("2026E revenue, USD bn", fontsize=10, color=AXIS)
ax.spines[["top", "right", "left"]].set_visible(False); ax.spines["bottom"].set_color(SPINE)
ax.tick_params(axis="x", colors=AXIS, labelsize=9.5); ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
fig.savefig(f"{D}/img/market.png", dpi=200, facecolor="white"); plt.close(fig)
