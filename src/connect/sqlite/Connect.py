'''
Created on 13-Dec-2016

@author: vijay
'''


import sqlite3
import sys

class ConnectSqlite():
    def __init__(self):
        self.connection = sqlite3.connect('_opal.sqlite')
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
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
#             print types
            for t in types:
#                 print t[0], type(t)
                tObjectArrayList = list()
                query = "select tbl_name from sqlite_master where type='%s' order by tbl_name;" % t[0]
                print query
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if t[0] != 'view':
                        tableColumnsOrIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
                        print tableColumnsOrIndexesSql
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
#                         print objChildList
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
#                             print objChild
                        tableColumnList.append([tObj[0], tableColumnsOrIndexes])
                    if t[0] == 'view':
                        tableColumnList.append([tObj[0], []])
                        print 'view'
                        
#                         print tableColumnList
#                 tObjectArrayList.append(tableColumnList)
#                 print tObjectArrayList
                dbObjects.append((t[0], tableColumnList))
            print dbObjects
#                 dbObjects.append(tObjectArrayList)
#             print dbObjects
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
        databaseList.append('database')
        databaseList.append(dbObjects)
        return databaseList
    
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
    connectSqlite = ConnectSqlite()
    connectSqlite.getObject()
    pass
