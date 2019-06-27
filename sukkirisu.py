# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
import urllib.request

url = 'http://www.ntv.co.jp/sukkiri/sukkirisu/index.html'

month = sys.argv[1]

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as res:
    body = res.read()
    soup = BeautifulSoup(body, features="html.parser")
    data = soup.find(id=("month"+str(month)))
    if 'type1' in data['class']:
        rank = "超スッキリす"
    elif 'type4' in data['class']:
        rank = "ガッカリす"
    else:
        rank = data.find("p", class_="rankTxt").text
    print(rank + ": " + data.find("p", class_="").text + "\tラッキーカラー: " + data.find("div", id = "color").text)
