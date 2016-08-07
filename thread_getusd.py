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
        XMRUSD = "https://www.cryptonator.com/api/ticker/xmr-usd"
        ETHUSD = "https://www.cryptonator.com/api/ticker/eth-usd" 
        BTCUSD = "https://www.cryptonator.com/api/ticker/btc-usd"
        while True:
                 
            try:

                TICKERRESPXMRUSD = requests.post(XMRUSD, headers={ "Accept": "application/json" })
                TICKERRESPETHUSD = requests.post(ETHUSD, headers={ "Accept": "application/json" })
                TICKERRESPBTCUSD = requests.post(BTCUSD, headers={ "Accept": "application/json" })
               
                XMRUSDPRICE = str(json.loads(TICKERRESPXMRUSD.text)['ticker']['price'])
                ETHUSDPRICE = str(json.loads(TICKERRESPETHUSD.text)['ticker']['price'])
                BTCUSDPRICE = str(json.loads(TICKERRESPBTCUSD.text)['ticker']['price'])


                self.ui.setXMRUSDPrice(round (float(XMRUSDPRICE),2))
                self.ui.setETHUSDPrice(round (float(ETHUSDPRICE),2))
                self.ui.setBTCUSDPrice(round (float(BTCUSDPRICE),2))
             
            


            except (ConnectionError, TimeoutError) as e:
                logging.debug("ERROR: thread_getusd Loop Exception Connection: " + str(e))
                self.ui.setNetworkStatus("Warning")
                self.ui.setXMRUSDPrice("N/A")
                self.ui.setETHUSDPrice("N/A")
                self.ui.setBTCUSDPrice("N/A")
                self.sleep(2)
                continue
            except Exception as e:
                self.ui.setXMRUSDPrice("N/A")
                self.ui.setETHUSDPrice("N/A")
                self.ui.setBTCUSDPrice("N/A")
                logging.debug("ERROR: thread_getusd: Could not set prices: " + str(e))
                continue




