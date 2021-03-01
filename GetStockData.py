class GetStockData:
    """ Get historical data about a stock """

    def __init__(self, stock: str, graph: bool):
        self.stock = stock
        self.graph = graph

        if graph:
            from BuildFigure import BuildFigure
            self.fig, self.ax1, self.ax2, self.ax3, self.ax4 = BuildFigure(stock).build_figure()

    # Get the stock history from yfinance
    # @ returns: df (Pandas dataframe: stock history)
    def __get_history(self):
        from yfinance import Ticker
        from pandas import DataFrame
        from datetime import datetime, timedelta, date

        # Get stock data from yfinance module from 60 days before 01/01 to today
        stock_data = Ticker(self.stock)
        df = DataFrame(stock_data.history(start=str(datetime.now().date().replace(month=1, day=1) - timedelta(60)),
                                          end=str(date.today())))

        return df

    # Calculate technical data using the TA-Lib package
    def get_technicals(self):
        import talib as ta

        stock_history = self.__get_history()

        # Get Bollinger bands
        stock_history['up_band'], \
            stock_history['mid_band'], \
            stock_history['low_band'] = ta.BBANDS(stock_history['Close'], timeperiod=20)

        # Get MACD
        stock_history['MACD'], \
            stock_history['MACD_signal'], \
            stock_history['MACD_hist'] = ta.MACDEXT(stock_history['Close'],
                                                         fastperiod=12, fastmatype=1,
                                                         slowperiod=26, slowmatype=1,
                                                         signalperiod=9, signalmatype=1)

        # Get OBV
        stock_history['OBV'] = ta.OBV(stock_history['Close'], stock_history['Volume'])

        # Get RSI
        stock_history['RSI'] = ta.RSI(stock_history['Close'], 14)

        if self.graph:
            self.__graph_technicals(stock_history)

        return stock_history

    # Graph the historical closing and technical data
    def __graph_technicals(self, stock_history):
        import matplotlib.pyplot as plt
        from datetime import date, datetime
        from pandas.plotting import register_matplotlib_converters

        # Explicitly register datetime converter for matplotlib plotting method
        register_matplotlib_converters()

        # Graph Bollinger
        self.ax1.plot(stock_history[['Close', 'up_band', 'mid_band', 'low_band']])

        # Graph MACD
        self.ax2.plot(stock_history['MACD_signal'])
        self.ax2.title.set_text('MACD')
        self.ax2.set_ylim(-10, 10)

        # Graph OBV
        self.ax3.plot(stock_history['OBV'])
        self.ax3.title.set_text('OBV')
        # self.ax3.set_ylim(-2, 2)

        # Graph RSI
        self.ax4.plot(stock_history['RSI'])
        self.ax4.title.set_text('RSI')
        self.ax4.set_ylim(0, 100)

        # Limit the x-axis to start on Jan-1 and end on the current date
        plt.xlim(datetime.now().date().replace(month=1, day=1), date.today())
        plt.show()
