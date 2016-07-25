from Constants import config, printConstants
import sqlite3 as lite
import CheckbookTransaction as CBT
from datetime import datetime

class SQLProcessor:
    """This class handles the saving and loading of the checkbook from a database"""
    @classmethod
    def _scrub(cls, string_to_scrub):
        return ''.join(s for s in string_to_scrub if s.isalnum())

    @classmethod
    def _table_exists(cls, table_name):
        conn = None
        returnVal = False
        try:
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = ?", (table_name,))
            returnVal = cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

        return returnVal[0]

    @classmethod
    def _create_columns(cls):
        columns = "("
        for i in range(len(CBT.KEYS)):
            data_type = "VARCHAR(" + str(printConstants.SIZELIST[i]) + ")"
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
    def _create_table(cls, table_name):
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
    def save(cls, table_name, checkbook_register):
        conn = None
        try:
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            table_name = cls._scrub(table_name.split('.')[0])
            if not cls._table_exists(table_name):
                cls._create_table(table_name)
            cursor.execute("DELETE FROM " + table_name)
            list_of_cbt_tuples = []
            for cbt in checkbook_register:
                cbt_list_before_tuple = []
                for key in CBT.KEYS:
                    value = cbt.getValue(key)
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
    def load(cls, table_name):
        conn = None
        return_list = []
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
                    cbt.setValue(key, row[key])
                return_list.append(cbt)

        except lite.Error as e:
            raise e
        finally:
            if conn:
                conn.close()

        return return_list