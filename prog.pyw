import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QThread
import thread
import thread2
import key
import ui_ResourceFile

from main import Ui_MainWindow

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

        self.lnPublicKey.setPlaceholderText("Place here your Public Key from Poloniex..")
        self.lnSecretKey.setPlaceholderText("Place here your Secret Key from Poloniex..")




    def setMenu(self, menu):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/XMRicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        menu.setWindowIcon(icon)
        _translate = QtCore.QCoreApplication.translate
        menu.setWindowTitle(_translate("MainWindow", "Poloniex Trader by Sebastian King Walecko"))
    def setLcdMonero(self,lcdmonero):
        _translate = QtCore.QCoreApplication.translate
        self.lcdMonero.display(_translate("MainWindow", lcdmonero))
    def setLcdBitcoin(self,lcdbitcoin):
        _translate = QtCore.QCoreApplication.translate
        self.lcdBitcoin.display(_translate("MainWindow", lcdbitcoin))
    def setLcdEthereum(self,lcdethereum):
        _translate = QtCore.QCoreApplication.translate
        self.lcdEthereum.display(_translate("MainWindow", lcdethereum)) 
    def setUSDPrice(self, usd):
        _translate = QtCore.QCoreApplication.translate
        self.lnPriceUSD.setText(_translate("MainWindow", str(usd)))  
    def setCurrency(self, currency):
        _translate = QtCore.QCoreApplication.translate
        self.lnCurrency.setText(_translate("MainWindow", str(currency)))         
    def setPrice(self, price):
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
    def setLcdMoneroinclIO(self, moneroinclio):
        _translate = QtCore.QCoreApplication.translate
        self.lcdMoneroinclO.display(_translate("MainWindow", moneroinclio))
    def setLcdEthereuminclIO(self, ethereuminclio):
        _translate = QtCore.QCoreApplication.translate
        self.lcdEthereuminclO.display(_translate("MainWindow", ethereuminclio))
    def setSellBTCTotal(self, sellbtctotal):
        _translate = QtCore.QCoreApplication.translate
        self.lnSellTotal.setText(_translate("MainWindow", str(sellbtctotal)))
    def setBuyXMRAmount(self, buyxmramount):
        _translate = QtCore.QCoreApplication.translate
        self.lnBuyAmount.setText(_translate("MainWindow", str(buyxmramount)))







def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MyGui()
    form.show()
    form.setMenu(form)
    myThread = thread.Thread(form, key.PUBLIC_KEY, key.SECRET_KEY)
    myThread.start()
    myThread.clickBuy()
    myThread.clickSell()
    myThread.clickSaveConfiguration()
    myThread.cancelOrder()
    myThread2 = thread2.Thread2(form)
    myThread2.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
	main()