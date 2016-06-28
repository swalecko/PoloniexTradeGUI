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
               
                
                try:
                    TICKERRESPXMRUSD = requests.post(XMRUSD, headers={ "Accept": "application/json" })
                    TICKERRESPETHUSD = requests.post(ETHUSD, headers={ "Accept": "application/json" })
                    TICKERRESPBTCUSD = requests.post(BTCUSD, headers={ "Accept": "application/json" })
                except ConnectionError as a:
                    self.ui.setXMRUSDPrice("N/A")
                    self.ui.setETHUSDPrice("N/A")
                    self.ui.setBTCUSDPrice("N/A")
                    
                    self.ui.setLog(logging.debug("ERROR: Connection GETUSD: " + str(a)))
                    self.ui.setNetworkStatus("ERROR")
                    self.sleep(1)
                    continue

                try:
                    XMRUSDPRICE = str(json.loads(TICKERRESPXMRUSD.text)['ticker']['price'])
                    ETHUSDPRICE = str(json.loads(TICKERRESPETHUSD.text)['ticker']['price'])
                    BTCUSDPRICE = str(json.loads(TICKERRESPBTCUSD.text)['ticker']['price'])

                except:
                    self.ui.setXMRUSDPrice("N/A")
                    self.ui.setETHUSDPrice("N/A")
                    self.ui.setBTCUSDPrice("N/A")
                    logging.debug("Error: Could not set the price variable")
                    continue

                
                self.ui.setXMRUSDPrice(round (float(XMRUSDPRICE),2))
                self.ui.setETHUSDPrice(round (float(ETHUSDPRICE),2))
                self.sleep(0.5)
                self.ui.setBTCUSDPrice(round (float(BTCUSDPRICE),2))


                self.getPoloInfo()
                self.setXMRPriceInfo()
                self.setETHPriceInfo()
                self.sleep (1)


            except (ConnectionError, TimeoutError) as e:
                self.ui.setLog(logging.debug("ERROR: thread_getusd Loop Exception Connection: " + str(e)))
                self.ui.setNetworkStatus("ERROR")
                self.sleep(2)
                continue
            except Exception as e:
                logging.debug("ERROR: thread_getusd Loop Exception: " + str(e))
                self.sleep(2)

    def setXMRPriceInfo(self):
        self.sleep(1)
        self.ui.setWindowTitle(self.lastXMR)
        self.sleep(0.5)
        self.ui.setXMRPrice(self.lastXMR)
        self.sleep(1)
        self.ui.setHigh(self.highXMR)
        self.sleep(0.5)
        self.ui.setLow(self.lowXMR)
        self.sleep(1)
        self.ui.setChange(str(round(float(self.changeXMR)*100,2)) + " %")



    def setETHPriceInfo(self):
        self.sleep(1) 
        self.ui.setETHPrice(self.lastETH)
        self.sleep(0.5)
        self.ui.setETHHigh(self.highETH)
        self.sleep(1)
        self.ui.setETHLow(self.lowETH)
        self.sleep(0.5)
        self.ui.setETHChange(str(round(float(self.changeETH)*100,2)) + " %")

       
    def getPoloInfo(self):
        self.poloInstance = polowrapper.poloniex(key.PUBLIC_KEY, key.SECRET_KEY)


        self.retTicker = self.poloInstance.returnTicker()

        self.tickerXMR = self.retTicker['BTC_XMR']
        self.tickerETH = self.retTicker['BTC_ETH']
        self.lastXMR = self.tickerXMR['last']
        self.highXMR = self.tickerXMR['high24hr']
        self.lowXMR = self.tickerXMR['low24hr']
        self.changeXMR = self.tickerXMR['percentChange']
        self.lastETH = self.tickerETH['last']
        self.highETH = self.tickerETH['high24hr']
        self.lowETH = self.tickerETH['low24hr']
        self.changeETH = self.tickerETH['percentChange']


