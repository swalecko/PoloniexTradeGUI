# PoloniexTradeGUI
(unofficial)

##Use at your own risk!

 [![Documentation](https://codedocs.xyz/swalecko/PoloniexTradeGUI.svg)](https://codedocs.xyz/swalecko/PoloniexTradeGUI/)
 

**Donations:** 
XMR: 49wH4MLdp62BrG7pUuh7dJ51icq1T2edpNJpHt7R2qoJTpuR7oK81jWXxH5K6Rz1nZHneK24jj7XdZDmc7U2W2dH8aso46n

Trading app for Monero(XMR) at the Poloniex exchange using the Poloniex API.

##Current Features:
  - Supported Currencies for trading: XMR
  - Live XMR Price
  - Live 24h High, 24h Low and 24h Change
  - Balance, Balance included open orders
  - Open Orders 
  - History 
  - Display your current overall asset in USD
  - Manually request Poloniex values with "Refresh" Button
  	- Display timestamp of the last successfull refresh
  - Trading (Simple Buy and Sell)
    - Note: Auto Button for setting current BTC price in the sell section and Total BTC in the buy section 
    - Note: Automatically calculated Total(BTC) on the sell side
    - Note: Automatically calculated Amount(XMR) on the buy side 
  - Configuration: Poloniex Public and Secret Key
  - Display Poloniex/Network connectivity

##Pre-Information:
  - Based on Qt 5.5.1
  - Using Qt Creator for the design
  - Using Pyqt for the python code
  - Python 3
  
##How to Start:

  **Windows**  
  - Download MoneroTrader_x.x.x_Win.zip from the latest release
  - Unzip MoneroTrader_x.x.x_Win.zip
  - Execute MoneroTrader.exe (Info: exe file is created with pyinstaller)
  - 2 files (key.py, qt.log) will be created in the same directory 

## How to Use:
  - Insert your Poloniex API keys into Configuration tab and save them. You can check your keys in the key.py file
  	- Restart the program to activate the API keys
  	- Now you should see your Balances and you are able to trade
  - Buy and Sell Button will be activated after the first refresh with the "Refresh" Button
  - It is recommended to refresh your values after every sell, buy or cancel Order to check your activities
  - Canceling Order with double click on the Order Number in the Open Orders view


##Screenshots:

Trading:
![Screenshot](https://raw.github.com/swalecko/PoloTradeGui/master/Dashboard_screenshot.JPG?raw=true "Trading Tab")

Open Orders:
![Screenshot](https://raw.github.com/swalecko/PoloTradeGui/master/Dashboard_screenshot_OO.JPG?raw=true "Open Orders Tab")

Configuration:
![Screenshot](https://raw.github.com/swalecko/PoloTradeGui/master/Dashboard_screenshot_API.JPG?raw=true "Configuration Tab")




