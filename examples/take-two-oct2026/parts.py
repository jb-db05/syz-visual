D=None
def css(D, DATE):
    CSS = f"""
    @font-face {{ font-family: 'Nunito'; src: url('file://{D}/fonts/Nunito-Regular.ttf'); font-weight: 400; }}
    @font-face {{ font-family: 'Nunito'; src: url('file://{D}/fonts/Nunito-Light.ttf'); font-weight: 300; }}
    @font-face {{ font-family: 'Nunito'; src: url('file://{D}/fonts/Nunito-SemiBold.ttf'); font-weight: 600; }}
    @font-face {{ font-family: 'Nunito'; src: url('file://{D}/fonts/Nunito-Bold.ttf'); font-weight: 700; }}
    @font-face {{ font-family: 'Nunito'; src: url('file://{D}/fonts/Nunito-ExtraBold.ttf'); font-weight: 800; }}
    
    @page {{
      size: A4;
      margin: 18mm 15mm 12.5mm 15mm;
      @top-right {{ content: url('file://{D}/img/logo.png'); image-resolution: 460dpi; vertical-align: bottom; padding-top: 9mm; }}
      @top-left {{ content: "Take-Two Interactive \\0000b7\\0000a0Ad-hoc Opinion"; font-family: 'Nunito'; font-size: 7pt; color: #9AA0A8; vertical-align: bottom; padding-bottom: 1.2mm; }}
      @bottom-left {{
        content: "Syz Research \\0000b7\\0000a0CIO Office, Equity Team \\0000b7\\0000a0Ad-hoc Opinion \\0000b7\\0000a0{DATE}";
        font-family: 'Nunito'; font-size: 7pt; color: #9AA0A8;
      }}
      @bottom-right {{ content: counter(page) " / " counter(pages); font-family: 'Nunito'; font-size: 7pt; color: #9AA0A8; }}
    }}
    @page :first {{ @top-left {{ content: none; }} }}
    
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Nunito'; color: #202945; font-size: 8.9pt; line-height: 1.42; }}
    b, strong {{ font-weight: 800; }}
    
    .gradbar {{ height: 3.5px; background: linear-gradient(90deg, #FF6C0E 0%, #FFC545 100%); margin-bottom: 4mm; }}
    .kicker {{ font-size: 8pt; font-weight: 700; letter-spacing: 1.6px; color: #FF6C0E; text-transform: uppercase; margin-bottom: 1.5mm; }}
    h1 {{ font-size: 17pt; font-weight: 800; color: #202945; line-height: 1.22; margin-bottom: 1.5mm; }}
    h1.big {{ font-size: 20pt; }}
    .dateline {{ font-size: 8.5pt; color: #6B7280; margin-bottom: 3.5mm; }}
    h2 {{ font-size: 11pt; font-weight: 800; color: #202945; line-height: 1.2; margin: 4mm 0 1.6mm 0; break-after: avoid; }}
    h2.first {{ margin-top: 0; }}
    h3 {{ font-size: 9.3pt; font-weight: 800; color: #202945; margin: 3mm 0 1.2mm 0; break-after: avoid; }}
    h3:first-child {{ margin-top: 0; }}
    h3 .n {{ color: #FF6C0E; }}
    h3.sub {{ color: #FF6C0E; font-size: 8pt; letter-spacing: 1.4px; text-transform: uppercase; margin-top: 0; }}
    p {{ margin-bottom: 2.2mm; text-align: justify; }}
    
    ul {{ list-style: none; margin: 0 0 2.2mm 0; }}
    li {{ position: relative; padding-left: 4mm; margin-bottom: 1.6mm; text-align: justify; }}
    li::before {{ content: ""; position: absolute; left: 0.6mm; top: 1.55mm; width: 1.5mm; height: 1.5mm; background: #FF6C0E; border-radius: 0.4mm; }}
    
    .cols {{ display: flex; gap: 8mm; }}
    .cols > div {{ flex: 1; min-width: 0; }}
    
    .notice {{ border-left: 3px solid #FF6C0E; background: #F6F7F9; padding: 3mm 4mm; margin: 1mm 0 5mm 0; font-size: 8.3pt; color: #4B5563; }}
    .notice b {{ color: #202945; }}
    
    /* At-a-glance table */
    table.glance {{ width: 100%; border-collapse: collapse; font-size: 8.3pt; margin-top: 1mm; }}
    table.glance th {{ background: #202945; color: #FFFFFF; font-weight: 700; text-align: left; padding: 2.4mm 2.2mm; font-size: 7.8pt; line-height: 1.25; vertical-align: bottom; }}
    table.glance th.r, table.glance td.r {{ text-align: right; }}
    table.glance td {{ padding: 2.6mm 2.2mm; border-bottom: 1px solid #E3E6EA; vertical-align: top; }}
    table.glance tr:nth-child(even) td {{ background: #F8F9FA; }}
    table.glance .tk {{ color: #8A8F98; font-size: 7.6pt; }}
    .bull {{ color: #3BAF90; font-weight: 800; }}
    .bear {{ color: #AC5D85; font-weight: 800; }}
    .note {{ font-size: 7.4pt; color: #6B7280; margin-top: 2mm; text-align: left; }}
    
    /* Company header */
    .co-head {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 3mm; }}
    .co-head h1 {{ margin: 0; }}
    .ticker {{ font-size: 8pt; font-weight: 700; color: #8A8F98; letter-spacing: 1px; }}
    .kpis {{ display: flex; gap: 3.5mm; margin-bottom: 2.5mm; }}
    .kpi {{ flex: 1; border-top: 2px solid #FF6C0E; padding-top: 1.6mm; }}
    .kpi .l {{ font-size: 7.4pt; color: #6B7280; }}
    .kpi .v {{ font-size: 13pt; font-weight: 800; color: #202945; line-height: 1.2; }}
    .kpi .v.o {{ color: #FF6C0E; }}
    .band {{ display: flex; background: #202945; border-radius: 2.5mm; padding: 2.6mm 4mm; margin-bottom: 4.5mm; gap: 3.5mm; }}
    .band > div {{ flex: 1; }}
    .band .l {{ font-size: 7.2pt; color: #FFA400; font-weight: 600; }}
    .band .v {{ font-size: 10pt; font-weight: 800; color: #FFFFFF; }}
    
    .concl {{ border-top: 2px solid #202945; margin-top: 4mm; padding-top: 2.5mm; }}
    .concl h3 {{ margin-top: 0; }}
    
    .bottomline {{ background: #202945; border-radius: 3.5mm; padding: 4mm 5.5mm; color: #FFFFFF; margin-top: 5mm; }}
    .bottomline .bl-head {{ font-size: 7.8pt; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: #FFA400; margin-bottom: 1.6mm; }}
    .bottomline p {{ color: #E8EAEF; margin-bottom: 0; font-size: 9.3pt; }}
    
    /* Technical charts pages */
    .chart-title {{ font-size: 9.5pt; font-weight: 700; color: #202945; margin: 1mm 0 1.5mm 0; }}
    .chart-title .num {{ color: #FF6C0E; }}
    .chart-sub {{ font-size: 7.2pt; color: #6B7280; margin: -1mm 0 1.6mm 0; }}
    img.chart {{ width: 100%; display: block; margin: 0 auto 2mm auto; }}
    .signals {{ background: #F4F5F7; border-radius: 3mm; padding: 3mm 4.5mm; margin: 2.5mm 0 4mm 0; }}
    .signals .top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.4mm; }}
    .signals .kick {{ font-size: 7.6pt; font-weight: 800; letter-spacing: 1.8px; color: #FF6C0E; text-transform: uppercase; }}
    .pill {{ font-size: 7pt; font-weight: 800; letter-spacing: 0.8px; color: #FFFFFF; border-radius: 3mm; padding: 0.8mm 3mm; }}
    .pill.pos {{ background: #3BAF90; }}
    .pill.neg {{ background: #AC5D85; }}
    .tri {{ display: inline-block; width: 0; height: 0; border-left: 1.1mm solid transparent; border-right: 1.1mm solid transparent; margin-right: 1.2mm; vertical-align: 0.15mm; }}
    .tri.up {{ border-bottom: 1.6mm solid #FFFFFF; }}
    .tri.dn {{ border-top: 1.6mm solid #FFFFFF; }}
    .signals p {{ margin: 0; font-size: 8.4pt; }}
    .caption {{ font-size: 7.8pt; color: #4B5563; margin-top: 2mm; }}
    .src {{ font-size: 7.4pt; color: #9AA0A8; margin-top: 2mm; }}
    .src .syz {{ color: #FF6C0E; font-weight: 800; }}
    
    /* Legal page */
    .legal {{ font-size: 6.8pt; color: #9AA0A8; line-height: 1.4; }}
    .legal .disc-head {{ color: #FF6C0E; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; margin: 6mm 0 1.5mm 0; font-size: 7.4pt; }}
    .legal p {{ font-size: 6.8pt; margin-bottom: 1.6mm; text-align: justify; }}
    .sources p {{ margin-bottom: 1.8mm; }}
    
    .pagebreak {{ page-break-before: always; }}
    img.mkt {{ width: 100%; display: block; margin: 0 auto 1mm auto; }}
    table.glance td.num, table.glance th.num {{ text-align: right; }}
    table.glance td.hl, table.glance th.hl {{ background: #FFF4EC; }}
    table.glance th.hl {{ background: #FF6C0E; }}
    .neu {{ color: #4B5F80; font-weight: 800; }}
    """
    
    return CSS

