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

    def __init__(self, config, logger):
        self.analysis = Analysis(config.get_value("SHAREABLE", "trade_log_file_name"))
        self.outfn = config.get_value("SHAREABLE", "stat_file_name")
        self.logger = logger
    
    def write(self):
        report_text = ""
        max_mo_length = len(str(self.analysis.max_markout_period()))
        max_ticker_length = max([len(x) for x in self.analysis.get_tickers()]) + 2
        out_cols = ["Markout Period", "Ticker", "Trade Count", "Return mu", "Return tstat", "Return sharpe"]
        header = ["{item:>{item_width}}".format(item=col, item_width=len(col)) for col in out_cols]
        report_text += "\t".join(header) + "\n"
        for mo_period in self.analysis.get_mo_periods():
            for ticker in self.analysis.get_tickers():
                out = {
                    'Markout Period' : mo_period, 
                    'Ticker' : ticker,
                    'Trade Count' : self.analysis.count(mo_period, ticker),
                    'Return mu' : "{:0.4f}".format(self.analysis.mean(mo_period, ticker)),
                    'Return tstat' : "{:0.2f}".format(self.analysis.tstat(mo_period, ticker)),
                    'Return sharpe' : "{:0.2f}".format(self.analysis.sharpe(mo_period, ticker))
                }
                output = []
                for column in out_cols:
                    if column in out:
                        output.append( "{item:>{item_width}}".format(item=out[column], item_width=len(column)) )
                report_text += "\t".join(output) + "\n"
            report_text += "\n"
        
        with open(self.outfn, 'w') as f:
            f.write(report_text)
        
        self.logger.info("Report written to " + self.outfn)
