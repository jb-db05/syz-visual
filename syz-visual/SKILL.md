---
name: "syz-visual"
description: "Produce Syz Research Comment PDFs and charts in the exact format of the Oct 2026 Global PMI comment (3-page A4: 2 content pages with section headings and 3 charts, navy Base Case box, page 3 source + disclaimer). Use for any 'Syz Visual' request."
---

# Syz Visual — Research Comment format

Reproduce **exactly** the format of *Research Comment — Global PMI: The Expansion Shifts into Higher Gear* (2 October 2026): same page layout, typography, section headings, spacing, text structure, voice and chart styling. Works for any macro dataset (PMI, CPI, retail sales, rates, breadth, cross-section), not only PMI.

Where this skill and `syz-house-style` differ, **this skill wins** (e.g. chart header = title + subtitle + orange→gold rule *under* the subtitle, not a bar on top). Apply silently; do not describe the style back to the user.

## Deliverables (every time)
1. `Research_Comment_<Topic>_<MonYYYY>.pdf` — 3-page A4 (pages 1–2 content, page 3 source + disclaimer).
2. Three standalone chart PNGs **with** their header/footnote (for decks and LinkedIn).
3. The build script (data → charts → PDF), parameterised for next month's update.

## Workflow
1. **Data first, silently.** Inspect every sheet; identify the date axis, series, units, weights. Note the window and the latest print per series. Flag stale, missing or revised values. Compute every number you will quote (levels, 1m/6m changes, "highest since", counts). Never invent or extrapolate.
2. **Pick the three charts** (see Chart archetypes). Default pattern: Chart 1 = headline time series; Chart 2 = breadth/distribution panels; Chart 3 = cross-section quadrant map.
3. **Setup** (fonts, logo, WeasyPrint), then write `syz_charts.py` (below) and build the charts.
4. **Crop** each chart for the PDF (`crop_for_pdf`): the PDF typesets titles in HTML, so the chart's own header/footnote is removed.
5. **Write the text and the section headings** following the Text format rules.
6. **Fill the HTML template** (below), render with WeasyPrint, rasterise all pages and **look at them**.
7. **Fit to exactly 3 pages** (Fit & QA). Then deliver PDF + 3 PNGs + script.

## Setup
```bash
pip install weasyprint --break-system-packages -q
mkdir -p /home/claude/fonts && cd /home/claude/fonts
curl -sL -o Nunito.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/Nunito%5Bwght%5D.ttf"
python3 -c "
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont
for w,n in [(300,'Light'),(400,'Regular'),(600,'SemiBold'),(700,'Bold'),(800,'ExtraBold')]:
    f=TTFont('Nunito.ttf'); instantiateVariableFont(f,{'wght':w},inplace=True); f.save(f'Nunito-{n}.ttf')
"
# Logo: the project file 'SYZ logo.png' (206x186 RGBA, transparent). Locate and copy:
find / -iname '*syz*logo*.png' 2>/dev/null | head -3   # then: cp <path> /home/claude/syz_logo_hq.png
```
Fallback for fonts if GitHub is blocked: `npm install @fontsource/nunito`, convert the woff files to ttf with fontTools (`f.flavor=None; f.save()`). Never ship without Nunito, and never use a logo with a white box. The font is **Nunito** (rounded terminals, as specified in the Syz Visual Guideline §3.2), not Nunito Sans.

## Chart kit — write to `/home/claude/syz_charts.py` verbatim
```python
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
```

### Chart archetypes and rules
| Archetype | Use for | Fixed geometry |
|---|---|---|
| `line_chart` | Headline series over the full window, with a threshold (50 for PMIs, 2% for inflation, 0 for growth) | 12.5×6.4 in, 200 dpi |
| `panel_bars` | Breadth, distributions, components: one panel per series, sharing the x-axis | 12.5 × 3.9·n in |
| `quadrant_scatter` | Cross-section: level vs. momentum (e.g. PMI level vs. 6-month change) | 12.5×7.6 in |

