from DataProcessors import SQLProcessor as SCP, XMLProcessor as XML


def main():
    """
    Converts from sql to xml or vice versa
    Returns:
        None
    """
    converting_to = input("What are you converting to? (sql | xml) : ")
    table_file_name = input("Enter the table or file name to load from : ")
    if converting_to == "sql":
        cbt_list = XML.XMLProcessor.load(table_file_name)
        SCP.SQLProcessor.save(table_file_name, cbt_list)
    elif converting_to == "xml":
        cbt_list = SCP.SQLProcessor.load(table_file_name)
        XML.XMLProcessor.save(table_file_name, cbt_list)
    else:
        print("invalid input... exiting")

if __name__ == '__main__':
    main()
