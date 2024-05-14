import csv
import yfinance as yf


def download(dataset):
    tickers = []
    with open(f'/Users/admin/dev/MyTraderStockSignals/datasets/{dataset}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0]:
                tickers.append(row[0])

    data = yf.download(
            tickers=tickers,
            period='70d',
            interval="1d",
            group_by='ticker',
            auto_adjust=True,
            prepost=True,
            threads=False,
            proxy=None
        )
    data.dropna()
    data = data.T
    for ticker in tickers:
        data.loc[(ticker,),].T.dropna().to_csv(f'/Users/admin/dev/MyTraderStockSignals/hist/{dataset}/daily/{ticker}.csv', sep=',', encoding='utf-8')


if __name__ == "__main__":
    download('bist')
    download('nasdaq')
