import polowrapper
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


if not os.path.exists("key.py") or os.stat("key.py").st_size == 0:
    with open("key.py", "w") as keyfile:
            keyfile.write("PUBLIC_KEY = ''\nSECRET_KEY = ''")
            keyfile.close()
import key

class Thread(QThread):
    def __init__(self, ui_instance, PUBLIC_KEY, SECRET_KEY):
        self.ui = ui_instance
        self.PUBLIC_KEY = PUBLIC_KEY
        self.SECRET_KEY = SECRET_KEY
        super(QThread, self).__init__()
        self.poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        
    def function():
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        z = 0 
        while True:
            try:
                self.retBalances = self.poloInstance.returnBalances()
                retTicker = self.poloInstance.returnTicker()

                self.ui.setTaskWindowTitle(self.ui, retTicker['BTC_XMR']['last'])
                
                currentPriceXMR = retTicker['BTC_XMR']['last']
                lastPriceXMR = self.ui.lnPriceBTC.text()
                self.ui.setWindowTitle(retTicker['BTC_XMR']['last'])
                self.ui.setXMRPrice(retTicker['BTC_XMR']['last'])
                self.ui.setETHPrice(retTicker['BTC_ETH']['last'])
                self.ui.setHigh(retTicker['BTC_XMR']['high24hr'])
                self.ui.setLow(retTicker['BTC_XMR']['low24hr'])
                self.ui.setChange(str(round(float(retTicker['BTC_XMR']['percentChange'])*100,2)) + " %")

                print ("Public key: " + str(self.PUBLIC_KEY))
                z = z + 1
                print ("Loop count: " + str(z))
                if self.PUBLIC_KEY == '' or self.SECRET_KEY == '':
                    break

                self.ui.setLcdMonero(self.retBalances['XMR'])
                self.ui.setLcdBitcoin(self.retBalances['BTC'])
                self.ui.setLcdEthereum(self.retBalances['ETH'])

                retHistoryXMR = self.poloInstance.returnTradeHistory("BTC_XMR")
                retHistoryETH = self.poloInstance.returnTradeHistory("BTC_ETH")
                self.countHistoryXMR = len(retHistoryXMR)
                self.countHistoryETH = len(retHistoryETH)
                self.retOpenOrdersXMR = self.poloInstance.returnOpenOrders("BTC_XMR")
                self.retOpenOrdersETH = self.poloInstance.returnOpenOrders("BTC_ETH")
                self.countOpenOrdersXMR = len(self.retOpenOrdersXMR)
                self.countOpenOrdersETH = len(self.retOpenOrdersETH)
                self.setBalanceInclIO(self.countOpenOrdersXMR, self.retOpenOrdersXMR, self.retBalances['XMR'], self.ui.setLcdMoneroinclIO)
                self.setBalanceInclIO(self.countOpenOrdersETH, self.retOpenOrdersETH, self.retBalances['ETH'], self.ui.setLcdEthereuminclIO)
                self.setOpenOrders(self.countOpenOrdersXMR, self.ui.OpenOrdersWidgetXMR, self.retOpenOrdersXMR)
                self.setOpenOrders(self.countOpenOrdersETH, self.ui.OpenOrdersWidgetETH, self.retOpenOrdersETH)
                self.setHistory(self.countHistoryXMR, self.ui.HistoryWidgetXMR, retHistoryXMR, "XMR")
                self.setHistory(self.countHistoryETH, self.ui.HistoryWidgetETH, retHistoryETH, "ETH")
   
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
            except:
                continue
    
    def setBalanceInclIO(self, countopenorders, retopenorders, currency, currencyio):
        count = 0
        OOAmount = 0
        for i in range(countopenorders):
            OOAmount = float(retopenorders[i]["amount"])
            count = count + OOAmount
        CompleteAmount = format(count + float(currency), '.8f')
        currencyio(str(CompleteAmount))
    def setOpenOrders(self, countopenorders, openorderswidget, retopenorders):
        openorderswidget.setRowCount(0)
        if countopenorders > openorderswidget.rowCount():
            openorderswidget.setRowCount(countopenorders)
        if countopenorders != 0:
            for i in range(countopenorders):              
                openorderswidget.setItem(i,0, QTableWidgetItem(retopenorders[i]["orderNumber"]))
                openorderswidget.setItem(i,1, QTableWidgetItem(retopenorders[i]["type"]))
                openorderswidget.setItem(i,2, QTableWidgetItem(retopenorders[i]["rate"]))
                openorderswidget.setItem(i,3, QTableWidgetItem(retopenorders[i]["startingAmount"]))
                openorderswidget.setItem(i,4, QTableWidgetItem(retopenorders[i]["amount"]))
                if retopenorders[i]["type"] == "sell":
                    openorderswidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                    openorderswidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                else:
                    openorderswidget.item(i, 1).setBackground(QtGui.QColor(10,189,82))
    def setHistory(self, counthistory, historywidget, rethistory, currency):
        historywidget.setRowCount(0)
        if counthistory > historywidget.rowCount():
           historywidget.setRowCount(counthistory)   
        if counthistory != 0:
            for i in range(counthistory):
                historywidget.setItem(i,0, QTableWidgetItem(currency))
                historywidget.setItem(i,1, QTableWidgetItem(rethistory[i]["type"]))
                historywidget.setItem(i,2, QTableWidgetItem(rethistory[i]["rate"]))
                historywidget.setItem(i,3, QTableWidgetItem(rethistory[i]["amount"]))
                historywidget.setItem(i,4, QTableWidgetItem(rethistory[i]["date"]))
                if rethistory[i]["type"] == "sell":
                    historywidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                    historywidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                else:
                    historywidget.item(i, 1).setBackground(QtGui.QColor(10,189,82))
    def cancelOrder(self):
        self.ui.OpenOrdersWidgetXMR.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
        self.poloInstance.cancel("BTC_XMR", orderNumberXMR)
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
        exeBuy = self.poloInstance.buy("BTC_XMR",self.BuyreadBTCprice,self.resultBuyXMRAmount)
    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
        exeSell = self.poloInstance.sell("BTC_XMR",self.SellreadBTCprice, self.SellreadXMRAmount)
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
        retTicker = self.poloInstance.returnTicker()
        self.ui.setSellBTCPrice(retTicker['BTC_XMR']['last'])
    def clickBuyGetBTCTotal(self):
        self.ui.btnBuyGetBTCTotal.clicked.connect(self.clickedBuyGetBTCTotal)
    def clickedBuyGetBTCTotal(self):
        self.retBalances = self.poloInstance.returnBalances()
        self.ui.setBuyBTCTotal(self.retBalances['BTC'])