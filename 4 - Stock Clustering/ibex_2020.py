import datetime

## from pandas.io.data import DataReader #OLD
##sudo pip install pandas-datareader
#import pandas_datareader.data as web
import fix_yahoo_finance as yf
lista_val=["MSFT","AAPL","T","GOOGL", "HPQ","VZ","CVX","ORAN","VOD","JPM","BBVA","RBS","BK"]

def lista_google (dstart,dend):
 lis=[]
 for i in range(0,len(lista_val)):
     f = yf.download(lista_val[i], dstart,dend)
#     f= web.DataReader(lista_val[i], 'stooq', dstart, dend)
     print(len(f.ix[:]['Close']))
     lis.append(f.ix[:]['Close'])
 return lis

lis=lista_google(datetime.datetime(2018, 1, 1),datetime.datetime(2019, 12, 31))
