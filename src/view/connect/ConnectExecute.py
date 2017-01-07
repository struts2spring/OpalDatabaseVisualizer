
import sqlite3 as lite
import os


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
if __name__ == "__main__":
    print('hi')
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
    book_row = [
                {'id':'2',
                 'book_name':'abc0'},
                {'id':'3', 'book_name':'abc1'}
            ]
    sqlExecuter.sqlite_insert_or_update('book', book_row)
    print(sqlExecuter.sqlite_select('book'))

    pass
