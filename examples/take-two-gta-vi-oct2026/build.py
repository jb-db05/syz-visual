"""Rebuild 'Take-Two Interactive: one month before Grand Theft Auto VI' (4-page ad-hoc opinion) in Syz Visual style.
Content is kept verbatim from the source note; only the layout and typography change."""
import os, sys
from weasyprint import HTML

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from parts import css, LEGAL

OUT = sys.argv[1] if len(sys.argv) > 1 else f"{D}/Take-Two_Ad-hoc_Opinion_GTA-VI_Oct2026.pdf"
DATE = "15 October 2026"

BODY = f"""
<!-- PAGE 1: the sector -->
<div class="gradbar"></div>
<div class="kicker">Ad-hoc Opinion &middot; Video Games</div>
<h1>Take-Two Interactive: one month before Grand Theft Auto VI</h1>
<div class="dateline">{DATE} &middot; CIO Office, Equity Team &middot; Syz Research</div>

<div class="notice"><b>Important notice.</b> This note gives our view on Take-Two Interactive and the video games sector. It relies on public information, company publications and third-party data. It contains no house price target and does not constitute a recommendation to buy or sell. Prices are as of 14 October 2026.</div>

<h2 class="first">The sector: big launches, recurring spending and the AI question</h2>
<div class="cols">
<div>
<p>Video games have become one of the largest forms of entertainment, ahead of cinema and recorded music. After the boom during the pandemic and two years of cost cuts, the industry is entering a new growth phase. Two events drive it: Nintendo&rsquo;s new Switch 2 console, which has sold strongly since mid-2025, and the launch of Grand Theft Auto VI on 19 November 2026, expected to be one of the largest entertainment launches ever.</p>
<p>The business model has changed. Most revenue no longer comes from selling a game once, but from what players spend afterwards: extra content, virtual currency and subscriptions. At Take-Two, this recurring spending accounts for 84% of revenue. It makes results more stable, but also more dependent on a few very popular titles.</p>
</div>
<div>
<p>The industry is consolidating. Developing a major game now takes five years or more and costs several hundred million dollars, which favours large groups with strong franchises. The $55bn takeover of Electronic Arts by a consortium including Saudi Arabia&rsquo;s sovereign fund shows how much investors are willing to pay for established game brands.</p>
<p><b>The AI question.</b> Generative AI cuts both ways. It can lower development costs, but it may also make it easier for new players to produce games and weaken the advantage of large studios. When Google unveiled a tool that creates explorable 3D worlds from text in January 2026, Take-Two lost 10% in a day. The tool cannot yet build a full game, but the fear can return with each new breakthrough.</p>
<p><b>What this means for investors.</b> The listed companies that benefit most own franchises that players return to for years. Take-Two owns several of the strongest, and the next few months will be decisive for its share price: few stocks depend so much on a single date.</p>
</div>
</div>

<!-- PAGE 2: the company -->
<div class="pagebreak"></div><div class="gradbar"></div>
<div class="co-head"><h1 class="big">Take-Two Interactive</h1><span class="ticker">TTWO US</span></div>
<div class="kpis">
<div class="kpi"><div class="l">Share price</div><div class="v">USD 201.2</div></div>
<div class="kpi"><div class="l">From the July record</div><div class="v o">&minus;24%</div></div>
<div class="kpi"><div class="l">Sales outlook to March 2027</div><div class="v">USD 8.0 to 8.2bn</div></div>
<div class="kpi"><div class="l">GTA VI launch</div><div class="v">19 November</div></div>
</div>
<div class="band">
<div><div class="l">Technical trend</div><div class="v">Neutral</div></div>
<div><div class="l">Support</div><div class="v">USD 196.3 / 188</div></div>
<div><div class="l">Resistance</div><div class="v">USD 220.2 / 224.3</div></div>
<div><div class="l">Turns negative below</div><div class="v">USD 188</div></div>
</div>
<div class="cols">
<div>
<h3><span class="n">1.</span> What the company does</h3>
<p>Take-Two is a US video game publisher with three labels. Rockstar Games makes Grand Theft Auto and Red Dead Redemption; GTA V alone has sold about 230 million copies since 2013. 2K publishes sports games such as NBA 2K, as well as Borderlands and Civilization. Zynga, acquired in 2022, makes mobile games such as Toon Blast and Match Factory!.</p>
<h3><span class="n">2.</span> Why it could do well</h3>
<ul>
<li><b>A record year in sight.</b> The company expects sales of USD 8.0bn to 8.2bn in the year to March 2027, about 20% more than last year, driven by Grand Theft Auto VI.</li>
<li><b>Revenue that lasts.</b> 84% of sales come from players who keep spending in games they already own. GTA V still generates revenue thirteen years after its launch, and GTA VI should follow the same model.</li>
<li><b>A strong rest of the portfolio.</b> NBA 2K27 launched in September, and mobile games generate more than half of sales today, which supports the business between major releases.</li>
</ul>
<h3><span class="n">3.</span> What sets it apart</h3>
<p>Rockstar&rsquo;s franchises are among the most valuable in entertainment, and few studios can deliver a game of this scale. The GTA series has sold about 475 million copies in total. Each new release builds a player base that spends for many years.</p>
</div>
<div>
<h3><span class="n">4.</span> Is the share expensive?</h3>
<p>It depends on the year you look at. On analysts&rsquo; estimates, the share price represents about 34 years of expected profits for the year to March 2027, but about 20 years for the following year, the first full year of the new game. In other words, the price already assumes a successful launch; the recent fall shows that investors are less certain than in the summer.</p>
<h3><span class="n">5.</span> Main risks</h3>
<ul>
<li>A third delay of the game, which would push the expected profits back by a year.</li>
<li>A launch that sells well but below very high expectations: shares often fall after long-awaited events.</li>
<li>Heavy dependence on one franchise, and on a handful of distributors such as Sony, Microsoft, Apple and Google.</li>
<li>Mobile games face rising costs to attract new players.</li>
</ul>
<h3><span class="n">6.</span> What to watch next</h3>
<p>Second-quarter results in early November, the launch on 19 November, first sales figures, and news on the online version and a possible PC release.</p>
<div class="concl"><h3>Conclusion</h3>
<p>Take-Two owns some of the strongest franchises in entertainment and is a month away from its most important launch in a decade. The opportunity is real, but so is the risk around a single date. Building a position in stages, around the launch rather than before it, seems prudent; USD 188 is the level to watch.</p></div>
</div>
</div>

<!-- PAGE 3: technical charts -->
<div class="pagebreak"></div><div class="gradbar"></div>
<div class="co-head"><h1 class="big">Take-Two: technical charts</h1><span class="ticker">TTWO US</span></div>
<div class="chart-title"><span class="num">Chart 1</span> &middot; Take-Two &ndash; Price, moving averages, momentum and relative strength</div>
<img class="chart" src="file://{D}/img/ttwo_top.png" style="width:86%">
<div class="caption">Share price with the 50-day average (blue) and the 200-day average (red), the USD 188 support (dotted line), momentum (middle panel) and performance relative to the S&amp;P 500 (lower panel).</div>
<div class="chart-title" style="margin-top:5mm"><span class="num">Chart 2</span> &middot; Take-Two &ndash; Trend regime and 100-day range</div>
<img class="chart" src="file://{D}/img/ttwo_bot.png" style="width:78%">
<div class="caption">Bars in blue when the 200-day average is rising, in red when it is falling; the dotted lines show the highest and lowest price of the last 100 days.</div>
<div class="src"><span class="syz">SYZ</span> Source: Syz Research, Bloomberg.</div>

<!-- PAGE 4: sources + disclaimer -->
<div class="pagebreak"></div><div class="gradbar"></div>
<h1 class="big">Sources</h1>
<div class="sources" style="margin-top:3mm">
<p>Market data, prices, valuation ratios and technical levels: Bloomberg, as of 14 October 2026.</p>
<p>Company information: published results and investor relations website of Take-Two Interactive Software, Inc., including the results for the first quarter of the financial year 2027 published on 7 August 2026.</p>
<p>Technical analysis: Syz Research, Bloomberg.</p>
</div>
{LEGAL}
"""

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css(D, DATE)}</style></head><body>{BODY}</body></html>"
open(f"{D}/doc.html", "w").write(html)
HTML(f"{D}/doc.html").write_pdf(OUT)
print("wrote", OUT)
