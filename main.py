#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tushare as ts
import datetime
from mymail import send_mail, MailTable
from settings import tushare_token
from utils import get_stock_data_from_yaml
from apscheduler.schedulers.blocking import BlockingScheduler


def check(pro, stock, mt):
    now = datetime.datetime.now()
    end_date = now.strftime("%Y%m%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y%m%d")
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


def monitor_task():
    pro = ts.pro_api(tushare_token)
    monitor_stocks = get_stock_data_from_yaml("config.yaml")
    mt = MailTable()
    for stock in monitor_stocks:
        check(pro, stock, mt)
    if mt.html:
        send_mail(mt.get_html())


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(monitor_task, 'cron', day_of_week='mon-fri', hour=14, minute=30)
    scheduler.add_job(monitor_task, 'cron', day_of_week='mon-fri', hour=18)
    try:
        print("monitor start ...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
