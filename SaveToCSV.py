import csv
from typing import Any, Dict, List

import Checkbook as CB
from CheckbookTransaction import KEYS
from DataProcessors import XMLProcessor as XML
import ConfigurationProcessor as Conf

conf = Conf.ConfigurationProcessor()

def _default_to_file_name(from_file_name : str = ""):
    to_file_name = conf.get_property("DEFAULT_TO_CSV")

    if(from_file_name != ""):
        base_from_name = from_file_name.split(".")[0].strip()
        to_file_name = base_from_name + ".csv"

    return to_file_name

def save_to_csv(from_book : str = ""):
    load_function = XML.XMLProcessor.load

    from_default_text : str = ""
    if(from_book != ""):
        from_default_text = "(" + from_book + ")"

    from_checkbook_name = input("Checkbook to save from " + from_default_text + ": ")

    if(from_checkbook_name.strip() == ""):
        from_checkbook_name = from_book

    to_csv_file_name : str = ""

    to_csv_file_name = _default_to_file_name(from_checkbook_name)
    to_csv_name = input("CSV file to save to (" + to_csv_file_name + "): ")

    if(to_csv_name.strip() == ""):
        to_csv_name = to_csv_file_name


    from_checkbook = CB.Checkbook()
    from_checkbook.load(from_checkbook_name, load_function)




    field_names = KEYS
    list_of_trans = from_checkbook.get_register()
    rows : List[Dict[str, Any]] = []
    for trans in list_of_trans:
        rows.append(trans.get_dictionary())

    with open(to_csv_name, 'w', encoding='UTF8',newline='') as f:
        writer = csv.DictWriter(f, field_names)

        # write the header
        writer.writeheader()

        # write the data
        writer.writerows(rows)

        print("save successful!")

if __name__ == "__main__":
    save_to_csv()
