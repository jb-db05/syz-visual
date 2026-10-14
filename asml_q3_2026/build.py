"""ASML Q3 2026 — Syz Visual Research Comment build (data -> charts -> PDF).

All figures are taken from the supplied research summary (14 October 2026):
ASML Q3 2026 release, UBS and BNP Paribas notes. Nothing is extrapolated;
the only derived figure is the compounded capacity index in Chart 3.

Update the DATA block for the next quarter and re-run:  python3 build.py
Requires /home/claude/syz_charts.py, /home/claude/template.html, the Nunito
faces in /home/claude/fonts and /home/claude/syz_logo_hq.png (see SKILL.md).
"""
import os
import sys

sys.path.insert(0, "/home/claude")
import numpy as np
import matplotlib.pyplot as plt
import syz_charts as sc

OUT = os.path.dirname(os.path.abspath(__file__))
WORK = "/home/claude/asml_build"
os.makedirs(WORK, exist_ok=True)
DATE, MONYYYY = "14 October 2026", "Oct2026"
ASOF = "October 2026"

# ------------------------------------------------------------------ DATA (from the research summary)
# Variance vs consensus, %; kind "q3" = reported Q3, "guide" = guidance midpoint
VARIANCE = [
    ("EPS (€12.95)*",                  21.0, "q3"),
    ("Installed Base Mgmt (€3.3bn)",    13.0, "q3"),
    ("Operating profit",                5.0, "q3"),
    ("Q4 revenue guide midpoint",       3.0, "guide"),
    ("FY26 revenue guide midpoint",     1.6, "guide"),
    ("EUV system sales (€4.1bn)",      -7.0, "q3"),
]
GM_BEAT_BP = 150
# Year-on-year growth, %
YOY = [("Revenue", 55, "€11.7bn"), ("Installed Base Mgmt", 68, "€3.3bn"),
       ("EUV system sales", 94, "€4.1bn"), ("EPS", 136, "€12.95")]
# Capacity framework: +30% in 2027, further +30% under investigation for 2028 (compounded index)
CAP = [("2026", 100.0, "base"), ("2027", 130.0, "plan"), ("2028", 169.0, "study")]
# Gross margin, %
GM = [("Q3 26\nreported", 57.5, "act"), ("Q4 26\nguidance", 57.0, "guide"),
      ("FY26\nguidance", 56.0, "guide"), ("2028\nconsensus", 56.5, "cons"),
      ("2028\nBNP Paribas", 60.0, "broker")]

sc.setup_fonts()
SRC = sc.source_line("ASML, UBS, BNP Paribas", ASOF)


def save(fig, path):
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ Chart 1: variance vs consensus
def chart1(path):
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.25, right=0.96)
    sc.style_ax(ax, grid_axis="x")
    labels = [v[0] for v in VARIANCE][::-1]
    vals = np.array([v[1] for v in VARIANCE])[::-1]
    kinds = [v[2] for v in VARIANCE][::-1]
    y = np.arange(len(vals))
    for yi, v, k, lab in zip(y, vals, kinds, labels):
        col = sc.BLUEB if v < 0 else (sc.GOLD if k == "guide" else sc.ORANGE)
        alpha = 0.55 if lab.startswith("EPS") else 0.95
        ax.barh(yi, v, height=0.58, color=col, alpha=alpha, linewidth=0, zorder=3)
        ax.annotate(f"{v:+.1f}%" if abs(v) < 2 else f"{v:+.0f}%", (v, yi),
                    xytext=(8 if v >= 0 else -8, 0), textcoords="offset points",
                    ha="left" if v >= 0 else "right", va="center",
                    color=col if col != sc.GOLD else sc.BRONZE, fontsize=10.5, fontweight="bold")
    ax.axvline(0, color=sc.NAVY, linestyle=sc.DASH, linewidth=1.1, alpha=0.85, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10.5, color=sc.NAVY, fontweight="bold")
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-12, 26)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
    ax.text(0.985, 0.04, f"Gross margin 57.5%: +{GM_BEAT_BP}bp vs. consensus",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10, color=sc.NAVY, fontweight="bold",
            bbox=dict(facecolor="white", edgecolor=sc.SPINE, boxstyle="round,pad=0.4"))
    from matplotlib.patches import Patch
    leg = ax.legend(handles=[Patch(color=sc.ORANGE, label="Q3 reported, beat"),
                             Patch(color=sc.GOLD, label="Guidance midpoint"),
                             Patch(color=sc.BLUEB, label="Q3 reported, miss")],
                    loc="center right", frameon=False, fontsize=10)
    for t in leg.get_texts():
        t.set_color(sc.NAVY); t.set_fontweight("bold")
    sc.header(fig, "ASML Q3 2026 — Results vs. Consensus",
              "Variance vs. consensus, % · Q3 reported and guidance midpoints · revenue of €11.7bn broadly in line",
              SRC + " · *EPS includes a one-off equity stake revaluation (shaded lighter)")
    save(fig, path)


