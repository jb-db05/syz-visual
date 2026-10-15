"""Build the Take-Two Interactive ad-hoc opinion in Syz Visual style (same structure as the European Luxury note)."""
import os, sys
from weasyprint import HTML

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from parts import css, LEGAL

OUT = sys.argv[1] if len(sys.argv) > 1 else f"{D}/Take-Two_Ad-hoc_Opinion_Oct2026.pdf"
DATE = "15 October 2026"
ASOF = "14 October 2026"


def company_page(name, ticker, kpis, band, left, right, conclusion):
    k = "".join(f'<div class="kpi"><div class="l">{l}</div><div class="v{" o" if o else ""}">{v}</div></div>' for l, v, o in kpis)
    b = "".join(f'<div><div class="l">{l}</div><div class="v">{v}</div></div>' for l, v in band)
    return f"""
<div class="pagebreak"></div><div class="gradbar"></div>
<div class="co-head"><h1 class="big">{name}</h1><span class="ticker">{ticker}</span></div>
<div class="kpis">{k}</div>
<div class="band">{b}</div>
<div class="cols"><div>{left}</div><div>{right}<div class="concl"><h3>Conclusion</h3><p>{conclusion}</p></div></div></div>
"""


BODY = f"""
<!-- PAGE 1: industry (1/2) -->
<div class="gradbar"></div>
<div class="kicker">Ad-hoc Opinion &middot; Video Games</div>
<h1>Take-Two Interactive: an ad-hoc opinion ahead of the launch of GTA&nbsp;VI</h1>
<div class="dateline">{DATE} &middot; CIO Office, Equity Team &middot; Syz Research</div>

<div class="notice"><b>Important notice.</b> This note relies on public information, company publications, broker research and third-party data. It contains no house price target and does not constitute a recommendation to buy or sell. Prices are as of {ASOF}.</div>

<h2 class="first">Where the industry is going: more spending per player, not more players</h2>
<div class="cols">
<div>
<p>The video game market is growing again, but slowly. Newzoo expects global games revenue of about $213.9bn in 2026, up 6.1% on 2025. The number of players is close to its ceiling: about 3.7 billion people play, 4.4% more than last year, and Newzoo sees that growth slowing to around 3% a year until 2029. Growth now comes from spending more per player&mdash;higher game prices, in-game purchases and subscriptions&mdash;rather than from new players.</p>
<p>Mobile remains the largest platform, at about $121bn, or more than half of the market. Console, at about $47bn, is where 2026 will be decided: Newzoo links much of its growth to a single title, Grand Theft Auto VI, due on 19 November.</p>
</div>
<div>
<p>Hardware is the weak link. Higher memory and storage costs have pushed console prices up: Nintendo raised the US price of the Switch 2 from $449.99 to $499.99 on 1 September. According to Circana, US hardware spending is down 11% this year to August. Fewer new consoles means publishers must earn more from the players they already have.</p>
<p><b>What this means for investors.</b> The industry now rewards the owners of a few large franchises that players come back to for years, and that can be sold at higher prices. Scale matters more than ever: Electronic Arts was taken private for $55bn, a deal completed on 4 August. Take-Two, with Grand Theft Auto, NBA 2K and a large mobile portfolio, is one of the few large listed pure plays left in the US.</p>
</div>
</div>

<div class="chart-title"><span class="num">Chart 1</span> &middot; Global games market &ndash; 2026 revenue by platform</div>
<div class="chart-sub">Newzoo forecast, USD bn &middot; growth versus 2025 &middot; console, the segment driven by GTA VI, highlighted</div>
<img class="mkt" src="file://{D}/img/market.png">

<!-- PAGE 2: industry (2/2) -->
<div class="pagebreak"></div><div class="gradbar"></div>
<h1>What could move the shares</h1>
<div class="cols" style="margin-top:3mm">
<div>
<h3 class="sub">The drivers</h3>
<ul>
<li><b>GTA VI.</b> The most awaited launch in the industry&rsquo;s history is due on 19 November, on PS5 and Xbox Series X|S only. Its first weeks will set the tone for the whole sector.</li>
<li><b>Game prices.</b> The base edition of GTA VI costs $80, against $70 for most new games. If players accept it, margins rise across the industry.</li>
<li><b>Console costs.</b> Memory costs have pushed hardware prices up and sales down: S&amp;P Global Kagan expects console shipments to fall 19.5% this year, to 33.9 million units. A smaller base of new consoles limits the audience for new games.</li>
<li><b>App store fees.</b> Court cases against Apple and Google are opening the door to cheaper ways of paying outside the app stores. Every point of commission saved goes straight to mobile margins.</li>
<li><b>Consolidation.</b> The $55bn take-private of Electronic Arts shows the value that private and sovereign buyers see in large franchises.</li>
</ul>
</div>
<div>
<h3 class="sub">The next dates</h3>
<ul>
<li><b>9 November:</b> Take-Two second-quarter results (July to September).</li>
<li><b>19 November:</b> launch of GTA VI on PS5 and Xbox Series X|S.</li>
<li><b>Late November to December:</b> Black Friday and the festive season, the first full read on GTA VI sales.</li>
<li><b>Early February 2027:</b> Take-Two third-quarter results, covering the launch quarter (date to be confirmed).</li>
<li><b>2027:</b> GTA VI on PC and the next GTA Online. No dates have been announced.</li>
</ul>
</div>
</div>

<h2>Take-Two at a glance: the GTA VI step-up</h2>
<table class="glance">
<tr><th>Fiscal year (to March)</th><th class="num">FY2026<br>actual</th><th class="num hl">FY2027<br>estimate</th><th class="num">FY2028<br>estimate</th><th class="num">FY2029<br>estimate</th></tr>
<tr><td><b>Net bookings</b> (USD bn)</td><td class="num">6.72</td><td class="num hl">8.20</td><td class="num">10.54</td><td class="num">n.a.</td></tr>
<tr><td><b>Adjusted EPS</b> (USD)</td><td class="num">4.10</td><td class="num hl">5.99</td><td class="num">10.18</td><td class="num">11.28</td></tr>
<tr><td><b>P/E</b> at USD 201.2</td><td class="num">49.1x</td><td class="num hl">33.6x</td><td class="num">19.8x</td><td class="num">17.8x</td></tr>
<tr><td><b>EBITDA margin</b></td><td class="num">17.3%</td><td class="num hl">19.7%</td><td class="num">31.1%</td><td class="num">33.2%</td></tr>
<tr><td><b>Free cash flow yield</b></td><td class="num">1.2%</td><td class="num hl">1.9%</td><td class="num">4.2%</td><td class="num">4.7%</td></tr>
</table>
<div class="note">FY2027 runs from April 2026 to March 2027 and includes the GTA VI launch; company guidance for net bookings is USD 8.0&ndash;8.2bn. Estimates are broker consensus. The P/E ratio shows how many years of expected profits the share price represents: the higher it is, the more growth the market already expects. It is computed here at the {ASOF} close.</div>
"""

