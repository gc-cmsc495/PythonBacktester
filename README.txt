Python Stock Back-tester
#########################

The purpose of this program is to perform back-tests on the
combination of well-know,pre-programmed, stock trading indicators.

Current indicators include:
###########################

HIGH_VOLUME: Traded share volume today is greater than 2 times
the trailing 20-period average volume.

CLOSE_HIGER_THAN_OPEN: The last price of the day for the stock
was higher that the first price of the day.

There are more indicators to come!

Back-tests
##########

Back-tests are actually defined experiments, which we must have
the ability reproduce.  Therefore, user input is provided in the
form of a configuration file.  See example.ini for an example
configuration file.

All status output is logged to STDOUT and a log file.  The user
can silence the output to STDOUT by using the command-line
option --silence.  

After a back-test, the program will generate detailed and summary
statistics, which will be placed in a file with the name
START_DATE.END_DATE.stats_out.txt

Where START_DATE and END_DATE are supplied by the user and 
define the sample period.

Installing the Program
######################
First the user must have installed the latest version of Python on their computer.  A copy of python can be located here: https: //www.python.org/downloads/

If you haven't already, download the entire repository from github: https://github.com/gc-cmsc495/PythonBacktester

Running the Program
###################

Once Python has been installed and the repository is located on your computer, navigate to the directory where you have installed the program and type the following in a terminal command line: 

python runBacktester.py --help

The help option will describe the different arguments.  A typical
call is like:

python runBacktester.py --config config_file.ini 20150101 20150231

Where config_file.ini is the name (and path) to the configuration file,
20150101 is the start date (January 01, 2015) and 20150331 is the 
ending date (February 31, 2015).  Note that the dates simply define
the lower and upper bounds of the sample period (they don't have to exist).

The queried ticker can also be changed withon the configuration file.










