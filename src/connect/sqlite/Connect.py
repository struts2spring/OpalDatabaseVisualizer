'''
Created on 13-Dec-2016

@author: vijay
'''


import sqlite3
import sys

class ConnectSqlite():
    def __init__(self):
        self.connection=None
        pass
    
    def getConnection(self):
    
        con = None
        
        try:
            self.connection = sqlite3.connect('_opal.sqlite')
            
            cur = self.connection.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            data = cur.fetchone()
            
            print "SQLite version: %s" % data   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            print cur.fetchall()
#             print cur.fetchallDict()
#             for row in cur.execute("select tbl_name from sqlite_master where type='table';"):
#                 print row                
            
#             data = cur.fetchone()
            
            
        except sqlite3.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
        finally:
            
            if self.connection:
                self.connection.close()
if __name__ == '__main__':
    connectSqlite=ConnectSqlite()
    connectSqlite.getConnection()
    pass