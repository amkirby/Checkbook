from Constants import config
import sqlite3 as lite
import CommandProcessor as CP
import CheckbookTransaction as CBT

class SQLCommandProcessor(CP.CommandProcessor):
    """This class handles the saving and loading of the checkbook from a database"""
    def __init__(self, checkbook):
        super(SQLCommandProcessor, self).__init__(checkbook)

    def _scrub(self, string_to_scrub):
        return ''.join(s for s in string_to_scrub if s.isalnum())

    def _table_exists(self, tableName):
        conn = None
        returnVal = False
        try:
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = ?", (tableName))
            returnVal = cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

        return returnVal

    def _create_table(self, tableName):
        conn = None
        try:
            scrubed_table_name = self._scrub(tableName)

            table_script = "CREATE TABLE " + scrubed_table_name + " ("
            for i in range(len(CBT.KEYS) - 1):
                table_script += self._scrub(CBT.KEYS[i]) + ", "
            table_script += self._scrub(CBT.KEYS[-1]) + ")"
            conn = lite.connect(config.DB_NAME)
            cursor = conn.cursor()
            cursor.execute(table_script)
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def _doSave(self):
        save = input("Would you like to save? (y or n) ")
        if(save.lower() == "y"):
            conn = None
            try:
                conn = lite.connect(config.DB_NAME)
                cursor = conn.cursor()
            except Exception as e:
                raise e
            finally:
                if conn:
                    conn.close()
            print("save successful!")

    def processLoadCommand(self):
        conn = None
        try:
            conn = lite.connect(config.DB_NAME)
            conn.row_factory = lite.Row
            cursor = conn.cursor()
            tableName = self.checkbook.fileName.split(".")[0]
            if self._table_exists(tableName):
                self._create_table(tableName)
            cursor.execute("SELECT * FROM " + tableName)
            rows = cursor.fetchall()
        except lite.Error as e:
            raise e
        finally:
            if conn:
                conn.close()
