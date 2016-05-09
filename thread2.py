import requests
import json
from PyQt5.QtCore import QThread

class Thread2(QThread):

    def __init__(self, ui_instance):
        self.ui = ui_instance
        super(QThread, self).__init__()

    def function():
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):

        while True:

            urlTicker = "https://www.cryptonator.com/api/ticker/xmr-usd"

            try:
                tickerResponse = requests.post(urlTicker, headers={ "Accept": "application/json" })
            except:
                print ("")
                print ("Error: Could not connect to the cryptonator API to get the XMR/USD price")


            try:
                price = str(json.loads(tickerResponse.text)['ticker']['price'])
            except:
                self.ui.setUSDPrice("N/A")
                print ("Error: Could not set the price variable")
                print ("")

            self.ui.setUSDPrice(price)

            self.sleep(1)