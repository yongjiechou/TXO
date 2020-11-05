# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

TXF_NAME = u'臺指現貨'
TE_NAME = u'電子現貨'
TF_NAME = u'金融現貨'

targets = set()
targets.add(TXF_NAME)
##targets.add(TE_NAME)
##targets.add(TF_NAME)

quotes = dict()

url = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx'


class Quote(object):

    def __init__(self):
        self.name = None
        self.trade_time = None
        self.trade_price = None
        self.change = None
        self.open = None
        self.high = None
        self.low = None

    def __str__(self):
        res = list()

        res.append(self.name)
        res.append(self.trade_time.strftime("%H:%M:%S"))
        res.append(self.trade_price)
        res.append(self.change)
        res.append(self.open)
        res.append(self.high)
        res.append(self.low)
        return str(res)

while True:

    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。

    html_data = requests.get(url)
    soup = BeautifulSoup(html_data.content, 'html.parser')

    rows = soup.find_all('tr', {"class": "custDataGridRow", "bgcolor": "White"})

    for row in rows:
        # print(row)

        items = row.find_all('td')
        name = items[0].a.text.strip()
        if name in targets:
            quote = Quote()
            quote.name = name
            quote.trade_price = float(items[6].font.text.replace(',', ''))
            quote.change = float(items[7].font.text)
            quote.trade_time = datetime.strptime(items[14].font.text, "%H:%M:%S")
            quote.open = float(items[10].font.text.replace(',', ''))
            quote.high = float(items[11].font.text.replace(',', ''))
            quote.low = float(items[12].font.text.replace(',', ''))

            quotes[name] = quote
            print(quote)

    # 根據取得的報價判斷條件，條件自訂。

    # 條件符合時通知使用者，如何通知？

    time.sleep(60)