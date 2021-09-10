#********************************************************************
# File    : main.py
# Date    : Sept. 2, 2015
# Author  : Allen Kirby
# Purpose : A checkbook program
#********************************************************************

import Checkbook as CB
import CommandProcessor as CP
# from Exceptions import *
from DataProcessors import SQLProcessor as SCP, XMLProcessor as XML
from Constants import config
from DisplayProcessors import CLIDisplayProcessor

checkbook = CB.Checkbook()
if config.USE_SQL:
    save_function = SCP.SQLProcessor.save
    load_function = SCP.SQLProcessor.load
else:
    save_function = XML.XMLProcessor.save
    load_function = XML.XMLProcessor.load

checkbook.load(config.FILE_NAME, load_function)
commProcessor = CP.CommandProcessor(checkbook)

if __name__ == "__main__":
    run = CLIDisplayProcessor.CLIRun(commProcessor, save_function, load_function)
    run.main()
