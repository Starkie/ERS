import datetime
import yfinance as yf

lista_val=["MSFT","AAPL","T","GOOGL", "HPQ","VZ","CVX","ORAN","VOD","JPM","BBVA","RBS","BK"]

def lista_google (dstart,dend):
 lis=[]
 for i in range(0,len(lista_val)):
     f = yf.download(lista_val[i], dstart, dend)
     print(f[0:]['Close'])
     lis.append(f[0:]['Close'])
 return lis

def analyse_variation (stocks):
    stock_history = []

    for stock in stocks:
        stock_history.append(analyse_daily_variation(stock))

    return stock_history

def analyse_daily_variation(stock):
    variation_ratio_histogram = [0]

    for i in range(1,len(stock)):
        ratio = (stock[i] - stock[i-1]) / 100
        variation_ratio_histogram.append(ratio)

    return variation_ratio_histogram


lis=lista_google(datetime.datetime(2018, 1, 1),datetime.datetime(2019, 12, 31))

analyse_variation(lis)
