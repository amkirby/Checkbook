#*********************************************************************
# File    : config.py
# Date    : 9/4/2015
# Author  : Allen Kirby
# Purpose : constants that are used for the configuration on the
#           program
#*********************************************************************

import locale

DATE_FORMAT = "%m/%d/%Y"        # the format for date print
THOUSAND_SEP = True             # whether the amount has a thousands
                                # separator
LOCALE = locale.LC_ALL          # the local to use for currency print
FILE_NAME = "myXML.xml"
DEBIT_CATEGORIES = ["Groceries", "Gas", "Bills", "Entertainment", "Vape", "Lunch", "Savings", "Other"]
CREDIT_CATEGORIES = ["Paycheck"]
CATEGORIES = DEBIT_CATEGORIES + CREDIT_CATEGORIES # Categories to choose for transactions
