'''
Created on Feb 19, 2017

@author: vijay
'''
import sqlite3
import os
import re
from os.path import expanduser
import sys

class SQLExecuter():
    '''
    '''
    def __init__(self, database='_opal.sqlite'):
        home = expanduser("~")
        databasePath = os.path.join(home, database)
        self.conn = sqlite3.connect(databasePath)
        self.createOpalTables()
        
    def sqlite_insert(self, table, rows):
        for row in rows:
            cols = ', '.join('"{}"'.format(col) for col in row.keys())
            vals = ', '.join(':{}'.format(col) for col in row.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            self.conn.cursor().execute(sql, row)
        self.conn.commit()
        
    def sqlite_insert_or_update(self, table, rows):
        try:
            for row in rows:
                cols = ', '.join('"{}"'.format(col) for col in row.keys())
                vals = ', '.join(':{}'.format(col) for col in row.keys())
                sql = 'INSERT OR REPLACE INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
                self.conn.cursor().execute(sql, row)
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e
    
    def sqlite_select(self, table):
        
        returnRows = list()
        with self.conn:    
            
            cur = self.conn.cursor() 
            print('before')
            cur.execute("SELECT * FROM " + table)
        
            rows = cur.fetchall()
            
            for row in rows:
                returnRows.append(row)
        return returnRows
    
    def getColumn(self, tableName=None):
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sql = "SELECT name, sql FROM sqlite_master WHERE type='table' AND name = '" + tableName + "';"
                rows = cur.execute(sql).fetchall()
                tableCreateStmt = rows[0][1]
                match = re.findall(r'[^[]*\[([^]]*)\]', tableCreateStmt)
                columns = set(match)
                if columns:
                    print(columns)
#                 tableCreateStmt.replace(/^[^\(]+\(([^\)]+)\)/g, '$1').split(',')
#                 print(rows)
#                 for idx, item in enumerate(rows):
#                     print(item)
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e
    
    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 print('before')
                rows = cur.execute(text).fetchall()
                print(rows)
                print(cur.description) 
#                 print(rows)
                if cur.description:
                    headerList = list()
                    for idx, desc in enumerate(cur.description):
    #                     print(idx, desc)
                        headerList.append(desc[0])
                    sqlOutput[0] = tuple(headerList)
                    for idx, item in enumerate(rows):
                        sqlOutput[idx + 1] = item
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e
#         print(sqlOutput)
        return sqlOutput
    
    
    def createOpalTables(self):
        '''
        '''
        sqlScript='''
        CREATE TABLE  if not exists conns
          (
            id INTEGER PRIMARY KEY,
            connection_name TEXT,
            path TEXT,
            jdbc_driver TEXT,
            user_name TEXT,
            password TEXT,
            host TEXT,
            port INTEGER,
            sid TEXT,
            service_name TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime'))
          );
        CREATE TABLE if not exists sql_log
          (
            id INTEGER PRIMARY KEY,
            sql TEXT,
            connection_name TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime')),
            executed INTEGER,
            duration INTEGER
          );
        '''
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 print('before')
                rows = cur.executescript(sqlScript).fetchall()
                print(cur.description) 

        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e

    def getObject(self):
    
        con = None
        
        try:
#             self.connection = sqlite3.connect('_opal.sqlite')
            
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            data = cur.fetchone()
            
            print("SQLite version: %s" % data)   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
#             print types
            for t in types:
#                 print t[0], type(t)
                tObjectArrayList = list()
                query = "select tbl_name from sqlite_master where type='%s' order by tbl_name;" % t[0]
                print(query)
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if t[0] == 'table' or t[0] == 'index':
                        tableColumnsOrIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
                        print(tableColumnsOrIndexesSql)
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
#                         print objChildList
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
#                             print objChild
                        tableColumnList.append([tObj[0], tableColumnsOrIndexes])
                    if t[0] == 'view':
                        tableColumnList.append([tObj[0], []])
                        print('view')
                        
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
            print("Error %s:" % e.args[0])
            sys.exit(1)
            
        finally:
            
            if self.conn:
                self.conn.close()
        databaseList.append('database')
        databaseList.append(dbObjects)
        return databaseList
if __name__ == "__main__":
    print('hi')
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
#     tableName = 'albums'
#     sqlExecuter.getColumn(tableName)
#     sql = "SELECT * FROM albums "
#     result = sqlExecuter.executeText(text=sql)
#     print(result)
    sqlExecuter.createOpalTables()
