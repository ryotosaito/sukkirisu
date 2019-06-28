# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import urllib.parse
import urllib.request
import sys

url = 'http://www.ntv.co.jp/sukkiri/sukkirisu/index.html'

def lambda_handler(event, context):
    month = urllib.parse.parse_qs(event['body'])['text'][0].rstrip()
    result = get_sukkirisu(month)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            "response_type": "in_channel",
            "text": get_sukkirisu
        })
    }

def get_sukkirisu(month):
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
        return rank + ": " + data.find("p", class_="").text + "\tラッキーカラー: " + data.find("div", id = "color").text

if __name__ == '__main__':
    print(get_sukkirisu(sys.argv[1]))