BODY += company_page(
    "Take-Two Interactive", "TTWO US",
    [("Share price", "USD 201.2", 0), ("From the July high", "&minus;24%", 1), ("P/E (FY2028 expected profits)", "19.8x", 0), ("GTA VI launch", "19 November", 0)],
    [("Technical trend", "Neutral"), ("Support", "USD 196.3 / 188.0"), ("Resistance", "USD 220.2 / 224.3"), ("Trend would turn bearish below", "USD 188.0")],
    """<h3><span class="n">1.</span> What the company does</h3>
<p>Take-Two is a New York-based video game publisher with three labels. Rockstar Games makes Grand Theft Auto and Red Dead Redemption: GTA V has sold close to 230 million copies since 2013. 2K publishes sports games such as NBA 2K and WWE 2K, and franchises such as Borderlands and Civilization. Zynga runs a large mobile portfolio, led by Toon Blast and Match Factory!. About 84% of net bookings come from spending inside games already on sale.</p>
<h3><span class="n">2.</span> Why it could do well</h3>
<ul>
<li><b>The biggest launch in the industry.</b> GTA VI is due on 19 November. BofA estimates that the USD 8.0&ndash;8.2bn guidance for the year to March assumes about 34 million copies sold; some analysts expect closer to 50 million. Management called pre-order demand &ldquo;exceptional&rdquo;.</li>
<li><b>A step change in earnings.</b> Analysts expect adjusted earnings per share to rise from USD 4.10 in FY2026 to USD 10.18 in FY2028, the first full year with GTA VI.</li>
<li><b>Steady spending inside games.</b> It made up 84% of net bookings in the June quarter. NBA 2K26 sold more than 12 million copies, and mobile reached its highest bookings since Zynga joined in 2022.</li>
</ul>
<h3><span class="n">3.</span> What sets it apart</h3>
<p>Few companies own franchises that last this long. GTA V is still selling 13 years after its launch, across three console generations, thanks to GTA Online. Rockstar releases few games, but each one becomes a reference. The flip side is concentration: the group&rsquo;s results depend heavily on a single franchise.</p>""",
    """<h3><span class="n">4.</span> Is the share expensive?</h3>
<p>On this year&rsquo;s profits, yes: about 34 years of expected FY2027 profits. On FY2028, the first full year with GTA VI, the multiple falls to about 20. Brokers are positive: BofA rates the share Buy, and JPMorgan Overweight with a USD 310 target, based on about 30 times FY2028 earnings. BofA notes that the share trades below its level right after the May 2025 delay, although the launch is now far less risky.</p>
<h3><span class="n">5.</span> Main risks</h3>
<ul>
<li>A further delay of GTA VI would push the earnings jump back by a year and hit the share hard.</li>
<li>High expectations: even a strong launch can disappoint if early sales fall short of the most optimistic forecasts.</li>
<li>Fewer new consoles: higher hardware prices could limit the number of players able to buy the game at launch.</li>
<li>Leaks: a hacker has published gameplay clips and threatens to release more. The effect on sales is seen as limited.</li>
<li>Five customers, mainly the console and app stores, account for about 82% of net revenue.</li>
</ul>
<h3><span class="n">6.</span> What to watch next</h3>
<p>Second-quarter results on 9 November, ten days before the launch: any update on GTA VI pre-orders and on the full-year guidance. Then the first sales data after 19 November.</p>""",
    "Take-Two has the strongest catalyst in the sector, and the valuation on FY2028 profits looks reasonable. The chart has weakened, though: the share has lost about a quarter since July and sits just above its March lows. The next page looks at the entry point and at how to manage an existing position.")

