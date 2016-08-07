import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import QThread

keypath = os.path.abspath('key.py')

if not os.path.exists(keypath) or os.stat(keypath).st_size == 0:
    with open(keypath, "w") as keyfile:
        keyfile.write("PUBLIC_KEY = ''\nSECRET_KEY = ''")
        keyfile.close()

from importlib.machinery import SourceFileLoader

importkey = SourceFileLoader("key", keypath).load_module()

import main_thread
import thread_getusd
import thread_getcrypto
import ui_ResourceFile
from main import Ui_MainWindow
import logging


class MyGui(QtWidgets.QMainWindow, Ui_MainWindow, logging.Handler):    
    def __init__(self, parent=None):
        super(MyGui, self).__init__(parent)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setObjectTransparent(self)
        
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate      
        self.lnSellPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnSellAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnSellTotal.setText(_translate("MainWindow", str(0.0)))
        self.lnBuyPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnBuyAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnBuyTotal.setText(_translate("MainWindow", str(0.0))) 
        self.lnETHSellPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnETHSellAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnETHSellTotal.setText(_translate("MainWindow", str(0.0)))
        self.lnETHBuyPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnETHBuyAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnETHBuyTotal.setText(_translate("MainWindow", str(0.0))) 
        self.lnPublicKey.setPlaceholderText("Insert your Poloniex Public key..")
        self.lnSecretKey.setPlaceholderText("Insert your Poloniex Secret key..")
        
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
    def setXMRPrice(self, price):
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
    def setETHUSDPrice(self, ethusd):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHPriceUSD.setText(_translate("MainWindow", str(ethusd)))
    def setBTCUSDPrice(self, btcusd):
        _translate = QtCore.QCoreApplication.translate
        self.lnBTCPriceUSD.setText(_translate("MainWindow", str(btcusd)))   

    def setETHPrice(self, ethprice):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceETH.setText(_translate("MainWindow", str(ethprice)))
    def setETHHigh(self, ethhigh):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHHigh.setText(_translate("MainWindow", str(ethhigh)))
    def setETHLow(self, ethlow):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHLow.setText(_translate("MainWindow", str(ethlow)))        
    def setETHChange(self, ethchange):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHChange.setText(_translate("MainWindow", ethchange))  
    def setLcdMoneroinclIO(self, moneroinclio):
        _translate = QtCore.QCoreApplication.translate

        if float(moneroinclio) > 0.0:
            self.lcdMoneroinclO.setPalette(self.palettegreen)
        else:
            self.lcdMoneroinclO.setPalette(self.palettered)

        self.lcdMoneroinclO.display(_translate("MainWindow", moneroinclio))
    def setLcdEthereuminclIO(self, ethereuminclio):
        _translate = QtCore.QCoreApplication.translate

        if float(ethereuminclio) > 0.0:
            self.lcdEthereuminclO.setPalette(self.palettegreen)
        else:
            self.lcdEthereuminclO.setPalette(self.palettered)

        self.lcdEthereuminclO.display(_translate("MainWindow", ethereuminclio))
    def setSellBTCTotal(self, sellbtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnSellTotal.setText(_translate("MainWindow", str(sellbtctotal)))
    def setETHSellBTCTotal(self, sellbtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHSellTotal.setText(_translate("MainWindow", str(sellbtctotal)))
    def setSellBTCPrice(self, sellbtcprice):
        _translate = QtCore.QCoreApplication.translate
        self.lnSellPrice.setText(_translate("MainWindow", str(sellbtcprice)))
    def setETHSellBTCPrice(self, sellbtcprice):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHSellPrice.setText(_translate("MainWindow", str(sellbtcprice)))   
    def setBuyXMRAmount(self, buyxmramount):
        _translate = QtCore.QCoreApplication.translate
        self.lnBuyAmount.setText(_translate("MainWindow", str(buyxmramount)))
    def setBuyETHAmount(self, buyethamount):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHBuyAmount.setText(_translate("MainWindow", str(buyethamount)))
    def setBuyBTCTotal(self, buybtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnBuyTotal.setText(_translate("MainWindow", str(buybtctotal)))
    def setETHBuyBTCTotal(self, buybtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnETHBuyTotal.setText(_translate("MainWindow", str(buybtctotal)))
    def setAppStatus(self, appstatus):
        _translate = QtCore.QCoreApplication.translate
        self.lblAppStatusResult.setText(_translate("MainWindow", str(appstatus)))
    def setNetworkStatus(self, networkstatus):
        _translate = QtCore.QCoreApplication.translate
        self.lblNetworkStatusResult.setText(_translate("MainWindow", str(networkstatus)))
    def setLog(self, log):
       _translate = QtCore.QCoreApplication.translate
       self.plainTextEdit.appendPlainText(log)
    def setMyAssets(self, myassets):
       _translate = QtCore.QCoreApplication.translate
       self.lnMyAssets.setText(str(myassets))




def main():
    logging.basicConfig(filename="qt.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
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
    
    myThread.clickETHBuy()
    myThread.clickETHSell()
    myThread.clickETHSellGetBTCPrice()
    myThread.clickETHBuyGetBTCTotal()
    myThread.cancelETHOrder()
    
    myThread.clickSaveConfiguration()
    myThread_getusd = thread_getusd.Thread(form)
    myThread_getusd.start()

    myThread_getcrypto = thread_getcrypto.Thread(form)
    myThread_getcrypto.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
	main()