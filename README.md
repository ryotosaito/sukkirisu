# sukkirisu
Today's sukkirisu (スッキリす, www.ntv.co.jp/sukkiri/sukkirisu/index.html) reporter

## Command line
### Installation
```sh
git clone https://github.com/ryotosaito/sukkirisu.git
cd sukkirisu
python3 -m venv .
. bin/activate
pip install -r requirements.txt
```

### Usage
```sh
python sukkirisu.py 1 #sukkirisu search for January
```

## Slack slash command using AWS Lambda
### Preparation
```sh
git clone https://github.com/ryotosaito/sukkirisu.git
cd sukkirisu
pip3 install -r requirements.txt -t .
zip -r sukkirisu.zip *
```
