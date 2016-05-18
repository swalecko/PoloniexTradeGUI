import polowrapper
import key

def getpoloInfo():
    poloInstance = polowrapper.poloniex(key.PUBLIC_KEY, key.SECRET_KEY)

    retBalances = poloInstance.returnBalances()
    retTicker = poloInstance.returnTicker()

    tickerXMR = retTicker['BTC_XMR']
    tickerETH = retTicker['BTC_ETH']
    print ("tickerXMR: " + str(tickerXMR))


    BalanceXMR = retBalances['XMR']

    BalanceETH = retBalances['ETH']
    BalanceBTC = retBalances['BTC']
    lastXMR = tickerXMR['last']
    highXMR = tickerXMR['high24hr']
    lowXMR = tickerXMR['low24hr']
    changeXMR = tickerXMR['percentChange']
    lastETH = tickerETH['last']
    highETH = tickerETH['high24hr']
    lowETH = tickerETH['low24hr']
    changeETH = tickerETH['percentChange']
