import sys

import Logger
from Config import Config
from TradeManager import TradeManager

def setup_backtest():
    """"This function gets all the information from the command line and ini file """

    from optparse import OptionParser
    p = OptionParser(usage='usage: %prog [options] [START_DATE] [END_DATE]')
    p.add_option('-c', '--config', dest='config', metavar='CONFIGFILE', help='Specifies input config file')
    opts,args = p.parse_args()
    
    if opts.config is None:
        print >>sys.stderr, "No config file specified"
        sys.exit(1)
    
    config = Config(opts.config, args)
    return config
    
def runBacktest():
    config = setup_backtest()
    tm = TradeManager(config)
    Logger.log('info', 'Hello World')
    

def main():
    return runBacktest()
    

if __name__ == '__main__':
    main()
