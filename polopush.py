from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner
from asyncio import coroutine


class PoloniexComponent(ApplicationSession):
    def onConnect(self):
        self.join(self.config.realm)

    @coroutine
    def onJoin(self, details):
        def onTicker(*args):
            
            
            if args[0] == "BTC_XMR":
                print (args[0])    
           
           
            # if args[0] == "BTC_XMR":
                                               
            #     # print ("")
            #     # print ("===================================")
                
            #     # print ("Currency: " + args[0])
            #     # print ("Current Prize: " + args[1] + " BTC") 
            #     # print ("24hr High: " + args[8] + " BTC")
            #     # print ("24hr Low: " + args[9] + " BTC")
            #     # print ("Percent Change: " + str(float(args[4])*100) + " %")

            #     return args[0]
            #     return args[1]
            # #if args[0] == "BTC_ETH":
                                               
            #     # print ("")
            #     # print ("===================================")
            #     # print ("Currency: " + args[0])
            #     # print ("Current Prize: " + args[1] + " BTC") 
            #     # print ("24hr High: " + args[8] + " BTC")
            #     # print ("24hr Low: " + args[9] + " BTC")
            #     # print ("Percent Change: " + str(float(args[4])*100) + " %")
            

        try:
            yield from self.subscribe(onTicker, 'ticker')
        except Exception as e:
            print("Could not subscribe to topic:", e)
         
        
def main():
    runner = ApplicationRunner("wss://api.poloniex.com:443", "realm1")
    runner.run(PoloniexComponent)


if __name__ == "__main__":
    main()