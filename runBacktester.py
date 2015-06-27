import sys

import logging
from Config import Config
from TradeManager import TradeManager
from ReportWriter import ReportWriter

## 
## Date: 2015-06-21
##
## Description:
## A Python Stock Back-tester
##
## The user must supply the -c,--config option, which is the location of
## their configuration file.  
##
## The user may also turn on the silent mode by passing --silent
##
## Team Members:
## 
##   Baker, Pierce
##   Casey, Garrett
##   Isaac, Nancy
##   Kelley, Justin
##   Owens, Chris
##


log_file_ext   = 'log_out.txt'
stat_file_ext  = 'stats_out.txt'
stat_file_name = ''

def setup_backtest():
    """"This function gets all the information from the command line and ini file """

    from optparse import OptionParser
    p = OptionParser(usage='usage: %prog [options] [START_DATE] [END_DATE]')
    p.add_option('-c', '--config', dest='config', metavar='CONFIGFILE', help='Specifies input config file')
    p.add_option('-s', '--silent', dest='silent', action='store_true', default=False, help="Specifies if logging to console should be disabled.")
    opts,args = p.parse_args()
    
    if opts.config is None:
        print >>sys.stderr, "No config file specified. Use --help"
        sys.exit(1)
    
    config = Config(opts, args)
    
    start_date = config.get_value('PORTFOLIO', 'startdate')
    end_date = config.get_value('PORTFOLIO', 'enddate')
    log_file_name = ".".join([str(start_date), str(end_date), config.get_value('PORTFOLIO','log_file_ext')])
    
    global stat_file_name
    stat_file_name = ".".join([str(start_date), str(end_date), config.get_value('PORTFOLIO','stat_file_ext')])
    
    logging.basicConfig(filename=log_file_name, filemode='w') ## file will be overwritten each time
    logger = logging.getLogger('backtester')
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING if config.get_value('BACKTEST', 'silent') else logging.INFO)
    logger.addHandler(console_handler)
    
    return config, logger

    
def runBacktest():
    config, logger = setup_backtest()
    tm = TradeManager(config)
    logger.info('Hello World')

    

def main():
    return runBacktest()
    

if __name__ == '__main__':
    main()
