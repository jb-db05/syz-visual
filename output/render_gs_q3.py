import re, os, sys
from weasyprint import HTML
from pdf2image import convert_from_path
OUT = os.path.dirname(os.path.abspath(__file__))
W1, W2, W3 = [int(a) for a in sys.argv[1:4]] if len(sys.argv) > 3 else (65, 64, 76)
def e(t): return t.replace("&", "&amp;").replace("'", "&rsquo;")
def P(*ps): return "\n".join(f"<p>{e(p)}</p>" for p in ps)
def S(h, *ps): return f'<div class="sec"><h2>{e(h)}</h2></div>\n' + P(*ps)
T = open("/home/claude/template.html").read()
fill = dict(
 DOC_TYPE="Research Comment", THEME="Financials", DATE="13 October 2026",
 TITLE="Goldman Sachs: Strong Execution, A Higher Bar", W1=W1, W2=W2, W3=W3,
 INTRO_PARAGRAPHS=P("Goldman Sachs has delivered another exceptional quarter. Q3 earnings per share reached $17.01, 33% above consensus and 39% higher year-on-year, while revenues of $18.7bn beat expectations by 12%. It was the firm's second-highest revenue quarter on record, with annualised return on tangible equity (ROTE) reaching 20.5%. The results confirm the strength of Goldman's franchise in a supportive capital markets environment. Yet at $894 per share ahead of the release, or around 12.5x 2027 earnings and 2.4x book value, much of that strength is already reflected in the valuation. The question for investors is how much of this profitability can be sustained as trading activity normalises."),
 H_C1=e("Q3: Equities continues to carry the franchise"),
 C1_TITLE="Goldman Sachs &ndash; Revenue Growth by Business", C1_SUB="Q3 2026 vs. Q3 2025, % change &middot; Markets in orange &middot; Growth rates as quoted in the Q3 results",
 C1_IMG="/home/claude/c1_crop.png",
 C1_COMMENT=P("Global Banking & Markets generated $13.5bn in revenues, 32% above last year. Equities was again the driving force, with revenues of $6.4bn, up 72% year-on-year and 25% ahead of consensus. The most interesting development was in financing, where revenues reached a record $3.4bn, up 96% year-on-year and another 3% sequentially, even after an exceptionally strong Q2. Prime brokerage and portfolio financing are becoming increasingly important contributors to the franchise. Unlike more volatile trading revenues, these activities can generate recurring income from client balances, although they still depend on market activity and balance-sheet capacity.",
  "The contrast with Fixed Income was striking. FICC revenues fell 24% quarter-on-quarter to $3.5bn, missing consensus by 7%, as weaker credit, mortgage and rates activity offset stronger currencies and commodities. Equities revenues also declined 13% from Q2's record, but remained unusually elevated. This leaves Goldman with two sources of earnings strength: a growing financing franchise that may prove more durable, and trading activity that remains sensitive to market conditions."),
 H_C2=e("Investment banking: strong fees, softer pipeline"),
 C2_TITLE="Goldman Sachs &ndash; Q3 2026 vs. Consensus", C2_SUB="Actual vs. consensus, % surprise &middot; Dashed line = in line &middot; Surprise figures as quoted in the text",
 C2_IMG="/home/claude/c2_crop.png",
 C2_COMMENT=P("Investment banking fees rose 21% year-on-year to $3.2bn, 12% above consensus. Advisory was the highlight, reaching a record $1.65bn, up 18% year-on-year and 20% sequentially, supported by higher completed M&A volumes. Equity underwriting grew 43%, while Debt underwriting increased 15%, reflecting stronger issuance activity, particularly in investment-grade credit.",
  "There is, however, an important qualification. The investment banking fee backlog declined during the quarter, primarily in Advisory, reversing the improvement reported in Q2. Strong completed transactions are supporting today's revenues, but the softer backlog provides less visibility on future quarters. For Goldman, a sustained recovery in M&A and underwriting would be particularly valuable, allowing earnings growth to rely less heavily on exceptionally favourable trading conditions."),
 H_C3=e("A second earnings engine is taking shape"),
 C3_TITLE="Goldman Sachs &ndash; Q3 2026 Revenues by Source", C3_SUB="$bn &middot; Equities and AWM split into recurring-type and activity-sensitive components &middot; Split components derived as segment total minus quoted component",
 C3_IMG="/home/claude/c3_crop.png",
 C3_COMMENT_1=P("Asset & Wealth Management delivered revenues of $5.1bn, up 14% year-on-year, with record management fees of $3.6bn, up 22%. Assets under supervision reached $4.1tn, supported by $97bn of long-term net inflows, marking the 35th consecutive quarter of positive long-term fee-based flows. This is strategically important: the expanding pool of managed assets provides a growing base of recurring revenues alongside the more cyclical investment banking and trading businesses.",
  "Not all of the quarterly strength is recurring. Incentive fees reached $587m, compared with $112m in Q2, boosted by fund distributions, while investment revenues were affected by markdowns in debt investments."),
 H_C3B=e("The trade-off: profitability versus capital consumption"),
 C3_COMMENT_2=P("Goldman continues to demonstrate strong operating leverage. Revenues increased 23% year-on-year against 20% expense growth, despite higher transaction-related costs and a $450m charitable contribution. Quarterly ROTE reached 20.5%, bringing the nine-month figure to 22.4%.",
  "Capital is becoming the more important constraint. The standardised CET1 ratio fell 50 basis points during the quarter to 12.4%, while total assets have expanded approximately 21% year-to-date. Goldman repurchased $3bn of shares, down from $4bn in Q2, and maintained its quarterly dividend at $5 per share. This is the trade-off investors will increasingly need to assess: expanding financing and lending activities can support revenues, but they also consume capital that might otherwise be returned to shareholders. Credit provisions also increased to $368m, primarily reflecting wholesale loan impairments."),
 LEADIN_SECTION=S("Valuation: excellent earnings, fewer surprises left to price",
  "At approximately 12.5x UBS's 2027 earnings estimate and 2.4x 2026 estimated book value, Goldman commands a substantial premium to its historical valuation. The franchise is generating ROTE above 20%, its Equities financing business continues to expand, and Asset & Wealth Management is providing a larger recurring fee base. JPMorgan expects the earnings beat to drive mid-single-digit upgrades to 2026 consensus EPS.",
  "The risk is that investors extrapolate today's trading performance too far into the future. Equities revenues have increased 72% year-on-year for two consecutive quarters, which becomes difficult to sustain. Any normalisation in trading, without a corresponding acceleration in investment banking fees, could limit further earnings upgrades. With the shares already pricing in strong execution, future returns will depend increasingly on sustainable earnings growth rather than multiple expansion.")
  + S("What would change our conviction",
  "Three developments matter most. First, a renewed expansion of the investment banking backlog would strengthen confidence in the durability of the dealmaking recovery. Second, continued growth in Equities financing without further material erosion of CET1 would support the case for sustainable returns above 20%. Third, a growing contribution from recurring Asset & Wealth Management fees would justify a higher-quality earnings multiple. Conversely, simultaneous weakness in trading and the investment banking pipeline, combined with further capital consumption, would challenge the current valuation."),
 BASE_CASE=e("We remain constructive on Goldman Sachs' operating performance but more selective on valuation. The Q3 beat demonstrates the strength of the franchise and should support upward earnings revisions. Existing exposure remains justified by the firm's profitability, market position and growing recurring revenue base. However, with the shares already trading at a premium, we would favour adding on valuation weakness or following evidence of a renewed investment banking pipeline recovery. Goldman's execution is strong; the next challenge is sustaining it."),
 SOURCE_LINE="Source: Syz Research, company reports",
)
for k, v in fill.items(): T = T.replace("{{" + k + "}}", str(v))
assert "{{" not in T
for k, v in [("C1_IMG",""),]: pass
open("/home/claude/doc.html", "w").write(T)
pdf = f"{OUT}/Research_Comment_Goldman_Sachs_Oct2026.pdf"
HTML("/home/claude/doc.html").write_pdf(pdf)
pages = convert_from_path(pdf, dpi=100)
for i, p in enumerate(pages): p.save(f"/home/claude/page{i+1}.png")
print("pages:", len(pages))
