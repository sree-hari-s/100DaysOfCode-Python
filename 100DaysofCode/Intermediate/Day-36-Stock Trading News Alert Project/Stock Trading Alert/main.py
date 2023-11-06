import os
import requests
from dotenv import load_dotenv
import datetime as dt
from twilio.rest import Client

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params={
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": os.environ["STOCK_API_KEY"],
    }
response = requests.get(STOCK_ENDPOINT,params=stock_params)
stock_data = response.json()["Time Series (Daily)"]

stock_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_list[1]
print(yesterday_data)
yesterday_closing_price = float(yesterday_data['4. close'])

day_before_yesterday_data = stock_list[2]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])
print(yesterday_closing_price)
print(day_before_yesterday_closing_price)

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = round((difference/yesterday_closing_price)*100)

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if diff_percent > 5:
    news_params = {
        "apiKey": os.environ['NEWS_API_KEY'],
        "qInTitle": COMPANY_NAME,        
    }
    print("Get News")
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()['articles']
    top3_articles = articles[:3]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.
    formatted_article =[f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in top3_articles]
    print(formatted_article)

    client = Client(os.environ["account_sid"], os.environ["auth_token"])
    for article in formatted_article:
        message = client.messages.create(
                body=article,
                from_= os.environ['from_phone'],
                to=os.environ['to_phone']
            )
        print(message.status)   

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
