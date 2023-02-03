#!/usr/bin/env python
# -*- coding:utf-8 -*-
import yaml

def get_stock_data_from_yaml(filename):
    stocks = []
    with open(filename, 'r', encoding='utf-8') as fr:
        data = fr.read()
        result = yaml.load(data, Loader=yaml.FullLoader)
        result = result['monitor_stocks']
        for stock in result:
            monitor = stock.get("monitor", None)
            if monitor and monitor == "false":
                continue
            stocks.append(stock)

    return stocks


class MailTable(object):
    html = None
    table_head = None
    td_head = None

    def __init__(self):
        self.table_head = "<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=756 style='width:567.0pt;margin-left:-.65pt;border-collapse:collapse'>"
        self.td_head = """
                    <td width=64 nowrap valign=bottom style='width:48.0pt;border:solid windowtext 1.0pt;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>股票名称<o:p></o:p></span></b></p></td>
                    <td width=96 valign=bottom style='width:1.0in;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>今日涨跌幅<o:p></o:p></span></b></p></td>
                    <td width=119 nowrap valign=bottom style='width:89.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>5日涨跌幅<o:p></o:p></span></b></p></td>
        """
        self.html = "<p>Hi,</p><p>检测到今日以下股票涨跌幅大于5%, 或者5日累计涨跌大于10%"
        self.html += self.table_head
        self.html += self.td_head

    def add_tr(self, stock_name, today_pct_chg, day5_pct_chg):
        td = """
                    <td width=64 nowrap style='width:48.0pt;border:solid windowtext 1.0pt;border-top:none;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>{}<o:p></o:p></span></p></td>
                    <td width=96 nowrap style='width:1.0in;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{}<o:p></o:p></span></p></td>
                    <td width=119 nowrap style='width:89.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun'>{}</span><span style='font-size:10.0pt;font-family:SimSun'><o:p></o:p></span></p></td>
        """.format(stock_name, str(today_pct_chg) + "%", str(day5_pct_chg) + "%")
        tr = "<tr style='height:15.0pt'>" + td + "</tr>"
        self.html += tr

    def get_html(self):
        self.html += '</table>'
        return self.html


def check(stock, mt):
    df = pro.daily(ts_code=stock["code"], start_date=start_date, end_date=end_date)
    # print(df[["ts_code", "trade_date", "pre_close", "pct_chg"]])
    today_pct_chg = df["pct_chg"][0]
    print("股票名称：", stock["name"])
    print("今日涨跌幅：", df["pct_chg"][0])
    print("5日涨跌幅:", sum(df["pct_chg"][:5]))
    if abs(today_pct_chg) > 5:
        print("今日涨跌幅大于5%， 发送邮件")
        mt.add_tr(stock["name"], df["pct_chg"][0], sum(df["pct_chg"][:5]))
    print("============================")
