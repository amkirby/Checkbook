from datetime import datetime
import xml.etree.ElementTree as ET

from Constants import config
import CheckbookTransaction as CBT


class XMLProcessor:
    @classmethod
    def load(cls, file_name):
        """
        Loads xml from the specified file
        Parameters:
            file_name (string): the file name to load the xml
        """
        return_list = []
        try:
            root = ET.parse(file_name)
            treeIter = root.iter("Transaction")
            for elem in treeIter:
                cbt = CBT.CheckbookTransaction()
                for child in list(elem):
                    cbt.setValue(child.tag, child.text)
                return_list.append(cbt)
        except FileNotFoundError:
            print("The file " + file_name + " was not found.")
        except ET.ParseError:
            print("There was an error parsing " + file_name, "(possibly empty).")

        return return_list

    @classmethod
    def save(cls, file_name, checkbook_register):
        """
        Saves the specified checkbook transactions to the specified file name as xml
        Args:
            checkbook_register (list): an array of checkbook transactions to save
            file_name (string): the file to save the xml
        """
        root = ET.Element('Transactions')
        for elem in checkbook_register:
            currTrans = ET.SubElement(root, "Transaction")
            for key, value in elem.getItems():
                transElem = ET.SubElement(currTrans, key)
                if (key == "Date"):
                    value = datetime.strftime(value, config.DATE_FORMAT)
                transElem.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_name, xml_declaration=True)
