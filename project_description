Author: Garrett Casey (@gc-cmsc495)

# Overview and Project Plan

## Description

A program that reads a series of historical equity price and volume data and then tests
if any program-supplied fixed indicator (Boolean function), or combination of indicators,
predicts future returns with a high statistical significance.

## IT Systems

The program will be a written python programming language. The user will interact via the command-line.
A configuration file will provide the user specific settings.  Output is sent to a well-formatted text file.

## Data

Historical equity price and volume data will be fetch from finance.yahoo.com via the 
[pandas library](http://pandas.pydata.org/pandas-docs/version/0.16.2/remote_data.html#remote-data-yahoo).
Data will include:

```
trade_date
open
high
low
close
volume
adj.close
```

# Primary Classes for the Application

## Config Class

The user will execute the program via the command line with three arguments: a start date, end date 
and the path to a text configuration file.  The purpose of the config file to so that 
back-tests (experiments) can be reproduced simply by providing the same config.

The Config class will parse the command line arguments and also the configuration file.
The configuration file will have the following format:

```
[PORTFOLIO]

name = large_cap
tickers=AAPL, INTC, ORCL, DELL  # and possibly more
startdate=20140101
enddate=20141231 ## these are overridden if present as program argument

[STRATEGY]

name = high_volume_up_days
markout_periods = 5,10,20 
period_length = daily # can also be weekly or monthly
indicators = HIGH_VOLUME, CLOSE_HIGHER_THAN_OPEN

[PORTFOLIO]

tickers: AAPL, intc, orcl, fb

```

There are a couple things the Config class must account for:

1. Collapse whitespace
1. Ignore all text after the octothorpe (the hash key #)
  1. Consider these comments.
1. Catetories, as define by the text in brackets (e.g. [PORTFOLIO])
1. key = value pairs
  1. The fully qualified key name will be `CATEGORY.key`
  1. The values may be lists delimited by commas (e.g. `STRATEGY.markout_periods = [5,10,20]`)
1. The file is parsed from top to bottom and key/value are overwritten if they appear multiple times
  1. This will allow us to use use the top part of the config file as a template and overwrite with custom settings later in the file.
  1. The interface for the Config class must provide immutable acess methods to the configuration values.

## Data Class
The data class is responsible for fetching, parsing, validating, and provide access methods
to the equity price and volume data.  The class will also provide methods to retrieve data by
index or date.  Finally, due to the nature of the data, this class will provide a trade-date
calendar interface.  The [pandas package](http://pandas.pydata.org/) will be a helful addition to this class.

## Indicator Library Class
An indicator is simply a Boolean function that consumes a series of price or volume information from
the Data Class. Certain methods will be private to the class, such as basic
mathematical function (average), while the indicators themselves will be class methods.
Some indicators may be composites of other indicators.

## TradeManager Class
The TradeManager class will use the Data class and Indicator Library to iterate through the
sample period, record the instances when the indicators are true, determine the future prices,
and ensure events are independent by ensuring no trade overlapping.

### TradeManager Example

|entry_date|exit_date|entry_price|markout_price|ticker|markout_length|indicator|
|----------:|--------:|----------:|------------:|-----:|-------------:|--------:|
|20150427|20150504|132.82|128.16|AAPL|5|HIGH_VOLUME|


The `markout_length` is in units of `STRATEGY.period_length'.  Every time the indidcator returns true, we note the trade
`entry_date` and the caculate the `exit_date` as: 

`exit_date = entry_date + markout_length`

The primary key for the TradeManager is: `ticker, markout_length, indicator`

The TradeManager will not allow another entry for that key until after the `exit_date`.  This methodology ensures that
each event is an indepent as possible.

## Analysis Class

After the TradeManager has iterated through all date, for all tickers in the portfolios,
and has collected each instance when the indicators were true, the Analysis class takes over.

The Analysis class gets the trade data from TradeManager and calculate statistics for each
indicator/markout_length pair.

### Analysis Class Statistics

Statistics for each indicator/markout_length may include

* Average return
* Standard deviation of return
* T-statistic or Sharpe ratio
* Cumulative return based on some beginning notional value 
* Maximum and minimum returns
* Skew, Kurtosis and other distribution stats regarding the returns

## Report Class

The report class will be responsible for taking results from the Analysis Class
and other classes and output the results in a well formatted text file.

We must carefully consider the format in which the results are published so they
can be easily processed by other programs or utilities (e.g. Strategy Comparison Tools, GUIs, etc.).

# Development Process

Each team member will be assigned one or more of the Classes to write and will also be tasked
with providing documentation and test units for said Classes.  

We will be using the GitHub.com as our code repository.  Each team member will code locally and
then submit their work to the group via pull requests, whereupon the team will review the code,
comment, and then eventually merge into the project’s master branch.
