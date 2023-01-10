import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import Checkbook as CB
from DataProcessors import XMLProcessor as XML

def main():
    checkbook_of_missing = process_compare()

    print(checkbook_of_missing)

def process_compare():
    load_function = XML.XMLProcessor.load

    comp1 = input("Checkbook for search transactions : ")
    comp2 = input("Checkbook to compare to : ")

    from_checkbook = CB.Checkbook()
    from_checkbook.load(comp1, load_function)

    to_checkbook = CB.Checkbook()
    to_checkbook.load(comp2, load_function)


    checkbook_of_missing = CB.Checkbook()

    trans_found = False
    for from_cbt in from_checkbook.get_register():
        for to_cbt in to_checkbook.get_register():
            if(from_cbt == to_cbt):
                trans_found = True
                break

        if(not trans_found):
                checkbook_of_missing.add_single_trans(from_cbt)
        
        trans_found = False
    
    
    return checkbook_of_missing



if __name__ == "__main__":
    main()


