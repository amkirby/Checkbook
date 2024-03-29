HELP_COMMAND  = "help"          # prints the help
ADD_COMMAND   = "add"           # adds a transaction
PRINT_COMMAND = "print"         # prints the checkbook
SAVE_COMMAND  = "save"          # saves the checkbook
EDIT_COMMAND = "edit"           # edit a transaction
REPORT_COMMAND = "report"       # generate a report
LOAD_COMMAND = "load"           # load an XML file
DELETE_COMMAND = "delete"
SORT_COMMAND = "sort"
SEARCH_COMMAND = "search"
RESEQUENCE_COMMAND = "reseq"
COPY_COMMAND = "copy"
CSV_COMMAND = "csv"
COMPARE_COMMAND = "compare"

TRANS_TYPES = ["Debit", "Credit"]

EXIT_LIST = ["Quit", "quit", "Exit", "exit", "q"] # the commands that exit the program
help_headers_format = "{:*^35}"
top_help_helper = help_headers_format.format(" HELP ")
bot_help_header = help_headers_format.format(" END HELP ")
# displays when the help command is executed
EXIT_HELP = """
How to exit:
    Quit/quit
    Exit/exit
    q
"""
COMMAND_HELP = """
Commands:
    help   : Prints this help
    add    : Add a transaction to the checkbook
    print  : Print the checkbook (print [<key> <value>])
    save   : Save the checkbook
    edit   : Edit a transaction (edit [number])
    report : Generate a report about the transactions
    load   : Load a checkbook (load [file name])
    delete : delete a transaction (delete [number])
    search : search for text in the description (search <text>)
    sort   : sort the checkbook by a given header (sort [header | Date])
    reseq  : re-number the entire checkbook
    csv    : save checkbook to a CSV file
"""
HELP_TEXT = ("""
{}
""" + EXIT_HELP + COMMAND_HELP + """
{}
""").format(top_help_helper, bot_help_header)
