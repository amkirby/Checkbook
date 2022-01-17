from datetime import datetime
from typing import Any, List, Tuple

from Exceptions import InvalidDateRangeError


class DateProcessor():
    

    def __init__(self, date_string: Any) -> None:
        self._load_defaults()
        if(date_string is not None):
            try:
                self.date_string = str(date_string)
                self.month_start, self.month_end, self.year_start, self.year_end = self._process_date_range(date_string)
                self.is_valid = self._validate_date_ranges()
                if(not self.is_valid):
                    raise InvalidDateRangeError(self.date_string ,"Invalid date range entered : ")
            except ValueError:
                # catches a letter in the value entered
                error = InvalidDateRangeError(self.date_string, "Invalid date range entered : ")
                raise error
            except InvalidDateRangeError as e:
                raise e


    def is_valid_date_range(self) -> bool:
        return self.is_valid

    def date_within_range(self, date : datetime) -> bool:
        within_range = False
        if (date.month >= self.month_start and date.month <= self.month_end) and (date.year >= self.year_start and date.year <= self.year_end):
            within_range = True
        
        return within_range


    def _load_defaults(self) -> None:
        self.date_string : str = ""
        self.month_start : int = 1
        self.month_end : int = 12
        self.year_start : int = 1998
        self.year_end : int = 9999
        self.is_valid : bool = True

    def _validate_date_ranges(self) -> bool:
        is_valid = True
        month_valid = False
        year_valid = False
        if(self.month_start <= self.month_end and 1 <= self.month_start <= 12 and 1 <= self.month_end <= 12):
            month_valid = True
        if(self.year_start <= self.year_end and 1998 <= self.year_start <= 9999 and 1998 <= self.year_end <= 9999):
            year_valid = True
        
        is_valid = month_valid and year_valid

        return is_valid

    def _process_date_range(self, month_str: str) -> Tuple[int, int, int, int]:
        month_start = 1
        month_end = 12
        year_start = 1998
        year_end = 9999

        vals = month_str.split() # separate month and year by spaces
        if(len(vals) == 1):
            # could be month (range) or year (range)
            ranges = vals[0].split("-")
            ranges = [int(i) for i in ranges]
            if(ranges[0] >= 1 and ranges[0] <= 12):
                #month value
                month_start, month_end = self._get_start_end_values(ranges)
            else:
                # assumed year value
                year_start, year_end = self._get_start_end_values(ranges)
        elif(len(vals) == 2):
            # both month (range) and year (range)
            month_ranges = vals[0].split("-")
            month_ranges = [int(i) for i in month_ranges]
            year_ranges = vals[1].split("-")
            year_ranges = [int(i) for i in year_ranges]

            month_start, month_end = self._get_start_end_values(month_ranges)
            year_start, year_end = self._get_start_end_values(year_ranges)


        return month_start, month_end, year_start, year_end

    def _get_start_end_values(self, ranges : List[int]) -> Tuple[int, int]:
        start = -1
        end = -1

        if(len(ranges) == 1):
            start = end = ranges[0]
        else:
            start = ranges[0]
            end = ranges[1]


        return start, end
