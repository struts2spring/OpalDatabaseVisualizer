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
        print("===================================================================================")
        print('databasePath:',databasePath)
        print("===================================================================================")
        self.conn = sqlite3.connect(databasePath)
#         self.createOpalTables()
        
    def sqlite_insert(self, table, rows):
        '''
        @param table: table name 
        @param rows: list of row dictionary of column values
        '''
        for row in rows:
            cols = ', '.join('"{}"'.format(col) for col in row.keys())
            vals = ', '.join(':{}'.format(col) for col in row.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            try:
                with self.conn:    
                    cur = self.conn.cursor() 
                    cur.execute(sql, row)
            except Exception as e:
                print(e)
#         self.conn.commit()
#         pass
        
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
#             print('before')
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
        error = 'success'
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 print('before')
                if text.strip().lower().startswith('update'):
                    cur.execute(text)
                else:
                    rows = cur.execute(text).fetchall()
#                     print(rows)
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
            error = e
            self.conn.rollback()
#             raise e
#         print(sqlOutput)
        return sqlOutput
    
    
    def createOpalTables(self):
        '''
        '''
        err = 'success'
        sqlScript = '''
        drop table if exists dbms;
        drop table if exists conns;
        CREATE TABLE  if not exists conns
          (
            id INTEGER PRIMARY KEY,
            connection_name TEXT UNIQUE,
            db_file_path TEXT,
            dbms_id integer not null,
            user_name TEXT,
            password TEXT,
            host TEXT,
            port INTEGER,
            sid TEXT,
            service_name TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime')),
            foreign key (dbms_id) references dbms(id)
          );
          
        create table if not exists dbms
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dbms_name text UNIQUE,
            vendor text,
            jdbc_driver TEXT,
            driver_path TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime'))
            
        );
        CREATE TABLE if not exists sql_log
          (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            sql TEXT,
            connection_name TEXT,
            created_time [timestamp] DEFAULT (datetime('now', 'localtime')),
            executed INTEGER,
            duration INTEGER
          );
          

          
        insert into dbms (dbms_name, vendor) values (  'SQLite','SQLite');
        insert into dbms (dbms_name, vendor) values (  'Oracle','Oracle');
        insert into dbms (dbms_name, vendor, jdbc_driver,driver_path) values (  'H2','H2','org.h2.Driver','/lib');
        insert into dbms (dbms_name, vendor, jdbc_driver,driver_path) values (  'HSQLDB','HSQLDB','org.hsqldb.jdbc.JDBCDriver','/lib');
        
        insert into conns (connection_name, db_file_path, dbms_id) values (  'database_sqlite_1','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_1.sqlite', 1);
        insert into conns (connection_name, db_file_path, dbms_id) values (  'database_sqlite_2','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_2.sqlite', 1);
        insert into conns (connection_name, db_file_path, dbms_id) values (  'database_sqlite_3','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_3.sqlite', 1);
        insert into conns (connection_name, db_file_path, dbms_id) values (  'database_H2','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_4.sqlite', 3);
        
        '''
        try:
            with self.conn:    
                cur = self.conn.cursor()    
#                 print('before')
                rows = cur.executescript(sqlScript).fetchall()
                print(cur.description) 

        except Exception as e:
            print(e)
            err = e
            self.conn.rollback()
        finally:
            self.conn.commit()
#             raise e
        return err

    def addNewConnectionRow(self, dbFilePath=None, connectionName=None):
        '''
        addNewConnectionRow adding a new row of connection
        '''
        row = dict()
        row['connection_name'] = connectionName
        row['db_file_path'] = dbFilePath
        row['dbms_id'] = 1
        rowList=list()
        rowList.append(row)
        self.sqlite_insert('conns', rowList)
#         "insert into conns (connection_name, db_file_path, dbms_id) values (  'database_sqlite_2','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_2.sqlite', 1);"
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
    
    def getListDatabase(self):
        '''
        This method will return list of database available to connect.
        assumption , conns and sql_log table will available.
        
        '''
#         self.createOpalTables()
        dbList = self.sqlite_select("conns")
        return dbList

    def getContectedObject(self, connectionName, databaseAbsolutePath):
        dbObjects = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath).getObject()
        return dbObjects
    
    def getDbFilePath(self, connectionName=None):
        sqlScript = "select db_file_path from conns where connection_name= '" + connectionName + "'"
        cur = self.conn.cursor()   
        rows = cur.execute(sqlScript).fetchone()
        dbFilePath = None
        if rows:
            dbFilePath = rows[0]
        return dbFilePath
    
class ManageSqliteDatabase():
    def __init__(self, connectionName=None, databaseAbsolutePath=None):
        '''
        @param param: connection_name
        @param param: databaseAbsolutePath
        '''
#         databaseAbsolutePath=os.path.abspath(databaseAbsolutePath)
#         databasePath=os.path.abspath(databaseAbsolutePath)
#         databaseAbsolutePath=os.path.normpath(databaseAbsolutePath)
        pathDir=os.path.dirname(databaseAbsolutePath)
        head, tail=os.path.split(databaseAbsolutePath)
        os.chdir(pathDir)
        self.conn = sqlite3.connect(tail)
        self.connectionName = connectionName
 
    def createTable(self):
        sql='''
        CREATE TABLE  if not exists ABC
          (
            id INTEGER PRIMARY KEY
        );
        '''
        cur = self.conn.cursor() 
        cur.execute(sql)
        
    def getObject(self):
        '''
        Method returns all database object [ table, view, index] from the given sqlite database path
        '''
    
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
                        tableColumnList.append({tObj[0]: tableColumnsOrIndexes})
                    if t[0] == 'view':
                        tableColumnList.append({tObj[0]: []})
                        print('view')

                dbObjects.append({t[0]: tableColumnList})
#             print(dbObjects)

        except sqlite3.Error as e:
            print("Error %s:" % e.args[0])
            sys.exit(1)
            
        finally:
            
            if self.conn:
                self.conn.close()
        databaseList.append(self.connectionName)
        databaseList.append(dbObjects)
        return databaseList        

    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        error = 'success'
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 print('before')
                if text.strip().lower().startswith('update'):
                    cur.execute(text)
                else:
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
            error = e
            self.conn.rollback()
#             raise e
#         print(sqlOutput)
        return sqlOutput
    
    def sqlite_insert(self, table, rows):
        '''
        @param table: table name 
        @param rows: list of row dictionary of column values
        '''
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
#             print('before')
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
    
if __name__ == "__main__":
    print('hi')
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
#     sqlExecuter.getDbFilePath('database_sqlite_1')
    sqlExecuter.addNewConnectionRow(dbFilePath=r"c:\soft\4.sqlite", connectionName='4')
    result=sqlExecuter.executeText("select * from conns")
    print(result)
#     obj=sqlExecuter.getObject()
#     print(obj)
#     tableName = 'albums'
#     sqlExecuter.getColumn(tableName)
#     sql = "SELECT * FROM albums "
#     result = sqlExecuter.executeText(text=sql)
#     print(result)

##########################################################################################
#     dbList = sqlExecuter.getListDatabase()
#     for db in dbList:
#         if db[3] == 1:
#             dbObjects = ManageSqliteDatabase(connectionName=db[1] ,databaseAbsolutePath=db[2]).getObject()
#             print(dbObjects)
##########################################################################################
            
#     print(dbList)
#     ManageSqliteDatabase(connectionName="1", databaseAbsolutePath=r"c:\soft\1.sqlite")
