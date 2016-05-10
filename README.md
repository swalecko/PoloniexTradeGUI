# PoloTradeGUI

Donations: soon

It`s a Trading app for XMR and also ETH soon at the Poloniex exchange via the Poloniex API.

**Current Features:**
  - Price informations XMRBTC, XMRUSD, ETHBTC
  - Balances for XMR, EMX included open orders, ETH, ETH included open orders, Bitcon
  - 24h High, 24h Low and 24h Change for XMR
  - Open Orders for XMR
    - Note: to cancel an open order double click the cell with the order number
  - History of executed orders
  - Trading: Buy and Sell XMR
    - Note: "A" Auto Button for setting current BTC price and Total BTC in the certain field
  - Configuration: Set and save the Poloniex Public and Secret Key

**Future Features:**
  - Adding ETH for trading and showing informations like open orders and history
  - There's more to come..
  
**Pre-Information:**
  - Based on Qt 5.5.1
  - Using Qt Creator for the design
  - Using Pyqt for the python code
  - Written in Python 3
  
**Requirements:**
  - Python3   
    - Additional modules:  
      - json  
      - requests  
  - PyQt5

**How to use:**
  - Execute the PoloTrader.pyw file 
  - When you execute the app for the first time, you need to add your PUBLIC and SECRET API Keys and save them.  
    A file "key.py" will be created with the following content:     
    first line: "PUBLIC_KEY = '<key>'"   
    second line: "SECRET_KEY = '<key>'"     
    **Important**: You need to restart the app to activate the keys
  - Happy trading :-)  
  Alternative:
  - Use for example pyinstaller to create a package or a "one-file" for execution
    Example: 
    Installation: pip install pyinstaller
    Command Example: pyinstaller -w -n PoloTrader -i XMRicon.ico -F prog.pyw  
    More information for pyinstaller: http://www.pyinstaller.org/


**Screenshot:**

![Screenshot](https://raw.github.com/swalecko/PoloTradeGui/master/Dashboard_screenshot.JPG?raw=true "Open Orders Tab")




