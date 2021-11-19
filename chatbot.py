from flask import Flask, request
from requests import Session
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)
api_key = 'ENTER YOUR API KEY'
bot_token = 'ENTER YOUR BOT TOKEN'

headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

ticker_base = []
id_base = []

# '@' is decorator -> func containing func returning func
# flask creates server on desktop to access
@app.route('/sms', methods=['POST'])  

def bot():
    incoming_msg = request.form.get('Body').lower()
    response = MessagingResponse()
    print(incoming_msg)
    message = response.message()

    if "hello" in incoming_msg:
        reply = "Hello! \nWhich crypto would you like to view?"
        message.body(reply)
    
    if "hello" not in incoming_msg:
        match(incoming_msg)
        price = get_crypto_price(incoming_msg) 
        reply = str(price)
        message.body(reply)
    
    return str(response)

def match(incoming_msg):
    parameters = {
        'limit': 5000,
        'convert':'SGD',
        'sort_dir': 'asc'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data_dict = json.loads(response.text)['data']

    for ticker in data_dict:
        ticker_base.append(ticker['name'].lower())
        id_base.append(ticker['id'])
    # print(ticker_base)

    if incoming_msg in ticker_base:
        get_crypto_price(incoming_msg)
    
    return ticker_base, id_base

def get_crypto_price(incoming_msg):
    parameters = {
        'id': id_base[ticker_base.index(incoming_msg)],
        'convert':'SGD'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data_dict = json.loads(response.text)['data']

    values_view = data_dict.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)
    price = first_value['quote']['SGD']['price']
    return price

if __name__ == '__main__':
    app.run(debug=True)