# ------------------------------------------------------------------ Chart 2: YoY growth
def chart2(path):
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.07, right=0.96)
    sc.style_ax(ax)
    x = np.arange(len(YOY))
    for xi, (lab, v, lvl) in zip(x, YOY):
        col = sc.BLUEB if lab == "Revenue" else sc.ORANGE
        alpha = 0.55 if lab == "EPS" else 0.95
        ax.bar(xi, v, width=0.56, color=col, alpha=alpha, linewidth=0, zorder=3)
        ax.annotate(f"+{v}%", (xi, v), xytext=(0, 6), textcoords="offset points", ha="center",
                    color=col, fontsize=12, fontweight="bold")
        ax.text(xi, 5, lvl, ha="center", va="bottom", color="white", fontsize=10.5, fontweight="bold", zorder=4)
    ax.axhline(YOY[0][1], color=sc.NAVY, linestyle=sc.DASH, linewidth=1.1, alpha=0.85, zorder=2)
    ax.text(len(YOY) - 0.5, YOY[0][1] + 2, "Group revenue growth", ha="right", va="bottom",
            fontsize=9, color=sc.NAVY, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels([v[0] for v in YOY], fontsize=11, color=sc.NAVY, fontweight="bold")
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 155); ax.set_xlim(-0.6, len(YOY) - 0.4)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    sc.header(fig, "ASML Q3 2026 — Year-on-Year Growth",
              "Q3 2026 vs. Q3 2025, % · Q3 2026 level shown in each bar · dashed line = group revenue growth",
              SRC + " · EPS growth includes a one-off equity stake revaluation (shaded lighter)")
    save(fig, path)


# ------------------------------------------------------------------ Chart 3: capacity + gross margin
def chart3(path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 6.4), dpi=200, gridspec_kw={"width_ratios": [1, 1.45]})
    fig.subplots_adjust(top=0.79, bottom=0.12, left=0.07, right=0.96, wspace=0.22)
    for ax in (a1, a2):
        sc.style_ax(ax)
    # capacity index
    for i, (lab, v, k) in enumerate(CAP):
        alpha = {"base": 0.95, "plan": 0.95, "study": 0.32}[k]
        col = sc.BLUEB if k == "base" else sc.ORANGE
        a1.bar(i, v, width=0.56, color=col, alpha=alpha, linewidth=0, zorder=3)
        a1.annotate(f"{v:.0f}", (i, v), xytext=(0, 5), textcoords="offset points", ha="center",
                    color=col, fontsize=11.5, fontweight="bold")
    a1.text(1, 8, "+30%\nplanned", ha="center", va="bottom", color="white", fontsize=9.5, fontweight="bold", zorder=4)
    a1.text(2, 8, "+30%\nunder\nstudy", ha="center", va="bottom", color=sc.ORANGE, fontsize=9.5, fontweight="bold", zorder=4)
    a1.set_xticks(range(len(CAP))); a1.set_xticklabels([c[0] for c in CAP], fontsize=10.5, color=sc.NAVY, fontweight="bold")
    a1.set_ylim(0, 195)
    a1.set_title("Low-NA EUV & immersion DUV capacity (2026 = 100)", fontsize=11.5, fontweight="bold",
                 color=sc.NAVY, loc="left", pad=7)
    # gross margin
    cols = {"act": sc.ORANGE, "guide": sc.GOLD, "cons": sc.BLUEB, "broker": sc.ORANGE}
    for i, (lab, v, k) in enumerate(GM):
        a2.bar(i, v, width=0.56, color=cols[k], alpha=0.32 if k == "broker" else 0.95, linewidth=0, zorder=3)
        txt = f">{v:.0f}%" if k == "broker" else (f"~{v:.1f}%" if k != "act" else f"{v:.1f}%")
        a2.annotate(txt, (i, v), xytext=(0, 5), textcoords="offset points", ha="center",
                    color=cols[k] if k != "guide" else sc.BRONZE, fontsize=11.5, fontweight="bold")
    a2.axhline(56.5, color=sc.NAVY, linestyle=sc.DASH, linewidth=1.1, alpha=0.85, zorder=4)
    a2.set_xticks(range(len(GM))); a2.set_xticklabels([g[0] for g in GM], fontsize=9.5, color=sc.NAVY, fontweight="bold")
    a2.set_ylim(50, 62)
    a2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    a2.set_title("Gross margin (%) · dashed = 2028 consensus", fontsize=11.5, fontweight="bold",
                 color=sc.NAVY, loc="left", pad=7)
    for ax in (a1, a2):
        ax.tick_params(axis="x", length=0)
    sc.header(fig, "ASML — Capacity and Pricing Drive the Earnings Path",
              "Capacity index compounded from ASML’s framework · gross margin y-axis starts at 50% · light bars = not committed",
              SRC + " · 2028 capacity step under investigation · >60% 2028 margin is a BNP Paribas estimate, not guidance",
              title_y=0.945, sub_y=0.906, bar_y=0.886)
    save(fig, path)