- **Colour convention:** first/reference series = Blueberry Blue `#4B5F80`; second/emphasis series = Tiger Orange `#FF6C0E`. Quadrants: top-right Tiger Orange, bottom-right Blueberry (label text bronze `#B87333`), top-left Mint, bottom-left Mulberry. Threshold lines are dashed navy `(0,(5,4))`. Shade the area below the threshold at α 0.14 in the series colour; in bar panels, bars below the threshold are drawn at α 0.32.
- **Standalone title** = `<Subject> — <Descriptor>` (em dash), e.g. "Global PMI — Manufacturing vs. Services". **Subtitle** = method, separated by ` · `. **Footnote** = `source_line(provider, "<Month YYYY>", notes…)`, always naming exclusions, truncations and stale prints.
- **Outliers:** if a crisis trough would flatten the chart, floor the y-axis (PMI: 45) and print the truncated values with `floor_note` and in the footnote.
- **Stale series:** the end label gets the month in brackets automatically ("53.7 (Aug)"); also say so in the footnote and in the PDF chart sub-line.
- **Scatter labels:** highlight only key markets (~10–14). Move any label that collides with a corner quadrant label or another label via `label_offsets={name: (dx, dy, ha)}`, e.g. `{"Switzerland": (-9, -3, "right")}`. Every label must sit unambiguously next to its own dot.
- **Other chart types** (e.g. a stacked contribution bar) are allowed only if built with `style_ax` + `header` + `source_line`, using the same figure width (12.5 in), 200 dpi and margins `left=0.07, right=0.96`; add a crop preset in `CROPS` and check the crop visually.

## HTML template — fill every `{{…}}`, change nothing else
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-Regular.ttf'); font-weight: 400; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-Light.ttf'); font-weight: 300; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-SemiBold.ttf'); font-weight: 600; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-Bold.ttf'); font-weight: 700; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-ExtraBold.ttf'); font-weight: 800; }