BODY += """
<div class="pagebreak"></div><div class="gradbar"></div>
<h1 class="big">Take-Two: our view on the share</h1>
<h2>Where is the stock?</h2>
<p>The primary trend has turned negative. The 200-day average (USD 222.9) is falling, and the 50-day average (USD 220.2) crossed below it on 7 October, a &ldquo;death cross&rdquo; that confirms the weakness. Since its record of USD 265.9 in July, the share has made lower highs and lower lows, and set a new 100-day low at USD 196.3 on 13 October. It now trades just above the March lows. As long as USD 188 holds, our technical reading remains Neutral.</p>
<p>The share has also lagged the market: its performance against the S&amp;P 500 is at a one-year low, well below its falling 200-day average. Momentum is weak and close to oversold, with the stochastic at 24 and the price near the lower Bollinger band (USD 194.5), which raises the chance of a rebound from support.</p>
<h2>Is it a good time to buy?</h2>
<p>The business case is at its strongest just as the share is at its weakest since March. That gap is what makes the setup interesting. The chart does not yet confirm a turn, however, and the launch on 19 November is an all-or-nothing event for the share in the short term.</p>
<p>For an investor without a position, a gradual approach makes sense: a first part close to the current support (USD 188 to 201), and the rest either once the share closes above USD 224.3, the September high, which would end the downtrend, or after the first sales figures for GTA VI. A close below USD 188 would call this view into question.</p>
<h2>How to handle an existing position?</h2>
<p>Keeping the position is justified ahead of the launch: the earnings step-up is close and well documented. Three levels help manage it:</p>
<ul>
<li><b>Above USD 224.3:</b> the downtrend ends, with USD 265.9 as the next objective.</li>
<li><b>Below USD 196.3:</b> the share breaks its latest low; a good moment to review the size of the position.</li>
<li><b>Below USD 188:</b> the reading turns Bearish, and reducing the position becomes reasonable.</li>
</ul>
<p>The results on 9 November and the launch on 19 November are likely to move the share sharply in either direction. Investors who cannot accept that volatility may prefer to hold less than their target weight until the first sales data are known.</p>
<h2>How does it compare with its peers?</h2>
<p>With Electronic Arts now private, Take-Two is one of the few large listed ways to own console and mobile games in the US. Its earnings growth over the next two years is tied to a single launch. That makes it more concentrated than diversified groups, but it also gives it the clearest catalyst in the sector.</p>
<div class="bottomline"><div class="bl-head">In short</div>
<p>Take-Two holds the sector&rsquo;s biggest catalyst, and its valuation on FY2028 profits is reasonable. The chart, however, is weak and stays Neutral only as long as USD 188 holds. A gradual entry around support, or after the first GTA VI sales data, is the prudent approach. Existing positions can be kept, with USD 196.3 and USD 188 as the levels to watch.</p></div>
"""

