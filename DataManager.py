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

import os, sys
import urllib,time,datetime

class Quote(object):

    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'

    def __init__(self):
        self.symbol = ''
        self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))

    def append(self,dt,open_,high,low,close,volume):
        self.date.append(dt.date())
        self.time.append(dt.time())
    	self.open_.append(float(open_))
    	self.high.append(float(high))
    	self.low.append(float(low))
    	self.close.append(float(close))
    	self.volume.append(int(volume))


    def to_csv(self):
        return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
                    self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
                    self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar])
                    for bar in xrange(len(self.close))])

    def write_csv(self,filename):
        with open(filename,'w') as f:
            f.write(self.to_csv())

    def read_csv(self,filename):
        self.symbol = ''
        self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        for line in open(filename,'r'):
            symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
            self.symbol = symbol
            dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
            self.append(dt,open_,high,low,close,volume)
        return True

    def __repr__(self):
        return self.to_csv()

class DataManager(Quote):

    def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
        super(DataManager,self).__init__()
        self.symbol = symbol.upper()
        start_year,start_month,start_day = start_date.split('-')
        start_month = str(int(start_month)-1)
        end_year,end_month,end_day = end_date.split('-')
        end_month = str(int(end_month)-1)
        url_string = "http://ichart.finance.yahoo.com/table.csv?s={0}".format(symbol)
        url_string += "&a={0}&b={1}&c={2}".format(start_month,start_day,start_year)
        url_string += "&d={0}&e={1}&f={2}".format(end_month,end_day,end_year)
        csv = urllib.urlopen(url_string).readlines()
        csv.reverse()
        for bar in xrange(0,len(csv)-1):
            ds,open_,high,low,close,volume,adjc = csv[bar].rstrip().split(',')
            open_,high,low,close,adjc = [float(x) for x in [open_,high,low,close,adjc]]
            if close != adjc:
                factor = adjc/close
                open_,high,low,close = [x*factor for x in [open_,high,low,close]]
            dt = datetime.datetime.strptime(ds,'%Y-%m-%d')
            self.append(dt,open_,high,low,close,volume)
    
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
        
      
'''    
if __name__ == '__main__':
#    import pdb; pdb.set_trace()
    q = DataManager('aapl','2011-01-01')              # download year to date Apple data
    print q                                          # print it out
    q = DataManager('orcl','2011-02-01','2011-02-28') # download Oracle data for February 2011
    q.write_csv('orcl.csv')                          # save it to disk
    q = Quote()                                      # create a generic quote object
    q.read_csv('orcl.csv')                           # populate it with our previously saved data
    print q   
'''

