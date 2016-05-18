import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QThread
import main_thread
import thread_getusd
import ui_ResourceFile
from main import Ui_MainWindow
import key

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
        self.lnETHSellPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnETHSellAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnETHSellTotal.setText(_translate("MainWindow", str(0.0)))
        self.lnETHBuyPrice.setText(_translate("MainWindow", str(0.0))) 
        self.lnETHBuyAmount.setText(_translate("MainWindow", str(0.0)))
        self.lnETHBuyTotal.setText(_translate("MainWindow", str(0.0))) 
        self.lnPublicKey.setPlaceholderText("Insert your Poloniex Public key..")
        self.lnSecretKey.setPlaceholderText("Insert your Poloniex Secret key..")
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
        self.lcdMonero.display(_translate("MainWindow", lcdmonero))
    def setLcdBitcoin(self,lcdbitcoin):
        _translate = QtCore.QCoreApplication.translate
        self.lcdBitcoin.display(_translate("MainWindow", lcdbitcoin))
    def setLcdEthereum(self,lcdethereum):
        _translate = QtCore.QCoreApplication.translate
        self.lcdEthereum.display(_translate("MainWindow", lcdethereum)) 
    def setXMRUSDPrice(self, xmrusd):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceUSD.setText(_translate("MainWindow", str(xmrusd))) 
    def setXMRPrice(self, price):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceBTC.setText(_translate("MainWindow", str(price)))
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
        self.lcdMoneroinclO.display(_translate("MainWindow", moneroinclio))
    def setLcdEthereuminclIO(self, ethereuminclio):
        _translate = QtCore.QCoreApplication.translate
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MyGui()
    form.show()
    form.setMenu(form)
    myThread = main_thread.Thread(form, key.PUBLIC_KEY, key.SECRET_KEY)
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
    sys.exit(app.exec_())

if __name__ == "__main__":
	main()