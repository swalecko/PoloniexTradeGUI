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
import datetime


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

    def refreshSellTotal(self):
        self.SellreadBTCprice = self.ui.lnSellPrice.text()
        self.SellreadXMRAmount = self.ui.lnSellAmount.text()
                       
        if not self.SellreadBTCprice.isalpha() and self.SellreadBTCprice != "" and not self.SellreadXMRAmount.isalpha() and self.SellreadXMRAmount != "":

            try:
                self.SellreadBTCprice = float(self.SellreadBTCprice)
                self.SellreadXMRAmount = float(self.SellreadXMRAmount)

                self.calcSellBTCTotal(self.SellreadBTCprice, self.SellreadXMRAmount)
            except ValueError:
                self.ui.lnSellTotal.setText("0.0")
        else:
            pass
    def refreshBuyAmount(self):
        self.BuyreadBTCprice = self.ui.lnBuyPrice.text()
        self.BuyreadBTCTotal = self.ui.lnBuyTotal.text() 

        
        if not self.BuyreadBTCprice.isalpha() and self.BuyreadBTCprice != "" and not self.BuyreadBTCTotal.isalpha() and self.BuyreadBTCTotal != "":
        
            try:
                self.BuyreadBTCprice = float(self.BuyreadBTCprice)        
                self.BuyreadBTCTotal = float(self.BuyreadBTCTotal)
                self.calcBuyAmount(self.BuyreadBTCprice, self.BuyreadBTCTotal)
            except ValueError:
                self.ui.lnBuyAmount.setText("0.0")
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

            self.ui.setAmountMonero(self.BalanceXMR)
            self.ui.setAmountBitcoin(self.BalanceBTC)

            count = 0
            OOAmount = 0

            if self.countOpenOrdersXMR != 0:
                for i in range(self.countOpenOrdersXMR):

                    if self.retOpenOrdersXMR[i]["type"] == "buy":
                        OOAmount = float(self.retOpenOrdersXMR[i]["amount"])
                        count = count + OOAmount
                    #else:
                    #    OOAmount = float(self.retOpenOrdersXMR[i]["amount"])
                    #    count = count - OOAmount
     
                CompleteAmount = format(count + float(self.BalanceXMR), '.8f')
                self.ui.setAmountMoneroinclIO(str(CompleteAmount))

            else:
                self.ui.setAmountMoneroinclIO(format(float(0.00000000), '.8f')) 
            print ("Balances refreshed...")   

    def popup(self, text, art):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #msg.setIcon(art)

        if art == "success":
            msg.setIconPixmap(QPixmap("C:\Projekte\PoloniexTradeGUI\/resource\checked.png"))
        elif art == "failed":
            msg.setIconPixmap(QPixmap("C:\Projekte\PoloniexTradeGUI\/resource\cancel.png"))
        else:
            msg.setIcon(art)
 
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QWidget {color: gray; padding-right: 10px;} QMessageBox {background-color: white; border-width: 1px; border-color:gray; border-style: solid; border-radius: 4;} QPushButton{color: gray; background-color: white; border-width: 1px;border-color: gray; border-style: solid;border-radius: 3;padding: 3px;font-size: 12px;padding-left: 5px;padding-right: 5px;} QPushButton:focus:pressed{background-color: rgb(235, 235, 235);} QPushButton:hover{ background-color: rgb(218, 218, 218);}")
        #msg.setStyleSheet("QWidget {color: gray; padding-right: 10px;} QMessageBox {background-color: white; border-width: 1px; border-color:gray; border-style: solid; border-radius: 4;}QPushButton:pressed{ background-color: orange; } QPushButton{ background-color: white;} QPushButton:disabled{ color: rgb(234, 234, 234); background-color: rgb(240, 240, 240); }QPushButton:focus:pressed{background-color: rgb(235, 235, 235);}QPushButton:hover{ background-color: rgb(218, 218, 218);}QPushButton:checked{ background-color: pink; }")



        msg.exec_()

    def confirmPopup(self, text):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msg.setIcon(QMessageBox.Question)
 
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Abort)
        btnConfirm = msg.button(QMessageBox.Ok)
        btnConfirm.setText("  Confirm  ")
        msg.setStyleSheet("QWidget {color: gray; padding-right: 10px;} QMessageBox {background-color: white; border-width: 1px; border-color:gray; border-style: solid; border-radius: 4;} QPushButton{color: gray; background-color: white; border-width: 1px;border-color: gray; border-style: solid;border-radius: 3;padding: 3px;font-size: 12px;padding-left: 5px;padding-right: 5px;} QPushButton:focus:pressed{background-color: rgb(235, 235, 235);} QPushButton:hover{ background-color: rgb(218, 218, 218);}")
        #msg.setStyleSheet("QWidget {color: gray; padding-right: 10px;} QMessageBox {background-color: white; border-width: 1px; border-color:gray; border-style: solid; border-radius: 4;}QPushButton:pressed{ background-color: orange; } QPushButton{ background-color: white;} QPushButton:disabled{ color: rgb(234, 234, 234); background-color: rgb(240, 240, 240); }QPushButton:focus:pressed{background-color: rgb(235, 235, 235);}QPushButton:hover{ background-color: rgb(218, 218, 218);}QPushButton:checked{ background-color: pink; }")
        ret = msg.exec_()

        if ret == QMessageBox.Ok:
            return True
        elif ret == QMessageBox.Abort:
            return False
                          
    def download(self, progress):
        while self.completed < progress:
            self.completed += 1
            self.ui.GprogressBar.setValue(self.completed)
    def clickRefresh(self):
        self.ui.btnRefresh.clicked.connect(self.clickedRefresh)
    
    def clickedRefresh(self):

        self.ui.GprogressBar.setMinimum(0)
        self.ui.GprogressBar.setMaximum(100)

        self.ui.GprogressBar.show()
        self.ui.GprogressBar.setValue(0)

        self.completed = 0
       
        if self.RefreshOO() is False:
            logging.critical("Refresh Open Orders failed")
            self.popup("Refresh failed \nPlease check your network connectivity and try again",QMessageBox.Warning)
        else:
            self.download(30)
     
            if self.RefreshHistory() is False:
                logging.critical("Refresh History failed")
                self.popup("Refresh failed \nPlease check your network connectivity and try again",QMessageBox.Warning)
                self.setProgressBarcs("red")
            else:
                self.download(50)
        
                if self.showBalances() is False:
                    logging.critical("Refresh Balances failed")
                    self.popup("Refresh failed \nPlease check your network connectivity and try again",QMessageBox.Warning)
                    self.setProgressBarcs("red")
                else:
                    self.stateButtons(sell=True, buy=True, refresh=True)
                    self.download(75)
                    if self.calcMyAssets() is False:
                        logging.critical("Refresh Asset failed")
                        self.popup("Refresh failed \nPlease check your network connectivity and try again",QMessageBox.Warning)
                        self.setProgressBarcs("red")
                    else:
                        self.download(100)
                        self.ui.lblLast.setText(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        self.setProgressBarcs("green")
                        

        self.stateRefresh = 1

    def setProgressBarcs(self, type):
        if type == "green":
            self.ui.GprogressBar.setStyleSheet("QProgressBar::chunk {background-color: rgb(0, 244, 0);} QProgressBar{border: 1px solid transparent;text-align: center;color:rgba(0,0,0,100);background-color: rgb(76, 76, 76);}")
        elif type == "orange":
            self.ui.GprogressBar.setStyleSheet("QProgressBar::chunk {background-color: rgb(255, 170, 0);} QProgressBar{border: 1px solid transparent;text-align: center;color:rgba(0,0,0,100);background-color: rgb(76, 76, 76);}")
        else:
            self.ui.GprogressBar.setStyleSheet("QProgressBar::chunk {background-color: rgb(255, 0, 0);} QProgressBar{border: 1px solid transparent;text-align: center;color:rgba(0,0,0,100);background-color: rgb(76, 76, 76);}")


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
                    self.ui.setHistory(i,0, QTableWidgetItem(currency))
                    self.ui.setHistory(i,1, QTableWidgetItem(rethistory[i]["type"]))
                    self.ui.setHistory(i,2, QTableWidgetItem(rethistory[i]["rate"]))
                    self.ui.setHistory(i,3, QTableWidgetItem(rethistory[i]["amount"]))
                    self.ui.setHistory(i,4, QTableWidgetItem(rethistory[i]["date"]))


                    if rethistory[i]["type"] == "sell":
                        historywidget.item(i, 1).setBackground(QtGui.QColor(176,10,49))
                        historywidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                    else:
                        historywidget.item(i, 1).setBackground(QtGui.QColor(0,139,0))
                        historywidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))

            self.ui.lblcountHistory.setText(str(counthistory))

            print ("History refreshed...")
    
    def calcMyAssets(self):
        
        XMRUSDPRICE = self.ui.lnPriceUSD.text()
        BTCUSDPRICE = self.ui.lnBTCPriceUSD.text()
        
        if XMRUSDPRICE != "" or BTCUSDPRICE != "":

            XMRUSDPRICE = float(XMRUSDPRICE)
            BTCUSDPRICE = float(BTCUSDPRICE)


            XMRAmount = float(self.ui.lnMonero.text())
            BTCAmount = float(self.ui.lnBitcoin.text())

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
                        openorderswidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                        #openorderswidget.item(i, 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
                                             
                    else:
                        openorderswidget.item(i, 1).setBackground(QtGui.QColor(0,139,0))
                        openorderswidget.item(i, 1).setForeground(QtGui.QColor(255,255,255))
                        #openorderswidget.item(i, 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

            self.ui.lblcountOO.setText(str(countopenorders))
            print ("Open Orders refreshed...")

    def clickSaveConfiguration(self):
        self.ui.saveButton.clicked.connect(self.clickedSaveConfiguration)
    def clickedSaveConfiguration(self):
        inputPublicKey = self.ui.lnPublicKey.text().strip()
        inputSecretKey = self.ui.lnSecretKey.text().strip()

        if (inputPublicKey == "" or inputSecretKey == ""):
            logging.warning("Invalid keys \nAPI keys not saved")
            self.popup("Invalid keys \nAPI keys not saved", QMessageBox.Warning)
        
        else:
            with open("key.py", "w") as keyfile:
                keyfile.write("PUBLIC_KEY = '" + inputPublicKey + "' \nSECRET_KEY = '" + inputSecretKey + "'")
            logging.info("API Keys succesfully saved")
            self.popup("API Keys saved \nRestart the app to activate the API keys", QMessageBox.Information)
        
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

        if self.retTicker is None or self.ui.lblPoloniexStatusResult.text() == "N/A" or self.ui.lblPoloniexStatusResult.text() == "Disconnected":
            logging.warning("self.retTicker = None: Ticker not refreshed")
            self.popup("Price not set \nPlease check your network connectivity and try again", QMessageBox.Warning)
        else:
            self.tickerXMR = self.retTicker['BTC_XMR']
            self.lastXMR = self.tickerXMR['last']     
            self.ui.setSellBTCPrice(self.lastXMR)
    def clickBuyGetBTCTotal(self):
        self.ui.btnBuyGetBTCTotal.clicked.connect(self.clickedBuyGetBTCTotal)
    def clickedBuyGetBTCTotal(self):
        if self.ui.lnBitcoin.text() != "N/A":
            self.ui.setBuyBTCTotal(self.BalanceBTC)
    
    def clickBuy(self):
        self.ui.buyButton.clicked.connect(self.clickedBuy)
    def clickedBuy(self):
        try:
            BuyreadBTCprice = float(self.ui.lnBuyPrice.text())
            resultBuyXMRAmount = float(self.ui.lnBuyAmount.text())
            buyreadbtctotal = float(self.ui.lnBuyTotal.text())

            if (BuyreadBTCprice != 0 or BuyreadBTCprice != 0.0) and (buyreadbtctotal != 0 or buyreadbtctotal != 0.0):

                if buyreadbtctotal > float(self.BalanceBTC):
                    self.popup("Invalid Amount \nPlease check your Balance", QMessageBox.Warning)
                else:

                    text = "Buy: Order details \n\nPrice: " + str(BuyreadBTCprice) + " BTC" + "\nAmount: " + str(resultBuyXMRAmount) + " XMR"

                    if self.confirmPopup(text) == True:

                        exeBuy = self.poloInstance.buy("BTC_XMR",BuyreadBTCprice,resultBuyXMRAmount)
                        QtCore.QCoreApplication.processEvents()

                        if exeBuy is False:
                            self.popup("Buy order not placed \nPlease check your network connectivity and try again", "failed")
                        elif "error" in exeBuy and exeBuy["error"] == "Total must be at least 0.0001.":
                            self.popup("Buy order not placed \nTotal must be at least 0.0001", "failed")
                        else:
                            if "orderNumber" in exeBuy and exeBuy["orderNumber"] != '':
                                logging.info("Buy Order placed: " + str(exeBuy["orderNumber"]))
                                self.popup("Buy order placed \n\n" + "Order Number: " + str(exeBuy["orderNumber"]), "success")
                                self.setProgressBarcs("orange")
                            else:
                                logging.debug("Buy Order failed! " + str(e))
                                self.popup("Place buy order failed", "failed")
                    else:
                        self.popup("Buy Order aborted", QMessageBox.Information)
            else:
                self.popup("Invalid input", QMessageBox.Warning)
        except ValueError:
            self.popup("Invalid input", QMessageBox.Warning)
            
    def clickSell(self):
        self.ui.sellButton.clicked.connect(self.clickedSell)
    def clickedSell(self):
        try:
            SellreadBTCprice = float(self.ui.lnSellPrice.text())
            SellreadXMRAmount = float(self.ui.lnSellAmount.text())

            if (SellreadBTCprice != 0 or SellreadBTCprice != 0.0) and (SellreadXMRAmount != 0 or SellreadXMRAmount != 0.0):

                if SellreadXMRAmount > float(self.BalanceXMR):
                    self.popup("Invalid Amount \nPlease check your Balance", QMessageBox.Warning)
                else:     

                    text = "Sell: Order details \n\nPrice: " + str(SellreadBTCprice) + " BTC" + "\nAmount: " + str(SellreadXMRAmount) + " XMR"

                    if self.confirmPopup(text) == True:
                    
                        exeSell = self.poloInstance.sell("BTC_XMR",SellreadBTCprice, SellreadXMRAmount)

                        if exeSell is False:
                            self.popup("Sell order not placed \nPlease check your network connectivity and try again", "failed")
                        elif "error" in exeSell and exeSell["error"] == "Invalid amount parameter.":
                            self.popup("Sell order not placed \nInvalid amount parameter", "failed")
                        else:
                            if "orderNumber" in exeSell and exeSell["orderNumber"] != '':
                                logging.info("Sell Order placed: " + str(exeSell["orderNumber"]))
                                self.popup("Sell order placed \n\n" + "Order Number: " + str(exeSell["orderNumber"]) , "success")
                                self.setProgressBarcs("orange")

                            else:
                                logging.debug("Place sell Order failed")
                                self.popup("Place sell order failed", "failed")
                    else:
                        self.popup("Sell Order aborted", QMessageBox.Information)
            else:
                self.popup("Invalid input", QMessageBox.Warning)

        except ValueError:
            self.popup("Invalid input", QMessageBox.Warning)

    def cancelOrder(self):
        self.ui.OpenOrdersWidgetXMR.cellDoubleClicked.connect(self.double_clicked)
    def double_clicked(self):
        orderNumberXMR = self.ui.OpenOrdersWidgetXMR.currentItem().text()
        
        text = "Cancel: Order details \n\nOrder Number: " + str(orderNumberXMR)

        if self.confirmPopup(text) == True:

            resultCancel = self.poloInstance.cancel("BTC_XMR", orderNumberXMR)
            QtCore.QCoreApplication.processEvents()
            
            if resultCancel is False:
                self.popup("Order not canceled \nPlease check your network connectivity and try again", "failed")
            else:

                if resultCancel["success"] == 1:
                    logging.info("Order canceled succesfully: " + str(orderNumberXMR))
                    self.popup("Order canceled \n\n" + "Order Number: " + str(orderNumberXMR), "success")
                    self.setProgressBarcs("orange")                
                else:
                    logging.debug("Order could not be canceled")
                    self.popup("Order could not be canceled \nPlease try again", "failed")
        else:
            self.popup("Cancel Order aborted", QMessageBox.Information)

    def setXMRPriceInfo(self):
        lastXMR = self.lastXMR
        self.ui.setXMRPrice(lastXMR)

        highXMR = self.highXMR
        self.ui.setHigh(highXMR)

        lowXMR = self.lowXMR
        self.ui.setLow(lowXMR)

        changeXMR = self.changeXMR
        self.ui.setChange(str(round(float(changeXMR)*100,2)) + " %")
        return True


    def setUSDPriceInfo(self):
        lastUSDXMR = self.lastUSDXMR
        self.ui.setXMRUSDPrice(round (float(lastUSDXMR),2))

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

    def clickMenuOO(self):
        self.ui.btnOO.clicked.connect(self.openOO)

    def openOO(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def clickMenuHistory(self):
        self.ui.btnHistory.clicked.connect(self.openHistory)

    def openHistory(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def clickMenuTrading(self):
        self.ui.btnTrading.clicked.connect(self.openTrading)

    def openTrading(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def clickMenuConfiguration(self):
        self.ui.btnConfiguration.clicked.connect(self.openConfiguration)

    def openConfiguration(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def clickMenuExit(self):
        self.ui.btnExit.clicked.connect(self.clickedExit)
    def clickedExit(self):    
        sys.exit()

    def clickMenuMini(self):
        self.ui.btnMini.clicked.connect(self.clickedMini)
        
    def clickedMini(self):
        self.ui.showMinimized()

    def qlineSellPriceChanged(self):
        self.ui.lnSellPrice.textChanged.connect(self.refreshSellTotal)
    
    def qlineSellAmountChanged(self):
        self.ui.lnSellAmount.textChanged.connect(self.refreshSellTotal)
    
    def qlineBuyPriceChanged(self):
        self.ui.lnBuyPrice.textChanged.connect(self.refreshBuyAmount)
    
    def qlineBuyTotalChanged(self):
        self.ui.lnBuyTotal.textChanged.connect(self.refreshBuyAmount)


