# Date: 2015-06-20
#
# Description:

# The Analysis class gets the trade data from TradeManager
# and calculate statistics for each indicator/markout_length pair.
# Statistics include: mean return, standard deviation, t-statistc or sharpe ratio,
# cumulative return, max and min returns, skew, kurtosis and other statistics.

# QUESTION: Should the Analysis class also provide generic math functions such
# as mean, median, sum, stdev, so it can be used by IndicatorLibrary?

# Class Authors: Garrett Casey and Justin Kelley

# Use Case:
# 1. TradeManager writes to log file for each trade
# 2. ReportWriter is called by main application to generate well-formatted text output
# 3. ReportWrite calls Analysis class
# 4. Analysis class reads and parses trade log file
# 5. Provides methods to return:
#   5.a Average return in mark-out period
#   5.b Sample Standard Deviation of returns 
#   5.c Test-statistic for returns (mean * sqrt(count) / sampleStandardDeviation)
#   5.d Other statistics

from RunningStat import RunningStat
import Util
import pprint
import math

class Analysis(object):
    def __init__(self, trade_log_path):
        print "Trade log is at " + trade_log_path
        
        stats = {}
        tickers = {}
        mo_periods = []
        
        with open(trade_log_path, 'r') as f:
            header, cols = Util.get_header_and_columns(f, delim=',')
            for line in f:
                h = line.rstrip('\n').split(',')
                ticker    = h[cols['ticker']]
                mo_period = h[cols['mo_period']]
                if mo_period not in stats:
                    mo_periods.append(mo_period)
                    stats[mo_period] = {}
                    stats[mo_period]['_all_'] = RunningStat()
                if ticker not in stats[mo_period]:
                    tickers[ticker] = 1
                    stats[mo_period][ticker] = RunningStat()
                log_return = math.log(float(h[cols['exit_price']])) - math.log(float(h[cols['entry_price']]))
                stats[mo_period][ticker].Push( log_return )
                stats[mo_period]['_all_'].Push( log_return )
               
        self.stats = stats
        self.tickers = ['_all_'] + tickers.keys()
        self.mo_periods = mo_periods

    def get_tickers(self):
        return self.tickers
     
    def get_mo_periods(self):
        return self.mo_periods
    
    def mean(self, mo_period, ticker):
        return self.stats[mo_period][ticker].Mean()

    def stdev(self, mo_period, ticker):
        return self.stats[mo_period][ticker].StandardDeviation()
        
    def sharpe(self, mo_period, ticker):
        return self.stats[mo_period][ticker].Sharpe() * math.sqrt(252) ### annualize the sharpe
        
    def tstat(self, mo_period, ticker):
        return self.stats[mo_period][ticker].TStat()
        
    def count(self, mo_period, ticker):
        return self.stats[mo_period][ticker].NumDataValues()
        
