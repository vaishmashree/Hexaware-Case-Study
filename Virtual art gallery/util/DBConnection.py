import pyodbc
from .PropertyUtil import PropertyUtil

class DBConnection:
    con = None

    @staticmethod
    def getConnection():
        try:
            if DBConnection.con is None or DBConnection.con.closed:  
                DBConnection.con = pyodbc.connect(PropertyUtil.getPropertyString())
        except pyodbc.Error as err:
            raise err  
        return DBConnection.con