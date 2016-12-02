# PoloniexTradeGUI
(unofficial)

 [![Documentation](https://codedocs.xyz/swalecko/PoloniexTradeGUI.svg)](https://codedocs.xyz/swalecko/PoloniexTradeGUI/)
 

**Donations:** 
XMR: 49wH4MLdp62BrG7pUuh7dJ51icq1T2edpNJpHt7R2qoJTpuR7oK81jWXxH5K6Rz1nZHneK24jj7XdZDmc7U2W2dH8aso46n

Trading app for Monero(XMR) at the Poloniex exchange using the Poloniex API.

##Current Features:
  - Supported Currencies for trading: XMR
  - Price informations 
  - Balances, Balances included open orders
  - 24h High, 24h Low and 24h Change 
  - Open Orders 
    - Note: to cancel an open order double click the cell with the order number
  - History 
  - Display your current overall Asset in USD
  - Manually request Poloniex values with "Refresh" Button
  - Trading (Simple Buy and Sell)
    - Note: "A" Auto Button for setting current BTC price in the sell section and Total BTC in the buy section 
    - Note: Automatically calculated Total(BTC) on the sell side
    - Note: Automatically calculated Amount(XMR) on the buy side 
  - Configuration: Poloniex Public and Secret Key

##Future Features:
  - There's more to come..
  
##Pre-Information:
  - Based on Qt 5.5.1
  - Using Qt Creator for the design
  - Using Pyqt for the python code
  - Written in Python 3
  
##Download and Configuration:  

  **Windows**  
  - Download PoloTrader_1.x.x_Win.zip from the latest release
  - Unzip PoloTrader_1.x.x_Win.zip
  - Execute PoloTrader.exe (Info: exe file is created with pyinstaller)
  - 2 files (key.py, qt.log) will be created in the same directory 
  - Restart the program to activate the API keys
  - Now you should see your Balances and you are able to trade
  - Info: If you have some problems, just restart the program 

## How to Use:
  - Insert your Poloniex API keys into configuration tab and save them. You can check your keys in the key.py file
  	- Restart the program to activate the API keys
  	- Now you should see your Balances and you are able to trade
  - Buy and Sell Button will be activated after the first manually refresh with the "Refresh" Button
  - It is recommended to refresh your values after every sell, buy or cancel Order
  - Canceling Order with double click on the Order Number in the Open Orders view

**Linux**
  - Just contact me for more informations

##Screenshot:

![Screenshot](https://raw.github.com/swalecko/PoloTradeGui/master/Dashboard_screenshot.JPG?raw=true "Open Orders Tab")




