'''
Created on 13-Dec-2016

@author: vijay
'''


import sqlite3
import sys
import logging

logger = logging.getLogger('extensive')

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
            
            logger.debug("SQLite version: %s" , data)   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
            for t in types:
                tObjectArrayList = list()
                query = "select tbl_name from sqlite_master where type='%s' order by tbl_name;" % t[0]
                logger.debug(query)
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if t[0] == 'table' or t[0] == 'index':
                        tableColumnsOrIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
                        logger.debug(tableColumnsOrIndexesSql)
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
                        tableColumnList.append([tObj[0], tableColumnsOrIndexes])
                    if t[0] == 'view':
                        tableColumnList.append([tObj[0], []])
                        logger.debug('view')
                        
#                     if t[0] == 'index':
#                         tablesHavingIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
#                         tablesHavingIndexesList = cur.execute(tablesHavingIndexesSql).fetchall()
#                         print tablesHavingIndexesSql
#                         for tableHavingIndexes in tablesHavingIndexesList:
#                             tableIndexesSql = "PRAGMA " + t[0] + "_list(%s);" % tObj[0]
# #                         print objChildList
#                         tableColumnsOrIndexes = list()
#                         for objChild in tableColumnsOrIndexesList:
#                             tableColumnsOrIndexes.append(objChild)
                        
#                         print tableColumnList
#                 tObjectArrayList.append(tableColumnList)
#                 print tObjectArrayList
                dbObjects.append((t[0], tableColumnList))
            print(dbObjects)
#                 dbObjects.append(tObjectArrayList)
#             print dbObjects
#             print cur.fetchallDict()
#             for row in cur.execute("select tbl_name from sqlite_master where type='table';"):
#                 print row                
            
#             data = cur.fetchone()
            
            
        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
            
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
#             cur.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'.format(tn=table_name, fn=id_field, ft=field_type))
        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
            sys.exit(1)
            
        finally:
            
            if self.connection:
                self.connection.close()
if __name__ == '__main__':
    connectSqlite = ConnectSqlite()
    connectSqlite.getObject()
    pass
