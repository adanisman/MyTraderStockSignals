import csv
import pandas
import technicalLib as clib
import traceback
import datetime as dt
import time
import threading
import nest_asyncio
import asyncio
from datetime import datetime


#app=Flask(__name__,template_folder='templates')

def ALL_BIST(num,datetimeObjStr):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    source  = 'nasdaq.csv0'+num
    i=0
    print(num,"-", i)
    nest_asyncio.apply()      
    stocks = {}
    with open('/Users/admin/dev/MyTraderStockSignals/datasets/nasdaq.csv') as f:
        for row in csv.reader(f):
            # print(row[1])
            stocks[row[0]] = row[1]
    
    with open('/Users/admin/dev/MyTraderStockSignals/datasets/'+source) as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            symbol_org=symbol
            try: 
                df = pandas.read_csv('/Users/admin/dev/MyTraderStockSignals/hist/nasdaq/daily/'+symbol +'.csv') 
                        
                ottx = clib.OTT_NEW(df) 
                last_ott = ottx[0][-1:].values[0]
                prev_ott =  ottx[0][-2:-1].values[0]
                last_var = ottx[1][-1:].values[0]
                prev_var =  ottx[1][-2:-1].values[0]
                
                if last_var>last_ott and prev_var<prev_ott:
                        #sendTextBist("OTT BUY->" + " https://www.tradingview.com/chart/?symbol=BIST:" + symbol.replace('.IS', '') +"&interval=1D" ) 
                        #result_stocks[symbol]['symbol_org'] ="https://www.tradingview.com/chart/?symbol=BIST:" + symbol_org
                        company=stocks.get(symbol_org)                       
                        print("OTT BUY => " + symbol_org + ":" +company)
                        #dbService.insert_stock_signal(symbol_org.replace('.IS', ''),company,'OTTBUY','BIST','BUY',symbol_org.replace('.IS', ''),'DAILY')
                       
                        
                if clib.rsi(df):
                        company=stocks.get(symbol_org)                       
                        print("RSI BUY => " + symbol_org + ":" +company)
                        #dbService.insert_stock_signal(symbol_org.replace('.IS', ''),company,'RSIBUY','BIST','BUY',symbol_org.replace('.IS', ''),'DAILY')
                        
            except:
                #traceback.print_exc()
                pass
            

#@app.route('/ott')
def all_bist():
    
    source  = 'bist'

    result_stocks = {}
    #print(source)       
    #dbService.delete_pattern('OTTBUY')  
    #dbService.delete_pattern('RSIBUY')
    start = time.time()
    datetimeObj = dt.date.today()
    datetimeObjStr = datetimeObj.strftime("%Y%m%d")
    
    t0 = threading.Thread(target=ALL_BIST, args=('0', datetimeObjStr,)) 
    t1 = threading.Thread(target=ALL_BIST, args=('1', datetimeObjStr,))
    t2 = threading.Thread(target=ALL_BIST, args=('2', datetimeObjStr,))
    t3 = threading.Thread(target=ALL_BIST, args=('3', datetimeObjStr,))
    t4 = threading.Thread(target=ALL_BIST, args=('4', datetimeObjStr,))
    t5 = threading.Thread(target=ALL_BIST, args=('5', datetimeObjStr,))
    t6 = threading.Thread(target=ALL_BIST, args=('6', datetimeObjStr,))
    t7 = threading.Thread(target=ALL_BIST, args=('7', datetimeObjStr,))
    t8 = threading.Thread(target=ALL_BIST, args=('8', datetimeObjStr,))
    t9 = threading.Thread(target=ALL_BIST, args=('9', datetimeObjStr,)) 

            
    # starting thread 1
    t1.start()
    t2.start()
    t3.start()
    t4.start()    
    t5.start()
    t6.start()
    t7.start()
    t8.start() 
    t9.start() 
    t0.start() 
       
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()    
    t9.join()  
    t0.join()   
    # both threads completely executed
    print("Done!")
    print("--- %s seconds ---" % (time.time() - start))
 

def main():
    print('main')
    all_bist()
        
if __name__ == '__main__':
    main()
    
# @app.route('/main')
# def main():
#     return render_template('main.html')


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8082)