LEGAL = r"""<div class="legal">
  <div class="disc-head">Important information</div>
  <p>This communication has been issued and made available to recipients for the purpose of advertising investment services and/or financial instruments. It has been sent for information purposes and cannot be considered as an offer or a personalised recommendation to buy or sell a financial instrument or any other investment or currency. This communication does not constitute investment research within the meaning of regulatory rules applicable in the European Economic Area, or research under the rules of the U.S. Self-Regulatory Organizations.</p>
  <p>This information is made solely for professional and institutional clients as defined by the Swiss Financial Services Act, as well as qualified investors according to the Swiss Collective Investment Schemes Act. It is not intended for retail clients or non-qualified investors and consequently cannot be transmitted to any third party.</p>
  <p>This communication is not directed to any person in any jurisdiction where, by reason of that person&rsquo;s nationality, residence or otherwise, its dissemination or use is prohibited. It cannot be quoted, reproduced, disclosed, distributed or otherwise referred to, in whole or in part, to any third party without the Bank&rsquo;s prior written consent.</p>
  <p>This communication may contain information on past performances of a financial product, all kinds of economic and financial valuations and analyses, as well as opinions of the Bank or of third parties. Any market valuations, terms and calculation methods, yields and opinions expressed are subject to change without notice. The information and opinions contained herein have been compiled and provided in good faith, based on information obtained from sources believed to be trustworthy. However, such information has not been independently verified. No guarantee, representation, or warranty of any kind, whether express or implied, is provided by the Bank or by relevant data vendors and other sources with respect to the accuracy, reliability, currentness or exhaustiveness of the information communicated, the methodology employed or the prices contained herein.</p>
  <p>Past performance is not a reliable indicator of current or future results. Any reference to the past performance of an investment does not guarantee its future performance. Fluctuations in exchange rates may adversely affect the value, price or income of any investment.</p>
  <p>Nothing in the present communication constitutes investment, legal, accounting or tax advice. This information is purely objective since it does not take into consideration the personal situation (including financial knowledge and experience), the investment objectives and risk profile of any recipient. Moreover, certain financial instruments mentioned (in particular, but not exclusively, derivatives, options and futures) involve a high risk of loss and may not be suitable. Accordingly, recipients should consult their own advisors on such matters, including but not limited to the possible tax consequences of investing in any financial product mentioned herein, and make their own assessment of the suitability of such investment product.</p>
  <p>Should a recipient make an investment on the basis of the present communication, the recipient alone shall bear the consequences thereof. In no event shall the Bank, its directors, employees, affiliates or agents be held responsible for damages of any kind arising out of the use of all or part of the information provided herein.</p>
</div>"""
