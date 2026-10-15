"""syz_charts.py — Syz Visual chart kit (white-background report charts, Research Comment format)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

FONT_DIR = "/home/claude/fonts"
ORANGE, AMBER, GOLD = "#FF6C0E", "#FFA400", "#FFC545"
NAVY, BLUEB = "#202945", "#4B5F80"
MINT, TEAL, SKY, PEACH, MULB = "#3BAF90", "#9DD9D2", "#79D6FF", "#E6A4AD", "#AC5D85"
GREY, AXIS_TXT, SPINE, GRID, BRONZE = "#8A8F98", "#5A5F68", "#D6D9DE", "#EDEFF2", "#B87333"
SYZ_GRAD = LinearSegmentedColormap.from_list("syz", [ORANGE, GOLD])
DASH = (0, (5, 4))


def setup_fonts():
    for w in ["Light", "Regular", "SemiBold", "Bold", "ExtraBold"]:
        fm.fontManager.addfont(f"{FONT_DIR}/Nunito-{w}.ttf")
    plt.rcParams["font.family"] = "Nunito"


def style_ax(ax, grid_axis="y"):
    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(SPINE)
    ax.tick_params(colors=AXIS_TXT, labelsize=9.5, length=3)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, zorder=0)


def header(fig, title, subtitle, footnote, title_y=0.945, sub_y=0.906, bar_y=0.886, foot_y=0.032):
    """Standalone-PNG header: navy title, grey subtitle, orange->gold rule, grey source footnote."""
    fig.patch.set_facecolor("white")
    fig.text(0.07, title_y, title, fontsize=16.5, fontweight="bold", color=NAVY, ha="left")
    fig.text(0.07, sub_y, subtitle, fontsize=10.5, color=AXIS_TXT, ha="left")
    bar = fig.add_axes([0.07, bar_y, 0.89, 0.006])
    bar.imshow(np.linspace(0, 1, 256).reshape(1, -1), aspect="auto", cmap=SYZ_GRAD)
    bar.set_axis_off()
    fig.text(0.07, foot_y, footnote, fontsize=8, color=GREY, ha="left")


def source_line(provider, asof, *notes):
    return " · ".join([f"Source: Syz Research, {provider}", f"As of {asof}", *[n for n in notes if n]])


def legend(ax, loc="lower left"):
    leg = ax.legend(loc=loc, frameon=False, fontsize=10.5)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")
    return leg


def _last(y):
    v = np.where(~np.isnan(y))[0]
    return v[-1] if len(v) else None


# ---------------------------------------------------------------- archetype 1: line + threshold
def line_chart(path, dates, series, title, subtitle, footnote, threshold=None, ylim=None,
               ylabel="", floor_note=None, year_step=1, legend_loc="lower left"):
    """series: list of dicts {y, label, color}. First series = Blueberry, second = Tiger Orange by convention."""
    x = mdates.date2num(dates)
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.07, right=0.96)
    style_ax(ax)
    if threshold is not None:
        for s in series:
            y = np.asarray(s["y"], float)
            ax.fill_between(x, y, threshold, where=~np.isnan(y) & (y < threshold), interpolate=True,
                            color=s["color"], alpha=0.14, linewidth=0, zorder=1)
        ax.axhline(threshold, color=NAVY, linestyle=DASH, linewidth=1.2, alpha=0.85, zorder=2)
    for s in series:
        ax.plot(x, s["y"], color=s["color"], linewidth=1.9, zorder=3, label=s["label"])
    # end markers + bold value labels (higher final value above, lower below)
    ends = []
    for s in series:
        y = np.asarray(s["y"], float); i = _last(y)
        tag = "" if i == len(y) - 1 else f" ({dates[i].strftime('%b')})"
        ends.append((y[i], i, s, tag))
    for rank, (val, i, s, tag) in enumerate(sorted(ends, key=lambda e: -e[0])):
        ax.plot(x[i], val, "o", color=s["color"], ms=5, zorder=4)
        ax.annotate(f"{val:.1f}{tag}", (x[i], val), xytext=(12, 6 if rank == 0 else -14),
                    textcoords="offset points", color=s["color"], fontsize=10, fontweight="bold")
    if ylim:
        ax.set_ylim(*ylim)
    if floor_note:   # (text, x_date_index) — grey label at the clipped floor
        txt, xi = floor_note
        ax.annotate(txt, (x[xi], ax.get_ylim()[0] + 0.3), xytext=(22, 4), textcoords="offset points",
                    ha="left", fontsize=8, color=GREY, fontweight="bold",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))
    ax.set_ylabel(ylabel, fontsize=10, color=AXIS_TXT)
    ax.xaxis.set_major_locator(mdates.YearLocator(year_step))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    first = min(np.where(~np.isnan(np.asarray(s["y"], float)))[0][0] for s in series)
    ax.set_xlim(x[first] - 40, x[-1] + 360)
    legend(ax, legend_loc)
    header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- archetype 2: stacked panels of bars
def panel_bars(path, dates, panels, title, subtitle, footnote, threshold=50, ylim=(0, 108),
               yticks=(0, 25, 50, 75, 100), pct=True, bar_width=24, year_step=1):
    """panels: list of dicts {y, color, label}. Bars below threshold drawn at alpha 0.32."""
    x = mdates.date2num(dates)
    fig, axes = plt.subplots(len(panels), 1, figsize=(12.5, 3.9 * len(panels)), dpi=200, sharex=True)
    axes = np.atleast_1d(axes)
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(top=0.855, bottom=0.09, left=0.07, right=0.96, hspace=0.30)
    for ax, p in zip(axes, panels):
        y = np.asarray(p["y"], float)
        style_ax(ax)
        above = y >= threshold; below = (~above) & ~np.isnan(y)
        ax.bar(x[above], y[above], width=bar_width, color=p["color"], alpha=0.95, linewidth=0, zorder=3)
        ax.bar(x[below], y[below], width=bar_width, color=p["color"], alpha=0.32, linewidth=0, zorder=3)
        ax.axhline(threshold, color=NAVY, linestyle=DASH, linewidth=1.1, alpha=0.85, zorder=4)
        ax.set_ylim(*ylim); ax.set_yticks(list(yticks))
        if pct:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
        i = _last(y)
        ax.annotate(f"{y[i]:.0f}{'%' if pct else ''}", (x[i], y[i]), xytext=(6, 3),
                    textcoords="offset points", color=p["color"], fontsize=11, fontweight="bold")
        ax.set_title(p["label"], fontsize=11.5, fontweight="bold", color=NAVY, loc="left", pad=7)
    axes[-1].xaxis.set_major_locator(mdates.YearLocator(year_step))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[-1].set_xlim(x[0] - 40, x[-1] + 220)
    header(fig, title, subtitle, footnote, sub_y=0.908, bar_y=0.888, foot_y=0.028)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- archetype 3: quadrant scatter
QUAD_LABELS = ("Expansion & accelerating", "Expansion & slowing",
               "Contraction & improving", "Contraction & deteriorating")   # TR, BR, TL, BL


def quadrant_scatter(path, pts, title, subtitle, footnote, xthr=50, ythr=0, xlabel="", ylabel="",
                     highlight=(), quad_labels=QUAD_LABELS, label_offsets=None):
    """pts: {name: (x, y)}. Highlighted names get large dots + bold navy labels."""
    label_offsets = label_offsets or {}
    xs = np.array([v[0] for v in pts.values()]); ys = np.array([v[1] for v in pts.values()])
    xmin, xmax = np.floor(xs.min()) - 0.7, np.ceil(xs.max()) + 0.7
    ymin, ymax = np.floor(ys.min() * 2) / 2 - 0.5, np.ceil(ys.max() * 2) / 2 + 1.0
    fig, ax = plt.subplots(figsize=(12.5, 7.6), dpi=200)
    fig.subplots_adjust(top=0.855, bottom=0.135, left=0.07, right=0.96)
    style_ax(ax, grid_axis="both")
    ax.axvline(xthr, color=NAVY, linestyle=DASH, linewidth=1.1, alpha=0.8, zorder=2)
    ax.axhline(ythr, color=NAVY, linestyle=DASH, linewidth=1.1, alpha=0.8, zorder=2)
    ax.fill_between([xthr, xmax], ythr, ymax, color=ORANGE, alpha=0.05, zorder=0)
    ax.fill_between([xmin, xthr], ymin, ythr, color=BLUEB, alpha=0.06, zorder=0)
    kw = dict(fontsize=8.5, fontweight="bold", alpha=0.75)
    tr, br, tl, bl = quad_labels
    ax.text(xmax - 0.15, ymax - 0.20, tr, color=ORANGE, ha="right", va="top", **kw)
    ax.text(xmax - 0.15, ymin + 0.20, br, color=BRONZE, ha="right", va="bottom", **kw)
    ax.text(xmin + 0.15, ymax - 0.20, tl, color=MINT, ha="left", va="top", **kw)
    ax.text(xmin + 0.15, ymin + 0.20, bl, color=MULB, ha="left", va="bottom", **kw)
    placed = []
    for k, (px, py) in sorted(pts.items(), key=lambda kv: -kv[1][1]):
        hi = k in highlight
        col = ORANGE if (px >= xthr and py >= ythr) else (BLUEB if px >= xthr else (MINT if py >= ythr else MULB))
        ax.scatter(px, py, s=64 if hi else 34, color=col, alpha=0.95 if hi else 0.55,
                   edgecolor="white", linewidth=0.8, zorder=3)
        if hi:
            dx, dy, ha = label_offsets.get(k, (7, 4, "left"))
            if k not in label_offsets and any(abs(a - px) < 1.1 and abs(b - py) < 0.45 for a, b in placed):
                dy = -12
            ax.annotate(k, (px, py), xytext=(dx, dy), textcoords="offset points",
                        fontsize=8.8, color=NAVY, fontweight="bold", zorder=4, ha=ha)
            placed.append((px, py))
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.set_xlabel(xlabel, fontsize=10, color=AXIS_TXT)
    ax.set_ylabel(ylabel, fontsize=10, color=AXIS_TXT)
    header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- PDF embedding
CROPS = {"line": (0.122, 0.052), "panels": (0.105, 0.048), "scatter": (0.125, 0.050)}


def crop_for_pdf(src, dst, kind):
    """Strip the standalone header/footnote: in the PDF, titles are typeset in HTML."""
    top, bot = CROPS[kind]
    im = Image.open(src); w, h = im.size
    im.crop((0, int(h * top), w, int(h * (1 - bot)))).save(dst)
