import sqlite3 as lite
from datetime import datetime
from typing import Any, List, Tuple

import CheckbookTransaction as CBT
from Constants import config, printConstants


class SQLProcessor:
    """This class handles the saving and loading of the checkbook from a database"""

    @classmethod
    def _scrub(cls, string_to_scrub: str) -> str:
        """
        Removes all characters except alphanumeric ones from the specified string

        Args:
            string_to_scrub (str): The string to scrub

        Returns:
            str: String containing only alphanumeric characters
        """
        return ''.join(s for s in string_to_scrub if s.isalnum())

    @classmethod
    def _table_exists(cls, table_name: str) -> bool:
        """
        Determines if the specified table exists

        Args:
            table_name (str): the table name to check

        Returns:
            bool: True if the table exists, False otherwise
        """
        conn = None
        return_val = False
        try:
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = ?", (table_name,))
            return_val = cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

        return return_val[0]

    @classmethod
    def _create_columns(cls) -> str:
        """
        Creates a script specifying the column names and types for a checkbook table

        Returns:
            str: a script containing column names and types
        """
        columns = "("
        for i in range(len(CBT.KEYS)):
            data_type = "VARCHAR(" + str(printConstants.SIZE_LIST[i]) + ")"
            if CBT.KEYS[i] == "Date":
                data_type = "DATETIME"
            elif CBT.KEYS[i] == "Amount":
                data_type = "FLOAT"
            columns += CBT.KEYS[i] + " " + data_type
            if i < len(CBT.KEYS) - 1:
                columns += ", "
        columns += ")"
        return columns

    @classmethod
    def _create_table(cls, table_name: str) -> None:
        """
        Creates the specified table if it does not exist

        Args:
            table_name (str): the table to create
        """
        conn = None
        try:
            scrubbed_table_name = cls._scrub(table_name)

            table_script = "CREATE TABLE " + scrubbed_table_name + " " + cls._create_columns()
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            cursor.execute(table_script)
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    @classmethod
    def save(cls, table_name: str, checkbook_register: List[CBT.CheckbookTransaction]) -> None:
        """
        Saves the specified checkbook to the table

        Args:
            table_name (str): the table to store the data
            checkbook_register (list): the transactions to save
        """
        conn = None
        try:
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            table_name = cls._scrub(table_name.split('.')[0])
            if not cls._table_exists(table_name):
                cls._create_table(table_name)
            cursor.execute("DELETE FROM " + table_name)
            list_of_cbt_tuples: List[Tuple[Any, ...]] = []
            for cbt in checkbook_register:
                cbt_list_before_tuple: List[Any] = []
                for key in CBT.KEYS:
                    value = cbt.get_value(key)
                    if key == "Date":
                        value = datetime.strftime(value, config.DATE_FORMAT)
                    cbt_list_before_tuple.append(value)
                list_of_cbt_tuples.append(tuple(cbt_list_before_tuple))
            cursor.executemany("INSERT INTO " + table_name + " VALUES(?, ?, ?, ?, ?, ?)", list_of_cbt_tuples)
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.rollback()
                conn.close()

    @classmethod
    def load(cls, table_name: str) -> List[CBT.CheckbookTransaction]:
        """
        Loads the checkbook from the database

        Args:
            table_name (str): the table to load from

        Returns:
            list: the checkbook transactions from the database
        """
        conn = None
        return_list: List[CBT.CheckbookTransaction] = []
        try:
            conn = lite.connect(config.DB_NAME)
            conn.row_factory = lite.Row
            cursor = conn.cursor()
            table_name = cls._scrub(table_name.split('.')[0])
            if not cls._table_exists(table_name):
                cls._create_table(table_name)
            cursor.execute("SELECT * FROM " + table_name)
            rows = cursor.fetchall()
            for row in rows:
                cbt = CBT.CheckbookTransaction()
                for key in CBT.KEYS:
                    cbt.set_value(key, row[key])
                return_list.append(cbt)

        except lite.Error as e:
            raise e
        finally:
            if conn:
                conn.close()

        return return_list
