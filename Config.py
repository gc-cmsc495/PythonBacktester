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

import sys,ConfigParser,os.path,Util

class Config:

    REQUIRED_SETTINGS = {}
    REQUIRED_SETTINGS['PORTFOLIO'] = {}
    REQUIRED_SETTINGS['STRATEGY'] = {}
    
    for field in ('tickers', 'startdate', 'enddate', 'name', 'log_file_ext', 'stat_file_ext', 'trade_log_file_ext'):
        REQUIRED_SETTINGS['PORTFOLIO'][field] = 1
    
    for field in ('indicators','name','markout_periods'):
        REQUIRED_SETTINGS['STRATEGY'][field] = 1
        
    DEFAULT_VALUES = {}
    DEFAULT_VALUES['PORTFOLIO'] = {}
    DEFAULT_VALUES['STRATEGY'] = {}
    
    DEFAULT_VALUES['PORTFOLIO']['name'] = 'pf'
    DEFAULT_VALUES['PORTFOLIO']['log_file_ext'] = 'log_out.txt'
    DEFAULT_VALUES['PORTFOLIO']['stat_file_ext'] = 'stats_out.txt'
    DEFAULT_VALUES['PORTFOLIO']['trade_log_file_ext'] = 'trades_out.txt'
    DEFAULT_VALUES['STRATEGY']['name'] = 'backtest'
    DEFAULT_VALUES['STRATEGY']['markout_periods'] = '5,10,20'
        
    def __init__(self, options, args):
        self.path = options.config
        self.args = args
        
        self.valid = True
        self.error_messages = []

        self.config = {}
        self.config['BACKTEST.silent'] = options.silent
        
        self.__parse()
        if args:
            if len(args) == 1:
                self.config['PORTFOLIO.startdate'], self.config['PORTFOLIO.enddate'] = args[0], args[0]
            else:
                self.config['PORTFOLIO.startdate'], self.config['PORTFOLIO.enddate'] = args[0], args[1]

        self.__inject_default_values()
        self.validate()
        
        
    def get_value(self, category, name, default=None):
        #val = self.value_beta(category,name)
        name = category + '.' + name
        if name in self.config:
            return self.config[name]
        else:
            print >>sys.stderr, "No config value for " + name
            sys.exit(1)
        return val
        
    def put(self, name, value):
        self.config['SHAREABLE' + '.' + name] = value
        
    def __parse(self):
        if os.path.isfile(self.path):
            
            config = ConfigParser.RawConfigParser()
            config.read(self.path)
            
            #iterate the properties
            for each_section in config.sections():
                for (key, val) in config.items(each_section):
                    self.config[each_section + "." + key] = self.__remove_comment(val)
        else:
            print >>sys.stderr, "File not found:" + self.path
            sys.exit(1)        
    
    #private method, remove comment
    def __remove_comment(self, msg):
        comment_pos = msg.find('#')
        if comment_pos != -1:
            return msg[:comment_pos]
        else:
            return msg

    def __inject_default_values(self):
        for section in Config.DEFAULT_VALUES:
            for field in Config.DEFAULT_VALUES[section]:        
                if section+'.'+field not in self.config:
                    self.config[section+'.'+field] = Config.DEFAULT_VALUES[section][field]
            
    def validate (self):
        """ Ensure that all required fields have values"""
        errors = []
        for section in Config.REQUIRED_SETTINGS:
            for field in Config.REQUIRED_SETTINGS[section]:
                if section +'.'+field not in self.config:
                    errors.append(section +'.'+ field + "is a required configuration setting")
        if errors:
            print >>sys.stderr, "\n".join(errors)
            sys.exit(1)

        try:
            start_date = int(self.config['PORTFOLIO.startdate'])
            end_date = int(self.config['PORTFOLIO.enddate'])
            if (start_date > end_date):
                print >>sys.stderr, "{0} > {1}".format(start_date, end_date)
                sys.exit(1)
            if (start_date < Util.DEFAULT_START_DATE):
                print >>sys.stderr, "Start date {0} > default date {1}".format(start_date, Util.DEFAULT_START_DATE)
                sys.exit(1)
                
            if (end_date > Util.DEFAULT_END_DATE):
                print >>sys.stderr, "End date {0} > default date {1}".format(end_date, Util.DEFAULT_END_DATE)
                sys.exit(1)
                
            self.config['PORTFOLIO.startdate'] = start_date
            self.config['PORTFOLIO.enddate'] = end_date
        except:
            print >>sys.stderr, "Invalid date when trying start and end dates"
            sys.exit(1)
  
        