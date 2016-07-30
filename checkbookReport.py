import locale
from Constants import config

REPORT_TYPES = ["Monthly", "Total"]
HEADER_FORMAT = "{:*^40}"


class CheckbookReport:
    def __init__(self, cb):
        """Initializes the report with the specified checkbook

        Args:
            cb (Checkbook) : the checkbook to operate on
        """
        self.checkbook = cb

    def gen_report(self, month=None):
        """
        Generates a report for the entire checkbook or a particular month if one is specified

        Args:
            month (int): The int value for a month

        Returns:
            str: A report of the checkbook broken out into categories
        """
        return_string = ""
        trans_total, pay_total = self._get_totals_for_reports(month)
        format_string = "{:<12}"
        return_string += "\n" + HEADER_FORMAT.format(" REPORT ") + "\n"
        return_string += ("\n" + format_string.format("Pay Total") + ": " +
                          locale.currency(pay_total, grouping=config.THOUSAND_SEP) + "\n")
        return_string += (format_string.format("Debit Total") + ": " +
                          locale.currency(trans_total, grouping=config.THOUSAND_SEP) + "\n")
        return_string += (format_string.format("Savings") + ": " +
                          locale.currency(pay_total - trans_total, grouping=config.THOUSAND_SEP) + "\n")
        return_string += "\n"  # add extra space before printing categories
        for cat in config.DEBIT_CATEGORIES:
            current_cat_list = self.checkbook.get_category(cat)
            return_string += cat + "\n"
            total = self._get_cbt_total_for_category(current_cat_list, month)

            return_string += ("  " + "{:.2%}".format(total / trans_total) + " (" +
                              locale.currency(total, grouping=config.THOUSAND_SEP) + ")" + "\n")
        return_string += "\n" + HEADER_FORMAT.format(" END REPORT ") + "\n"
        return return_string

    def _get_totals_for_reports(self, month):
        """Gets the debit total and the credit total for the checkbook.

        Args:
            month (None | int) : if None, it is a total report, otherwise it is a monthly report
        """
        if month is None:
            # ASSERT: this report is a total report
            trans_total = abs(self.checkbook.get_total_for_trans("Debit"))
            pay_total = self.checkbook.get_total_for_trans("Credit")
        else:
            # ASSERT: this report is a monthly report
            trans_total = abs(self.checkbook.get_total_for_trans_month("Debit", month))
            pay_total = self.checkbook.get_total_for_trans_month("Credit", month)
        return trans_total, pay_total

    def _get_cbt_total_for_category(self, cbt_list, month):
        """Gets the total for the given CBT list.

        Args:
            cbt_list (list) : CBTs for a specific category
            month (None | int) : if None, it is a total report, otherwise it is a monthly report
        """
        total = 0
        for cbt in cbt_list:
            if cbt.getValue("Trans") == "Debit":  # added Debit check b/c some categories can be both
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
        REPORT_TYPES[0]: gen_report,
        REPORT_TYPES[1]: gen_report
    }
