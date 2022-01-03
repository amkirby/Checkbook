"""Configuration constants"""

import locale
from typing import List

def _unique(data_list: List[str]) -> List[str]:
    return_list: List[str] = []
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
DEBIT_CATEGORIES = ["Groceries", "Gas", "Bills", "Entertainment", "Food", "Savings", "Good Time","Vacation","Christmas", "Wedding", "Medical","Whiskey", "Other"]
CREDIT_CATEGORIES = ["Bills", "Other", "Paycheck"]
CATEGORIES = _unique(DEBIT_CATEGORIES + CREDIT_CATEGORIES)  # Categories to choose for transactions
CATEGORIES_FOR_ADD = {"Debit": DEBIT_CATEGORIES, "Credit": CREDIT_CATEGORIES, "all": CATEGORIES}
DEBIT_MULTIPLIER = -1
SORT_BY_KEY = "Date"
