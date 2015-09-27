#*********************************************************************
# File    : config.py
# Date    : 9/4/2015
# Author  : Allen Kirby
# Purpose : constants that are used for the configuration on the
#           program
#*********************************************************************

import locale

# DATE_FORMAT = "%Y-%m-%d"        # the format for date print
DATE_FORMAT = "%m/%d/%Y"        # the format for date print
THOUSAND_SEP = True             # whether the amount has a thousands
                                # separator
COMMAND_SEP = ","               # the separator used to split the CLI
                                # input
LOCALE = locale.LC_ALL          # the local to use for currency print
FILE_NAME = "myXML.xml"
CATEGORIES = ["Groceries", "Gas", "Bills"] # Categories to choose for transactions
