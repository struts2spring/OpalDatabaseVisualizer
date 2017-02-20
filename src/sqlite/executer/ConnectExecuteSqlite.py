'''
Created on Feb 19, 2017

@author: vijay
'''
import sqlite3
import os
import re

class SQLExecuter():
    '''
    '''
    def __init__(self, database=None):
        print(os.getcwd())
        self.conn = sqlite3.connect('C:\sampleDatabase\chinook.db')
        
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
                sql="SELECT name, sql FROM sqlite_master WHERE type='table' AND name = '"+tableName+"';"
                rows = cur.execute(sql).fetchall()
                tableCreateStmt=rows[0][1]
                match=re.findall(r'[^[]*\[([^]]*)\]',tableCreateStmt)
                columns=set(match)
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
                print('before')
                rows = cur.execute(text).fetchall()
                print(rows)
                print(cur.description) 
#                 print(rows)
                headerList=list()
                for idx,desc in enumerate(cur.description):
                    print(idx, desc)
                    headerList.append(desc[0])
                sqlOutput[0]=tuple(headerList)
                for idx, item in enumerate(rows):
                    sqlOutput[idx+1] = item
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e
#         print(sqlOutput)
        return sqlOutput
    
    
if __name__ == "__main__":
    print('hi')
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuter = SQLExecuter()
    tableName='albums'
    sqlExecuter.getColumn(tableName)
    sql="SELECT * FROM albums "
    result = sqlExecuter.executeText(text=sql)
    print(result)