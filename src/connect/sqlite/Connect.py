'''
Created on 13-Dec-2016

@author: vijay
'''


import sqlite3
import sys

class ConnectSqlite():
    def __init__(self):
        self.connection=sqlite3.connect('_opal.sqlite')
        pass
    
    
    def getObject(self):
    
        con = None
        
        try:
#             self.connection = sqlite3.connect('_opal.sqlite')
            
            cur = self.connection.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            data = cur.fetchone()
            
            print "SQLite version: %s" % data   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types=cur.execute("select distinct type from sqlite_master;").fetchall()
            dbObjects=list()
            print types
            for t in types:
                print t[0], type(t)
                tObjectArrayList=list()
                query="select tbl_name from sqlite_master where type='"+t[0]+"' order by tbl_name;"
                print query
                tObjectList=cur.execute(query).fetchall()
                for tObj in tObjectList:
                    tObjectArrayList.append(tObj[0])
                dbObjects.append((t[0],tObjectArrayList))
#                 dbObjects.append(tObjectArrayList)
            print dbObjects
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
        return dbObjects
    
    def createTable(self):
        try:
            self.connection = sqlite3.connect('_opal.sqlite')
            cur = self.connection.cursor() 
            cur.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'.format(tn=table_name, fn=id_field, ft=field_type))
        except sqlite3.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
        finally:
            
            if self.connection:
                self.connection.close()
if __name__ == '__main__':
    connectSqlite=ConnectSqlite()
    connectSqlite.getObject()
    pass