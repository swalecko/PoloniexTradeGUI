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

            self.ui.setETHPrice(retTicker['BTC_ETH']['last'])
            self.ui.setLcdEthereum(retBalances['ETH'])

 
            retHistoryETH = poloInstance.returnTradeHistory("BTC_ETH")
            countHistoryETH = len(retHistoryETH)
            retOpenOrdersETH = poloInstance.returnOpenOrders("BTC_ETH")



            countOpenOrdersETH = len(retOpenOrdersETH)


            countETH = 0
            OOAmountETH = 0

            for i in range(countOpenOrdersETH):
                #if retOpenOrdersETH[i]["type"] == "buy":
                OOAmountETH = float(retOpenOrdersETH[i]["amount"])
                print (OOAmountETH)
                countETH = countETH + OOAmountETH
                print (countETH)
                

            ETHCompleteAmount = format(countETH + float(retBalances['ETH']), '.8f')
            self.ui.setLcdMoneroinclIO(str(ETHCompleteAmount))
            
            countETH = 0
            OOAmountETH = 0
            for i in range(countOpenOrdersETH):
            	#if retOpenOrdersETH[i]["type"] == "buy":
                OOAmountETH = float(retOpenOrdersETH[i]["amount"])
                countETH = countETH + OOAmountETH

            ETHCompleteAmount = format(countETH + float(retBalances['ETH']), '.8f')

            self.ui.setLcdEthereuminclIO(str(ETHCompleteAmount))
            

            if countOpenOrdersETH > self.ui.OpenOrdersWidgetETH.rowCount():
               self.ui.OpenOrdersWidgetETH.setRowCount(countOpenOrdersETH)
               print ("After setting rows Open Orders: " + str(self.ui.OpenOrdersWidgetETH.rowCount()))
               self.sleep(1)
 
            if countOpenOrdersETH != 0:
                self.ui.OpenOrdersWidgetETH.clearContents()

                for i in range(countOpenOrdersETH):
            
                    self.ui.OpenOrdersWidgetETH.setItem(i,0, QTableWidgetItem(retOpenOrdersETH[i]["orderNumber"]))
                    self.ui.OpenOrdersWidgetETH.setItem(i,1, QTableWidgetItem(retOpenOrdersETH[i]["type"]))
                    self.ui.OpenOrdersWidgetETH.setItem(i,2, QTableWidgetItem(retOpenOrdersETH[i]["rate"]))
                    self.ui.OpenOrdersWidgetETH.setItem(i,3, QTableWidgetItem(retOpenOrdersETH[i]["startingAmount"]))
                    self.ui.OpenOrdersWidgetETH.setItem(i,4, QTableWidgetItem(retOpenOrdersETH[i]["amount"]))
                    if retOpenOrdersETH[i]["type"] == "sell":
                        self.ui.OpenOrdersWidgetETH.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                        self.ui.OpenOrdersWidgetETH.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                    else:
                        self.ui.OpenOrdersWidgetETH.item(i, 1).setBackground(QtGui.QColor(10,189,82))

            print ("countHistoryETH: " + str(countHistoryETH))
            print ("rowcount: " + str(self.ui.HistoryWidgetETH.rowCount()))

            if countHistoryETH > self.ui.HistoryWidgetETH.rowCount():
               self.ui.HistoryWidgetETH.setRowCount(countHistoryETH)
               print ("After setting rows History: " + str(self.ui.HistoryWidgetETH.rowCount()))
               self.sleep(1)


            if countHistoryETH != 0:
                self.ui.HistoryWidgetETH.clearContents()

                for i in range(countHistoryETH):

                    self.ui.HistoryWidgetETH.setItem(i,0, QTableWidgetItem("ETH"))
                    self.ui.HistoryWidgetETH.setItem(i,1, QTableWidgetItem(retHistoryETH[i]["type"]))
                    self.ui.HistoryWidgetETH.setItem(i,2, QTableWidgetItem(retHistoryETH[i]["rate"]))
                    self.ui.HistoryWidgetETH.setItem(i,3, QTableWidgetItem(retHistoryETH[i]["amount"]))
                    self.ui.HistoryWidgetETH.setItem(i,4, QTableWidgetItem(retHistoryETH[i]["date"]))

                    if retHistoryETH[i]["type"] == "sell":
                        self.ui.HistoryWidgetETH.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                        self.ui.HistoryWidgetETH.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                    else:
                        self.ui.HistoryWidgetETH.item(i, 1).setBackground(QtGui.QColor(10,189,82))
            

            #read Input for trading for using in def calcSellBTCTotal and calcBuyETHAmount
            self.SellreadBTCprice = self.ui.lnETHSellPrice.text()
            self.SellreadBTCprice = float(self.SellreadBTCprice)
            self.SellreadETHAmount = self.ui.lnETHSellAmount.text()
            self.SellreadETHAmount = float(self.SellreadETHAmount)
            self.calcSellBTCTotal(self.SellreadBTCprice, self.SellreadETHAmount)

            self.BuyreadBTCprice = self.ui.lnETHBuyPrice.text()
            self.BuyreadBTCprice = float(self.BuyreadBTCprice)
            
            self.BuyreadBTCTotal = self.ui.lnETHBuyTotal.text()
            
            try:
                self.BuyreadBTCTotal = float(self.BuyreadBTCTotal)
            except ValueError:
                continue
            self.calcBuyETHAmount(self.BuyreadBTCprice, self.BuyreadBTCTotal)



            self.sleep (1)

    




    def cancelOrder(self):
        self.ui.OpenOrdersWidgetETH.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        orderNumberETH = self.ui.OpenOrdersWidgetETH.currentItem().text()
        poloInstance.cancel("BTC_ETH", orderNumberETH)



    def calcSellBTCTotal(self, sellreadbtcprice, sellreadETHamount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadETHamount = sellreadETHamount

        self.resultSellBTCTotal = self.sellreadbtcprice*self.sellreadETHamount
        self.ui.setETHSellBTCTotal(self.resultSellBTCTotal)


    def calcBuyETHAmount(self, buyreadbtcprice, buyreadbtctotal):
        self.buyreadbtcprice = buyreadbtcprice
        self.buyreadbtctotal = buyreadbtctotal

        try:
            self.resultBuyETHAmount = self.buyreadbtctotal/self.buyreadbtcprice
        except ZeroDivisionError:
            self.resultBuyETHAmount = 0.0
            
        self.ui.setBuyETHAmount(self.resultBuyETHAmount)

    

    def clickBuy(self):
        self.ui.buyETHButton.clicked.connect(self.clickedBuy)
    def clickedBuy(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)       
        try:
            exeBuy = poloInstance.buy("BTC_ETH",self.BuyreadBTCprice,self.resultBuyETHAmount)
            print ("Buy Order executed")
        except:
            print ("Buy Order not executed")

    

    def clickSell(self):
        self.ui.sellETHButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        try:
            exeSell = poloInstance.sell("BTC_ETH",self.SellreadBTCprice, self.SellreadETHAmount)
            print ("Sell Order executed")
        except:
            print ("Sell Order not executed")      



    def clickSellGetBTCPrice(self):
        self.ui.btnETHSellGetBTCPrice.clicked.connect(self.clickedSellGetBTCPrice)
    def clickedSellGetBTCPrice(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        retTicker = poloInstance.returnTicker()
        self.ui.setETHSellBTCPrice(retTicker['BTC_ETH']['last'])

    def clickBuyGetBTCTotal(self):
        self.ui.btnETHBuyGetBTCTotal.clicked.connect(self.clickedBuyGetBTCTotal)
    def clickedBuyGetBTCTotal(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        retBalances = poloInstance.returnBalances()
        self.ui.setETHBuyBTCTotal(retBalances['BTC'])