sc.CROPS["bars"] = (0.122, 0.052)
sc.CROPS["duo"] = (0.115, 0.052)
charts = [("c1", chart1, "bars"), ("c2", chart2, "bars"), ("c3", chart3, "duo")]
for name, fn, kind in charts:
    png = f"{OUT}/ASML_Q3_2026_Chart{name[1]}.png"
    fn(png)
    sc.crop_for_pdf(png, f"{WORK}/{name}_crop.png", kind)

# ------------------------------------------------------------------ TEXT
P = lambda s: f"<p>{s}</p>"
fill = {
    "DOC_TYPE": "Research Comment",
    "THEME": "European Equities",
    "TITLE": "ASML: Margins and Capacity Drive Upgrades",
    "DATE": DATE,
    "W1": "64", "W2": "62", "W3": "76",
    "INTRO_PARAGRAPHS": P(
        "ASML&rsquo;s Q3 2026 results deliver the type of beat we look for: margin and services, not just "
        "volume. Revenue of &euro;11.7bn, up 55% YoY, was broadly in line, but the gross margin of 57.5% came in "
        "150bp above consensus and lifted operating profit about 5% above expectations, at a 44.4% operating "
        "margin. Q4 revenue guidance of &euro;14.2&ndash;15.2bn puts the midpoint about 3% above consensus, and "
        "FY2026 guidance rises to &euro;44&ndash;45bn. More important than the quarter, management signalled that "
        "planned capacity will fall short of demand through 2028. We read this as the start of an upgrade cycle, "
        "not a one-quarter beat."
    ) + P(
        "The headline EPS beat needs a discount. EPS of &euro;12.95, up 136% YoY, was about 21% ahead of "
        "consensus, but part of that reflects a one-off revaluation of an equity stake. We anchor on the operating "
        "line, where the beat is smaller but recurring. The tension for the shares is positioning: BNP Paribas "
        "cautions that investors may already expect stronger earnings and will look for explicit 2027 guidance."
    ),
    "H_C1": "A quality beat, flattered at the EPS line",
    "C1_TITLE": "ASML Q3 2026 &ndash; Results vs. Consensus",
    "C1_SUB": "Variance vs. consensus, % &middot; Q3 reported and guidance midpoints &middot; EPS includes a one-off "
              "gain &middot; revenue broadly in line (not shown)",
    "C1_IMG": f"{WORK}/c1_crop.png",
    "C1_COMMENT": P(
        "Installed Base Management, at &euro;3.3bn, beat consensus by 13%, with services and productivity "
        "upgrades the main operational outperformer. EUV system sales of &euro;4.1bn were the one shortfall, 7% "
        "below consensus despite 94% growth; in a capacity-constrained year we read this as shipment timing rather "
        "than weaker demand. The guidance beats are modest in revenue terms, but a Q4 gross margin of around 57% "
        "implies about 7% EBIT upside, according to UBS."
    ),
    "H_C2": "Services and EUV carry the growth",
    "C2_TITLE": "ASML Q3 2026 &ndash; Year-on-Year Growth",
    "C2_SUB": "Q3 2026 vs. Q3 2025, % &middot; Q3 2026 level in each bar &middot; dashed line = group revenue growth",
    "C2_IMG": f"{WORK}/c2_crop.png",
    "C2_COMMENT": P(
        "EUV system sales rose 94% and Installed Base Management 68%, both well ahead of group revenue growth of "
        "55%, while EPS rose 136% on operating leverage and the one-off gain. The installed base matters most for "
        "the earnings path: upgrades and services scale with a growing EUV fleet, are less cyclical than new tools "
        "and support margins even when shipments are capped by capacity."
    ),
    "H_C3": "Capacity, not demand, is the constraint",
    "C3_TITLE": "ASML &ndash; Capacity and Pricing Drive the Earnings Path",
    "C3_SUB": "Capacity compounded from ASML&rsquo;s framework &middot; light bars = 2028 step under study and "
              "BNP Paribas &gt;60% estimate",
    "C3_IMG": f"{WORK}/c3_crop.png",
    "C3_COMMENT_1": P(
        "Capacity is now the binding variable. ASML&rsquo;s release clarifies that its framework envisaged a 30% "
        "increase in Low-NA EUV and immersion DUV capacity in 2027, with a further 30% under investigation for "
        "2028; compounded, that would take capacity to about 1.7 times the 2026 level. Management now says even "
        "this will not be sufficient and is exploring additional capacity, particularly for 2028. Order intake for "
        "2028 is already significant, and customers have shown strong interest for 2029 and 2030. We treat that "
        "interest as visibility, not backlog: it is not the same as firm orders. But a supplier that is sold out "
        "two years forward has pricing power, and the quantified decision on 2028 capacity is, in our view, the "
        "most important input for 2028 estimates."
    ),
    "H_C3B": "Pricing opens a path to 60% gross margins",
    "C3_COMMENT_2": P(
        "Pricing is the second lever. According to BNP Paribas, concluded price negotiations should contribute "
        "partially in 2027 and fully in 2028, and its analysis points to gross margins above 60% in 2028, against "
        "consensus of about 56.5%. That is a broker assessment, not company guidance, but the direction matches "
        "what ASML delivered this quarter: 57.5% in Q3 and around 57% guided for Q4, against around 56% for the "
        "full year. Both brokers expect upgrades: UBS sees 5&ndash;10% consensus EPS upgrades for 2027&ndash;28 "
        "(Buy, &euro;2,350 target), and BNP Paribas also expects upgrades (Outperform, &euro;2,450 target). The "
        "main risk is China, at 23% of system sales versus 14% in Q2, if export restrictions tighten."
    ),
    "LEADIN_SECTION": '<div class="sec"><h2>Valuation: the growth has to arrive</h2></div>' + P(
        "On UBS&rsquo;s earnings assumptions, the shares trade on about 25x 2027E and 17x 2028E earnings. The "
        "compression between the two years is the investment case, and it holds only if capacity is delivered and "
        "pricing reaches the P&amp;L on schedule; these multiples should not be read against a separate consensus "
        "EPS series. Capacity execution, slower customer capital spending, High-NA adoption delays and elevated "
        "expectations are the variables to monitor. The next catalysts are today&rsquo;s investor call, formal "
        "FY2027 guidance in January and a quantified decision on additional 2028 capacity."
    ),
    "BASE_CASE": (
        "We see ASML entering a multi-year earnings upgrade cycle driven by volume, installed-base growth and "
        "pricing, with demand exceeding planned capacity through 2028. We favour exposure to leading-edge "
        "lithography and the services annuity its installed base creates. The qualifier is China: at 23% of "
        "system sales, it is the main source of downside to estimates should export restrictions tighten."
    ),
    "SOURCE_LINE": "Source: Syz Research, ASML, UBS, BNP Paribas",
}

html = open("/home/claude/template.html").read()
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html, "unfilled placeholder"
open(f"{WORK}/doc.html", "w").write(html)
pdf = f"{OUT}/Research_Comment_ASML_{MONYYYY}.pdf"
from weasyprint import HTML
HTML(f"{WORK}/doc.html").write_pdf(pdf)
from pdf2image import convert_from_path
pages = convert_from_path(pdf, dpi=100)
for i, p in enumerate(pages):
    p.save(f"{WORK}/page{i+1}.png")
print("pages:", len(pages))