@page {
  size: A4;
  margin: 18mm 15mm 12.5mm 15mm;
  @top-right { content: url('file:///home/claude/syz_logo_hq.png'); image-resolution: 370dpi; vertical-align: bottom; padding-top: 9mm; }
  @bottom-left {
    /* 6-digit escapes: \0000b7 = middle dot, \0000a0 = no-break space (keeps the space after each dot) */
    content: "Syz Research \0000b7\0000a0{{DOC_TYPE}} \0000b7\0000a0{{DATE}}";
    font-family: 'Nunito'; font-size: 7pt; color: #9AA0A8;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: 'Nunito'; font-size: 7pt; color: #9AA0A8;
  }
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Nunito'; color: #202945; font-size: 8.9pt; line-height: 1.42; }

.gradbar { height: 3.5px; background: linear-gradient(90deg, #FF6C0E 0%, #FFC545 100%); margin-bottom: 4mm; }

.kicker { font-size: 8pt; font-weight: 700; letter-spacing: 1.6px; color: #FF6C0E; text-transform: uppercase; margin-bottom: 1.5mm; }
h1 { font-size: 17pt; font-weight: 800; color: #202945; line-height: 1.22; margin-bottom: 1.5mm; }
.dateline { font-size: 8.5pt; color: #6B7280; margin-bottom: 3.5mm; }

/* Section heading (level 2) — plain text, no rule above */
.sec { break-inside: avoid; break-after: avoid; margin-top: 3.2mm; }
.sec.first { margin-top: 0; }
h2 { font-size: 11pt; font-weight: 800; color: #202945; line-height: 1.2; margin-bottom: 1.4mm; }

p { margin-bottom: 2.2mm; text-align: justify; }

.chart-title { font-size: 9.5pt; font-weight: 700; color: #202945; margin: 1.5mm 0 1.5mm 0; }
.chart-sub { font-size: 7.2pt; color: #6B7280; margin: -1mm 0 1.2mm 0; }
.chart-title .num { color: #FF6C0E; }
img.chart { width: {{W1}}%; display: block; margin: 0 auto 1.2mm auto; }
img.c2 { width: {{W2}}%; }
img.c3 { width: {{W3}}%; }

.bottomline {
  background: #202945; border-radius: 3.5mm; padding: 4mm 5.5mm; color: #FFFFFF;
  margin-top: 3mm;
}
.bottomline .bl-head { font-size: 7.8pt; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: #FFA400; margin-bottom: 1.6mm; }
.bottomline p { color: #E8EAEF; margin-bottom: 0; font-size: 9.3pt; }

/* Page 3: source + disclaimer, pinned to the bottom of the page */
.legal { font-size: 6.8pt; color: #9AA0A8; line-height: 1.4; position: absolute; bottom: 0; left: 0; right: 0; }
.legal .syz { color: #FF6C0E; font-weight: 800; }
.legal .src-line { margin-bottom: 4mm; }
.legal .disc-head { color: #FF6C0E; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 1.5mm; }
.legal p { font-size: 6.8pt; margin-bottom: 1.6mm; text-align: justify; }

.pagebreak { page-break-before: always; }
</style>
</head>
<body>

<!-- PAGE 1 -->
<div class="gradbar"></div>
<div class="kicker">{{DOC_TYPE}} &middot; {{THEME}}</div>
<h1>{{TITLE}}</h1>
<div class="dateline">{{DATE}} &middot; Syz Research</div>

{{INTRO_PARAGRAPHS}}

<div class="sec"><h2>{{H_C1}}</h2></div>
<div class="chart-title"><span class="num">Chart 1</span> &middot; {{C1_TITLE}}</div>
<div class="chart-sub">{{C1_SUB}}</div>
<img class="chart" src="file://{{C1_IMG}}">

{{C1_COMMENT}}

<div class="sec"><h2>{{H_C2}}</h2></div>
<div class="chart-title"><span class="num">Chart 2</span> &middot; {{C2_TITLE}}</div>
<div class="chart-sub">{{C2_SUB}}</div>
<img class="chart c2" src="file://{{C2_IMG}}">
{{C2_COMMENT}}

<!-- PAGE 2 -->
<div class="pagebreak"></div>
<div class="gradbar"></div>

<div class="sec first"><h2>{{H_C3}}</h2></div>
<div class="chart-title"><span class="num">Chart 3</span> &middot; {{C3_TITLE}}</div>
<div class="chart-sub">{{C3_SUB}}</div>
<img class="chart c3" src="file://{{C3_IMG}}">
<div style="height: 2mm;"></div>

{{C3_COMMENT_1}}

<div class="sec"><h2>{{H_C3B}}</h2></div>
{{C3_COMMENT_2}}

{{LEADIN_SECTION}}

<div style="height: 4mm;"></div>
<div class="bottomline">
  <div class="bl-head">Base Case &amp; Implications</div>
  <p>{{BASE_CASE}}</p>
</div>

<!-- PAGE 3: source + disclaimer only, pinned to the bottom -->
<div class="pagebreak"></div>
<div class="gradbar"></div>
<div class="legal">
  <div class="src-line"><span class="syz">SYZ</span> {{SOURCE_LINE}}</div>
  <div class="disc-head">Disclaimer</div>
  <p>This communication has been issued and made available to recipients for the purpose of advertising investment services and/or financial instruments. It has been sent for information purposes and cannot be considered as an offer or a personalised recommendation to buy or sell a financial instrument or any other investment or currency. This communication does not constitute investment research within the meaning of regulatory rules applicable in the European Economic Area, or research under the rules of the U.S. Self-Regulatory Organizations.</p>
  <p>This information is made solely for professional and institutional clients as defined by the Swiss Financial Services Act, as well as qualified investors according to the Swiss Collective Investment Schemes Act. It is not intended for retail clients or non-qualified investors and consequently cannot be transmitted to any third party.</p>
  <p>This communication is not directed to any person in any jurisdiction where, by reason of that person&rsquo;s nationality, residence or otherwise, its dissemination or use is prohibited. It cannot be quoted, reproduced, disclosed, distributed or otherwise referred to, in whole or in part, to any third party without the Bank&rsquo;s prior written consent.</p>
  <p>This communication may contain information on past performances of a financial product, all kinds of economic and financial valuations and analyses, as well as opinions of the Bank or of third parties. Any market valuations, terms and calculation methods, yields and opinions expressed are subject to change without notice. The information and opinions contained herein have been compiled and provided in good faith, based on information obtained from sources believed to be trustworthy. However, such information has not been independently verified. No guarantee, representation, or warranty of any kind, whether express or implied, is provided by the Bank or by relevant data vendors and other sources with respect to the accuracy, reliability, currentness or exhaustiveness of the information communicated, the methodology employed or the prices contained herein.</p>
  <p>Past performance is not a reliable indicator of current or future results. Any reference to the past performance of an investment does not guarantee its future performance. Fluctuations in exchange rates may adversely affect the value, price or income of any investment.</p>
  <p>Nothing in the present communication constitutes investment, legal, accounting or tax advice. This information is purely objective since it does not take into consideration the personal situation (including financial knowledge and experience), the investment objectives and risk profile of any recipient. Moreover, certain financial instruments mentioned (in particular, but not exclusively, derivatives, options and futures) involve a high risk of loss and may not be suitable. Accordingly, recipients should consult their own advisors on such matters, including but not limited to the possible tax consequences of investing in any financial product mentioned herein, and make their own assessment of the suitability of such investment product.</p>
  <p>Should a recipient make an investment on the basis of the present communication, the recipient alone shall bear the consequences thereof. In no event shall the Bank, its directors, employees, affiliates or agents be held responsible for damages of any kind arising out of the use of all or part of the information provided herein.</p>
</div>

</body>
</html>
```
**Default values:** `DOC_TYPE` = "Research Comment"; `THEME` = "Global Macro" (or the asset class); `DATE` = publication date, e.g. "2 October 2026" (it appears in both the dateline and the footer); `W1/W2/W3` = 65 / 64 / 76; `SOURCE_LINE` = "Source: Syz Research, Bloomberg". Paragraph placeholders take complete `<p>…</p>` blocks. `LEADIN_SECTION` is either `<div class="sec"><h2>…</h2></div><p>…</p>` or an empty string. The image paths are absolute (`/home/claude/c1_crop.png`). The disclaimer text is fixed: never edit, shorten or paraphrase it.

**Fill and render:**
```python
html = open("template.html").read()
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html, "unfilled placeholder"
open("doc.html", "w").write(html)
from weasyprint import HTML; HTML("doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))   # must be 3 — then Read page1.png, page2.png and page3.png
```

## Text format
**Page plan (fixed):**
- **Page 1:** kicker → title → dateline → 2 intro paragraphs (no heading) → section heading → Chart 1 + 1 comment paragraph → section heading → Chart 2 + 1 comment paragraph.
- **Page 2:** section heading → Chart 3 → comment paragraph 1 → section heading → comment paragraph 2 → optional lead-in section (heading + paragraph) → navy **Base Case & Implications** box. No source line on page 2.
- **Page 3:** gradient rule only, then the source line and the fixed disclaimer, pinned to the bottom of the page. Nothing else on page 3.

**Element rules:**
- **Title:** `<Topic>: <conviction message in Title Case>`, ≤ ~50 characters, e.g. "Global PMI: The Expansion Shifts into Higher Gear". It states the verdict, not the topic.
- **Section headings (h2):** five per document (H_C1, H_C2, H_C3, H_C3B, plus the lead-in heading if used). Each is a takeaway, not a label, in sentence case, ≤ ~45 characters so it fits on one line, with no full stop. Examples: "Both engines now at 53 or above", "Breadth: synchronised expansion returns", "Asia rejoins the cycle", "Brazil: idiosyncratic, not contagious", "Rates: the hike is in; the next one is the question". The heading sits above the chart title; the chart title stays descriptive. Don't repeat the H1's verdict in a heading. Style is plain 11pt ExtraBold Space Blue: no rule, bar or colour accent above or beside it.
- **Intro paragraph 1** (~90–110 words): open with the release ("The September PMI data…"), give the verdict and back it with 2–4 numbers. Link to the previous edition where relevant ("the inflection we flagged last month", "the main test we set out in July").
- **Intro paragraph 2** (~60–80 words): the second dimension or counterpoint, opened by a short framing sentence ("The cycle has also absorbed its first policy test.").
- **Chart titles in the PDF:** `<span class="num">Chart N</span> &middot; <Subject> &ndash; <Descriptor>` (en dash in the PDF, em dash in the PNG). **Chart sub-line:** one line of methodology (window, units, thresholds, truncations, stale data), joined by `&middot;`. With the page 2 source line gone, the sub-line is where stale or partial data must be disclosed.
- **Charts 1 and 2:** one paragraph each, ~60–90 words, in the order fact → interpretation → implication.
- **Chart 3:** two paragraphs, ~110–150 words each. The first covers the leaders; the second, under its own heading (H_C3B), covers the laggards plus the allocation implication.
- **Optional lead-in section** (~80–110 words): it covers the transmission channel to markets (e.g. rates). The heading replaces the old bold lead-in phrase, so the paragraph starts directly with the argument.
- **Base Case box:** 2–3 sentences, ~50–70 words. State the regime ("We remain in an early-to-mid-cycle reflation environment…"), name the favoured sectors or exposures, and give one qualifier. No list of invalidation triggers in the box.
- **Source line (page 3):** `Source: Syz Research, Bloomberg` by default. Add a provider only if the charts genuinely use one beyond Bloomberg (e.g. `Source: Syz Research, Bloomberg, FactSet`). No method notes or as-of notes here.

**Voice:**
- Institutional, quantified and decisive. Write in the first person plural ("We read this as…", "We expect…").
- Every claim carries a number taken from the data: one decimal for indices, "points" for changes in an index, % for shares, and "highest since <Month YYYY>" computed from the series.
- Separate signal from noise explicitly: a volatile series or a one-month move gets a caveat, and a weather or one-off effect gets named.
- No bullet lists, exclamation marks or marketing adjectives inside the document; the only headings are the H1 and the five section headings. British spelling (stabilised, synchronised, programme).
- Typography uses HTML entities: `&mdash;` with no spaces around it for asides, `&ndash;` for ranges (2022&ndash;25), `&rsquo;` for apostrophes, `&ldquo;…&rdquo;` for quotes, `&amp;`.
- Never invent numbers or consensus figures. Web-sourced facts (central bank decisions, market pricing) are stated with their date in the text (e.g. "on 16 September") and flagged to the user for a Bloomberg check.

## Fit & QA (mandatory)
1. The PDF must be **exactly 3 pages**. Page 1 must end with the complete Chart 2 comment; page 2 starts with the Chart 3 section heading and ends with the Base Case box; page 3 holds only the source line and the disclaimer at the bottom.
2. **If pages 1–2 overflow,** apply these levers in order:
   - reduce `W1`/`W2` by 1–2 points (minimum 60%) and `W3` (minimum 72%);
   - tighten the prose.
   Never change font sizes, margins, colours, headings or the page plan. Never let a heading sit alone at the bottom of a page (the `.sec` rule prevents it; check anyway).
3. **Rasterise all three pages at 100 dpi and look at them.** Check for:
   - logo top-right and gradient rule on every page;
   - five section headings, each on one line, with no rule above them;
   - footer reads "Syz Research · Research Comment · <date>" with a space after each dot;
   - no clipped chart titles inside the panels (the `panels` crop keeps the panel titles);
   - scatter labels not colliding;
   - the Base Case box intact on page 2, with no source line under it;
   - page 3: source line followed by the full disclaimer, pinned above the footer.
4. Run `pdffonts` on the output: only Nunito faces may be embedded.
5. In the reply, report:
   - the data window and any stale or excluded series;
   - the 3–5 numbers the document turns on;
   - any figure from outside the dataset that needs verifying.

## Reference instance — monthly Global PMI
- **Chart 1:** Global Manufacturing (Blueberry) vs. Services (Orange), threshold 50, y floor 45, with the Covid trough noted.
- **Chart 2:** breadth panels (Manufacturing in Orange, Services in Blueberry), % of countries above 50.
- **Chart 3:** momentum map of the latest level vs. the **6-month** change. Exclude Global, the EU aggregate (it duplicates the Eurozone), dead series (Denmark) and any country without a print in the latest month.
- **Headings (Oct 2026 edition):** "Both engines now at 53 or above" · "Breadth: synchronised expansion returns" · "Asia rejoins the cycle" · "Brazil: idiosyncratic, not contagious" · "Rates: the hike is in; the next one is the question".