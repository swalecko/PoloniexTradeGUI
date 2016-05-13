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
    ETHEREUM = "ETH"

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
        #poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        z = 0
        
        while True:
            try:
                poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)

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

                print ("Public key: " + str(self.PUBLIC_KEY))
                z = z + 1
                print ("Loop count: " + str(z))
                if self.PUBLIC_KEY == '' or self.SECRET_KEY == '':
                    break

                

                self.ui.setLcdMonero(retBalances['XMR'])
                self.ui.setLcdBitcoin(retBalances['BTC'])
                self.ui.setLcdEthereum(retBalances['ETH'])

                retHistoryXMR = poloInstance.returnTradeHistory("BTC_XMR")
                retHistoryETH = poloInstance.returnTradeHistory("BTC_ETH")
                self.countHistoryXMR = len(retHistoryXMR)
                self.countHistoryETH = len(retHistoryETH)
                self.retOpenOrdersXMR = poloInstance.returnOpenOrders("BTC_XMR")
                self.retOpenOrdersETH = poloInstance.returnOpenOrders("BTC_ETH")
                print (self.retOpenOrdersXMR)

                self.countOpenOrdersXMR = len(self.retOpenOrdersXMR)
                self.countOpenOrdersETH = len(self.retOpenOrdersETH)


                countXMR = 0
                OOAmountXMR = 0
                for i in range(self.countOpenOrdersXMR):
                #if self.retOpenOrdersXMR[i]["type"] == "buy":
                    OOAmountXMR = float(self.retOpenOrdersXMR[i]["amount"])
                    print (OOAmountXMR)
                    countXMR = countXMR + OOAmountXMR
                    print (countXMR)                               

                XMRCompleteAmount = format(countXMR + float(retBalances['XMR']), '.8f')
                self.ui.setLcdMoneroinclIO(str(XMRCompleteAmount))
                
                countETH = 0
                OOAmountETH = 0
                for i in range(self.countOpenOrdersETH):
                	#if retOpenOrdersETH[i]["type"] == "buy":
                    OOAmountETH = float(self.retOpenOrdersETH[i]["amount"])
                    countETH = countETH + OOAmountETH

                ETHCompleteAmount = format(countETH + float(retBalances['ETH']), '.8f')

                self.ui.setLcdEthereuminclIO(str(ETHCompleteAmount))
                                 

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
    

    def setOpenOrders(self, countopenorders, openorderswidget, retopenorders):
        if countopenorders > openorderswidget.rowCount():
            openorderswidget.setRowCount(countopenorders)
            print ("After setting rows Open Orders: " + str(openorderswidget.rowCount()))
        if countopenorders != 0:
            openorderswidget.clearContents()
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
        print ("self.countHistoryXMR: " + str(counthistory))
        print ("rowcount: " + str(historywidget.rowCount()))
        if counthistory > historywidget.rowCount():
           historywidget.setRowCount(counthistory)
           print ("After setting rows History: " + str(historywidget.rowCount()))            
        if counthistory != 0:
            historywidget.clearContents()
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
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
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

            