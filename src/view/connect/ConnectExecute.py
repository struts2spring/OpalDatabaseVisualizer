
import sqlite3 as lite
import os
import subprocess
import shlex

class SqlExecuterProcess():
    '''
    '''
    def __init__(self):
#         subprocess.call(cmd, shell=True)
        pass
    
    def executeCmd(self, command):
#         subprocess.call(cmd, shell=True)
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc

class SQLExecuter():
    '''
    '''
    def __init__(self, database=None):
        print(os.getcwd())
        self.conn = lite.connect('_opal.sqlite')
        
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
            print('before'   )
            cur.execute("SELECT * FROM " + table)
        
            rows = cur.fetchall()
            
            for row in rows:
                returnRows.append(row)
        return returnRows
    
    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        sqlOutput=dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                print('before'   )
                rows=cur.execute(text).fetchall()
                print(cur.description) 
#                 print(rows)
                for idx,item in enumerate(rows):
                    sqlOutput[idx]=item
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e
#         print(sqlOutput)
        return sqlOutput
    
    
if __name__ == "__main__":
    print('hi')
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuterProcess=SqlExecuterProcess()
    command="""sqlite3 _opal.sqlite &
    select * from book;
    """
    result=sqlExecuterProcess.executeCmd(command)
    print(result)
    
#     book_row = [
#                 {'id':'2',
#                  'book_name':'abc0'},
#                 {'id':'3', 'book_name':'abc1'}
#             ]
#     sqlExecuter.sqlite_insert_or_update('book', book_row)
#     print(sqlExecuter.sqlite_select('book'))
#     text="select * from book;"
#     sqlExecuter.executeText(text)

    pass
