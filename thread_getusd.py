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

        price = 0	
        while True:

            urlTicker = "https://www.cryptonator.com/api/ticker/xmr-usd"

            try:
                tickerResponse = requests.post(urlTicker, headers={ "Accept": "application/json" })
            except:
                self.ui.setUSDPrice("N/A")
                print ("Error: Could not connect to the cryptonator API to get the XMR/USD price")
                break


            try:
                price = str(json.loads(tickerResponse.text)['ticker']['price'])
            except:
                self.ui.setUSDPrice("N/A")
                print ("Error: Could not set the price variable")
                print ("")
                break

            #self.ui.setUSDPrice(round(price,2))
            self.ui.setUSDPrice(round (float(price),2))
            self.sleep(1)