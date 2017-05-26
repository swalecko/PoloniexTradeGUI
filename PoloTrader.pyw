import os
import sys
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QGraphicsColorizeEffect
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QPlainTextEdit, QProgressBar


keypath = os.path.abspath('key.py')

if not os.path.exists(keypath) or os.stat(keypath).st_size == 0:
    with open(keypath, "w") as keyfile:
        keyfile.write("PUBLIC_KEY = ''\nSECRET_KEY = ''")
        keyfile.close()

from importlib.machinery import SourceFileLoader

importkey = SourceFileLoader("key", keypath).load_module()

import main_thread
import res_rc
import logging
from main import Ui_MainWindow
import trace
 
class MyGui(QtWidgets.QMainWindow, Ui_MainWindow):   
    def __init__(self, parent=None):
        super(MyGui, self).__init__(parent)
        #self.ui = uic.loadUi("mainwindow.ui", self)

        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate      
        self.lnSellPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnSellAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnSellTotal.setText(_translate("MainWindow", str(0.0)))
        self.lnBuyPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnBuyAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnBuyTotal.setText(_translate("MainWindow", str(0.0))) 
        self.lnPublicKey.setPlaceholderText("Insert your Poloniex Public key..")
        self.lnSecretKey.setPlaceholderText("Insert your Poloniex Secret key..")
        self.setWindowTitle(_translate("MainWindow", "Monero Trading"))    
        self.palettegreen = QPalette()
        self.palettegreen.setColor(self.palettegreen.WindowText, QColor(112,245,20))
        self.palettered = QPalette()
        self.palettered.setColor(self.palettered.WindowText, QColor(216,32,32))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)    

    def setAmountMonero(self,amountmonero):
        _translate = QtCore.QCoreApplication.translate
        
        if float(amountmonero) > 0.0:
            self.lnMonero.setPalette(self.palettegreen)
        else:
            self.lnMonero.setPalette(self.palettered)
        _translate = QtCore.QCoreApplication.translate
        self.lnMonero.setText(_translate("MainWindow", str(amountmonero)))
    
    def setAmountMoneroinclIO(self, moneroinclio):
        _translate = QtCore.QCoreApplication.translate

        if float(moneroinclio) > 0.0:
            self.lnMoneroOO.setPalette(self.palettegreen)
        else:
            self.lnMoneroOO.setPalette(self.palettered)

        self.lnMoneroOO.setText(_translate("MainWindow", str(moneroinclio)))
    
    def setAmountBitcoin(self,amountbitcoin):
        _translate = QtCore.QCoreApplication.translate

        if float(amountbitcoin) > 0.0:
            self.lnBitcoin.setPalette(self.palettegreen)
        else:
            self.lnBitcoin.setPalette(self.palettered)

        self.lnBitcoin.setText(_translate("MainWindow", str(amountbitcoin)))
    
    def setXMRUSDPrice(self, xmrusd):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceUSD.setText(_translate("MainWindow", str(xmrusd))) 
    
    def setXMRPrice(self,price):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceXMR.setText(_translate("MainWindow", str(price)))
    
    def setHigh(self, high):
        _translate = QtCore.QCoreApplication.translate
        self.lnHigh.setText(_translate("MainWindow", str(high)))
    
    def setLow(self, low):
        _translate = QtCore.QCoreApplication.translate
        self.lnLow.setText(_translate("MainWindow", str(low)))     
    
    def setChange(self, change):
        _translate = QtCore.QCoreApplication.translate
        self.lnChange.setText(_translate("MainWindow", change))
    
    def setBTCUSDPrice(self, btcusd):
        _translate = QtCore.QCoreApplication.translate
        self.lnBTCPriceUSD.setText(_translate("MainWindow", str(btcusd)))   
    
    def setSellBTCTotal(self, sellbtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnSellTotal.setText(_translate("MainWindow", str(sellbtctotal)))
    
    def setETHSellBTCTotal(self, sellbtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHSellTotal.setText(_translate("MainWindow", str(sellbtctotal)))
    
    def setSellBTCPrice(self, sellbtcprice):
        _translate = QtCore.QCoreApplication.translate
        self.lnSellPrice.setText(_translate("MainWindow", str(sellbtcprice)))
    
    def setBuyXMRAmount(self, buyxmramount):
        _translate = QtCore.QCoreApplication.translate
        self.lnBuyAmount.setText(_translate("MainWindow", str(buyxmramount)))
    
    def setBuyBTCTotal(self, buybtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnBuyTotal.setText(_translate("MainWindow", str(buybtctotal)))
    
    def setAppStatus(self, appstatus):
        _translate = QtCore.QCoreApplication.translate
        self.lblAppStatusResult.setText(_translate("MainWindow", str(appstatus)))
    
    def setPoloniexStatus(self, poloniexstatus):
        _translate = QtCore.QCoreApplication.translate
        self.lblPoloniexStatusResult.setText(_translate("MainWindow", str(poloniexstatus)))

    def setMyAssets(self, myassets):
       _translate = QtCore.QCoreApplication.translate
       self.lnMyAssets.setText(str(myassets))
    
    def setOpenOrders(self, row, col, typ):
       _translate = QtCore.QCoreApplication.translate
       try:
            self.OpenOrdersWidgetXMR.setItem(row, col, QTableWidgetItem(typ))
            self.OpenOrdersWidgetXMR.item(row,col).setTextAlignment(QtCore.Qt.AlignCenter)
           
       except Exception as e:
            print (str(e))
     
    def setHistory(self, row, col, typ):
        _translate = QtCore.QCoreApplication.translate
        try:
            self.HistoryWidgetXMR.setItem(row, col, QTableWidgetItem(typ))
            self.HistoryWidgetXMR.item(row,col).setTextAlignment(QtCore.Qt.AlignCenter)
        
        except Exception as e:
            print (str(e))

    def setOpenOrdersRowCount(self, c):
        _translate = QtCore.QCoreApplication.translate
        self.OpenOrdersWidgetXMR.setRowCount(c)

def main():
    logging.basicConfig(filename="qt.log", level=logging.INFO, format='{asctime} {filename} {lineno} [{levelname:8}] {message}', datefmt='%m/%d/%Y %I:%M:%S', style = "{")
    logging.getLogger("requests").setLevel(logging.WARNING)
    app = QtWidgets.QApplication(sys.argv)
    form = MyGui()
    form.show()

    myThread = main_thread.Thread(form, importkey.PUBLIC_KEY, importkey.SECRET_KEY)
    myThread.start()
    myThread.clickBuy()
    myThread.clickSell()
    myThread.clickSellGetBTCPrice()
    myThread.clickBuyGetBTCTotal()
    myThread.cancelOrder() 
    myThread.clickRefresh()
    myThread.clickMenuOO()
    myThread.clickMenuHistory()
    myThread.clickMenuConfiguration()
    myThread.clickMenuTrading()
    myThread.clickMenuExit()
    myThread.clickMenuMini()
    myThread.clickSaveConfiguration()
    myThread.qlineSellPriceChanged()
    myThread.qlineSellAmountChanged()
    myThread.qlineBuyPriceChanged()
    myThread.qlineBuyTotalChanged()

    app.exec_()
if __name__ == "__main__":
    #tracer = trace.Trace()
    #tracer.run("main()")
    #r = tracer.results()
    #r.write_results(show_missing=True, coverdir=ergebnis)
    main()