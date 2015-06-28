# Date: 2015-06-20
#
# Description:
#
# The report class will be responsible for taking results from the Analysis Class
# and other classes and output the results in a well formatted text file.
#
# We must carefully consider the format in which the results are published so they
# can be easily processed by other programs or utilities (e.g. Strategy Comparison Tools, GUIs, etc.).
# 

# Class Author: TBD
#
# Use Case:
#   1. Instantiated by main application, passed configuration object.
#   2. Instantiates Analysis class and passes path to trade log (value was set SHARABLE in config by TradeManager)
#   3. Builds well-formatted text from config settings and Analysis results
#   4. Outputs results to stat file
#

from Analysis import Analysis
from Config import Config

class ReportWriter(object):

    def __init__(self):
        return True
