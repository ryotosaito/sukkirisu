# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import urllib.parse
import urllib.request
import re
import sys

url = 'http://www.ntv.co.jp/sukkiri/sukkirisu/index.html'

def lambda_handler(event, context):
    birth_month = int(urllib.parse.parse_qs(event['body'])['text'][0].rstrip())
    result = get_sukkirisu(birth_month)
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
    return "{}月: {}\n{}\nラッキーカラー: {}\n(更新日: {})".format(
                result["birth_month"],
                result["type"] + (("(" + str(result["rank"]) + "位)") if 2 <= result["rank"] <= 11 else ''),
                result["description"],
                result["lucky_color"],
                "/".join(result["modified_date"])
            )

# argument:
#   birth_month: month number you want to search sukkirisu result
# return:
#   dict: {
#       birth_month: int: argument
#       modified_date: list: [month, date of month]
#       rank: int: sukkirisu rank
#       type: str: "超スッキリす" or "スッキリす" or "まぁまぁスッキリす" or "ガッカリす"
#       description: str: fortune description
#       lucky_color: str: lucky color
#   }
def get_sukkirisu(birth_month):
    if type(birth_month) != int:
        raise TypeError("birth_month must be int.")

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        soup = BeautifulSoup(body, features="html.parser")
        data = soup.find(id=("month"+str(birth_month)))
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
            'birth_month': birth_month,
            'modified_date': re.findall(r"\d+", soup.find("span", class_="date").text),
            'rank': rank,
            'type': type_,
            'description': data.find("p", class_="").text,
            'lucky_color': data.find("div", id="color").text
        }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("argument error: {} <month in int>\n".format(sys.argv[0]))
        sys.exit(1)
    result = get_sukkirisu(int(sys.argv[1]))
    print(format_text(result))
