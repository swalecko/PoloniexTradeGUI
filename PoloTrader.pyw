import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QPlainTextEdit, QProgressBar


keypath = os.path.abspath('key.py')

if not os.path.exists(keypath) or os.stat(keypath).st_size == 0:
    with open(keypath, "w") as keyfile:
        keyfile.write("PUBLIC_KEY = ''\nSECRET_KEY = ''")
        keyfile.close()

from importlib.machinery import SourceFileLoader

importkey = SourceFileLoader("key", keypath).load_module()

import main_thread
import ui_ResourceFile
from main import Ui_MainWindow
import logging


class MyGui(QtWidgets.QMainWindow, Ui_MainWindow):    
    def __init__(self, parent=None):
        super(MyGui, self).__init__(parent)

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
        self.setWindowTitle(_translate("MainWindow", "Poloniex Monero Trading"))       
        self.palettegreen = QPalette()
        self.palettegreen.setColor(self.palettegreen.WindowText, QColor(120,255,195))
        self.palettered = QPalette()
        self.palettered.setColor(self.palettered.WindowText, QColor(216,32,32))
    
    def setTaskWindowTitle(self, gui, price):
        self.gui = gui
        _translate = QtCore.QCoreApplication.translate
        self.gui.setWindowTitle(_translate("MainWindow", str(price)))
    def setMenu(self, menu):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/XMRicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        menu.setWindowIcon(icon)
        _translate = QtCore.QCoreApplication.translate
    def setLcdMonero(self,lcdmonero):
        _translate = QtCore.QCoreApplication.translate
        
        if float(lcdmonero) > 0.0:
            self.lcdMonero.setPalette(self.palettegreen)
        else:
            self.lcdMonero.setPalette(self.palettered)

        self.lcdMonero.display(_translate("MainWindow", lcdmonero))
    def setLcdBitcoin(self,lcdbitcoin):
        _translate = QtCore.QCoreApplication.translate

        if float(lcdbitcoin) > 0.0:
            self.lcdBitcoin.setPalette(self.palettegreen)
        else:
            self.lcdBitcoin.setPalette(self.palettered)

        self.lcdBitcoin.display(_translate("MainWindow", str(lcdbitcoin)))
    def setLcdEthereum(self,lcdethereum):
        _translate = QtCore.QCoreApplication.translate

        if float(lcdethereum) > 0.0:
            self.lcdEthereum.setPalette(self.palettegreen)
        else:
            self.lcdEthereum.setPalette(self.palettered)

        self.lcdEthereum.display(_translate("MainWindow", lcdethereum)) 
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
    def setLcdMoneroinclIO(self, moneroinclio):
        _translate = QtCore.QCoreApplication.translate

        if float(moneroinclio) > 0.0:
            self.lcdMoneroinclO.setPalette(self.palettegreen)
        else:
            self.lcdMoneroinclO.setPalette(self.palettered)

        self.lcdMoneroinclO.display(_translate("MainWindow", moneroinclio))
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
     def setLog(self, log):
       _translate = QtCore.QCoreApplication.translate
       self.plainTextEdit.appendPlainText(log)
    def setMyAssets(self, myassets):
       _translate = QtCore.QCoreApplication.translate
       self.lnMyAssets.setText(str(myassets))
    def setOpenOrders(self, row, col, typ):
       _translate = QtCore.QCoreApplication.translate
       try:
            self.OpenOrdersWidgetXMR.setItem(row, col, QTableWidgetItem(typ))   
       except Exception as e:
            print (str(e))
     
    def setOpenOrdersRowCount(self, c):
        _translate = QtCore.QCoreApplication.translate
        #print ("setOpenOrdersRowCount: " + str(c))
        self.OpenOrdersWidgetXMR.setRowCount(c)
        #self.OpenOrdersWidgetETH.setRowCount(c)

def main():
    logging.basicConfig(filename="qt.log", level=logging.INFO, format='{asctime} {filename} {lineno} [{levelname:8}] {message}', datefmt='%m/%d/%Y %I:%M:%S', style = "{")
    logging.getLogger("requests").setLevel(logging.WARNING)
    app = QtWidgets.QApplication(sys.argv)
    form = MyGui()
    form.show()
    form.setMenu(form)

    myThread = main_thread.Thread(form, importkey.PUBLIC_KEY, importkey.SECRET_KEY)
    myThread.start()
    myThread.clickBuy()
    myThread.clickSell()
    myThread.clickSellGetBTCPrice()
    myThread.clickBuyGetBTCTotal()
    myThread.cancelOrder() 
    myThread.clickRefresh()
    myThread.clickXmrChart() 
    myThread.clickSaveConfiguration()
    sys.exit(app.exec_())

if __name__ == "__main__":
	main()