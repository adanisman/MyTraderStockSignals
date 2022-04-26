import talib as ta
import numpy as np


def rsi(df):
    #print("rsi system ****")    
    df["rsi"]  = ta.RSI(df["Close"])    
    rsi_tail= df.tail(5)
    #print(rsi_tail)
    last=0
    neg=0
    
    for ind in rsi_tail.index: 
        #print(ind)
        #print(slp_tail['close_slope'][ind])      
        last=rsi_tail['rsi'][ind]      
        try:    
            if(last<50):
                neg=neg+1
        except ValueError as e:
            last=0

    last_close = df["Close"].iloc[-1]
    prev_close= df["Close"].iloc[-2]
    #print(last_close)
        #Gunluk Fark yuzdesi
    gfark=(last_close/prev_close-1)*100
            
    if(last>50 and neg==4 and gfark>0 and gfark<5):
    #if(last>50):
        #print(symbol)
        return True


def OTT_NEW(df):
    #print('burada')
    pds = 2
    percent = 1.4
    alpha = 2 / (pds + 1)

    df['ud1'] = np.where(df['Close'] > df['Close'].shift(1), (df['Close'] - df['Close'].shift()) , 0)
    df['dd1'] = np.where(df['Close'] < df['Close'].shift(1), (df['Close'].shift() - df['Close']) , 0)
    df['UD'] = df['ud1'].rolling(9).sum()
    df['DD'] = df['dd1'].rolling(9).sum()
    df['CMO'] = ((df['UD'] - df['DD']) / (df['UD'] + df['DD'])).fillna(0).abs()
    
    # df['Var'] = talib.EMA(df['Close'], timeperiod=5)
    df['Var'] = 0.0
    for i in range(pds, len(df)):
        df['Var'].iat[i] = (alpha * df['CMO'].iat[i] * df['Close'].iat[i]) + (1 - alpha * df['CMO'].iat[i]) * df['Var'].iat[i-1]
    
    df['fark'] = df['Var'] * percent * 0.01
    df['newlongstop'] = df['Var'] - df['fark']
    df['newshortstop'] = df['Var'] + df['fark']
    df['longstop'] = 0.0
    df['shortstop'] = 999999999999999999
    # df['dir'] = 1
    for i in df['UD']:
    
        def maxlongstop():
            df.loc[(df['newlongstop'] > df['longstop'].shift(1)) , 'longstop'] = df['newlongstop']
            df.loc[(df['longstop'].shift(1) > df['newlongstop']), 'longstop'] = df['longstop'].shift(1) 
            
            return df['longstop']
    
        def minshortstop():
            df.loc[(df['newshortstop'] < df['shortstop'].shift(1)), 'shortstop'] = df['newshortstop']
            df.loc[(df['shortstop'].shift(1) < df['newshortstop']), 'shortstop'] = df['shortstop'].shift(1)
            
            return df['shortstop']
    
        df['longstop']= np.where (
            (
                (df['Var'] > df['longstop'].shift(1))
            ),maxlongstop(),df['newlongstop']
        )
    
    
        df['shortstop'] = np.where(
            (
                (df['Var'] < df['shortstop'].shift(1))
            ), minshortstop(), df['newshortstop'])
    
    #get xover
    
    df['xlongstop'] = np.where (
        (
            (df['Var'].shift(1) > df['longstop'].shift(1)) & 
            (df['Var'] < df['longstop'].shift(1))
        ), 1,0)
    
    df['xshortstop'] =np.where(
        (
            (df['Var'].shift(1) < df['shortstop'].shift(1)) & 
            (df['Var'] > df['shortstop'].shift(1))
        ), 1,0)
    
    df['trend']=0
    df['dir'] = 0
    for i in df['UD']:
            df['trend'] = np.where(
            (
                (df['xshortstop'] == 1)
            ),1, (np.where((df['xlongstop'] == 1),-1,df['trend'].shift(1)))
        )
    
            df['dir'] = np.where(
            (
                (df['xshortstop'] == 1)
            ),1, (np.where((df['xlongstop'] == 1),-1,df['dir'].shift(1).fillna(1)))
        )
    
    
    #get OTT
    
    df['MT'] = np.where(df['dir'] == 1, df['longstop'], df['shortstop'])
    df['OTT'] = np.where(df['Var'] > df['MT'], (df['MT'] * (200 + percent) / 200), (df['MT'] * (200 - percent) / 200))
    df['OTT'] = df['OTT'].shift(2) 
    
    
    return df['OTT'], df['Var']

