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
import Util, sys, pprint


class TradeManager(object):

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.start_date = config.get_value('PORTFOLIO','startdate')
        self.end_date = config.get_value('PORTFOLIO', 'enddate')
        self.name = self.config.get_value('PORTFOLIO', 'name')
        self.prevent_overlaps = {}  ## used to disallow same ticker+markout overlapping
        
        ## Get the list of indicators from the config file, then start IndicatorLibrary
        self.list_of_user_indicators = [s.upper() for s in Util.str_to_list(config.get_value('STRATEGY', 'indicators'))]
        if not self.list_of_user_indicators:
            self.logger.critical("Unable to determine list of user indicators")
            sys.exit(1)
        self.strategy = IndicatorLibrary(self.list_of_user_indicators)
        
        self.list_of_markout_periods = []
        try:
            for x in Util.str_to_list(config.get_value('STRATEGY', 'markout_periods')):
                self.list_of_markout_periods.append(int(x))
        except:
            self.logger.critical("Non integer-type value provided in STRATEGY.markout_periods")
            sys.exit(1)
        max_markout_periods = max(self.list_of_markout_periods)
        
        max_historical_periods = self.strategy.periods_required()
        self.dm = DataManager(logger, self.start_date,self.end_date,max_markout_periods,max_historical_periods)
        self.__trade_log_fn()
        
    def __trade_log_fn(self):
        strategy_name = self.config.get_value('STRATEGY','name')
        ext = self.config.get_value('PORTFOLIO', 'trade_log_file_ext')
        self.trade_log_name = ".".join([str(self.start_date),str(self.end_date),self.name,strategy_name,ext])
        print self.trade_log_name
        self.config.put('trade_log_file_name', self.trade_log_name)
        
    def run(self):
        
        with open(self.trade_log_name, 'w') as trade_log:
            trade_log.write('date,ticker,mo_period,entry_price,exit_price,exit_date\n')
            self.logger.info("Writing to " + self.trade_log_name)
            
            list_of_user_tickers = [s.upper() for s in Util.str_to_list(self.config.get_value("PORTFOLIO", "tickers"))]
            if not list_of_user_tickers:
                self.logger.critical("Unable to determine list of user-provided tickers")
                sys.exit(1)
            
            for trade_date in self.dm.trading_dates():
                for ticker in list_of_user_tickers:
                    if (self.strategy.calc(self.dm, ticker, trade_date)):
                        today_price = self.dm.get(ticker, trade_date).close
                        for mo_period in self.list_of_markout_periods:
                            future_date = self.dm.date_by_offset(trade_date, mo_period)
                            overlap_key = ticker + str(mo_period)
                            if overlap_key in self.prevent_overlaps and trade_date <= self.prevent_overlaps[overlap_key]:
                                print "Preventing overlap in {0}".format(overlap_key)
                                continue
                            self.prevent_overlaps[overlap_key] = future_date
                            future_price = self.dm.get(ticker, future_date).close
                            trade_log.write("{0},{1},{2},{3},{4},{5}\n".format(trade_date,ticker,mo_period,today_price,future_price,future_date))
        return True
