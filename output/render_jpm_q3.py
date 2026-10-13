import os, sys
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
 TITLE="JPMorgan Chase: Stronger Outlook, Fewer Buybacks", W1=W1, W2=W2, W3=W3,
 INTRO_PARAGRAPHS=P("JPMorgan Chase delivered a mixed Q3, but its outlook for 2027 was considerably stronger than expected. Reported EPS of $5.57 missed consensus of $5.92, partly reflecting $658m in investment securities losses, while managed revenues reached $50.9bn, up 8% year-on-year. Excluding those losses, EPS was $5.75 and return on tangible common equity (ROTCE) reached 21%, comfortably above management's 17% medium-term target. The more important development came from guidance: JPMorgan now expects $107bn in net interest income excluding Markets in 2027, around $2.5–4bn above analysts' estimates. At $334 ahead of the release, or 12.2x 2027 earnings, the investment case increasingly rests on the bank's ability to turn its expanding balance sheet into sustainable earnings growth. The complication is that management is retaining more capital to fund that expansion, at the expense of share buybacks."),
 H_C1="Q3: lending leads, markets remain resilient",
 C1_TITLE="JPMorgan Chase &ndash; Growth by Business", C1_SUB="Q3 2026 vs. Q3 2025, % change &middot; Markets in orange &middot; Growth rates as quoted in the Q3 results",
 C1_IMG="/home/claude/j1_crop.png",
 C1_COMMENT=P("Net interest income reached $27.0bn, up 13% year-on-year, supported by higher deposit balances, credit card lending and wholesale loans. Average loans increased 10% year-on-year and deposits grew 8%, demonstrating that JPMorgan continues to capture business across its consumer and corporate franchises. Excluding Markets, net interest income reached $24.7bn, while the net interest margin improved by five basis points sequentially to 3.70%.",
  "Capital markets provided a second source of growth. Markets revenues rose 15% to $10.3bn, with Equities up 49% to $5.0bn, particularly in prime brokerage and derivatives. Fixed Income was weaker, declining 4% as activity softened in rates, credit and commodities. Investment banking fees increased 14% to $3.0bn, supported by a 32% increase in Advisory revenues, although underwriting activity moderated from Q2. Trading remains a valuable earnings contributor, but the strength of the quarter was ultimately more visible in lending and recurring client activity."),
 H_C2="The real surprise: a stronger 2027 income base",
 C2_TITLE="JPMorgan Chase &ndash; 2027 Net Interest Income Outlook", C2_SUB="NII excluding Markets, $bn &middot; Axis starts at $94bn &middot; Analyst range as quoted in the text",
 C2_IMG="/home/claude/j2_crop.png",
 C2_COMMENT=P("Management raised its 2026 net interest income guidance to $106.2bn from $105.5bn, including Markets, and introduced a preliminary 2027 target of $107bn excluding Markets, compared with $97.2bn expected for 2026. That implies approximately 10% growth next year and exceeds analysts' forecasts of around $103–104.5bn.",
  "This matters because net interest income represents a relatively predictable earnings stream compared with trading and investment banking fees. The higher outlook reflects a combination of loan growth, deposit gathering and a more favourable interest rate environment.",
  "The uncertainty lies in the assumptions underpinning that growth. Higher rates have improved asset yields, but deposit competition is also intensifying. The durability of the $107bn target will depend on how much of the benefit JPMorgan can retain as depositors demand higher remuneration and the loan book continues to expand."),
 H_C3="Diversification remains JPMorgan's greatest advantage",
 C3_TITLE="JPMorgan Chase &ndash; Q3 2026 Revenues by Business", C3_SUB="$bn, with year-on-year growth &middot; Markets split into Equities and Fixed Income &middot; Fixed Income derived as Markets minus Equities",
 C3_IMG="/home/claude/j3_crop.png",
 C3_COMMENT_1=P("The quarter also highlighted the breadth of JPMorgan's earnings base. Consumer & Community Banking revenues rose 9% to $21.2bn, supported by stronger credit card balances and deposit income. Card Services net charge-offs declined to 2.91%, from 3.34% in Q2.",
  "Asset & Wealth Management revenues increased 14% to $6.9bn, with assets under management reaching $5.2tn, up 13% year-on-year."),
 H_C3B="The capital trade-off: growth takes priority over buybacks",
 C3_COMMENT_2=P("The strongest message from management concerned capital allocation. JPMorgan repurchased only $1.1bn of shares on a gross basis, against market expectations of approximately $7.7bn. Net repurchases were just $664m, while dividends totalled $4.4bn. Management explicitly prioritised reinvestment in the franchise and client activity, arguing that retained capital can be deployed at attractive returns.",
  "The decision comes as the standardised CET1 ratio declined 30 basis points to 13.9%. Capital remains comfortably above the bank's estimated 12% target, but the shift creates uncertainty around the pace of future distributions. Goldman Sachs Research estimates that consensus expectations for approximately $32.5bn in 2027 buybacks may need to be revised lower.",
  "Operating expenses rose 12% year-on-year to $27.3bn, outpacing revenue growth. Management increased its 2026 expense guidance from $107.5bn to $108.6bn. Crucially, JPMorgan offered no corresponding guidance for 2027 expenses.",
  "Credit quality remains reassuring for now. Net charge-offs fell year-on-year to $2.2bn, although JPMorgan added $539m to reserves, predominantly in wholesale lending."),
 LEADIN_SECTION=S("Valuation: paying for resilience and scale",
  "At $334.30, JPMorgan trades at approximately 12.2x Goldman Sachs' 2027 EPS estimate of $27.43 and nearly 3.0x its latest tangible book value. The premium reflects a franchise generating ROTCE above 20%.",
  "The investment debate has shifted towards capital efficiency. If the additional net interest income translates into higher sustainable earnings, the current valuation remains supported. However, lower repurchases reduce an important source of EPS growth, while higher operating costs could absorb part of the revenue upside.")
  + S("What would change our conviction",
  "Three developments deserve particular attention. First, delivery against the $107bn net interest income outlook. Second, the 2027 expense trajectory, which will determine how much of the revenue increase reaches the bottom line. Third, the pace of capital returns, with investors likely to reassess buyback expectations following the sharp Q3 reduction. Conversely, continued ROTCE above 20%, with stable credit and disciplined costs, would reinforce the premium valuation."),
 BASE_CASE=e("We remain constructive on JPMorgan's long-term earnings outlook. The Q3 headline miss masks a stronger underlying lending franchise and a materially improved 2027 net interest income forecast. However, the reduction in buybacks and absence of 2027 cost guidance limit the immediate upside. We would favour maintaining exposure, with additional purchases more attractive on valuation weakness or once management provides greater visibility on expenses and capital returns."),
 SOURCE_LINE="Source: Syz Research, company reports",
)
for k, v in fill.items(): T = T.replace("{{" + k + "}}", str(v))
assert "{{" not in T
open("/home/claude/doc_jpm.html", "w").write(T)
pdf = f"{OUT}/Research_Comment_JPMorgan_Chase_Oct2026.pdf"
HTML("/home/claude/doc_jpm.html").write_pdf(pdf)
for f in os.listdir("/home/claude"):
    if f.startswith("jpage"): os.remove("/home/claude/" + f)
pages = convert_from_path(pdf, dpi=100)
for i, p in enumerate(pages): p.save(f"/home/claude/jpage{i+1}.png")
print("pages:", len(pages))