BODY += f"""
<div class="pagebreak"></div><div class="gradbar"></div>
<div class="co-head"><h1 class="big">Take-Two: technical charts</h1><span class="ticker">TTWO US</span></div>
<div class="chart-title"><span class="num">Chart 2</span> &middot; Take-Two &ndash; Price, moving averages, momentum and relative strength</div>
<div class="chart-sub">Daily, log scale &middot; 50-day average (blue), 200-day average (red), March support at 188 (dotted) &middot; panels: stochastic momentum; relative strength vs. S&amp;P 500</div>
<img class="chart" src="file://{D}/img/ttwo_top.png" style="width:80%">
<div class="signals"><div class="top"><span class="kick">Breakout &amp; momentum signals</span><span class="pill neg"><span class="tri dn"></span>NEGATIVE</span></div>
<p><b>The last band broken was the lower band</b> &mdash; a new 100-day low at <b>USD 196.3</b> on 13 October 2026, a negative trend signal; the upper band (<b>USD 265.9</b>) has not been broken since 7 July 2026. <b>Long-term momentum is negative:</b> the latest bar is red, so the momentum regime remains unfavourable.</p></div>
<div class="chart-title"><span class="num">Chart 3</span> &middot; Take-Two &ndash; Trend regime and 100-day range</div>
<div class="chart-sub">Daily, log scale &middot; bars coloured by the slope of the 200-day average &middot; dotted lines: 100-day high and low</div>
<img class="chart" src="file://{D}/img/ttwo_bot.png" style="width:62%">
<div class="caption">Top chart: share price with the 50-day average (blue) and the 200-day average (red); the middle panel shows momentum and the lower panel the share&rsquo;s performance against the S&amp;P 500. Bottom chart: bars in blue when the 200-day average is rising, in red when it is falling; the dotted lines show the highest and lowest price of the last 100 days.</div>
<div class="src"><span class="syz">SYZ</span> Source: Syz Research, Bloomberg.</div>

<div class="pagebreak"></div><div class="gradbar"></div>
<h1 class="big">Sources</h1>
<div class="sources" style="margin-top:3mm">
<p>Market data, prices, valuation ratios and technical levels: Bloomberg, as of {ASOF} (close).</p>
<p>Company information: Take-Two Interactive first-quarter fiscal 2027 results (August 2026) and investor relations website. Broker research: BofA Global Research (9 October 2026) and JPMorgan; consensus estimates.</p>
<p>Industry data: Newzoo (Global Games Market Report 2026), Circana, S&amp;P Global Market Intelligence Kagan; company announcements by Nintendo and Electronic Arts.</p>
<p>Technical analysis: Syz Research, Bloomberg.</p>
</div>
{LEGAL}
"""

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css(D, DATE)}</style></head><body>{BODY}</body></html>"
open(f"{D}/doc.html", "w").write(html)
HTML(f"{D}/doc.html").write_pdf(OUT)
print("wrote", OUT)
