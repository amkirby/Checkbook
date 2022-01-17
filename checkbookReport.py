import locale
from typing import Any, Dict, List, Optional, Tuple

import ConfigurationProcessor as Conf
from Checkbook import Checkbook
from CheckbookTransaction import CheckbookTransaction
from DateProcessor import DateProcessor

conf = Conf.ConfigurationProcessor()

REPORT_TYPES = ["Date Criteria", "Total"]
HEADER_FORMAT = "{:*^40}"
MAX_REPORT_TYPE = len(max(REPORT_TYPES, key=len))

class CheckbookReport:
    def __init__(self, cb: Checkbook):
        """Initializes the report with the specified checkbook

        Args:
            cb (Checkbook) : the checkbook to operate on
        """
        self.checkbook = cb

    def gen_report(self, date_range: Optional[Any]=None) -> str:
        """
        Generates a report for the entire checkbook or a particular date range if one is specified

        Args:
            date_range (None | string): The date range

        Returns:
            str: A report of the checkbook broken out into categories
        """
        return_string = ""
        date_processor = DateProcessor(date_range)
        trans_total, pay_total = self._get_totals_for_reports(date_processor)
        trans_divisor = trans_total if trans_total > 0 else 1
        pay_divisor = pay_total if pay_total > 0 else 1
        register_format = "{:<20}"
        format_string = "{:<12}"
        left_border = "|"
        return_string += "\n" + HEADER_FORMAT.format(" REPORT ") + "\n"
        return_string += ("\n" + format_string.format("Pay Total") + ": " +
                          locale.currency(pay_total, grouping=conf.get_property("THOUSAND_SEP")) + "\n")
        return_string += (format_string.format("Debit Total") + ": " +
                          locale.currency(trans_total, grouping=conf.get_property("THOUSAND_SEP")) + "\n")
        return_string += (format_string.format("Savings") + ": " +
                          locale.currency(pay_total - trans_total, grouping=conf.get_property("THOUSAND_SEP")) + "\n")
        return_string += "\n"  # add extra space before printing categories
        h_line = ("-" * 42)
        return_string += left_border + h_line + "\n"
        return_string += left_border + register_format.format("Debit") + " | " + "Credit" + "\n"
        return_string += left_border + h_line + "\n"
        for cat in conf.get_property("CATEGORIES"):
            current_cat_list = self.checkbook.get_category(cat)
            return_string += left_border + register_format.format(cat) + "\n"
            total = self._get_cbt_total_for_category(current_cat_list, date_processor)
            debit_print, credit_print = self._get_transaction_print(trans_divisor, pay_divisor, total)

            return_string += left_border + register_format.format(debit_print) + " |"
            return_string += credit_print + "\n"
            return_string += left_border + h_line + "\n"

        return_string += "\n" + HEADER_FORMAT.format(" END REPORT ") + "\n"
        return return_string

    def _get_transaction_print(self, trans_divisor: float, pay_divisor: float, total: Dict[str, float]):
        debit_print = ("  " + "{:.2%}".format(total["Debit"] / trans_divisor) + " (" + locale.currency(total["Debit"], grouping=conf.get_property("THOUSAND_SEP")) + ")")
        credit_print = ("  " + "{:.2%}".format(total["Credit"] / pay_divisor) + " (" + locale.currency(total["Credit"], grouping=conf.get_property("THOUSAND_SEP")) + ")")
        if(not conf.get_property("REPORT_DISPLAY_0")):
            if(total["Debit"] == 0):
                debit_print = ""
            if(total["Credit"] == 0):
                credit_print = ""

        return debit_print, credit_print

    def _get_totals_for_reports(self, date_processor: DateProcessor) -> Tuple[float, float]:
        """Gets the debit total and the credit total for the checkbook.

        Args:
            date_processor (DateProcessor): The date range
        """

        trans_total = abs(self.checkbook.get_total_for_trans_month("Debit", date_processor))
        pay_total = self.checkbook.get_total_for_trans_month("Credit", date_processor)
        return trans_total, pay_total

    def _get_cbt_total_for_category(self, cbt_list: List[CheckbookTransaction], date_processor: DateProcessor) -> Dict[str, float]:
        """Gets the total for the given CBT list.

        Args:
            cbt_list (list) : CBTs for a specific category
            date_ (DateProcessor): The date range
        """
        debitTotal = 0
        creditTotal = 0
        transTotal: Dict[str, float] = {};
        for cbt in cbt_list:
            if cbt.get_value("Trans") == "Debit":  # added Debit check b/c some categories can be both
                # debit and credit and reports were wrong
                date = cbt.get_date()
                if date_processor.date_within_range(date):
                    debitTotal += abs(cbt.get_amount())
            elif cbt.get_value("Trans") == "Credit":
                date = cbt.get_date()
                if date_processor.date_within_range(date):
                    creditTotal += abs(cbt.get_amount())
        
        transTotal["Debit"] = debitTotal
        transTotal["Credit"] = creditTotal
        return transTotal

    # A dictionary used to more generically call the methods for this class
    dispatcher = {
        REPORT_TYPES[0]: gen_report,
        REPORT_TYPES[1]: gen_report
    }
