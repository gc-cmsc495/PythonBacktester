# Date: 2015-06-20
#
# Description:
# The data class is responsible for fetching, parsing, validating,
# and provide access methods to the equity price and volume data.
# The class will also provide methods to retrieve data by index
# or date. Finally, due to the nature of the data, this class will
# provide a trade-date calendar interface.

# Class Author: Nancy Isaac

# Use Case:
#   1. Main application instantiates the DataManager
#       1.a. provides the following arguments
#           1.a.1 Sample period start date and end date
#           1.a.2 The maximum number of historical periods required by all Indicators
#               1.a.2.a.  allowing the DataManager to fetch enough data for indicators to have values on start date
#       1.b. DataManager initializes trade date calendar
#           1.b.1. If the end date is beyond current trade date calendar end date
#               1.b.1.a. Fetch GE price quote from Jan 1 1960 to now, store in data structures, write to file
#           1.b.2. else initialize calendar from calendar file
#   2. Main application passes ticker
#   3. DataManager Loads price and volume data for that ticker from YAHOO api or file (if caching is turned on)
#   4. DataManager is passed to IndicatorLibrary
#   5. IndicatorLibrary queries DataManager for serial price and/or volume data
#       5.a. returns iterator object with the time boundaries defined by the Indicator function

class DataManager(object):

    def __init__(self, start, end, max_markout_periods=20, num_historical_periods=0):
        self.start_date = start
        self.end_date = end
        self.num_periods = num_historical_periods
        self.max_markout = max_markout_periods
        
        self.set_calendar()
    
    def set_calendar(self):
      ## fetch data for GE, which has trade data going back
      ## to Jan 2, 1962.
      
      self.calendar_list = []  ## keep a list for order
      self.calendar_hash = {}  ## keep a dict for fast lookup
      ## Or should we used OrderedDict???
      
    def get_value(ticker, type, date):
        ## basic getter method to return a data for a single ticker/day
        ## example get_value('AAPL', 'close', 20150602)
        pass;
    
    def get_value(ticker, type, date, periods_back):
        pass;
        
      
      
      
    
