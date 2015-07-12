# Date: 2015-06-20
# Description:
# The user will execute the program via the command line with three arguments:
# a start date, end date and the path to a text configuration file. The purpose of 
# the config file to so that back-tests (experiments) can be reproduced simply
# by providing the same config.

# The Config class will parse the command line arguments and also the
# configuration file. See example.ini for an example configuration file.

# Class Author: Chris Owens

# Use Case:
#  1. user provides main application with command-line arguments
#  2. main application instantiates the Config class as passes command-line arguments
#  3. Config class parses command-line arguments
#    3.a. Opens configuration file and parses
#    3.b. Verifies correctness of parameters and settings
#  4. Returns OK status or croaks with error
#  5. Main application and Classes requests settings via Config class immutable getter methods
#  6. Classes may set SHAREABLE values via put method.

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
            if name == 'log_file_ext': return 'log_out.txt'
            if name == 'stat_file_ext': return 'stats_out.txt'
            if name == 'trade_log_file_ext': return 'trades_out.txt'
        elif category == 'STRATEGY':
            if name == 'name': return 'high_volume_up_days'
            if name == 'markout_periods': return [5,10,20]
            if name == 'period_length': return 'daily'
            if name == 'indicators': return ['HIGH_VOLUME', 'CLOSE_HIGHER_THAN_OPEN']
        elif category == 'BACKTEST':
            if name == 'silent': return self.silent
        elif category == 'SHAREABLE':
            return self.config['SHAREABLE' + '.' + name]  ## TODO check for existence
        
        return default
        
    def get_value(self, category, name, default=None):
        val = self.value_beta(category,name)
        return val
        
    def put(self, name, value):
        self.config['SHAREABLE' + '.' + name] = value
        
    def parse(self):
        ##TODO
        ## This should be a private function (if possible in python)
        ## that parses the config file.  There may be a core module available to help
        pass;
     
    def validate (self):
        ## TODO
        ## A private function that validates the that minimum parameters were provided
        ## and that the values are correct
        pass;
        
        