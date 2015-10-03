#*********************************************************************
# File : checkbookReport.py
# Date: 9/8/2015
# Author: Allen Kirby
# Purpose: Generate reports for a checkbook
#*********************************************************************


from Constants import config
import locale

class CheckbookReport:

    def __init__(self, cb):
        self.checkbook = cb

    def genReport(self):
        transTotal = abs(self.checkbook.getTotalForTrans("Debit"))
        print("*" * 15 + " REPORT " + "*" * 15)
        print("Debit Total : ", transTotal)
        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            print(cat)
            for cbt in currentCatList:
                total += abs(cbt.getAmount())
            print("  " + "{:.2%}".format(total / transTotal),
                  "(" + locale.currency(total, grouping=config.THOUSAND_SEP) + ")")
            

        
            

    
