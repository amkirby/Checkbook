"""Configuration constants"""

import locale

def _unique(data_list):
    return_list = []
    for cat in data_list:
        if cat not in return_list:
            return_list.append(cat)

    return return_list

DATE_FORMAT = "%m/%d/%Y"        # the format for date print
THOUSAND_SEP = True             # whether the amount has a thousands separator
LOCALE = locale.LC_ALL          # the local to use for currency print
USE_SQL = False                 # determines whether to use SQL or XML
FILE_NAME = "2021.xml"         # the XML file name
DB_NAME = "checkbook.db"        # the SQL database file name
DEBIT_CATEGORIES = ["Groceries", "Gas", "Bills", "Entertainment", "Vape", "Food", "Savings", "Other", "Good Time","Vacation","Christmas", "Wedding", "Medical","Whiskey"]
CREDIT_CATEGORIES = ["Bills", "Other", "Paycheck"]
CATEGORIES = _unique(DEBIT_CATEGORIES + CREDIT_CATEGORIES)  # Categories to choose for transactions
CATEGORIES_FOR_ADD = {"Debit": DEBIT_CATEGORIES, "Credit": CREDIT_CATEGORIES}
DEBIT_MULTIPLIER = -1
SORT_BY_KEY = "Date"
