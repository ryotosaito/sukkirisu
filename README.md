# sukkirisu

![slack sample](images/slack_sample.png)
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
python src/sukkirisu.py 1 #sukkirisu search for January
```

## Slack slash command using AWS Lambda
### Preparation
```sh
git clone https://github.com/ryotosaito/sukkirisu.git
cd sukkirisu/src
pip3 install -r requirements.txt -t .
zip -r sukkirisu.zip *
```

### In your AWS console: Lambda
#### Designer

![setting sample](images/aws_apigateway.png)

- Click `+ Add triger`
- Select `API Gateway`
- Settings
 - API: Create a new API
 - Security: Open
 - Additional Settings: None
- Click `Add`
 - Redirects to Designer pane
- Click `API Gateway`
- Scroll Down
- Note down `API endpoint` URL in the API Gateway pane

#### Function Code

![setting sample](images/aws_lambda.png)

- Code entry type: Upload a .zip file (upload sukkirisu.zip created before)
- Runtime: Python 3.x
- Handler: `sukkirisu.lambda_handler`

### In your Slack API console

![Slash Commands window](images/slack_slashlist.png)
![setting sample](images/slack_settings.png)
- Click `Create New Command` in Slash Commands
- Settings
 - Command: /sukkirisu
 - Request URL: *noted API endpoint URL*
 - Short Description: Today's sukkirisu
 - Usage Hint: &lt;month in int&gt;
