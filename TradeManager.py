# Date: 2015-06-20
#
# Description:
#
# The TradeManager class will use the Data class and Indicator Library
# to iterate through the sample period, record the instances when the
# indicators are true, determine the future prices, and ensure events
# are independent by ensuring no trade overlapping.
# 

# Class Author: Garrett Casey

# Use Case:
#   1. Main application instantiates TradeManager with Config object.
#   2. TradeManager instantiates Datamanager and IndicatorLibrary
#   3. For each ticker in the portfolio
#       3.a. Request series of price data from DataManager
#       3.b. For each date
#           3.b.1. Pass date and price data to IndicatorLibrary for evaluation
#           3.b.2. If IndicatorLibrary return true.
#               3.b.2.a. For each markout-period
#                   3.b.2.a.1. request future date and price form Data Manager
#                   3.b.2.a.2. block any future Indicator queries until after future date
#                   3.b.2.a.3. write results to trade log

from Config import Config
from DataManager import DataManager
from IndicatorLibrary import IndicatorLibrary

class TradeManager(object):

    def __init__(self, config):
        self.config = config
        self.indicators = IndicatorLibrary(config.get_value('STRATEGY', 'indicators'))
        
        start_date = config.get_value('PORTFOLIO','startdate')
        end_date = config.get_value('PORTFOLIO', 'enddate')
        max_markout_periods = max(config.get_value('STRATEGY', 'markout_periods'))
        max_historical_periods = self.indicators.periods_required()
        self.dm = DataManager(start_date,end_date,max_markout_periods,max_historical_periods)
        self.__trade_log_fn()
        
    def __trade_log_fn(self):
        start_date = self.config.get_value('PORTFOLIO','startdate')
        end_date = self.config.get_value('PORTFOLIO', 'enddate')
        name = self.config.get_value('STRATEGY', 'name')
        ext = self.config.get_value('PORTFOLIO', 'trade_log_file_ext')
        fn = ".".join([str(start_date),str(end_date),name,ext])
        self.config.put('trade_log_file_name', fn)
        
        
