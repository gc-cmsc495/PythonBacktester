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
## This is the entry point for PythonBacktester.  This program is run from 
## the command line only.  
## The user must supply the -c,--config option, which is the location of
## their configuration file.  
##
## The user may also turn on the silent mode by passing --silent
##
## To run the program, one must pass the confile file, start date and
## end date to collect the information.
## details of the confile file are in config.py
##  python ./runBacktester.py --config <filename.ini> <start_dt> <end_dt>
## example:
##   python ./runBacktester.py --config example.ini 20150101 20150515

## Team Members:
## 
##   Baker, Pierce
##   Casey, Garrett
##   Isaac, Nancy
##   Kelley, Justin
##   Owens, Chris
##

def setup_backtest():
    """"
    This function gets all the information from the command line and ini file 
    Basic Config errors go to STDERR and not the log file.
    This also sets up the log file.  A separate log file will be created each time 
    program is executed.
    """

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
    this_name = ".".join([config.get_value('PORTFOLIO','name'),  config.get_value('STRATEGY','name')])
    
    log_file_name = ".".join([str(start_date), str(end_date), this_name , config.get_value('PORTFOLIO','log_file_ext')])
    config.put('stat_file_name', ".".join([str(start_date), str(end_date), this_name, config.get_value('PORTFOLIO','stat_file_ext')]))
    
    logging.basicConfig(filename=log_file_name, filemode='w') ## file will be overwritten each time
    logger = logging.getLogger('backtester')
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING if config.get_value('BACKTEST', 'silent') else logging.INFO)
    logger.addHandler(console_handler)
    
    return config, logger

##
## this is called by the main routine.
## This method calls setup_backtest to parse the inputs and calls the config
## class with the input parameters to get the parameters needed for TradeManager and ReportWriter.
##
def runBacktest():
    config, logger = setup_backtest()
    tm = TradeManager(config, logger)
    if tm.run():
        rw = ReportWriter(config, logger)
        rw.write()

##
## main routing for the program
##
def main():
    return runBacktest()
    
if __name__ == '__main__':
    main()
