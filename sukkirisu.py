# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import urllib.parse
import urllib.request
import sys

url = 'http://www.ntv.co.jp/sukkiri/sukkirisu/index.html'

def lambda_handler(event, context):
    month = int(urllib.parse.parse_qs(event['body'])['text'][0].rstrip())
    result = get_sukkirisu(month)
    text = format_text(result)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            "response_type": "in_channel",
            "text": text
        })
    }

def format_text(result):
    return str(result["month"]) + "月: " + result["type"] \
            + (("(" + str(result["rank"]) + "位)") if 2 <= result["rank"] <= 11 else '') + "\n" \
            + result["description"] + "\n" \
            + "ラッキーカラー: " + result["lucky_color"]

def get_sukkirisu(month):
    if type(month) != int:
        raise TypeError("Month must be int.")

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        soup = BeautifulSoup(body, features="html.parser")
        data = soup.find(id=("month"+str(month)))
        if 'type1' in data['class']:
            rank = 1
            type_ = "超スッキリす"
        elif 'type4' in data['class']:
            rank = 12
            type_ = "ガッカリす"
        else:
            rank = int(data.find("p", class_="rankTxt").text.replace('位', ''))
            type_ = ''
            if 'type2' in data['class']:
                type_ = "スッキリす"
            elif 'type3' in data['class']:
                type_ = "まぁまぁスッキリす"
        return {
            'month': month,
            'rank': rank,
            'type': type_,
            'description': data.find("p", class_="").text,
            'lucky_color': data.find("div", id = "color").text
        }

if __name__ == '__main__':
    result = get_sukkirisu(int(sys.argv[1]))
    print(format_text(result))
