# Date: 2015-06-20
#
# Description:
#
# The report class will be responsible for taking results from the Analysis Class
# and other classes and output the results in a well formatted text file.
#
# We must carefully consider the format in which the results are published so they
# can be easily processed by other programs or utilities (e.g. Strategy Comparison Tools, GUIs, etc.).
# 

# Class Author: TBD
#
# Use Case:
#   1. Instantiated by main application, passed configuration object.
#   2. Instantiates Analysis class and passes path to trade log (value was set SHAREABLE in config by TradeManager)
#   3. Builds well-formatted text from config settings and Analysis results
#   4. Outputs results to stat file
#

from Analysis import Analysis
from Config import Config

class ReportWriter(object):

    def __init__(self, config, out_fn):
        self.analysis = Analysis(config.get_value("SHAREABLE", "trade_log_file_name"))
        pass
    
    def write(self):
        for mo_period in self.analysis.get_mo_periods():
            for ticker in self.analysis.get_tickers():
                count = self.analysis.count(mo_period, ticker)
                mean = self.analysis.mean(mo_period, ticker)
                tstat= self.analysis.tstat(mo_period, ticker)
                sharpe= self.analysis.sharpe(mo_period, ticker)
                print "{0} {1} {2} {3} {4} {5}".format(mo_period, ticker, count, mean, tstat, sharpe)
