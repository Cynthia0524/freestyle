from pandas_datareader import data
from datetime import date, timedelta

symbols = ['AAPL', 'MSFT','KO','SPY','SMI']
data_source = 'google'
start = str(date.today() - timedelta(days=600)) #> '2017-07-09'
end = str(date.today())
response = data.DataReader(symbols, data_source, start, end)
daily_closing_prices = response.ix["Close"]
daily_closing_prices
daily_closing_prices.to_csv("portfolio.csv", sep=',')
