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

import urllib,logging,Util

class Quote(object):

    def __init__(self, date, open, high, low, close, volume):
        self.date, self.open, self.high, self.low, self.close, self.volume = date, float(open), float(high), float(low), float(close), int(volume)

class HistoricalQuotes(object):

    def __init__(self, symbol, start_date, end_date):
        
        symbol = symbol.upper()
        start_year,start_month,start_day = Util.parse_date(start_date)
        end_year,end_month,end_day = Util.parse_date(end_date)
        
        start_month = str(int(start_month) - 1)
        end_month   = str(int(end_month) - 1)

        self.data = [];
        
        url_string = "http://ichart.finance.yahoo.com/table.csv?g=d&s={0}".format(symbol)
        url_string += "&a={0}&b={1}&c={2}".format(start_month,start_day,start_year)
        url_string += "&d={0}&e={1}&f={2}".format(end_month,end_day,end_year)
        
        try:
            url = urllib.urlopen(url_string)
            if url.getcode() == 200:
                csv = url.readlines()
                csv.reverse()
                for bar in xrange(0,len(csv)-1):
                    ds,open,high,low,close,volume,adjc = csv[bar].rstrip().split(',')
                    open,high,low,close,adjc = [float(x) for x in [open,high,low,close,adjc]]
                    if close != adjc:
                        factor = adjc/close
                        open,high,low,close = [x*factor for x in [open,high,low,close]]
                    ds = int(ds.translate(None, '-'))
                    self.data.append(Quote(ds, open, high, low, close, volume))
        except:
            pass ## just leave data empty

class TradeCalendar(object):
    
    def __init__(self, logger, start_date, end_date, pre_buffer, post_buffer):
    
        self.logger = logger
        self.logger.info("Creating trading calendar...")
        self.calendar_list = []  ## keep a list for order
        self.calendar_hash = {}  ## keep a dict for fast lookup

        start_date_index        = -1
        end_date_index          = -1
        
        self.actual_start_date  = 0
        self.actual_end_date    = 0
        self.min_date           = 0
        self.max_date           = 0

        cal = HistoricalQuotes("GE", Util.DEFAULT_START_DATE, Util.DEFAULT_END_DATE)
        if not cal.data:
            self.logger.critical("Was not able to fetch trading calendar from Yahoo!")
            exit(1)
            
        i=0
        for quote in cal.data:
            date = quote.date
            if (start_date_index == -1 and date >= start_date): start_date_index = i
            if (start_date_index != -1):
                if date > end_date: 
                    end_date_index = i-1
                    break
            i += 1
        
        if int(start_date_index == -1):
            self.logger.critical("STRANGE: I could not find startdate {0} in trade calendar".format(start_date))
            exit(1)
        if int(end_date_index == -1):
            self.logger.critical("enddate {0} is beyond trading calendar".format(end_date))
            exit(1)
    
        if start_date_index - pre_buffer < 0: 
            self.logger.critical("To load indicators, I need {0} periods before {1}, which I don't have in the trading calendar.".format(pre_buffer, start_date))
            exit(1)
        if end_date_index + post_buffer >= len(cal.data): 
            self.logger.critical("To perform markouts, I need {0} periods after {1}, which I don't have in the trading calendar".format(post_buffer, start_date))
            exit(1)
        
        k=0
        for i in range(start_date_index - pre_buffer, end_date_index + post_buffer):
            date = cal.data[i].date
            self.calendar_list.append(date);
            self.calendar_hash[date] = k
            k += 1

        self.actual_start_date = cal.data[start_date_index].date
        self.actual_end_date   = cal.data[end_date_index].date
        self.min_date          = self.calendar_list[0]
        self.max_date          = self.calendar_list[-1]
        self.logger.info("Max and Min dates are {0} and {1}".format(self.min_date, self.max_date))
        self.logger.info("Setting trade dates to {0} - {1}".format(self.actual_start_date,self.actual_end_date))
        

class DataManager(object):  


    def __init__(self,logger,start_date,end_date,pre_buffer=20, post_buffer=20):

        self.logger = logger
        self.calendar = TradeCalendar(logger, start_date, end_date, pre_buffer, post_buffer)
        self.tickers = {} ## Dictionary to hold quotes
    
    def trading_dates(self, asHash = False):
        start_date_index = self.calendar.calendar_hash[self.calendar.actual_start_date]
        end_date_index   = self.calendar.calendar_hash[self.calendar.actual_end_date]
        return self.calendar.calendar_list[start_date_index:(end_date_index+1)]

    def date_by_offset(self, anchor, offset):
        index = self.calendar.calendar_hash[anchor]
        return self.calendar.calendar_list[index + offset]

        
    def get(self, ticker, date, periods=0):
        if (date > self.calendar.max_date): 
            self.logger.critical("In DataManager.get() date {0} is greater than max date {1}".format(date, self.calendar.max_date))
            exit(1)
        if (date < self.calendar.min_date):
            self.logger.critical("In DataManager.get() date {0} is less than min date {1}".format(date, self.calendar.min_date))
            exit(1)

        if (not ticker in self.tickers):
            self.logger.info("Fetching historical data from yahoo for:" + ticker)
            self.tickers[ticker] = HistoricalQuotes(ticker, self.calendar.calendar_list[0], self.calendar.calendar_list[-1])
            if not self.tickers[ticker].data:
                self.logger.critical("DataManager could not get Yahoo quotes for ticker {0}".format(ticker))
                exit(1)
            if self.tickers[ticker].data[0].date > self.calendar.calendar_list[0]:
                self.logger.critical("There is not enough to run analysis on {0}, earliest date {1} is greater than {2}".format(ticker,self.tickers[ticker].data[0].date, self.calendar.calendar_list[0]))
                exit(1)
            if self.tickers[ticker].data[-1].date < self.calendar.calendar_list[-1]:
                self.logger.critical("There is not enough to run analysis on {0}, latest date {1} is greater than {2}".format(ticker,self.tickers[ticker].data[-1].date, self.calendar.calendar_list[-1]))
                exit(1)
                

        input_date_index = self.calendar.calendar_hash[int(date)]
        calc_date_index = input_date_index + periods
        
        if calc_date_index > len(self.calendar.calendar_list) or calc_date_index < 0:
            self.logger.critical("In DataManager.get() date {0} plus the number of periods requested {1} exceeds the trading calendar".format(date, periods))
            exit(1)
        
        if (input_date_index > calc_date_index):
            return self.tickers[ticker].data[calc_date_index:input_date_index+1]
        elif(input_date_index < calc_date_index):
            return self.tickers[ticker].data[input_date_index:calc_date_index+1]
        else:
            return self.tickers[ticker].data[input_date_index]
            
