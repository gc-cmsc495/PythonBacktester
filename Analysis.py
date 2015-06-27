# Date: 2015-06-20
#
# Description:

# The Analysis class gets the trade data from TradeManager
# and calculate statistics for each indicator/markout_length pair.
# Statistics include: mean return, standard deviation, t-statistc or sharpe ratio,
# cumulative return, max and min returns, skew, kurtosis and other statistics.

# QUESTION: Should the Analysis class also provide generic math functions such
# as mean, median, sum, stdev, so it can be used by IndicatorLibrary?

# Class Author: Justin Kelley

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



class Analysis(object):

    def __init__(self, trade_log_path):
        pass;
