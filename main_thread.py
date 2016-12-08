import polowrapper
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QProgressBar
import requests
import json
import sys
from requests.exceptions import ConnectionError
import logging
import webbrowser


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

        self.stateRefresh = 0

        while True:
            print ("While Looping state: running")

            if self.PUBLIC_KEY == '' or self.SECRET_KEY == '':
                self.stateRefresh = 1
                self.stateButtons(sell=False, buy=False, refresh=False)
                break     
        
            if self.getPoloInfo() is True:
                self.ui.setPoloniexStatus("Connected")
                self.stateButtons(sell=True, buy=True, refresh=True)
                self.setXMRPriceInfo()
                self.setUSDPriceInfo()

            else:
                self.ui.setPoloniexStatus("Disconnected")
                self.stateButtons(sell=False, buy=False, refresh=False)
           
            self.refreshXMRvalues(calc=True)

            self.sleep (2)
                       
        else:
            logging.critical("Loop stopped")
    
    def stateButtons(self, **kargs):
        if self.stateRefresh == 1:
            if kargs['sell'] == True:
                self.ui.sellButton.setEnabled(True)
            else:
                self.ui.sellButton.setEnabled(False)
            
            if kargs['buy'] == True:
                self.ui.buyButton.setEnabled(True)
            else:
                self.ui.buyButton.setEnabled(False)
            
            if kargs['refresh'] == True:
                self.ui.btnRefresh.setEnabled(True)
            else:
                self.ui.btnRefresh.setEnabled(False)
        else:
            self.ui.sellButton.setEnabled(False)
            self.ui.buyButton.setEnabled(False)



    def refreshXMRvalues(self, **kargs):
        
        self.SellreadBTCprice = self.ui.lnSellPrice.text()
        self.SellreadXMRAmount = self.ui.lnSellAmount.text()
                       
        if not self.SellreadBTCprice.isalpha() and self.SellreadBTCprice != "" and not self.SellreadXMRAmount.isalpha() and self.SellreadXMRAmount != "":

            self.SellreadBTCprice = float(self.SellreadBTCprice)
            self.SellreadXMRAmount = float(self.SellreadXMRAmount)

            if kargs['calc'] == True:
                self.calcSellBTCTotal(self.SellreadBTCprice, self.SellreadXMRAmount)
            else:
                pass
        else:
            pass
        
        self.BuyreadBTCprice = self.ui.lnBuyPrice.text()
        self.BuyreadBTCTotal = self.ui.lnBuyTotal.text() 

        
        if not self.BuyreadBTCprice.isalpha() and self.BuyreadBTCprice != "" and not self.BuyreadBTCTotal.isalpha() and self.BuyreadBTCTotal != "":
        
            self.BuyreadBTCprice = float(self.BuyreadBTCprice)        
            self.BuyreadBTCTotal = float(self.BuyreadBTCTotal)
            
            if kargs['calc'] == True:
                self.calcBuyAmount(self.BuyreadBTCprice, self.BuyreadBTCTotal)
            else:
                pass
        else:
            pass   

    def showBalances(self):
        
        self.retBalances = self.poloInstance.returnBalances()
        self.retOpenOrdersXMR = self.poloInstance.returnOpenOrders("BTC_XMR")     

        if self.retBalances is False or self.retOpenOrdersXMR is False:
            logging.warning("retBalances or retOpenOrdersXMR = None: Balances not refreshed")
            self.ui.setPoloniexStatus("Disconnected")

            return False
        else:
            
            self.countOpenOrdersXMR = len(self.retOpenOrdersXMR)
            self.BalanceXMR = self.retBalances['XMR']

            self.BalanceBTC = self.retBalances['BTC']

            self.ui.setLcdMonero(self.BalanceXMR)
            self.ui.setLcdBitcoin(self.BalanceBTC)

            count = 0
            OOAmount = 0

            if self.countOpenOrdersXMR != 0:
                for i in range(self.countOpenOrdersXMR):

                    OOAmount = float(self.retOpenOrdersXMR[i]["amount"])
                    count = count + OOAmount
     
                CompleteAmount = format(count + float(self.BalanceXMR), '.8f')
                self.ui.setLcdMoneroinclIO(str(CompleteAmount))

            else:
                self.ui.setLcdMoneroinclIO(format(float(0.00000000), '.8f')) 
            print ("Balances refreshed...")   

    def popup(self, text, art):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msg.setIcon(art)
 
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QWidget {color: white;} QMessageBox {background-color: #333333; border-width: 1px; border-color:orange; border-style: solid; border-radius: 6;} QPushButton{color: orange; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646); border-width: 1px;border-color: orange; border-style: solid;border-radius: 6;padding: 3px;font-size: 12px;padding-left: 5px;padding-right: 5px;} QPushButton:pressed {background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d30, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252530)} QPushButton:hover {border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}")

        msg.exec_()

    def confirmPopup(self, text):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msg.setIcon(QMessageBox.Question)
 
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Abort)
        btnConfirm = msg.button(QMessageBox.Ok)
        btnConfirm.setText("  Confirm  ")
        msg.setStyleSheet("QWidget {color: white;} QMessageBox {background-color: #333333; border-width: 1px; border-color:orange; border-style: solid; border-radius: 6;} QPushButton{color: orange; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646); border-width: 1px;border-color: orange; border-style: solid;border-radius: 6;padding: 3px;font-size: 12px;padding-left: 5px;padding-right: 5px;} QPushButton:pressed {background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d30, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252530)} QPushButton:hover {border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}")

        ret = msg.exec_()

        if ret == QMessageBox.Ok:
            return True
        elif ret == QMessageBox.Abort:
            return False


    # def setBalanceInclIO(self, countopenorders, retopenorders, currency, currencyio):
    #     count = 0
    #     OOAmount = 0

    #     if countopenorders != 0:
    #         for i in range(countopenorders):
    #       #      try:
    #             OOAmount = float(retopenorders[i]["amount"])
    #             count = count + OOAmount
    #    #         except Exception as e:
    #     #            logging.error("ERROR: Could not calculate the Open Orders amount")
    #         CompleteAmount = format(count + float(currency), '.8f')
    #         currencyio(str(CompleteAmount))

    #     else:
    #         currencyio(format(float(0.00000000), '.8f'))
                           

    def clickRefresh(self):
        self.ui.btnRefresh.clicked.connect(self.clickedRefresh)
    def clickedRefresh(self):

        self.ui.GprogressBar.setMinimum(0)
        self.ui.GprogressBar.setMaximum(100)

        self.ui.GprogressBar.show()
        self.ui.GprogressBar.setValue(0)
       
        if self.RefreshOO() is False:
            logging.critical("Refresh Open Orders failed")
            self.popup("Refresh not completed. \nPlease refresh again.",QMessageBox.Warning)
        else:

            self.ui.GprogressBar.setValue(30)
        
            if self.RefreshHistory() is False:
                logging.critical("Refresh History failed")
                self.popup("Refresh not completed. \nPlease refresh again.",QMessageBox.Warning)
            else:
                self.ui.GprogressBar.setValue(60)
        
                if self.showBalances() is False:
                    logging.critical("Refresh Balances failed")
                    self.popup("Refresh not completed. \nPlease refresh again.",QMessageBox.Warning)
                else:
                    self.stateButtons(sell=True, buy=True, refresh=True)
                   
                    self.ui.GprogressBar.setValue(75)

                    if self.calcMyAssets() is False:
                        logging.critical("Refresh Asset failed")
                        self.popup("Refresh not completed. \nPlease refresh again.",QMessageBox.Warning)
                    else:
                        self.ui.GprogressBar.setValue(100)

        self.stateRefresh = 1

    def RefreshHistory(self):  
     

        retHistoryXMR = self.poloInstance.returnTradeHistory("BTC_XMR")
                
        if retHistoryXMR == False:
            logging.warning("retHistory = None: History not refreshed")
            return False

        else:
            self.countHistoryXMR = len(retHistoryXMR)
         
            counthistory = self.countHistoryXMR
            historywidget = self.ui.HistoryWidgetXMR
            rethistory = retHistoryXMR
            currency = "XMR"                   

            historywidget.setRowCount(0)
            if counthistory > historywidget.rowCount():
               historywidget.setRowCount(counthistory)   
            if counthistory != 0:
                for i in range(counthistory):

                    QtCore.QCoreApplication.processEvents()
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
            print ("History refreshed...")
    
    def calcMyAssets(self):
        
        XMRUSDPRICE = self.ui.lnPriceUSD.text()
        BTCUSDPRICE = self.ui.lnBTCPriceUSD.text()
        
        if XMRUSDPRICE != "" or BTCUSDPRICE != "":

            XMRUSDPRICE = float(XMRUSDPRICE)
            BTCUSDPRICE = float(BTCUSDPRICE)


            XMRAmount = self.ui.lcdMonero.value() 
            BTCAmount = self.ui.lcdBitcoin.value()

            XMRMYASSETVALUE = XMRUSDPRICE * XMRAmount
            BTCMYASSETVALUE = BTCUSDPRICE * BTCAmount

            FINALVALUE = XMRMYASSETVALUE + BTCMYASSETVALUE
            self.ui.setMyAssets(round(FINALVALUE,2))

            print ("Calc Asset refreshed...")
            return True

        else:
            self.ui.setMyAssets("N/A")
            return False


    def RefreshOO(self):
        

        self.retOpenOrdersXMR = self.poloInstance.returnOpenOrders("BTC_XMR")


        if self.retOpenOrdersXMR == False:
            logging.warning("retOpenOrdersXMR = None: Open Orders not refreshed")
            return False
            
        else:

            self.countOpenOrdersXMR = len(self.retOpenOrdersXMR)

            countopenorders = self.countOpenOrdersXMR
            openorderswidget = self.ui.OpenOrdersWidgetXMR
            retopenorders = self.retOpenOrdersXMR

            self.ui.setOpenOrdersRowCount(0)

            if countopenorders > openorderswidget.rowCount():

                self.ui.setOpenOrdersRowCount(countopenorders)

            if countopenorders != 0:
                for i in range(countopenorders):
                    QtCore.QCoreApplication.processEvents()
                    self.ui.setOpenOrders(i,0, retopenorders[i]["orderNumber"])
                    self.ui.setOpenOrders(i,1, retopenorders[i]["type"])
                    self.ui.setOpenOrders(i,2, retopenorders[i]["rate"])
                    self.ui.setOpenOrders(i,3, retopenorders[i]["startingAmount"])
                    self.ui.setOpenOrders(i,4, retopenorders[i]["amount"])

                    if retopenorders[i]["type"] == "sell":
                        openorderswidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                       
                    else:
                        openorderswidget.item(i, 1).setBackground(QtGui.QColor(0,139,0))
                        openorderswidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
            print ("Open Orders refreshed...")

    def clickSaveConfiguration(self):
        self.ui.saveButton.clicked.connect(self.clickedSaveConfiguration)
    def clickedSaveConfiguration(self):

        inputPublicKey = self.ui.lnPublicKey.text().strip()
        inputSecretKey = self.ui.lnSecretKey.text().strip()

        if (inputPublicKey == "" or inputSecretKey == ""):
            logging.warning("Warning: Could not save API keys. Invalid Input.")
            self.popup("API keys not saved. Invalid input.", QMessageBox.Warning)
        
        else:
            with open("key.py", "w") as keyfile:
                keyfile.write("PUBLIC_KEY = '" + inputPublicKey + "' \nSECRET_KEY = '" + inputSecretKey + "'")
            logging.info("API Keys succesfully saved.")
            self.popup("API Keys succesfully saved", QMessageBox.Information)
        
    def calcSellBTCTotal(self, sellreadbtcprice, sellreadxmramount):
        self.sellreadbtcprice = sellreadbtcprice
        self.sellreadxmramount = sellreadxmramount
        resultSellBTCTotal = self.sellreadbtcprice*self.sellreadxmramount
        self.ui.setSellBTCTotal(resultSellBTCTotal)
    def calcBuyAmount(self, buyreadbtcprice, buyreadbtctotal):
        self.buyreadbtcprice = buyreadbtcprice
        self.buyreadbtctotal = buyreadbtctotal

        if self.buyreadbtctotal != 0.0 and self.buyreadbtcprice != 0.0:
            self.resultBuyXMRAmount = self.buyreadbtctotal/self.buyreadbtcprice
        else:
            self.resultBuyXMRAmount = 0.0
    
        self.ui.setBuyXMRAmount(self.resultBuyXMRAmount)    
    def clickSellGetBTCPrice(self):
        self.ui.btnSellGetBTCPrice.clicked.connect(self.clickedSellGetBTCPrice)   
    def clickedSellGetBTCPrice(self):
        self.retTicker = self.poloInstance.returnTicker()

        if self.retTicker is None:
            logging.warning("self.retTicker = None: Ticker not refreshed")
            self.popup("Price not refreshed. \nPlease try again.")
        else:
            self.tickerXMR = self.retTicker['BTC_XMR']
            self.lastXMR = self.tickerXMR['last']     
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
        elif self.buyreadbtctotal > float(self.BalanceBTC):
            self.popup("Invalid Amount. \nCheck your Balance.", QMessageBox.Warning)
        else:
            self.refreshXMRvalues(calc=False)
            fixBuyreadBTCprice = self.BuyreadBTCprice
            fixresultBuyXMRAmount = self.resultBuyXMRAmount

            text = "Order details: \n\nCurrency: XMR \nPrice: " + str(fixBuyreadBTCprice) + "\nAmount: " + str(fixresultBuyXMRAmount)

            if self.confirmPopup(text) == True:

                exeBuy = self.poloInstance.buy("BTC_XMR",fixBuyreadBTCprice,fixresultBuyXMRAmount)
                QtCore.QCoreApplication.processEvents()

                if exeBuy["orderNumber"] != '':

                    logging.info("Buy Order executed: " + str(exeBuy["orderNumber"]))
                    self.popup("Buy order placed: \n\n" + "Order Number: " + str(exeBuy["orderNumber"]), QMessageBox.Information)
                else:
                    logging.debug("Buy Order failed! " + str(e))
                    self.popup("Buy order failed",QMessageBox.Critical)
            else:
                self.popup("Order aborted!", QMessageBox.Information)
            
    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):

        if self.SellreadBTCprice == "" or self.SellreadBTCprice == 0.0 or self.SellreadXMRAmount == "" or self.SellreadXMRAmount == 0.0:     
            self.popup("Invalid input", QMessageBox.Warning)
        elif self.SellreadXMRAmount > float(self.BalanceXMR):
            self.popup("Invalid Amount. \nCheck your Balance.", QMessageBox.Warning)
        else:   
            self.refreshXMRvalues(calc=False)
            fixSellreadBTCprice = self.SellreadBTCprice
            fixSellreadXMRAmount = self.SellreadXMRAmount    

            text = "Order details: \n\nCurrency: XMR \nPrice: " + str(fixSellreadBTCprice) + "\nAmount: " + str(fixSellreadXMRAmount)

            if self.confirmPopup(text) == True:
            
                exeSell = self.poloInstance.sell("BTC_XMR",fixSellreadBTCprice, fixSellreadXMRAmount)
                QtCore.QCoreApplication.processEvents()

                if exeSell["orderNumber"] != '':
                    logging.info("Sell Order executed: " + str(exeSell["orderNumber"]))
                    self.popup("Sell order placed: \n\n" + "Order Number: " + str(exeSell["orderNumber"]) , QMessageBox.Information)
                else:
                    logging.debug("Sell Order failed! " + str(e))
                    self.popup("Sell order failed",QMessageBox.Critical)
            else:
                self.popup("Order aborted!", QMessageBox.Information)

    def cancelOrder(self):
        self.ui.OpenOrdersWidgetXMR.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
        resultCancel = self.poloInstance.cancel("BTC_XMR", orderNumberXMR)
        QtCore.QCoreApplication.processEvents()
        
        if resultCancel["success"] == 1:
            logging.info("Order cancelled succesfully: " + str(orderNumberXMR))
            self.popup("Order cancelled: \n\n" + str(orderNumberXMR),QMessageBox.Information)
           
        else:
            logging.debug("ERROR: Order could not be cancelled. Try again..")
            self.popup("ERROR! Order could not be cancelled",QMessageBox.Critical)
    
    def clickXmrChart(self):
        self.ui.buttonChart.clicked.connect(self.clickedXmrChart)
    def clickedXmrChart(self):
        webbrowser.open('https://bitcoinwisdom.com/markets/poloniex/xmrbtc')

    def setXMRPriceInfo(self):
        lastXMR = self.lastXMR
        self.ui.setXMRPrice(lastXMR)
        #self.sleep(0.2)
        highXMR = self.highXMR
        self.ui.setHigh(highXMR)
        #self.sleep(0.2)
        lowXMR = self.lowXMR
        self.ui.setLow(lowXMR)
        #self.sleep(0.2)
        changeXMR = self.changeXMR
        self.ui.setChange(str(round(float(changeXMR)*100,2)) + " %")
        return True


    def setUSDPriceInfo(self):
        lastUSDXMR = self.lastUSDXMR
        self.ui.setXMRUSDPrice(round (float(lastUSDXMR),2))
        #self.sleep(0.2)
        #self.sleep(0.2)
        lastUSDBTC = self.lastUSDBTC
        self.ui.setBTCUSDPrice(round (float(lastUSDBTC),2))
        return True


    def getPoloInfo(self):
        self.retTicker = self.poloInstance.returnTicker()

        if self.retTicker is False:
            logging.warning("self.retTicker = None: No connection")
            return False
        else:
            self.tickerXMR = self.retTicker['BTC_XMR']
            self.tickerUSDXMR = self.retTicker['USDT_XMR']
            self.tickerUSDBTC = self.retTicker['USDT_BTC']
            self.lastXMR = self.tickerXMR['last']
            self.highXMR = self.tickerXMR['high24hr']
            self.lowXMR = self.tickerXMR['low24hr']
            self.changeXMR = self.tickerXMR['percentChange']
            self.lastUSDXMR = self.tickerUSDXMR['last']
      
            self.lastUSDBTC = self.tickerUSDBTC['last']
            return True



