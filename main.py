#********************************************************************
# File    : main.py
# Date    : Sept. 2, 2015
# Author  : Allen Kirby
# Purpose : A checkbook program
#********************************************************************

from Constants import commands
from Constants import config
import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR
checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)
cbEdited = False

def _doSave():
    """Saves the checkbook"""
    save = input("Would you like to save? (y or n) ")
    if(save.lower() == "y"):
        checkbook.save()
        print("save successful!")
    

if __name__ == "__main__":
    print("Welcome to your checkbook!")
    print(checkbook)
    val = input("What would you like to do? : ")

    while(val not in commands.EXIT_LIST):
        if(val == commands.HELP_COMMAND):
            print(commands.HELP_TEXT)
        elif(val == commands.PRINT_COMMAND):
            print(checkbook)
        elif(val == commands.ADD_COMMAND):
            cbEdited = True
            print("Enter your transaction")
            cbt = CBT.CheckbookTransaction()
            for key in CBT.KEYS:
                if key != "Num":
                    if key == "Category":
                        print("Categories to choose:")
                        for cat in config.CATEGORIES:
                            print("  " + cat)
                    val = input(key + " : ")
                    cbt.setValue(key, val)
            checkbook.addSingleTrans(cbt)
        elif(val == commands.EDIT_COMMAND):
            cbEdited = True
            editTrans = int(input("Which transaction do you want to edit? : "))
            trans = checkbook.findTransaction(editTrans)
            for key in CBT.KEYS:
                if key != "Num":
                    if key == "Category":
                        print("Categories to choose:")
                        for cat in config.CATEGORIES:
                            print("  " + cat)
                    val = input(key + " (" + str(trans.getValue(key)) + ")" + " : ")
                    if(val.strip() != ""):
                        trans.setValue(key, val)
        elif(val == commands.REPORT_COMMAND):
            cr = CR.CheckbookReport(checkbook)
            cr.genReport()
        elif(val == commands.LOAD_COMMAND):
            if(cbEdited):
                _doSave()
                
            fileName = input("Enter an XML file to load : ")
            checkbook = CB.Checkbook()
            checkbook.load(fileName)
        elif(val == commands.SAVE_COMMAND):
            if(cbEdited):
                _doSave()

        print(checkbook)

        val = input("What would you like to do? : ")

    # Save prompt
    if(cbEdited):
        _doSave()
