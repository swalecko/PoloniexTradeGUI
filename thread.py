import polowrapper
import key
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QThread
import xmrusd


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


            self.ui.setCurrency("XMR_BTC")
            self.ui.setPrice(retTicker['BTC_XMR']['last'])
            self.ui.setHigh(retTicker['BTC_XMR']['high24hr'])
            self.ui.setLow(retTicker['BTC_XMR']['low24hr'])
            self.ui.setChange(str(round(float(retTicker['BTC_XMR']['percentChange'])*100,2)) + " %")
            
            xmr = retBalances['XMR']
            btc = retBalances['BTC']
            eth = retBalances['ETH']
            self.ui.setLcdMonero(xmr)
            self.ui.setLcdBitcoin(btc)
            self.ui.setLcdEthereum(eth)
            print ("Balance: " + str(xmr))
            print ("Balance: " + str(btc))
            print ("Balance: " +  str(eth))
         
            retHistoryXMR = poloInstance.returnTradeHistory("BTC_XMR")
            retHistoryETH = poloInstance.returnTradeHistory("BTC_ETH")
            countHistoryXMR = len(retHistoryXMR)
            countHistoryETH = len(retHistoryETH)
            retOpenOrdersXMR = poloInstance.returnOpenOrders("BTC_XMR")
            retOpenOrdersETH = poloInstance.returnOpenOrders("BTC_ETH")
            print (retOpenOrdersXMR)
            print (retOpenOrdersETH)
            countOpenOrdersXMR = len(retOpenOrdersXMR)
            countOpenOrdersETH = len(retOpenOrdersETH)

            print ("HistoryXMR " + str(countHistoryXMR))
            print ("HistoryETH " + str(countHistoryETH))

            countXMR = 0
            OOAmountXMR = 0

            for i in range(countOpenOrdersXMR):
                OOAmountXMR = float(retOpenOrdersXMR[i]["amount"])
                countXMR =+ OOAmountXMR 
            XMRCompleteAmount = countXMR + float(xmr)
            self.ui.setLcdMoneroinclIO(str(XMRCompleteAmount))
            
            countETH = 0
            OOAmountETH = 0
            for i in range(countOpenOrdersETH):
            	OOAmountETH = float(retOpenOrdersETH[i]["amount"])
            	print ("OOAmountETH: " + str(OOAmountETH))
            	countETH =+ OOAmountETH
            	print ("countETH: " + str(countETH))
            ETHCompleteAmount = format(countETH + float(eth), '.8f')
            print (ETHCompleteAmount)
            self.ui.setLcdEthereuminclIO(str(ETHCompleteAmount))
                        
            


            print ("Open Orders: " + str(countOpenOrdersXMR))
            self.ui.OpenOrdersWidget.clearContents()
            self.ui.HistoryWidget.clearContents()
           
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

            print ("Count History XMR: " + str(countHistoryXMR))
            if countHistoryXMR != 0:

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

        print ("cell double clicked" + orderNumberXMR)

    def calcSellBTCTotal(self, sellreadbtcprice, sellreadxmramount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadxmramount = sellreadxmramount

        print (self.sellreadbtcprice)
        print (self.sellreadxmramount)
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

    
        print (inputPublicKey)
        print (inputSecretKey)