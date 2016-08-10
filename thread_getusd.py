import requests
import json
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import polowrapper
import key
from requests.exceptions import ConnectionError
import logging
import socket

import urllib.request
import urllib


class Thread(QThread):

    def __init__(self, ui_instance):
        self.ui = ui_instance
        super(QThread, self).__init__()

    def function():
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):

        
        XMRUSDPRICE = 0 
        ETHUSDPRICE = 0
        BTCUSDPRICE = 0
        CRYPWEB = "https://www.cryptonator.com"
        XMRUSD = "https://www.cryptonator.com/api/ticker/xmr-usd"
        ETHUSD = "https://www.cryptonator.com/api/ticker/eth-usd" 
        BTCUSD = "https://www.cryptonator.com/api/ticker/btc-usd"
        while True:
                 
            try:

                urllib.request.urlopen(CRYPWEB, timeout=1)
                TICKERRESPXMRUSD = requests.post(XMRUSD, headers={ "Accept": "application/json" })
                TICKERRESPETHUSD = requests.post(ETHUSD, headers={ "Accept": "application/json" })
                TICKERRESPBTCUSD = requests.post(BTCUSD, headers={ "Accept": "application/json" })
               
                XMRUSDPRICE = str(json.loads(TICKERRESPXMRUSD.text)['ticker']['price'])
                ETHUSDPRICE = str(json.loads(TICKERRESPETHUSD.text)['ticker']['price'])
                BTCUSDPRICE = str(json.loads(TICKERRESPBTCUSD.text)['ticker']['price'])


                self.ui.setXMRUSDPrice(round (float(XMRUSDPRICE),2))
                self.ui.setETHUSDPrice(round (float(ETHUSDPRICE),2))
                self.ui.setBTCUSDPrice(round (float(BTCUSDPRICE),2))
             
                self.ui.setCryptonatorStatus("Connected")

            except Exception as e:
                self.ui.setXMRUSDPrice("N/A")
                self.ui.setETHUSDPrice("N/A")
                self.ui.setBTCUSDPrice("N/A")
                self.ui.setCryptonatorStatus("Disconnected")
                #logging.debug("ERROR: thread_getusd: " + str(e))
                continue




