#*********************************************************************
# File : checkbookReport.py
# Date: 9/8/2015
# Author: Allen Kirby
# Purpose: Generate reports for a checkbook
#*********************************************************************


from Constants import config
import locale

REPORT_TYPES = ["Monthly", "Total"]
headerFormat = "{:*^40}"
class CheckbookReport:

    def __init__(self, cb):
        """Initializes the report with the specified checkbook
        Parameter:
            cb (Checkbook) : the checkbook to operate on
        """
        self.checkbook = cb

    def genReport(self):
        """Generates an Expense report for all Debit transactions"""
        transTotal = abs(self.checkbook.getTotalForTrans("Debit"))
        catTotal = 0.0
        print("\n" + headerFormat.format(" REPORT "))
        print("\nDebit Total : ", locale.currency(transTotal, grouping=config.THOUSAND_SEP) + "")
        print("Pay Total   : ", locale.currency(self.checkbook.getTotalForCat("Paycheck"),
                                                grouping=config.THOUSAND_SEP) + "\n")
        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            print(cat)
            for cbt in currentCatList:
                total += abs(cbt.getAmount())
            catTotal += total
            print("  " + "{:.2%}".format(total / transTotal),
                  "(" + locale.currency(total, grouping=config.THOUSAND_SEP) + ")")
        print("\nSavings :", str(locale.currency(self.checkbook.getTotalForCat("Paycheck") - catTotal,
                                               grouping=config.THOUSAND_SEP)))
        print("\n" + headerFormat.format(" END REPORT "))

    def genMonthlyReport(self, month):
        """Generates an Expense report for all Debit transactions for the specified month
        Parameters:
            month : an integer representing the month used to generate the report
        """
        transTotal = abs(self.checkbook.getTotalForTransMonth("Debit", month))
        catTotal = 0.0
        print("\n" + headerFormat.format(" MONTHLY REPORT "))
        print("\nDebit Total : ", locale.currency(transTotal, grouping=config.THOUSAND_SEP) + "")
        print("Pay Total   : ", locale.currency(self.checkbook.getTotalForCatMonth("Paycheck", month),
                                                grouping=config.THOUSAND_SEP) + "\n")
        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            print (cat)
            for cbt in currentCatList:
                date = cbt.getDate().month
                if date == month:
                    total += abs(cbt.getAmount())
            catTotal += total
            print("  " + "{:.2%}".format(total / transTotal),
                  "(" + locale.currency(total, grouping=config.THOUSAND_SEP) + ")")
        print("\nSavings :", str(locale.currency(self.checkbook.getTotalForCatMonth("Paycheck", month) - catTotal,
                                               grouping=config.THOUSAND_SEP)))
                    
        print("\n" + headerFormat.format(" END REPORT "))
