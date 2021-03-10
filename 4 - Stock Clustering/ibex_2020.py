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

lis=lista_google(datetime.datetime(2018, 1, 1),datetime.datetime(2019, 12, 31))
