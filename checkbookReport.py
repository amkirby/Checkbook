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

    def genReport(self, month=None):
        returnString = ""
        transTotal, payTotal = self._getTotalsForReports(month)
        formatString = "{:<12}"
        returnString += "\n" + headerFormat.format(" REPORT ") + "\n"
        returnString += ("\n" + formatString.format("Pay Total") + ": " + 
            locale.currency(payTotal, grouping=config.THOUSAND_SEP) + "\n")
        returnString += (formatString.format("Debit Total") + ": " + 
            locale.currency(transTotal, grouping=config.THOUSAND_SEP) + "\n")
        returnString += (formatString.format("Savings") + ": " + 
            locale.currency(payTotal - transTotal, grouping=config.THOUSAND_SEP) + "\n")
        returnString +="\n" # add extra space before printing categories
        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            returnString += cat + "\n"
            total = self._getCBTTotalForCategory(currentCatList, month)

            returnString += ("  " + "{:.2%}".format(total / transTotal) + " (" + 
                locale.currency(total, grouping=config.THOUSAND_SEP) + ")" + "\n")
        returnString += "\n" + headerFormat.format(" END REPORT ") + "\n"
        return returnString

    def _getTotalsForReports(self, month):
        """Gets the debit total and the credit total for the checkbook.
        Parameter:
            month (None | int) : if None, it is a total report, otherwise it is a monthly report
        """
        if month is None:
            # ASSERT: this report is a total report
            transTotal = abs(self.checkbook.getTotalForTrans("Debit"))
            payTotal = self.checkbook.getTotalForTrans("Credit")
        else:
            # ASSERT: this report is a monthly report
            transTotal = abs(self.checkbook.getTotalForTransMonth("Debit", month))
            payTotal = self.checkbook.getTotalForTransMonth("Credit", month)
        return transTotal, payTotal

    def _getCBTTotalForCategory(self, cbtList, month):
        """Gets the total for the given CBT list.
        Parameters:
            cbtList (list) : CBTs for a specific category
            month (None | int) : if None, it is a total report, otherwise it is a monthly report
        """
        total = 0
        for cbt in cbtList:
            if cbt.getValue("Trans") == "Debit": # added Debit check b/c some categories can be both
                                                 # debit and credit and reports were wrong
                if month is None:
                    # ASSERT: this report is a total report
                    total += abs(cbt.getAmount())
                else:
                    # ASSERT: this report is a monthly report
                    date = cbt.getDate().month
                    if date == month:
                        total += abs(cbt.getAmount())

        return total

    # A dictionary used to more generically call the methods for this class
    dispatcher = {
        REPORT_TYPES[0] : genReport,
        REPORT_TYPES[1] : genReport
    }
