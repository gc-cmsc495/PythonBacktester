# Date: 2015-06-20
#
# Description:
# The data class is responsible for fetching, parsing, validating,
# and provide access methods to the equity price and volume data.
# The class will also provide methods to retrieve data by index
# or date. Finally, due to the nature of the data, this class will
# provide a trade-date calendar interface.

# Class Author: Nancy Isaac

class DataManager(object):

    def __init__(self, start, end, num_periods=0):
        self.start_date = start
        self.end_date = end
        self.num_periods = num_periods
        
        self.set_calendar()
    
    def set_calendar(self):
      ## fetch data for GE, which has trade data going back
      ## to Jan 2, 1962.
      
      self.calendar_list = []  ## keep a list for order
      self.calendar_hash = {}  ## keep a dict for fast lookup
      ## Or should we used OrderedDict???
      
      
      
    
