# Date: 2015-06-20
# Description:
# The user will execute the program via the command line with three arguments:
# a start date, end date and the path to a text configuration file. The purpose of 
# the config file to so that back-tests (experiments) can be reproduced simply
# by providing the same config.

# The Config class will parse the command line arguments and also the
# configuration file. See example.ini for an example configuration file.

# Class Author: Chris Owens

class Config:

    def __init__(self, options, args):
        self.path = options.config
        self.silent = options.silent
        self.args = args

        self.config = {}
        
        ## TODO
        ## Read and parse the file and store in dictionary
        
    def value_beta(self, category,name, default=None):
        """"Function for beta, return static values"""
        
        if category == 'PORTFOLIO':
            if name == 'name': return 'large_cap'
            if name == 'tickers': return ['AAPL','INTC']
            if name == 'startdate': return 20150101
            if name == 'enddate': return 20150131
        elif category == 'STRATEGY':
            if name == 'name': return 'high_volume_up_days'
            if name == 'markout_periods': return [5,10,20]
            if name == 'period_length': return 'daily'
            if name == 'indicators': return ['HIGH_VOLUME', 'CLOSE_HIGHER_THAN_OPEN']
        elif category == 'BACKTEST':
            if name == 'silent': return self.silent
        
        return default
        
    def get_value(self, category, name, default=None):
        val = self.value_beta(category,name)
        return val
        
      