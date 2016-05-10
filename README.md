# PoloTradeGui

Donations: soon

It`s a Trading app for XMR and also ETH soon at the Poloniex exchange via the Poloniex API.

Current Features:
  - Price informations XMRBTC, XMRUSD, ETHBTC
  - Balances for XMR, EMX included open orders, ETH, ETH included open orders, Bitcon
  - 24h High, 24h Low and 24h Change for XMR
  - Open Orders for XMR
    - Note: to cancel an open order double click the cell with the order number
  - History of executed orders
  - Trading: Buy and Sell XMR
    - Note: "A" Auto Button for setting current BTC price and Total BTC in the certain field
  - Configuration: Set and save the Poloniex Public and Secret Key
    - Note: You need to create a "key.py" file in the same folder where the keys will be saved:  
      Content of the key.py file should be: first line: "PUBLIC_KEY =" second line: "SECRET_KEY =".
      After that its possible to save the keys via the GUI.
    
Future Features:
  - Adding ETH for trading and showing informations like open orders and history
  - There's more to come..
  
Pre-Information:
  - Based on QT 5.5.1
  - Using QT Creator for the design
  - Using Pyqt for the python code
  - Written in Python 3

How to use:
  - Execute the prog.pyw file
  Alternative:
  - Use for example pyinstaller to create a package or a "one-file" for execution
    Example: 
    Installation: pip install pyinstaller
    Command Example: pyinstaller -w -n PoloTrader -i XMRicon.ico -F prog.pyw  
    More information for pyinstaller: http://www.pyinstaller.org/


Screenshot:

![Alt text](C:\Users\swalecko\Documents\PoloTradeGui\Dashboard_screenshot.JPG?raw=true "Open Orders Tab")




