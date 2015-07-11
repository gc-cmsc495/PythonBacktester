# Date: 2015-06-20
#
# Description:
#
# An indicator is a Boolean class method that consumes a series of 
# price or volume information from the Data Class.
# Some indicators may be composites of other indicators

# Class Author: Pierce Baker

# Use Case:
#   1. instantiated by TradeManager with DataManager object and indicator_list
#   2. for indicator (class method) in indicator_list
#       2.a. calculate Boolean result
#   3. return intersection of results (AND logic) of indicators in indicator_list
#

from DataManagerGarrett import DataManagerGarrett

def mean(l):
    ## see http://stackoverflow.com/questions/7716331/calculating-arithmetic-mean-average-in-python
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')


def get_stdv(sample):
    #first find the mean of the data
    mean = 0
    for i in sample:
        mean += i
    mean /= len(sample)
    #with the mean the variance can be found
    variance = 0
    for i in sample:
        variance += (i - mean) ** 2
    variance /= len(sample)
    #with the variance the standard deviation can be found
    return variance ** 0.5

class Indicator(object):

    def __init__(self):
        self.max_history = 0
     
    def periods_required(self):
        return self.max_history
        
    def calc(self, DataManager, ticker, date):
        return True
        
class High_Volume(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 20
    
    def calc(self, DataManager, ticker, date):
        quote_list = DataManager.get(ticker, date, -20)
        quote = quote_list.pop()
        hist_volume = []
        for q in quote_list[-20:]:
            hist_volume.append(q.volume)
        return quote.volume > mean(hist_volume)

class Close_Higher_Than_Open(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        
    def calc(self, DataManager, ticker, date):
        quote = DataManager.get(ticker, date)
        return quote.close > quote.open
     
def new_high_volume():
    return High_Volume()

def new_close_higher_than_open():
    return Close_Higher_Than_Open()

registered_indicators = {
    'HIGH_VOLUME' : new_high_volume,
    'CLOSE_HIGHER_THAN_OPEN' : new_close_higher_than_open,
}

class IndicatorLibrary(object):
    
    def __init__(self, indicator_list):
        self.indicators = []
        for indicator in indicator_list:
            if indicator in registered_indicators:
                self.indicators.append(registered_indicators[indicator]())
    
    def periods_required(self):
        max_history = 0
        for indicator in self.indicators:
            max_history = max(max_history, indicator.periods_required())
        return max_history
    
    def calc(self, dm, ticker, today):
        for indicator in self.indicators:
            if not indicator.calc(dm,ticker,today):
                return False
        return True
        