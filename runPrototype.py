import sys
import logging
import random ## only for prototype

from Config import Config  

## 
## Date: 2015-06-21
##
## Description:
## This is a prototype of the Python Stock Back-tester
##
## The user must supply the -c,--config option, which is the location of
## their configuration file.  For the prototype, this file does not need to 
## exist.  Default configuration files are provided by the prototype.
##
## The user may also turn on the silent mode by passing --silent
##
## The application will start and display to the screen (if not silent)
## and log file the a mock back-test.  Finally, the program writes to the
## stats_out file, but just a one-line description describing the future
## contents.
##
## See README.txt for more user doc.
##
## Team Members:
## 
##   Baker, Pierce
##   Casey, Garrett
##   Isaac, Nancy
##   Kelley, Justin
##   Owens, Chris
##

log_file_ext = 'log_out.txt'
stat_file_ext = 'stats_out.txt'

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
    log_file_name = ".".join([str(start_date), str(end_date), log_file_ext])
    
    global stat_file_name
    stat_file_name = ".".join([str(start_date), str(end_date), stat_file_ext])
    
    logging.basicConfig(filename=log_file_name, filemode='w') ## file will be overwritten each time
    logger = logging.getLogger('backtester')
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING if config.get_value('BACKTEST', 'silent') else logging.INFO)
    logger.addHandler(console_handler)
    
    return config, logger

def makeMockStatFile(fn = stat_file_ext):
    stats = open(fn, 'w')
    stats.write("PROTOTYPE:\n\n")
    stats.write("This file will contain the well-formatted, easy to parse,\nhuman-readable results of the back-test.")
    stats.close()

    
def runMockBacktest():
    config, logger = setup_backtest()
    logger.info('============== START_BACKTEST ==============')
    portfolio = config.get_value('PORTFOLIO', 'tickers')
    logger.info('Portfolio is: ' + ','.join(portfolio))
    
    logger.info(
        'Sample period is: ' 
        + '-'.join([str(config.get_value('PORTFOLIO', 'startdate')), str(config.get_value('PORTFOLIO', 'enddate'))]) 
        + ' (' + config.get_value('STRATEGY', 'period_length') + ')'
    )
    
    logger.info('Test Indicator(s): ' + ' AND '.join(config.get_value('STRATEGY', 'indicators')))
    logger.info('')
    
    sample_trade_dates = [
        20150102, 
        20150105, 20150106, 20150107, 20150108, 20150109,
        20150112, 20150113, 20150114, 20150115, 20150116,
        20150120, 20150121, 20150122, 20150123,
        20150126, 20150127, 20150128, 20150129, 20150130,
    ]
    
    rand = random.randint(1,4)
    for ticker in portfolio:
        logger.info('')
        logger.info('Testing: ' + ticker)
        for date in sample_trade_dates:
            msg = str(date)
            if random.randint(1,5) == 1:
                ## Fake an indicator trigger
                msg += ' STRATEGY TRIGGER'
            logger.info(msg)
    
    logger.info('')
    logger.info('Printint Stat Report to: ' + stat_file_name)
    makeMockStatFile(stat_file_name)
    logger.info('')
    logger.info('============== END_BACKTEST ==============')
    

def main():
    return runMockBacktest()
    

if __name__ == '__main__':
    main()
