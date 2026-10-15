"""build_rheinmetall.py — Syz Visual Research Comment: Rheinmetall (RHM GY), October 2026.

Data -> 3 charts (standalone PNG + PDF crop) -> HTML template -> 3-page A4 PDF.
All figures are the analyst inputs below; update DATA and the text blocks for the next edition.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import syz_charts as sc  # noqa: E402

OUT_PDF = os.path.join(HERE, "Research_Comment_Rheinmetall_Oct2026.pdf")
DATE = "15 October 2026"
ASOF = "October 2026"

# ---------------------------------------------------------------- data (EUR bn unless stated)
DATA = {
    "sales_guide_fy26": (13.7, 14.2),
    "sales_target_2030": 50.0,
    "backlog_jun26": 80.4,
    "backlog_firm_share": 0.70,
    "backlog_target_ye26": (100.0, 120.0),
    "years": ["2025", "2026e", "2027e", "2028e"],
    "pe": [70.0, 28.0, 18.9, 13.6],
    "fcf_yield": [2.0, 6.9, 4.2, 6.8],
    "nfp_jun26": -2.7,
    "arminius_dp": 3.0,          # ">EUR 3bn" down payment, taken at the floor
    "nfp_ye26_implied": 1.8,     # consensus-implied (EV below market cap)
}

sc.setup_fonts()


# ---------------------------------------------------------------- chart 1: backlog vs. sales (custom bars)
def chart_backlog(path):
    d = DATA
    lo, hi = d["sales_guide_fy26"]; blo, bhi = d["backlog_target_ye26"]
    labels = ["FY26 sales\nguidance", "2030 sales\ntarget", "Backlog\nend-June 2026", "Backlog target\nyear-end 2026"]
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.07, right=0.96)
    sc.style_ax(ax)
    mid_s, mid_b = (lo + hi) / 2, (blo + bhi) / 2
    firm = d["backlog_jun26"] * d["backlog_firm_share"]
    ax.bar(x[0], mid_s, width=0.55, color=sc.BLUEB, zorder=3)
    ax.errorbar(x[0], mid_s, yerr=[[mid_s - lo], [hi - mid_s]], color=sc.NAVY, capsize=6, lw=1.3, zorder=4)
    ax.bar(x[1], d["sales_target_2030"], width=0.55, color=sc.BLUEB, alpha=0.32, zorder=3)
    ax.bar(x[2], firm, width=0.55, color=sc.ORANGE, zorder=3, label="Firm orders (70%)")
    ax.bar(x[2], d["backlog_jun26"] - firm, bottom=firm, width=0.55, color=sc.ORANGE, alpha=0.32, zorder=3,
           label="Frame contracts / other (30%)")
    ax.bar(x[3], mid_b, width=0.55, color=sc.ORANGE, alpha=0.32, zorder=3)
    ax.errorbar(x[3], mid_b, yerr=[[mid_b - blo], [bhi - mid_b]], color=sc.NAVY, capsize=6, lw=1.3, zorder=4)
    kw = dict(ha="center", fontsize=10.5, fontweight="bold")
    ax.text(x[0], hi + 3, f"{lo:.1f}–{hi:.1f}", color=sc.BLUEB, **kw)
    ax.text(x[1], d["sales_target_2030"] + 3, f"~{d['sales_target_2030']:.0f}", color=sc.BLUEB, **kw)
    ax.text(x[2], d["backlog_jun26"] + 3, f"{d['backlog_jun26']:.1f}", color=sc.ORANGE, **kw)
    ax.text(x[3], bhi + 3, f"{blo:.0f}–{bhi:.0f}", color=sc.ORANGE, **kw)
    ax.annotate(f"{d['backlog_jun26'] / mid_s:.1f}x FY26\nsales guidance", (x[2] + 0.30, d["backlog_jun26"] * 0.55),
                fontsize=9, color=sc.NAVY, fontweight="bold", ha="left")
    ax.set_xticks(x, labels)
    ax.tick_params(axis="x", length=0, labelsize=10, labelcolor=sc.NAVY)
    ax.set_ylim(0, 135); ax.set_xlim(-0.6, 3.6)
    ax.set_ylabel("EUR bn", fontsize=10, color=sc.AXIS_TXT)
    sc.legend(ax, "upper left")
    sc.header(fig, "Rheinmetall — Backlog vs. Sales",
              "EUR bn · FY26 guidance and year-end backlog target shown as ranges · light bars = targets / non-firm",
              sc.source_line("Rheinmetall, Bloomberg", ASOF, "Backlog as of 30 June 2026"))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- chart 2: valuation panels (categorical panel bars)
def chart_valuation(path):
    d = DATA
    x = np.arange(len(d["years"]))
    panels = [
        {"y": d["pe"], "color": sc.ORANGE, "label": "P/E (x)", "fmt": "{:.1f}x", "ylim": (0, 82)},
        {"y": d["fcf_yield"], "color": sc.BLUEB, "label": "FCF yield (%)", "fmt": "{:.1f}%", "ylim": (0, 8.2)},
    ]
    fig, axes = plt.subplots(2, 1, figsize=(12.5, 3.9 * 2), dpi=200, sharex=True)
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(top=0.855, bottom=0.09, left=0.07, right=0.96, hspace=0.30)
    for ax, p in zip(axes, panels):
        sc.style_ax(ax)
        y = np.asarray(p["y"], float)
        alphas = [0.32] + [0.95] * (len(y) - 1)       # 2025 actual muted, consensus years solid
        for xi, yi, a in zip(x, y, alphas):
            ax.bar(xi, yi, width=0.5, color=p["color"], alpha=a, linewidth=0, zorder=3)
            ax.annotate(p["fmt"].format(yi), (xi, yi), xytext=(0, 4), textcoords="offset points",
                        ha="center", color=p["color"], fontsize=11, fontweight="bold")
        ax.set_ylim(*p["ylim"])
        ax.set_title(p["label"], fontsize=11.5, fontweight="bold", color=sc.NAVY, loc="left", pad=7)
    axes[-1].set_xticks(x, d["years"])
    axes[-1].tick_params(axis="x", length=0, labelsize=10.5, labelcolor=sc.NAVY)
    sc.header(fig, "Rheinmetall — Valuation on Consensus",
              "Consensus, current scope · 2025 actual (muted) and 2026e–2028e",
              sc.source_line("Bloomberg consensus", ASOF),
              sub_y=0.908, bar_y=0.888, foot_y=0.028)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- chart 3: net financial position bridge (waterfall)
def chart_bridge(path):
    d = DATA
    start, dp, end = d["nfp_jun26"], d["arminius_dp"], d["nfp_ye26_implied"]
    other = end - start - dp
    labels = ["Net financial\nposition, end-June", "Arminius\ndown payment", "Other H2 cash flow\n(implied residual)",
              "Consensus-implied\nyear-end 2026"]
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    fig.subplots_adjust(top=0.84, bottom=0.17, left=0.07, right=0.96)
    sc.style_ax(ax)
    ax.axhline(0, color=sc.NAVY, linestyle=sc.DASH, linewidth=1.2, alpha=0.85, zorder=2)
    w = 0.55
    ax.bar(x[0], start, width=w, color=sc.BLUEB, zorder=3)
    ax.bar(x[1], dp, bottom=start, width=w, color=sc.ORANGE, zorder=3)
    ax.bar(x[2], other, bottom=start + dp, width=w, color=sc.ORANGE, alpha=0.32, zorder=3)
    ax.bar(x[3], end, width=w, color=sc.BLUEB, zorder=3)
    for xa, ya in [(0, start), (1, start + dp), (2, end)]:   # connectors
        ax.plot([x[xa] + w / 2, x[xa + 1] - w / 2], [ya, ya], color=sc.GREY, lw=0.9, ls=":", zorder=2)
    kw = dict(ha="center", fontsize=10.5, fontweight="bold")
    ax.text(x[0], start - 0.35, f"{start:+.1f}", va="top", color=sc.BLUEB, **kw)
    ax.text(x[1], start + dp + 0.15, f"+{dp:.1f} (>3bn)", va="bottom", color=sc.ORANGE, **kw)
    ax.text(x[2], end + 0.15, f"{other:+.1f}", va="bottom", color=sc.BRONZE, **kw)
    ax.text(x[3], end + 0.15, f"{end:+.1f}", va="bottom", color=sc.BLUEB, **kw)
    ax.set_xticks(x, labels)
    ax.tick_params(axis="x", length=0, labelsize=10, labelcolor=sc.NAVY)
    ax.set_ylim(-4.2, 3.2); ax.set_xlim(-0.6, 3.6)
    ax.set_ylabel("EUR bn", fontsize=10, color=sc.AXIS_TXT)
    sc.header(fig, "Rheinmetall — FY26 Net Financial Position Bridge",
              "EUR bn · positive = net cash · year-end implied by consensus EV below market cap · residual derived",
              sc.source_line("Rheinmetall, Bloomberg consensus", ASOF,
                             "Down payment taken at EUR 3.0bn floor; residual = implied, not guided"))
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


sc.CROPS.update({"panels2": (0.118, 0.048)})   # 2-panel figure: header rule sits lower than the kit preset
CHARTS = [("c1", chart_backlog, "line"), ("c2", chart_valuation, "panels2"), ("c3", chart_bridge, "line")]
for name, fn, kind in CHARTS:
    full = os.path.join(HERE, f"Rheinmetall_Chart{name[1]}.png")
    fn(full)
    sc.crop_for_pdf(full, os.path.join(HERE, f"{name}_crop.png"), kind)

# ---------------------------------------------------------------- text
P = lambda s: f"<p>{s}</p>"
fill = {
    "DOC_TYPE": "Research Comment",
    "THEME": "European Defence",
    "TITLE": "Rheinmetall: From Demand Story to Delivery Test",
    "DATE": DATE,
    "INTRO_PARAGRAPHS": P(
        "Rheinmetall (RHM GY, not on our focus list) remains a structural winner of European rearmament, but the "
        "debate has moved from demand to delivery. Market capitalisation is down ~38% since end-2025 (&euro;44.7bn vs "
        "&euro;71.6bn) and the P/E has compressed from 70x to 28x 2026e. The stock no longer prices &ldquo;unlimited "
        "demand&rdquo;; it prices strong execution. Owning it therefore requires two convictions: that management "
        "converts a record &euro;80.4bn backlog into cash on schedule, and that the war in Ukraine does not end in the "
        "near term. If either weakens, we expect the risk/reward to deteriorate quickly."
    ) + P(
        "The second conviction is the less comfortable one. European defence budgets are structural and would survive "
        "a ceasefire, but the stock trades on urgency: mere peace headlines have repeatedly triggered &ndash;5% "
        "sessions. As Europe&rsquo;s largest land-systems and ammunition supplier&mdash;vehicles, weapons &amp; "
        "ammunition, digital, air defence and, since 2026, naval&mdash;vertically integrated in 155mm ammunition and "
        "propellants, with ~60% of the backlog in Germany, Rheinmetall is the purest expression of that urgency."
    ),
    "H_C1": "A &euro;80bn backlog that now has to convert",
    "C1_TITLE": "Backlog &ndash; Conversion Task vs. Sales",
    "C1_SUB": "EUR bn &middot; FY26 guidance and year-end backlog target as ranges &middot; backlog as of 30 June 2026",
    "C1_IMG": os.path.join(HERE, "c1_crop.png"),
    "C1_COMMENT": P(
        "The backlog stands at 5.8x FY26 sales guidance of &euro;13.7&ndash;14.2bn, with the firm share up to 70% from "
        "58% a year earlier. Its value lies in conversion, not intake. The 2030 target of ~&euro;50bn sales at a margin "
        "above 20% implies ~30% annual growth with a backloaded 2028&ndash;29 profile. Q2 shows the leverage is real "
        "(sales +69% to &euro;3.29bn, operating result +115% to &euro;562m), but mass production leaves no room for "
        "single-component bottlenecks that stall platforms and trap cash."
    ),
    "H_C2": "De-rated, but the multiples assume delivery",
    "C2_TITLE": "Valuation &ndash; P/E and FCF Yield on Consensus",
    "C2_SUB": "Consensus, current scope &middot; 2025 actual and 2026e&ndash;2028e",
    "C2_IMG": os.path.join(HERE, "c2_crop.png"),
    "C2_COMMENT": P(
        "On the surface the multiples look undemanding: P/E falls to 13.6x by 2028e, EV/EBITDA to 6.7x and the PEG is "
        "0.5x. But this rests on consensus EPS growth of ~45&ndash;50% in 2027 and ~40% in 2028, which is precisely the "
        "execution bet. Free cash flow is the weak link: the 6.9% FCF yield for 2026e implies ~&euro;3bn of FCF, broadly "
        "the size of a single expected Arminius down payment."
    ),
    "H_C3": "Arminius decides the FY26 cash print",
    "C3_TITLE": "Net Financial Position &ndash; FY26 Bridge to Consensus",
    "C3_SUB": "EUR bn &middot; year-end implied by consensus EV below market cap &middot; down payment at &euro;3.0bn floor; residual derived",
    "C3_IMG": os.path.join(HERE, "c3_crop.png"),
    "C3_COMMENT_1": P(
        "H1 operating free cash flow was &ndash;&euro;1.6bn, driven by inventory build and delayed down payments, "
        "leaving an equity ratio of 28% and a net financial position of &ndash;&euro;2.7bn at end-June. Consensus EV "
        "below market cap implies ~&euro;1.8bn of net cash by year-end. Closing that gap requires the Arminius down "
        "payment of more than &euro;3bn plus a further ~&euro;1.5bn of H2 inflow as inventory unwinds. Arminius is "
        "Germany&rsquo;s large Boxer wheeled armoured vehicle programme: an initial package of ~&euro;25bn, split 50/50 "
        "with KNDS Deutschland via the Artec JV, worth ~&euro;14.4&ndash;14.5bn to Rheinmetall (&euro;12.4bn vehicles, "
        "~&euro;2bn services); follow-on phases remain unfunded. The Bundestag vote is expected on 9 December, with "
        "signing 5&ndash;10 days later. A slip into January would leave FY26 FCF sharply below consensus with no change "
        "to the underlying business, and would dent backlog optics against management&rsquo;s &euro;100&ndash;120bn "
        "year-end target."
    ),
    "H_C3B": "Peace is the risk the multiples cannot absorb",
    "C3_COMMENT_2": P(
        "The re-rating of European defence has been driven by both budget commitments and urgency. Budgets would likely "
        "survive a ceasefire, as NATO spending targets are structural; urgency and multiples would not, and a credible "
        "peace process would likely trigger a sharp sector de-rating regardless of fundamentals. Weapon &amp; "
        "Ammunition, the highest-margin segment at 25.8% in Q2, is the most exposed to a normalisation of "
        "consumption-driven demand. Beyond geopolitics, procurement timing is a live risk&mdash;the F126 frigate "
        "cancellation already forced a cut to FY26 sales guidance&mdash;as is concentration on Germany, a monopsony "
        "buyer whose pricing power should grow. Low-cost drones and software-native strike systems could partly "
        "displace heavy land platforms over time, and JV structures (Artec, Leonardo) dilute consolidated revenue and "
        "net income. Against this, in-house nitrocellulose and propellants and a sovereign production footprint in "
        "frontline NATO states remain genuine moats."
    ),
    "LEADIN_SECTION": '<div class="sec"><h2>Catalysts: cash first, backlog second</h2></div>' + P(
        "Q3 results on 5 November are the first test of the operating cash flow trajectory and the inventory unwind. "
        "The Arminius vote on 9 December, and above all the timing of the down payment, is decisive for FY26 FCF "
        "versus consensus. We also watch the year-end backlog against the &euro;100bn mark and the capex update for "
        "2027&ndash;28, after 2026 guidance was cut from ~16% to 8&ndash;9% of sales. Concrete progress towards a "
        "ceasefire in Ukraine is the primary downside risk for the sector; a sharp geopolitical deterioration would "
        "likely support multiples."
    ),
    "BASE_CASE": (
        "Rheinmetall offers unmatched exposure to European rearmament, and the de-rating has brought outer-year "
        "multiples below some peers such as Leonardo. At current levels, however, the case rests on delivery rather "
        "than demand: backlog conversion, Arminius cash timing and a backdrop that sustains urgency. Without conviction "
        "on both execution and a prolonged conflict, we see the risk/reward as less compelling."
    ),
    "W1": "65", "W2": "64", "W3": "76",
    "SOURCE_LINE": "Source: Syz Research, Bloomberg",
}

html = open(os.path.join(HERE, "template.html")).read()
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html, "unfilled placeholder"
doc = os.path.join(HERE, "doc.html")
open(doc, "w").write(html)
from weasyprint import HTML  # noqa: E402
HTML(doc).write_pdf(OUT_PDF)
from pdf2image import convert_from_path  # noqa: E402
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(os.path.join(HERE, f"page{i + 1}.png"))
print("pages:", len(pages))
