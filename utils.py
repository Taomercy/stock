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
