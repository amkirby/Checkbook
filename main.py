#********************************************************************
# File    : main.py
# Date    : Sept. 2, 2015
# Author  : Allen Kirby
# Purpose : A checkbook program
#********************************************************************

import argparse

import Checkbook as CB
import CommandProcessor as CP
import ConfigurationProcessor as Conf
from DataProcessors import SQLProcessor as SCP
from DataProcessors import XMLProcessor as XML
from DisplayProcessors import CLIDisplayProcessor, QtDisplayProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    conf = Conf.ConfigurationProcessor()

    checkbook = CB.Checkbook()
    if conf.get_property("USE_SQL"):
        save_function = SCP.SQLProcessor.save
        load_function = SCP.SQLProcessor.load
    else:
        save_function = XML.XMLProcessor.save
        load_function = XML.XMLProcessor.load

    checkbook.load(conf.get_property("FILE_NAME"), load_function)

    parser.add_argument("-t", "--Type",  help="Run GUI or CLI") # choices=['GUI', 'gui', 'CLI', 'cli'],
    args = parser.parse_args()

    use_gui = conf.get_property("USE_GUI")
    if args.Type:
        if args.Type.lower() == "gui":
            use_gui = True
        elif args.Type.lower() == "cli":
            use_gui = False
        
    if use_gui:
        ##################
        # Qt GUI
        ##################
        run = QtDisplayProcessor.QtDisplayProcessor(save_function, load_function, checkbook)
        run.main()
    else:
        ##################
        # CLI
        ##################
        display_processor = CLIDisplayProcessor.CLIDisplayProcessor()
        commProcessor = CP.CommandProcessor(checkbook, display_processor)

        run = CP.CLIRun(commProcessor, display_processor, save_function, load_function)
        run.main()

