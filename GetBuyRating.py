class GetBuyRating:
    """ Get the buy/sell recommendation based on analyst reviews """

    def __init__(self):
        pass

    def get_sp500_recommendations(self, stocks=['all'], print_ratings=False):
        import pandas as pd
        from yfinance import Ticker

        # Call the get_sp500_tickers to get a list of tickers
        if stocks == ['all']:
            tickers = self.__get_sp500_tickers()
        else:
            tickers = []
            for stock in stocks:
                tickers.append(Ticker(stock))

        # Get a list of analyst ratings for each ticker in tickers
        length = len(tickers)
        i = 1
        recs = []
        symbols = []
        print('Getting analyst ratings...')
        for ticker in tickers:
            print('\tGetting ratings for ', ticker.ticker, ' (', i, '/', length, ')', sep='')
            symbols.append(ticker.ticker)
            try:
                recs.append(ticker.recommendations)
            except:
                recs.append('No ratings found')
            i += 1
        print('Done!')

        # Get the numerical and average rating for each recommendation
        numerical_ratings, avg_ratings = self.__rating_to_num(recs, print_ratings)

        # Create data frame with all calculated info
        sp500_ratings_df = pd.DataFrame()
        sp500_ratings_df['Tickers'] = symbols
        sp500_ratings_df['Analyst Ratings'] = recs
        sp500_ratings_df['Numerical Ratings'] = numerical_ratings
        sp500_ratings_df['Average Rating'] = avg_ratings
        sp500_ratings_df = sp500_ratings_df.sort_values(by='Average Rating')

        return sp500_ratings_df

    @staticmethod
    def __get_sp500_tickers():
        import requests
        import bs4 as bs
        from yfinance import Ticker

        # Get a list of SP500 tickers from wikipedia
        print('Getting S&P500 tickers...')
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(Ticker(ticker.strip()))
        print('Done!\n')

        return tickers

    @staticmethod
    def __rating_to_num(recs, print_ratings):
        """ Handle exception when getting numerical, create logger file? """
        numerical_ratings = []
        avg_ratings = []
        # dict to act as a switch case
        switcher = {
            'strong buy': 1,

            'moderate buy': 2,
            'accumulate': 2,
            'overweight': 2,
            'outperform': 2,
            'add': 2,
            'buy': 2,
            'speculative buy': 2,

            'neutral': 3,
            'hold': 3,
            'market perform': 3,
            'sector perform': 3,
            'equal-weight': 3,

            'moderate sell': 4,
            'weak hold': 4,
            'underweight': 4,
            'underperform': 4,
            'reduce': 4,
            'sell': 4,

            'strong sell': 5
        }

        for rec in recs:
            try:
                indv_ticker_ratings = []
                total_rating = 0
                ratings = 0
                if print_ratings:
                    print(rec['To Grade'])
                for rate in rec['To Grade']:
                    num_rating = switcher.get(rate.lower())
                    if num_rating is not None:
                        indv_ticker_ratings.append(num_rating)
                        total_rating += num_rating
                        ratings += 1

                avg_rating = round(total_rating / ratings, 1)

                numerical_ratings.append(indv_ticker_ratings)
                avg_ratings.append(avg_rating)

            # Append -1 if the ratings don't exist for a ticker
            except Exception as e:
                numerical_ratings.append([-1])
                avg_ratings.append(-1)

        return numerical_ratings, avg_ratings
