# Date: 2015-06-20
#
# Description:
#
# An indicator is a Boolean function that consumes a series of 
# price or volume information from the Data Class.
# Some indicators may be composites of other indicators

# Class Author: Pierce Baker

import pprint
 
class Indicator(object):

    def __init__(self):
        self.max_history = 0
     
    def periods_required(self):
        return self.max_history
        
class High_Volume(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        self.max_history = 20

class Close_Higher_Than_Open(Indicator):

    def __init__(self):
        Indicator.__init__(self)
        
      
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
        