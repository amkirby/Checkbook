#*********************************************************************
# File: printConstants.py
# Date: 9/2/2015
# Author: Allen Kirby
# Purpose: Constants that are used when generating print for the
#          checkbook and checkbook transactions.
#          This file WILL need to be modified if new columns are added 
#*********************************************************************
DATE_SIZE   = 12                # size of the date column
TRANS_SIZE  = 8                 # size of the trans type column
DESC_SIZE   = 40                # size of the description column
AMOUNT_SIZE = 12                # size of the amount column
NUM_SIZE    = 6                 # size of the trans num column
CAT_SIZE    = 15
SIZELIST    = [DATE_SIZE, TRANS_SIZE, CAT_SIZE, DESC_SIZE, AMOUNT_SIZE, NUM_SIZE] # used for spacing when print the trans
HLINE_CHAR = '-'                # the character used as the horizontal separator
VLINE_CHAR = '|'                # the character used as the veritcal separator
