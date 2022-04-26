import csv
import yfinance as yf


def downloadBIST():
    source  = 'bist'
    ticker_list = []
    with open('C:/stock/datasets/'+source+'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0]:
                ticker_list.append(row[0])
      
    data = yf.download(
            tickers = ticker_list,
            period='70d',
            interval = "1d",
            group_by = 'ticker',
            auto_adjust = True,
            prepost = True,
            threads = False,
            proxy = None
        )
    data.dropna()
    data = data.T
    for ticker in ticker_list:
        data.loc[(ticker,),].T.dropna().to_csv('C:/stock/datasets/bist/daily/'+ ticker + '.csv', sep=',', encoding='utf-8')

    # dataW = yf.download(
    #         tickers = ticker_list,
    #         period='70d',
    #         interval = "1wk",
    #         group_by = 'ticker',
    #         auto_adjust = True,
    #         prepost = True,
    #         threads = False,
    #         proxy = None
    #     )
    # dataW.dropna()
    # dataW = dataW.T
    # for ticker in ticker_list:
    #     dataW.loc[(ticker,),].T.dropna().to_csv('C:/stock/datasets/bist/weekly/'+ ticker + '.csv', sep=',', encoding='utf-8')

if __name__ == "__main__":
    downloadBIST()
    