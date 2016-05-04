import json
import time
import random
import datetime
import time
import logging
import smtplib
import sys
import requests


def getUSDPrice():

    urlTicker = "https://www.cryptonator.com/api/ticker/xmr-usd"

    try:
        tickerResponse = requests.post(urlTicker, headers={ "Accept": "application/json" })
    except:
        print ("")
        print ("Error: Could not connect to the cryptonator API to get the XMR/USD price")


    try:
        price = str(json.loads(tickerResponse.text)['ticker']['price'])
    except:
        price = ("N/A")
        print ("Error: Could not set the price variable")
        print ("")


    return (price)

