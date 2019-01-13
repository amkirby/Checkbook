"""Configuration constants"""

import locale

DATE_FORMAT = "%m/%d/%Y"        # the format for date print
THOUSAND_SEP = True             # whether the amount has a thousands separator
LOCALE = locale.LC_ALL          # the local to use for currency print
USE_SQL = False                 # determines whether to use SQL or XML
FILE_NAME = "myXML.xml"         # the XML file name
DB_NAME = "checkbook.db"        # the SQL database file name
DEBIT_CATEGORIES = ["Groceries", "Gas", "Bills", "Entertainment", "Vape", "Lunch", "Savings", "Other", "Good Time","Christmas"]
CREDIT_CATEGORIES = ["Paycheck"]
CATEGORIES = DEBIT_CATEGORIES + CREDIT_CATEGORIES  # Categories to choose for transactions
DEBIT_MULTIPLIER = -1
SORT_BY_KEY = "Date"
