## This clas is used by the Analysis Class to  calculate mean, min, max, sum 
## variance and standard deviation
## from a data stream (as values appear).
## http://www.johndcook.com/standard_deviation.html
##
## Class Author: 
##

import math

class RunningStat(object):
    def __init__(self):
        self.num_data_values = 0
        self.old_mean        = 0.0
        self.new_mean        = 0.0
        self.old_var         = 0.0
        self.new_var         = 0.0
        self.min             = 1e16
        self.max             = -1e16

    def clear(self):
      self.num_data_values = 0

    def Push(self, value):

        self.num_data_values += 1
        value = float(value)

        ## See Knuth TAOCP vol 2, 3rd edition, page 232
        if (self.num_data_values == 1):
            self.old_mean = self.new_mean = value
            self.old_var  = 0.0;
        else:
            self.new_mean = self.old_mean + (value - self.old_mean) / self.num_data_values
            self.new_var  = self.old_var  + (value - self.old_mean) * (value - self.new_mean)
            self.old_mean = self.new_mean
            self.old_var  = self.new_var

        if value > self.max: self.max = value 
        if value < self.min: self.min = value 

    def NumDataValues(self):
        return self.num_data_values

    def Mean(self):
        return self.new_mean if self.num_data_values > 0 else 0.0;

    def Min(self):
        return self.min

    def Max(self):
        return self.max

    def Sum(self):
        return self.num_data_values * self.new_mean

    def  Variance(self):
        return self.new_var / (self.num_data_values - 1) if self.num_data_values > 1 else 0.0

    def  StandardDeviation(self):
      return math.sqrt( self.Variance() );

    def  Sharpe(self):
      var = self.StandardDeviation();
      if ( var != 0 ):
        return self.Mean() / var;
      else:
        return 0;

    def  TStat(self):
      if self.num_data_values < 1: return 0
      
      stderr = self.StandardDeviation() / math.sqrt(self.num_data_values)
      if stderr == 0 : return 0
      return self.Mean() / stderr


