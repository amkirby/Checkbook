from typing import List
from DataProcessors import XMLProcessor as XML
import CheckbookTransaction as CT
import Checkbook as CB

def copy():
    save_function = XML.XMLProcessor.save
    load_function = XML.XMLProcessor.load

    from_checkbook_name = input("Checkbook to copy from : ")
    to_checkbook_name = input("Checkbook to copy to : ")

    from_checkbook = CB.Checkbook()
    from_checkbook.load(from_checkbook_name, load_function)

    to_checkbook = CB.Checkbook()
    to_checkbook.load(to_checkbook_name, load_function)

    last_trans_of_to = to_checkbook.get_register()[-1]

    # COPY LOGIC
    # print("Last trans of to :\n", last_trans_of_to)
    reversed_from_checkbook = from_checkbook.get_register()[::-1]
    trans_to_add : List[CT.CheckbookTransaction] = []
    for current_trans in reversed_from_checkbook:
        # print(current_trans)
        if(current_trans != last_trans_of_to):
            trans_to_add.append(current_trans)
        else:
            break

    print("*" * 10 + " Transactions Being Added " + "*" * 10)
    for current_trans in trans_to_add[::-1]:
        print(current_trans)
    print("*" * len("*" * 10 + " Transactions Being Added " + "*" * 10))


    for current_trans in trans_to_add[::-1]:
        # print(current_trans)
        to_checkbook.add_single_trans(current_trans)


    # print(to_checkbook)
    if(to_checkbook.is_edited()):
        to_checkbook.save(save_function)
        print("saved successfully!")


# COMPARE LOGIC
# for trans in from_checkbook.get_register():
#     if(trans not in to_checkbook.get_register()):
#         print(trans)