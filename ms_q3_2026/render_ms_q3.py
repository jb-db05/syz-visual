"""Morgan Stanley Q3 2026 Research Comment -> 3-page PDF. Text condensed from the 14 Oct 2026 draft to fit the format."""
import os, sys
from weasyprint import HTML
from pdf2image import convert_from_path
OUT = os.path.dirname(os.path.abspath(__file__))
W1, W2, W3 = [int(a) for a in sys.argv[1:4]] if len(sys.argv) > 3 else (62, 62, 74)
def e(t): return t.replace("&", "&amp;").replace("'", "&rsquo;")
def P(*ps): return "\n".join(f"<p>{e(p)}</p>" for p in ps)
def S(h, *ps): return f'<div class="sec"><h2>{e(h)}</h2></div>\n' + P(*ps)
T = open("/home/claude/template.html").read()
fill = dict(
 DOC_TYPE="Research Comment", THEME="Financials", DATE="14 October 2026",
 TITLE="Morgan Stanley: The $232 Billion Question", W1=W1, W2=W2, W3=W3,
 INTRO_PARAGRAPHS=P("Morgan Stanley delivered another strong quarter, but the biggest surprise came from Wealth Management rather than trading. Q3 earnings per share reached $3.03, 4% above consensus and 8% higher year-on-year, while revenues of $20.3bn exceeded expectations by 2% and return on tangible common equity (ROTCE) reached 22.6%. The standout figure was $232bn in net new assets, more than twice the $113bn expected by analysts. At $186.64 per share ahead of the release, or approximately 13.1x 2027 earnings and 3.5x tangible book value, Morgan Stanley already commands a premium valuation. The central question is whether exceptional client inflows can translate into sustained fee growth and higher profitability, particularly as wealth management margins come under pressure."),
 H_C1="Q3: Equities delivers, investment banking is more mixed",
 C1_TITLE="Morgan Stanley &ndash; Growth by Business", C1_SUB="Q3 2026 vs. Q3 2025, % change &middot; revenues and client assets &middot; Institutional Securities in orange",
 C1_IMG="/home/claude/m1_crop.png",
 C1_COMMENT=P("Institutional Securities generated $10.0bn in revenues, up 18% year-on-year. Equities was again the driving force, with revenues of $5.8bn, up 41% year-on-year and approximately 19% above consensus, with strength across businesses and regions, particularly in Asia. However, Equities declined 8% sequentially, while Fixed Income fell 7% year-on-year to $2.0bn on weaker securitised credit products and commodities.",
  "Investment banking presented a more nuanced picture. Revenues increased just 2% to $2.16bn, despite Advisory rising 30% to $887m on higher completed M&A activity. Equity underwriting declined 19% on lower IPO and block activity, while Debt underwriting fell 3%. After Goldman Sachs delivered a 12% revenue beat the previous day, Morgan Stanley's more modest surprise highlights the increasingly demanding expectations facing US investment banks."),
 H_C2="Wealth Management: record inflows, but how much is repeatable?",
 C2_TITLE="Morgan Stanley &ndash; Wealth Management Flows", C2_SUB="$bn &middot; Q3 2026 net new assets vs. analysts&rsquo; expectation; fee-based flows vs. Q2 2026",
 C2_IMG="/home/claude/m2_crop.png",
 C2_COMMENT=P("Wealth Management delivered record revenues of $9.1bn, up 10% year-on-year, with asset management revenues up 16% to $5.5bn and fee-based client assets up 19% to $3.16tn. Net new assets of $232bn represent an annualised growth rate of 11.4%, well above the long-term 5–7% target range, but just over half were associated with IPO activity, making part of the quarterly performance difficult to extrapolate.",
  "The more durable signal is fee-based flows, which reached a record $80.5bn, more than double Q2's $39bn, supported by the advisor-led channel and a new corporate retirement mandate. These flows contribute directly to recurring management revenues. Years of building the platform, including E*TRADE and Solium, are bringing new assets into the franchise; the next test is converting them into lasting, fee-generating client balances."),
 H_C3="Valuation: strong fundamentals, high expectations",
 C3_TITLE="Morgan Stanley &ndash; Share Price vs. Consensus Earnings", C3_SUB="Weekly, Apr 2005&ndash;Oct 2026 &middot; BEst EPS (lhs) vs. price and 40-week average (rhs) &middot; log scales cross at 12x P/E &middot; no consensus EPS Dec 2007&ndash;Mar 2009",
 C3_IMG="/home/claude/m3_crop.png",
 C3_COMMENT_1=P("At approximately 13.1x Goldman Sachs' 2027 EPS estimate of $14.28 and 3.5x tangible book value, Morgan Stanley trades at a substantial premium that reflects its wealth franchise, recurring fee revenues and consistently strong profitability. On Bloomberg consensus, the shares trade at 13.9x forward earnings against an average of 11.4x since 2005, and have slipped below their 40-week moving average. Goldman Sachs Research values the shares at $207 and UBS has a $236 price target, but the beat was modest and JPMorgan expects limited changes to 2026 consensus EPS. The valuation leaves less room for disappointment if IPO-related inflows normalise or deposit costs keep weighing on margins."),
 H_C3B="The margin challenge: growth comes at a price",
 C3_COMMENT_2=P("Despite record revenues and flows, Wealth Management profitability was slightly below expectations. The pre-tax margin of 30.4% missed consensus of approximately 30.7%, while net interest income declined 1% sequentially to $2.23bn, despite guidance for modest growth. Deposits rose 7% sequentially to approximately $465bn, but average deposit costs rose 18 basis points to 2.72%, offsetting the benefit of larger balances. With expenses up 10%, matching revenue growth, margins were broadly unchanged. Morgan Stanley has prioritised attracting client deposits over short-term interest margins; sustained margin expansion would provide an important justification for the valuation."),
 LEADIN_SECTION=S("Capital: capacity for growth and shareholder returns",
  "The standardised CET1 ratio held at 14.9% despite balance-sheet expansion and $1.54bn of share repurchases, approximately 260 basis points above Goldman Sachs Research's estimated 12.3% target. Unlike JPMorgan, Morgan Stanley maintained buybacks broadly in line with expectations. Group expenses rose 12%, matching revenue growth, although over nine months revenues grew 18% against 13% expense growth. Earnings volatility remains: Investment Management revenues fell 12% to $1.46bn on a carried interest reversal, even as its assets reached $2.05tn and combined client assets across Wealth and Investment Management reached $10.5tn.")
  + S("What would change our conviction",
  "Three developments matter most: the persistence of wealth inflows once the IPO contribution fades, particularly into fee-based relationships; the trajectory of Wealth Management net interest income and pre-tax margins; and the sustainability of Equities trading alongside a recovery in underwriting. Stronger conversion of flows into recurring fees with improving margins would reinforce the thesis; slowing asset gathering with sustained margin pressure would challenge current valuation expectations."),
 BASE_CASE=e("We remain constructive on Morgan Stanley's long-term franchise, supported by its leading Wealth Management platform, strong Equities business and substantial capital flexibility. The record inflows are encouraging, although the IPO contribution makes the headline figure difficult to repeat. At the current valuation, we would favour maintaining existing exposure while looking for evidence that asset gathering is translating into higher recurring revenues and improved margins before adding aggressively."),
 SOURCE_LINE="Source: Syz Research, Bloomberg, company reports",
)
for k, v in fill.items(): T = T.replace("{{" + k + "}}", str(v))
assert "{{" not in T
open("/home/claude/doc_ms.html", "w").write(T)
pdf = f"{OUT}/Research_Comment_Morgan_Stanley_Oct2026.pdf"
HTML("/home/claude/doc_ms.html").write_pdf(pdf)
for f in os.listdir("/home/claude"):
    if f.startswith("mpage"): os.remove("/home/claude/" + f)
pages = convert_from_path(pdf, dpi=100)
for i, p in enumerate(pages): p.save(f"/home/claude/mpage{i+1}.png")
print("pages:", len(pages))
