from GetStockData import GetStockData
from GetBuyRating import GetBuyRating

stock = 'RTX'

stock_hist = GetStockData(stock, graph=True).get_technicals()
print(stock_hist)

# recs = GetBuyRating().get_sp500_recommendations()
# recs.to_excel('ticker recommendations.xlsx')
