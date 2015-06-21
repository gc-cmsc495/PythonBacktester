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

from DataManager import DataManager
from IndicatorLibrary import IndicatorLibrary
import ReportWriter

class TradeManager(object):

    def __init__(self, config):
        self.indicators = IndicatorLibrary(config.get_value('STRATEGY', 'indicators'))
        self.dm = DataManager(config.get_value('PORTFOLIO','startdate'), config.get_value('PORTFOLIO', 'enddate'), self.indicators.periods_required())
        
        