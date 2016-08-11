import polowrapper
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import json
import sys
from requests.exceptions import ConnectionError
import logging
import thread_getusd



class Thread(QThread):
    def __init__(self, ui_instance, PUBLIC_KEY, SECRET_KEY):
        self.ui = ui_instance
        self.PUBLIC_KEY = PUBLIC_KEY
        self.SECRET_KEY = SECRET_KEY
        super(QThread, self).__init__()
        self.poloInstance = polowrapper.poloniex(self.PUBLIC_KEY, self.SECRET_KEY)
        self.OFFLINEAMOUNT = 0
        self.XMRLIST = []
        self.ETHLIST = []
        

    def function():
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):

        while True:
            try:
                
                if self.PUBLIC_KEY == '' or self.SECRET_KEY == '':
                    
                    break

                self.retBalances = self.poloInstance.returnBalances()

                self.retTicker = self.poloInstance.returnTicker()
             
                self.BalanceXMR = self.retBalances['XMR']
                self.BalanceETH = self.retBalances['ETH']
                self.BalanceBTC = self.retBalances['BTC']
                
                self.tickerXMR = self.retTicker['BTC_XMR']
                self.tickerETH = self.retTicker['BTC_ETH']
                self.lastXMR = self.tickerXMR['last']
                self.lastETH = self.tickerETH['last']

                
                self.ui.setLcdMonero(self.BalanceXMR)
                self.ui.setLcdBitcoin(self.BalanceBTC)
                self.ui.setLcdEthereum(self.BalanceETH)

                retHistoryXMR = self.poloInstance.returnTradeHistory("BTC_XMR")
                retHistoryETH = self.poloInstance.returnTradeHistory("BTC_ETH")
                self.countHistoryXMR = len(retHistoryXMR)
                self.countHistoryETH = len(retHistoryETH)
                self.retOpenOrdersXMR = self.poloInstance.returnOpenOrders("BTC_XMR")
                self.retOpenOrdersETH = self.poloInstance.returnOpenOrders("BTC_ETH")
                self.countOpenOrdersXMR = len(self.retOpenOrdersXMR)
                self.countOpenOrdersETH = len(self.retOpenOrdersETH)
               
                self.setBalanceInclIO(self.countOpenOrdersXMR, self.retOpenOrdersXMR, self.BalanceXMR, self.ui.setLcdMoneroinclIO)
                self.setBalanceInclIO(self.countOpenOrdersETH, self.retOpenOrdersETH, self.BalanceETH, self.ui.setLcdEthereuminclIO)
               
                self.setOpenOrders(self.countOpenOrdersXMR, self.ui.OpenOrdersWidgetXMR, self.retOpenOrdersXMR)
                self.setOpenOrders(self.countOpenOrdersETH, self.ui.OpenOrdersWidgetETH, self.retOpenOrdersETH)
                self.setHistory(self.countHistoryXMR, self.ui.HistoryWidgetXMR, retHistoryXMR, "XMR")
                self.setHistory(self.countHistoryETH, self.ui.HistoryWidgetETH, retHistoryETH, "ETH")

                #XMR
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
                    logging.debug()
                    continue
                self.calcBuyAmount(self.BuyreadBTCprice, self.BuyreadBTCTotal)

                
                #ETH
                self.SellETHreadBTCprice = self.ui.lnETHSellPrice.text()
                self.SellETHreadBTCprice = float(self.SellETHreadBTCprice)
                
                self.SellETHreadAmount = self.ui.lnETHSellAmount.text()
                self.SellETHreadAmount = float(self.SellETHreadAmount)

                self.calcETHSellBTCTotal(self.SellETHreadBTCprice, self.SellETHreadAmount)

                self.BuyETHreadBTCprice = self.ui.lnETHBuyPrice.text()
                self.BuyETHreadBTCprice = float(self.BuyETHreadBTCprice)        
                self.BuyETHreadBTCTotal = self.ui.lnETHBuyTotal.text()          
                try:
                    self.BuyETHreadBTCTotal = float(self.BuyETHreadBTCTotal)
                except ValueError:
                    continue
                self.calcETHBuyAmount(self.BuyETHreadBTCprice, self.BuyETHreadBTCTotal)

                self.calcMyAssets()


                self.sleep (1)
                           
            except (ConnectionError, TimeoutError) as x:
                logging.debug("ERROR: main_thread Loop Exception HTTPSConnectionPool: " + str(x))
                self.ui.setXMRPrice("")
                self.ui.setHigh("")
                self.ui.setLow("")
                self.ui.setChange("")
                self.ui.setETHPrice("")
                self.ui.setETHHigh("")
                self.ui.setETHLow("")
                self.ui.setETHChange("")
                self.ui.setPoloniexStatus("Disconnected")
                self.sleep(2)
                continue         
            except Exception as e:
                logging.debug("ERROR: main_thread Loop Exception: " + str(e))
                self.sleep(2)
                continue

    def popup(self, text, art):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msg.setIcon(art)
 
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QWidget {color: white;} QMessageBox {background-color: #333333; border-width: 1px; border-color:orange; border-style: solid; border-radius: 6;} QPushButton{color: orange; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646); border-width: 1px;border-color: orange; border-style: solid;border-radius: 6;padding: 3px;font-size: 12px;padding-left: 5px;padding-right: 5px;} QPushButton:pressed {background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d30, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252530)} QPushButton:hover {border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}")

        msg.exec_()

    def setBalanceInclIO(self, countopenorders, retopenorders, currency, currencyio):
        count = 0
        OOAmount = 0
        if countopenorders != 0:
            for i in range(countopenorders):
                OOAmount = float(retopenorders[i]["amount"])
                count = count + OOAmount
            CompleteAmount = format(count + float(currency), '.8f')
            currencyio(str(CompleteAmount))
        else:
            currencyio(format(float(0.00000000), '.8f'))

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
                   
                else:
                    openorderswidget.item(i, 1).setBackground(QtGui.QColor(0,139,0))
                    openorderswidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
    
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
                else:
                    historywidget.item(i, 1).setBackground(QtGui.QColor(0,139,0))
                    historywidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))

    def calcMyAssets(self):
       XMRUSDPRICE = self.ui.lnPriceUSD.text()
       ETHUSDPRICE = self.ui.lnETHPriceUSD.text()
       BTCUSDPRICE = self.ui.lnBTCPriceUSD.text()

       if XMRUSDPRICE == " " or ETHUSDPRICE == " " or BTCUSDPRICE == " ":
       	    self.ui.setMyAssets(" ")
       else:
            XMRUSDPRICE = float(self.ui.lnPriceUSD.text())
       	    ETHUSDPRICE = float(self.ui.lnETHPriceUSD.text())
       	    BTCUSDPRICE = float(self.ui.lnBTCPriceUSD.text())
       
            XMRAmount = self.ui.lcdMonero.value() 
            ETHAmount = self.ui.lcdEthereum.value()
            BTCAmount = self.ui.lcdBitcoin.value()

            #Calculate Value of all Coins in Poloniex
            XMRMYASSETVALUE = XMRUSDPRICE * XMRAmount
            ETHMYASSETVALUE = ETHUSDPRICE * ETHAmount
            BTCMYASSETVALUE = BTCUSDPRICE * BTCAmount

            FINALVALUE = XMRMYASSETVALUE + ETHMYASSETVALUE + BTCMYASSETVALUE

            #Set both Values
            self.ui.setMyAssets(round(FINALVALUE,2))

    def clickSaveConfiguration(self):
        self.ui.saveButton.clicked.connect(self.clickedSaveConfiguration)
    def clickedSaveConfiguration(self):
        try:
            inputPublicKey = self.ui.lnPublicKey.text().strip()
            inputSecretKey = self.ui.lnSecretKey.text().strip()

            if (inputPublicKey == "" or inputSecretKey == ""):
                logging.warning("Warning: Could not save API keys. Invalid Input.")
                self.popup("API keys not saved. Invalid input.", QMessageBox.Warning)
            
            else:

                with open("key.py", "w") as keyfile:
                    keyfile.write("PUBLIC_KEY = '" + inputPublicKey + "' \nSECRET_KEY = '" + inputSecretKey + "'")
                logging.info("INFO: API Keys succesfully saved.")
                self.popup("API Keys succesfully saved", QMessageBox.Information)
        
        except Exception as e:
            logging.debug("Error: API Keys not saved.")
            self.popup("Error! API Keys not saved",QMessageBox.Critical)

    #XMR
    def calcSellBTCTotal(self, sellreadbtcprice, sellreadxmramount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadxmramount = sellreadxmramount
        resultSellBTCTotal = self.sellreadbtcprice*self.sellreadxmramount
        self.ui.setSellBTCTotal(resultSellBTCTotal)
    def calcBuyAmount(self, buyreadbtcprice, buyreadbtctotal):
        self.buyreadbtcprice = buyreadbtcprice
        self.buyreadbtctotal = buyreadbtctotal
        try:
            self.resultBuyXMRAmount = self.buyreadbtctotal/self.buyreadbtcprice
        except ZeroDivisionError:
            self.resultBuyXMRAmount = 0.0      
        self.ui.setBuyXMRAmount(self.resultBuyXMRAmount)    
    def clickSellGetBTCPrice(self):
        self.ui.btnSellGetBTCPrice.clicked.connect(self.clickedSellGetBTCPrice)   
    def clickedSellGetBTCPrice(self):
        self.ui.setSellBTCPrice(self.lastXMR)
    def clickBuyGetBTCTotal(self):
        self.ui.btnBuyGetBTCTotal.clicked.connect(self.clickedBuyGetBTCTotal)
    def clickedBuyGetBTCTotal(self):
        self.ui.setBuyBTCTotal(self.BalanceBTC)
    
    def clickBuy(self):
        self.ui.buyButton.clicked.connect(self.clickedBuy)
    def clickedBuy(self):
        
        if self.BuyreadBTCprice == "" or self.BuyreadBTCprice == 0.0 or self.resultBuyXMRAmount == "" or self.resultBuyXMRAmount == 0.0:
            self.popup("Invalid input", QMessageBox.Warning)           
        else:
            try:
                exeBuy = self.poloInstance.buy("BTC_XMR",self.BuyreadBTCprice,self.resultBuyXMRAmount)
                print (exeBuy)

                if exeBuy["orderNumber"] != '':

                    logging.info("INFO: Buy Order executed.")
                    self.popup("Buy order succesfully executed",QMessageBox.Information)
                else:
                    logging.debug("ERROR: Buy Order failed! " + str(e))
                    self.popup("Buy order failed",QMessageBox.Critical)
            
            except Exception as e:
                logging.debug("ERROR: Buy Order failed! " + str(e))
                self.popup("Buy order failed",QMessageBox.Critical)
    
    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
        if self.SellreadBTCprice == "" or self.SellreadBTCprice == 0.0 or self.SellreadXMRAmount == "" or self.SellreadXMRAmount == 0.0:     
            self.popup("Invalid input", QMessageBox.Warning)
        elif self.SellreadXMRAmount > float(self.BalanceXMR):
            self.popup("Amount > than Balance. Reduce your amount.", QMessageBox.Warning)
        else:   
            try:      
                exeSell = self.poloInstance.sell("BTC_XMR",self.SellreadBTCprice, self.SellreadXMRAmount)
                print (exeSell)

                if exeSell["orderNumber"] != '':
                    logging.info("INFO: Sell Order executed.")
                    self.popup("Sell order succesfully executed", QMessageBox.Information)
                else:
                    logging.debug("ERROR: Sell Order failed! " + str(e))
                    self.popup("Sell order failed",QMessageBox.Critical)

            except Exception as e:
                logging.debug("ERROR: Sell Order failed! Exp " + str(e))
                self.popup("Sell order failed Exp", QMessageBox.Critical)

    def cancelOrder(self):
        self.ui.OpenOrdersWidgetXMR.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        try:
            orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
            resultCancel = self.poloInstance.cancel("BTC_XMR", orderNumberXMR)
            print (resultCancel)
            print (resultCancel["success"])
            print (type(resultCancel["success"]))
            
            if resultCancel["success"] == 1:
                logging.info("INFO: Order cancelled succesfully!")
                self.popup("Order cancelled successfully",QMessageBox.Information)
            else:
                logging.debug("Error: Order could not be cancelled. Try again..")
                self.popup("Error! Order could not be cancelled",QMessageBox.Critical)
        except Exception as e:
            logging.debug("Error: Order could not be cancelled. Try again..")
            self.popup("Error! Order could not be cancelled",QMessageBox.Critical)

    #ETH
    def calcETHBuyAmount(self, buyreadbtcprice, buyreadbtctotal):
        self.buyreadbtcprice = buyreadbtcprice
        self.buyreadbtctotal = buyreadbtctotal
        try:
            self.resultBuyETHAmount = self.buyreadbtctotal/self.buyreadbtcprice
        except ZeroDivisionError:
            self.resultBuyETHAmount = 0.0      
        self.ui.setBuyETHAmount(self.resultBuyETHAmount)
    def calcETHSellBTCTotal(self, sellreadbtcprice, sellreadethamount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadethamount = sellreadethamount
        resultSellBTCTotal = self.sellreadbtcprice*self.sellreadethamount
        self.ui.setETHSellBTCTotal(resultSellBTCTotal)    
    def clickETHSellGetBTCPrice(self):
        self.ui.btnETHSellGetBTCPrice.clicked.connect(self.clickedETHSellGetBTCPrice)   
    def clickedETHSellGetBTCPrice(self):
        self.ui.setETHSellBTCPrice(self.lastETH)
    def clickETHBuyGetBTCTotal(self):
        self.ui.btnETHBuyGetBTCTotal.clicked.connect(self.clickedETHBuyGetBTCTotal)
    def clickedETHBuyGetBTCTotal(self):
        self.ui.setETHBuyBTCTotal(self.BalanceBTC)
    
    def clickETHBuy(self):
        self.ui.buyETHButton.clicked.connect(self.clickedETHBuy)
    def clickedETHBuy(self): 
        if self.BuyETHreadBTCprice == "" or self.BuyETHreadBTCprice == 0.0 or self.resultBuyETHAmount == "" or self.resultBuyETHAmount == 0.0:     
            self.popup("Invalid input", QMessageBox.Warning)
        else:   
            try:
                exeBuy = self.poloInstance.buy("BTC_ETH",self.BuyETHreadBTCprice,self.resultBuyETHAmount)
                if exeBuy["orderNumber"] != '':

                    logging.info("INFO: Buy Order executed.")
                    self.popup("Buy order succesfully executed",QMessageBox.Information)
                else:
                    logging.debug("ERROR: Buy Order failed " + str(e))
                    self.popup("Buy order failed",QMessageBox.Critical)

            except Exception as e:
                logging.debug("ERROR: Buy Order failed! " + str(e))
                self.popup("Buy order failed",QMessageBox.Critical)
    
    def clickETHSell(self):
        self.ui.sellETHButton.clicked.connect(self.clickedETHSell)
    def clickedETHSell(self):
        if self.SellETHreadBTCprice == "" or self.SellETHreadBTCprice == 0.0 or self.SellETHreadAmount == "" or self.SellETHreadAmount == 0.0:     
            self.popup("Invalid input", QMessageBox.Warning)
        elif self.SellETHreadAmount > float(self.BalanceETH):
            self.popup("Amount > than Balance. Reduce your amount.", QMessageBox.Warning)
        else:
            try:
                exeSell = self.poloInstance.sell("BTC_ETH",self.SellETHreadBTCprice, self.SellETHreadAmount)
                
                if exeSell["orderNumber"] != '':
                    logging.info("INFO: Sell Order executed.")
                    self.popup("Sell order succesfully executed!", QMessageBox.Information)
                else:
                    logging.debug("ERROR: Sell Order failed!" + str(e))
                    self.popup("Sell order failed", QMessageBox.Critical)

            except Exception as e:
                logging.debug("ERROR: Sell Order failed!" + str(e))
                self.popup("Sell order failed", QMessageBox.Critical)
    
    def cancelETHOrder(self):
        self.ui.OpenOrdersWidgetETH.cellDoubleClicked.connect(self.doubleETH_clicked)
    def doubleETH_clicked(self):
        try:
            orderNumberETH = self.ui.OpenOrdersWidgetETH.currentItem().text()
            self.poloInstance.cancel("BTC_ETH", orderNumberETH)
            logging.info("INFO: Order cancelled succesfully!")
            self.popup("Order cancelled successfully",QMessageBox.Information)
        except Exception as e:
            logging.debug("Error: Order could not be cancelled.")
            self.popup("Error! Order could not be cancelled.",QMessageBox.Critical)



