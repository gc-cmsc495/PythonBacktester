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

from DataManager import DataManager

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

class New_20_Period_Closing_High(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 20

    def calc(self, DataManager, ticker, date):
        quote_list = DataManager.get(ticker, date, -20)
        quote = quote_list.pop()
        is_new_high = True
        for q in quote_list[-20:]:
            if quote.close < q.close:
                is_new_high = False
        return is_new_high
        
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
        return quote.volume > mean(hist_volume) * 2

class New_52_Week_Low(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 260

    def calc(self, DataManager, ticker, date):
        quote_list = DataManager.get(ticker, date, -260)
        quote = quote_list.pop()
        is_new_low = True
        for q in quote_list[-260:]:
            if quote.close > q.close:
                is_new_low = False
        return is_new_low

class New_52_Week_High(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 260

    def calc(self, DataManager, ticker, date):
        quote_list = DataManager.get(ticker, date, -260)
        quote = quote_list.pop()
        is_new_high = True
        for q in quote_list[-260:]:
            if quote.close < q.close:
                is_new_high = False
        return is_new_high

class Crossed_Above_200d_Moving_Average(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 200

    def calc(self, DataManager, ticker, date):
        quote_list = DataManager.get(ticker, date, -200)
        quote_today = quote_list.pop()
        quote_yesterday = quote_list.pop()
        hist_close = []
        for q in quote_list[-200:]:
            hist_close.append(q.close)
        return quote_today.close > mean(hist_close) & quote_yesterday.close < mean(hist_close)

class Close_Higher_Than_Open(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        
    def calc(self, DataManager, ticker, date):
        quote = DataManager.get(ticker, date)
        return quote.close > quote.open

def new_new_20_period_closing_high():
    return New_20_Period_Closing_High()

def new_high_volume():
    return High_Volume()

def new_new_52_week_low():
    return New_52_Week_Low()

def new_new_52_week_high():
    return New_52_Week_High()

def new_crossed_above_200d_moving_average():
    return Crossed_Above_200d_Moving_Average()

def new_close_higher_than_open():
    return Close_Higher_Than_Open()

registered_indicators = {
    'NEW_20_PERIOD_CLOSING_HIGH' : new_new_20_period_closing_high,
    'HIGH_VOLUME' : new_high_volume,
    'NEW_52_WEEK_LOW' : new_new_52_week_low,
    'NEW_52_WEEK_HIGH' : new_new_52_week_high,
    'CROSSED_ABOVE_200D_MOVING_AVERAGE' : new_crossed_above_200d_moving_average,
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
        
