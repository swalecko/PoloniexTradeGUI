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
        
        while True:      
            try:
                self.getPoloInfo()
                self.ui.setPoloniexStatus("Connected")
                self.setXMRPriceInfo()
                self.setETHPriceInfo()
                self.setUSDPriceInfo()

            except (ConnectionError, TimeoutError) as e:
                logging.debug("ERROR: thread_getcrypto Loop Exception Connection: " + str(e))
                self.ui.setPoloniexStatus("Disconnected")
                self.ui.setXMRPrice("")
                self.ui.setHigh("")
                self.ui.setLow("")
                self.ui.setChange("")
                self.ui.setETHPrice("")
                self.ui.setETHHigh("")
                self.ui.setETHLow("")
                self.ui.setETHChange("")
                self.sleep(2)
                continue
            except Exception as e:
                self.ui.setXMRPrice("")
                self.ui.setHigh("")
                self.ui.setLow("")
                self.ui.setChange("")
                self.ui.setETHPrice("")
                self.ui.setETHHigh("")
                self.ui.setETHLow("")
                self.ui.setETHChange("")
                logging.debug("ERROR: thread_getcrypto: Could not set prices: " + str(e))
                continue

    def setXMRPriceInfo(self):
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
        self.ui.setETHPrice(self.lastETH)
        self.sleep(0.5)
        self.ui.setETHHigh(self.highETH)
        self.sleep(1)
        self.ui.setETHLow(self.lowETH)
        self.sleep(0.5)
        self.ui.setETHChange(str(round(float(self.changeETH)*100,2)) + " %")

    def setUSDPriceInfo(self):
        self.ui.setXMRUSDPrice(round (float(self.lastUSDXMR),2))
        self.sleep(0.5)
        self.ui.setETHUSDPrice(round (float(self.lastUSDETH),2))
        self.sleep(0.5)
        self.ui.setBTCUSDPrice(round (float(self.lastUSDBTC),2))


    def getPoloInfo(self):
        self.poloInstance = polowrapper.poloniex(key.PUBLIC_KEY, key.SECRET_KEY)

        self.retTicker = self.poloInstance.returnTicker()

        self.tickerXMR = self.retTicker['BTC_XMR']
        self.tickerETH = self.retTicker['BTC_ETH']
        self.tickerUSDXMR = self.retTicker['USDT_XMR']
        self.tickerUSDETH = self.retTicker['USDT_ETH']
        self.tickerUSDBTC = self.retTicker['USDT_BTC']
        self.lastXMR = self.tickerXMR['last']
        self.highXMR = self.tickerXMR['high24hr']
        self.lowXMR = self.tickerXMR['low24hr']
        self.changeXMR = self.tickerXMR['percentChange']
        self.lastETH = self.tickerETH['last']
        self.highETH = self.tickerETH['high24hr']
        self.lowETH = self.tickerETH['low24hr']
        self.changeETH = self.tickerETH['percentChange']
        self.lastUSDXMR = self.tickerUSDXMR['last']
        self.lastUSDETH = self.tickerUSDETH['last']       
        self.lastUSDBTC = self.tickerUSDBTC['last']




