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
                self.ui.setAppStatus("OK")
                self.ui.setNetworkStatus("OK")
           
            except (ConnectionError, TimeoutError) as x:
                self.ui.setLog(logging.debug("main_thread Loop Exception HTTPSConnectionPool: " + str(x)))
                self.ui.setNetworkStatus("ERROR")
                self.sleep(2)
                continue         
            except Exception as e:
                logging.debug("main_thread Loop Exception: " + str(e))
                self.ui.setAppStatus("ERROR")
                self.sleep(2)
                continue

    def popup(self, text, art):
        msg = QMessageBox()
        msg.setIcon(art)

        msg.setText(text)
        msg.setWindowTitle("Notification")
        msg.setStandardButtons(QMessageBox.Ok)
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
       XMRUSDPRICE = float(self.ui.lnPriceUSD.text())
       XMRAmount = self.ui.lcdMoneroinclO.value()
       
       ETHUSDPRICE = float(self.ui.lnETHPriceUSD.text())
       ETHAmount = self.ui.lcdEthereuminclO.value()
       
       BTCUSDPRICE = float(self.ui.lnBTCPriceUSD.text())
       BTCAmount = self.ui.lcdBitcoin.value()

       #Calculate Value of all Coins in Poloniex
       XMRMYASSETVALUE = XMRUSDPRICE * XMRAmount
       ETHMYASSETVALUE = ETHUSDPRICE * ETHAmount
       BTCMYASSETVALUE = BTCUSDPRICE * BTCAmount

       FINALVALUE = XMRMYASSETVALUE + ETHMYASSETVALUE + BTCMYASSETVALUE

       #Calculate Value of all Coins in Poloniex and Offline Wallet
       XMRWITHOFFLINE = XMRAmount + self.OFFLINEAMOUNT
       XMRMYASSETVALUEALL = XMRUSDPRICE * XMRWITHOFFLINE
       FINALVALUEALL = XMRMYASSETVALUEALL + ETHMYASSETVALUE + BTCMYASSETVALUE

       #Set both Values
       self.ui.setMyAssets(round(FINALVALUE,2), round(FINALVALUEALL,2))


    def clickSaveConfiguration(self):
        self.ui.saveButton.clicked.connect(self.clickedSaveConfiguration)
    def clickedSaveConfiguration(self):
        try:
            inputPublicKey = self.ui.lnPublicKey.text().strip()
            inputSecretKey = self.ui.lnSecretKey.text().strip()


            if (inputPublicKey == "" or inputSecretKey == ""):
                logging.debug("Could not save API keys. One input field is empty.")
                self.popup("API keys not saved. One or more API keys are missing.", QMessageBox.Critical)
            
            else:

                with open("key.py", "w") as keyfile:
                    keyfile.write("PUBLIC_KEY = '" + inputPublicKey + "' \nSECRET_KEY = '" + inputSecretKey + "'")
                logging.info("API Keys succesfully saved.")
                self.popup("API Keys succesfully saved.", QMessageBox.Information)
        
        except Exception as e:
            logging.debug("Error! API Keys not saved.")
            self.popup("Error! API Keys not saved.",QMessageBox.Critical)


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
        try:
            exeBuy = self.poloInstance.buy("BTC_XMR",self.BuyreadBTCprice,self.resultBuyXMRAmount)
            logging.info("Buy Order executed.")
            self.popup("Buy order succesfully executed!",QMessageBox.Information)
        except Exception as e:
            logging.debug("Buy Order Error!" + str(e))
            self.popup("Buy order Failed!",QMessageBox.Critical)
    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
    
        try:
            exeSell = self.poloInstance.sell("BTC_XMR",self.SellreadBTCprice, self.SellreadXMRAmount)
            logging.info("Sell Order executed.")
            self.popup("Sell order succesfully executed!", QMessageBox.Information)

        except Exception as e:
            logging.debug("Sell Order Error!" + str(e))
            self.popup("Sell order failed!", QMessageBox.Critical)

    def cancelOrder(self):
        self.ui.OpenOrdersWidgetXMR.cellDoubleClicked.connect(self.double_clicked)

    def double_clicked(self):
        try:
            orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
            self.poloInstance.cancel("BTC_XMR", orderNumberXMR)
            logging.info("Order cancelled succesfully!")
            self.popup("Order cancelled successfully!",QMessageBox.Information)
        except Exception as e:
            logging.debug("Error! Order could not be cancelled.")
            self.popup("Error! Order could not be cancelled.",QMessageBox.Critical)

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
        try:
            exeBuy = self.poloInstance.buy("BTC_ETH",self.BuyETHreadBTCprice,self.resultBuyETHAmount)
            logging.info("Buy Order executed.")
            self.popup("Buy order succesfully executed!",QMessageBox.Information)
        except Exception as e:
            logging.debug("Buy Order Error!" + str(e))
            self.popup("Buy order Failed!",QMessageBox.Critical)
    def clickETHSell(self):
        self.ui.sellETHButton.clicked.connect(self.clickedETHSell)
    def clickedETHSell(self):
        
        try:
            exeSell = self.poloInstance.sell("BTC_ETH",self.SellETHreadBTCprice, self.SellETHreadAmount)
            logging.info("Sell Order executed.")
            self.popup("Sell order succesfully executed!", QMessageBox.Information)

        except Exception as e:
            logging.debug("Sell Order Error!" + str(e))
            self.popup("Sell order failed!", QMessageBox.Critical)
    def cancelETHOrder(self):
        self.ui.OpenOrdersWidgetETH.cellDoubleClicked.connect(self.doubleETH_clicked)
    def doubleETH_clicked(self):
        try:
            orderNumberETH = self.ui.OpenOrdersWidgetETH.currentItem().text()
            self.poloInstance.cancel("BTC_ETH", orderNumberETH)
            logging.info("Order cancelled succesfully!")
            self.popup("Order cancelled successfully!",QMessageBox.Information)
        except Exception as e:
            logging.debug("Error! Order could not be cancelled.")
            self.popup("Error! Order could not be cancelled.",QMessageBox.Critical)



