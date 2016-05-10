import polowrapper
import key
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QThread



class Thread(QThread):

    def __init__(self, ui_instance, PUBLIC_KEY, SECRET_KEY):
        self.ui = ui_instance
        self.PUBLIC_KEY = PUBLIC_KEY
        self.SECRET_KEY = SECRET_KEY
        super(QThread, self).__init__()

    def function():
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        
        

        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        
        
        while True:

            retBalances = poloInstance.returnBalances()
            retTicker = poloInstance.returnTicker()

            self.ui.setTaskWindowTitle(self.ui, retTicker['BTC_XMR']['last'])
            
            currentPriceXMR = retTicker['BTC_XMR']['last']
            lastPriceXMR = self.ui.lnPriceBTC.text()
            self.ui.setWindowTitle(retTicker['BTC_XMR']['last'])
            self.ui.setXMRPrice(retTicker['BTC_XMR']['last'])
            self.ui.setETHPrice(retTicker['BTC_ETH']['last'])
            self.ui.setHigh(retTicker['BTC_XMR']['high24hr'])
            self.ui.setLow(retTicker['BTC_XMR']['low24hr'])
            self.ui.setChange(str(round(float(retTicker['BTC_XMR']['percentChange'])*100,2)) + " %")

            self.ui.setLcdMonero(retBalances['XMR'])
            self.ui.setLcdBitcoin(retBalances['BTC'])
            self.ui.setLcdEthereum(retBalances['ETH'])

            retHistoryXMR = poloInstance.returnTradeHistory("BTC_XMR")
            retHistoryETH = poloInstance.returnTradeHistory("BTC_ETH")
            countHistoryXMR = len(retHistoryXMR)
            countHistoryETH = len(retHistoryETH)
            retOpenOrdersXMR = poloInstance.returnOpenOrders("BTC_XMR")
            retOpenOrdersETH = poloInstance.returnOpenOrders("BTC_ETH")
            print (retOpenOrdersXMR)

            countOpenOrdersXMR = len(retOpenOrdersXMR)
            countOpenOrdersETH = len(retOpenOrdersETH)


            countXMR = 0
            OOAmountXMR = 0

            for i in range(countOpenOrdersXMR):
                #if retOpenOrdersXMR[i]["type"] == "buy":
                OOAmountXMR = float(retOpenOrdersXMR[i]["amount"])
                print (OOAmountXMR)
                countXMR = countXMR + OOAmountXMR
                print (countXMR)
                

            XMRCompleteAmount = format(countXMR + float(retBalances['XMR']), '.8f')
            self.ui.setLcdMoneroinclIO(str(XMRCompleteAmount))
            
            countETH = 0
            OOAmountETH = 0
            for i in range(countOpenOrdersETH):
            	#if retOpenOrdersETH[i]["type"] == "buy":
                OOAmountETH = float(retOpenOrdersETH[i]["amount"])
                countETH = countETH + OOAmountETH

            ETHCompleteAmount = format(countETH + float(retBalances['ETH']), '.8f')

            self.ui.setLcdEthereuminclIO(str(ETHCompleteAmount))
            

            if countOpenOrdersXMR > self.ui.OpenOrdersWidget.rowCount():
               self.ui.OpenOrdersWidget.setRowCount(countHistoryXMR)
               print ("After setting rows Open Orders: " + str(self.ui.OpenOrdersWidget.rowCount()))
               self.sleep(1)
 
            if countOpenOrdersXMR != 0:
                self.ui.OpenOrdersWidget.clearContents()

                for i in range(countOpenOrdersXMR):
            
                    self.ui.OpenOrdersWidget.setItem(i,0, QTableWidgetItem(retOpenOrdersXMR[i]["orderNumber"]))
                    self.ui.OpenOrdersWidget.setItem(i,1, QTableWidgetItem(retOpenOrdersXMR[i]["type"]))
                    self.ui.OpenOrdersWidget.setItem(i,2, QTableWidgetItem(retOpenOrdersXMR[i]["rate"]))
                    self.ui.OpenOrdersWidget.setItem(i,3, QTableWidgetItem(retOpenOrdersXMR[i]["startingAmount"]))
                    self.ui.OpenOrdersWidget.setItem(i,4, QTableWidgetItem(retOpenOrdersXMR[i]["amount"]))
                    if retOpenOrdersXMR[i]["type"] == "sell":
                        self.ui.OpenOrdersWidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                        self.ui.OpenOrdersWidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                    else:
                        self.ui.OpenOrdersWidget.item(i, 1).setBackground(QtGui.QColor(10,189,82))

            print ("countHistoryXMR: " + str(countHistoryXMR))
            print ("rowcount: " + str(self.ui.HistoryWidget.rowCount()))

            if countHistoryXMR > self.ui.HistoryWidget.rowCount():
               self.ui.HistoryWidget.setRowCount(countHistoryXMR)
               print ("After setting rows History: " + str(self.ui.HistoryWidget.rowCount()))
               self.sleep(1)


            if countHistoryXMR != 0:
                self.ui.HistoryWidget.clearContents()

                for i in range(countHistoryXMR):

                    self.ui.HistoryWidget.setItem(i,0, QTableWidgetItem("XMR"))
                    self.ui.HistoryWidget.setItem(i,1, QTableWidgetItem(retHistoryXMR[i]["type"]))
                    self.ui.HistoryWidget.setItem(i,2, QTableWidgetItem(retHistoryXMR[i]["rate"]))
                    self.ui.HistoryWidget.setItem(i,3, QTableWidgetItem(retHistoryXMR[i]["amount"]))
                    self.ui.HistoryWidget.setItem(i,4, QTableWidgetItem(retHistoryXMR[i]["date"]))

                    if retHistoryXMR[i]["type"] == "sell":
                        self.ui.HistoryWidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                        self.ui.HistoryWidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                    else:
                        self.ui.HistoryWidget.item(i, 1).setBackground(QtGui.QColor(10,189,82))
            

            #read Input for trading for using in def calcSellBTCTotal and calcBuyXMRAmount
            self.SellreadBTCprice = self.ui.lnSellPrice.text()
            self.SellreadBTCprice = float(self.SellreadBTCprice)
            self.SellreadXMRAmount = self.ui.lnSellAmount.text()
            self.SellreadXMRAmount = float(self.SellreadXMRAmount)
            self.calcSellBTCTotal(self.SellreadBTCprice, self.SellreadXMRAmount)

            self.BuyreadBTCprice = self.ui.lnBuyPrice.text()
            self.BuyreadBTCprice = float(self.BuyreadBTCprice)
            
            self.BuyreadBTCTotal = self.ui.lnBuyTotal.text()
            
            try:
                self.BuyreadBTCTotal = float(self.BuyreadBTCTotal)
            except ValueError:
                continue
            self.calcBuyXMRAmount(self.BuyreadBTCprice, self.BuyreadBTCTotal)



            self.sleep (1)

    def cancelOrder(self):
        self.ui.OpenOrdersWidget.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        orderNumberXMR = self.ui.OpenOrdersWidget.currentItem().text()
        poloInstance.cancel("BTC_XMR", orderNumberXMR)



    def calcSellBTCTotal(self, sellreadbtcprice, sellreadxmramount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadxmramount = sellreadxmramount

        self.resultSellBTCTotal = self.sellreadbtcprice*self.sellreadxmramount
        self.ui.setSellBTCTotal(self.resultSellBTCTotal)


    def calcBuyXMRAmount(self, buyreadbtcprice, buyreadbtctotal):
        self.buyreadbtcprice = buyreadbtcprice
        self.buyreadbtctotal = buyreadbtctotal

        try:
            self.resultBuyXMRAmount = self.buyreadbtctotal/self.buyreadbtcprice
        except ZeroDivisionError:
            self.resultBuyXMRAmount = 0.0
            
        self.ui.setBuyXMRAmount(self.resultBuyXMRAmount)

    

    def clickBuy(self):
        self.ui.buyButton.clicked.connect(self.clickedBuy)
    def clickedBuy(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)       
        try:
            exeBuy = poloInstance.buy("BTC_XMR",self.BuyreadBTCprice,self.resultBuyXMRAmount)
            print ("Buy Order executed")
        except:
            print ("Buy Order not executed")

    

    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        try:
            exeSell = poloInstance.sell("BTC_XMR",self.SellreadBTCprice, self.SellreadXMRAmount)
            print ("Sell Order executed")
        except:
            print ("Sell Order not executed")      

    def clickSaveConfiguration(self):
        self.ui.saveButton.clicked.connect(self.clickedSaveConfiguration)
    def clickedSaveConfiguration(self):
        inputPublicKey = self.ui.lnPublicKey.text()
        inputSecretKey = self.ui.lnSecretKey.text()

        with open("key.py", "w") as keyfile:
            keyfile.write("PUBLIC_KEY = '" + inputPublicKey + "' \nSECRET_KEY = '" + inputSecretKey + "'")

    def clickSellGetBTCPrice(self):
        self.ui.btnSellGetBTCPrice.clicked.connect(self.clickedSellGetBTCPrice)
    def clickedSellGetBTCPrice(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        retTicker = poloInstance.returnTicker()
        self.ui.setSellBTCPrice(retTicker['BTC_XMR']['last'])

    def clickBuyGetBTCTotal(self):
        self.ui.btnBuyGetBTCTotal.clicked.connect(self.clickedBuyGetBTCTotal)
    def clickedBuyGetBTCTotal(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        retBalances = poloInstance.returnBalances()
        self.ui.setBuyBTCTotal(retBalances['BTC'])