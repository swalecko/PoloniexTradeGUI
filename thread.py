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
        retBalances = poloInstance.returnBalances()
        retTicker = poloInstance.returnTicker()
        
        while True:


            self.ui.setCurrency("XMR_BTC")
            self.ui.setPrice(retTicker['BTC_XMR']['last'])
            self.price = retTicker['BTC_XMR']['last']
            #self.ui.setUSDPrice(xmrusd.getUSDPrice())
            #print (xmrusd.getUSDPrice())
            self.ui.setHigh(retTicker['BTC_XMR']['high24hr'])
            self.ui.setLow(retTicker['BTC_XMR']['low24hr'])
            self.ui.setChange(str(round(float(retTicker['BTC_XMR']['percentChange'])*100,2)) + " %")
            
            xmr = retBalances['XMR']
            btc = retBalances['BTC']
            eth = retBalances['ETH']
            self.ui.setLcdMonero(xmr)
            self.ui.setLcdBitcoin(btc)
            self.ui.setLcdEthereum(eth)
            print (xmr)
            print (btc)
         
            retHistoryXMR = poloInstance.returnTradeHistory("BTC_XMR")
            countHistoryXMR = len(retHistoryXMR)
            retOpenOrders = poloInstance.returnOpenOrders("BTC_XMR")
            countOpenOrders = len(retOpenOrders)
            print ("HistoryXMR" + str(countHistoryXMR))

            count = 0
            for i in range(countOpenOrders):
                OOAmount = float(retOpenOrders[i]["amount"])
                count = OOAmount + OOAmount 
                print (count)
            XMRCompleteAmount = count + float(xmr)
            self.ui.setLcdMoneroinclIO(str(XMRCompleteAmount))
            

                        
            print (countOpenOrders)
            self.ui.OpenOrdersWidget.clearContents()
            self.ui.HistoryWidget.clearContents()
           
            for i in range(countOpenOrders):
        
                self.ui.OpenOrdersWidget.setItem(i,0, QTableWidgetItem(retOpenOrders[i]["orderNumber"]))
                self.ui.OpenOrdersWidget.setItem(i,1, QTableWidgetItem(retOpenOrders[i]["type"]))
                self.ui.OpenOrdersWidget.setItem(i,2, QTableWidgetItem(retOpenOrders[i]["rate"]))
                self.ui.OpenOrdersWidget.setItem(i,3, QTableWidgetItem(retOpenOrders[i]["startingAmount"]))
                self.ui.OpenOrdersWidget.setItem(i,4, QTableWidgetItem(retOpenOrders[i]["amount"]))
                if retOpenOrders[i]["type"] == "sell":
                    self.ui.OpenOrdersWidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                    self.ui.OpenOrdersWidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                else:
                    self.ui.OpenOrdersWidget.item(i, 1).setBackground(QtGui.QColor(10,189,82))

            
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
            
            else:
                continue

            self.SellreadBTCprice = self.ui.lnSellPrice.text()
            self.SellreadBTCprice = float(self.SellreadBTCprice)
            self.SellreadXMRAmount = self.ui.lnSellAmount.text()
            self.SellreadXMRAmount = float(self.SellreadXMRAmount)

            # if self.SellreadBTCprice or self.SellreadXMRAmount == "":
            #     print ("Sell price or amount empty")
            #     continue
            # else:
            self.calcSellBTCTotal(self.SellreadBTCprice, self.SellreadXMRAmount)



            self.sleep (1)

    def calcSellBTCTotal(self, sellreadbtcprice, sellreadxmramount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadxmramount = sellreadxmramount

        resultSellBTCTotal = self.sellreadbtcprice*self.sellreadxmramount
        self.ui.setSellBTCTotal(resultSellBTCTotal)
        return (resultSellBTCTotal)


    






    def clickBuy(self):
        self.ui.buyButton.clicked.connect(self.clickedBuy)
    def clickedBuy(self):
        poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)

        
        try:
            exeBuy = poloInstance.buy("BTC_XMR",self.SellreadBTCprice,self.buyTotalAmount)
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
