class BuildFigure:
    """ Build a figure with 4 subplots to contain the close, RSI, MACD, and OBV plots """

    def __init__(self, stock):
        self.stock = stock

    def build_figure(self):
        import plotly.graph_objects as go
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Set seaborn to make the plots look nicer
        sns.set()

        # Get rid of the x-axis margins matplotlib makes by default
        plt.rcParams['axes.xmargin'] = 0

        # Create the figure and the subplot layout
        fig = plt.figure(figsize=(20, 13.5))
        fig.suptitle('YTD: ' + self.stock, fontsize=32)
        # Set the height ratio so the first plot is 4x the height of the rest
        gs = plt.GridSpec(4, 1, height_ratios=[4, 1, 1, 1])
        fig.tight_layout(rect=[0, 0.3, 1, 1.5])

        # Create the subplots. Synchronize the x-axes
        ax1 = plt.subplot(gs[0, 0])

        ax2 = plt.subplot(gs[1, 0], sharex=ax1)
        ax2_x_axis = ax2.axes.get_xaxis()
        ax2_x_axis.set_visible(False)

        ax3 = plt.subplot(gs[2, 0], sharex=ax1)
        ax3_x_axis = ax3.axes.get_xaxis()
        ax3_x_axis.set_visible(False)

        ax4 = plt.subplot(gs[3, 0], sharex=ax1)
        ax4_x_axis = ax4.axes.get_xaxis()
        ax4_x_axis.set_visible(False)

        # fig = go.Figure(fig)

        return fig, ax1, ax2, ax3, ax4
