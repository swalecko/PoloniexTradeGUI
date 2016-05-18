import requests
import json
from PyQt5.QtCore import QThread

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
        while True:

            XMRUSD = "https://www.cryptonator.com/api/ticker/xmr-usd"
            ETHUSD = "https://www.cryptonator.com/api/ticker/eth-usd"

            try:
                TICKERRESPXMRUSD = requests.post(XMRUSD, headers={ "Accept": "application/json" })
                TICKERRESPETHUSD = requests.post(ETHUSD, headers={ "Accept": "application/json" })
            except:
                self.ui.setXMRUSDPrice("N/A")
                self.ui.setETHUSDPrice("N/A")
                print ("Error: Could not connect to the cryptonator API to get the USD price")
                break

            try:
                XMRUSDPRICE = str(json.loads(TICKERRESPXMRUSD.text)['ticker']['price'])
                ETHUSDPRICE = str(json.loads(TICKERRESPETHUSD.text)['ticker']['price'])
            except:
                self.ui.setXMRUSDPrice("N/A")
                self.ui.setETHUSDPrice("N/A")
                print ("Error: Could not set the price variable")
                print ("")
                break

            #self.ui.setUSDPrice(round(price,2))
            self.ui.setXMRUSDPrice(round (float(XMRUSDPRICE),2))
            self.ui.setETHUSDPrice(round (float(ETHUSDPRICE),2))
            self.sleep(1)