'''
Created on Feb 18, 2017

@author: vijay
'''
import os
import sys
import subprocess


print(sys.platform)
class SqliteConnect():
    def __init__(self):
        
        pass
    

    def getSqlitePath(self):
        print(sys.version)
        print( sys.version_info)
#         path=os.path.join("src",'sqlite',sys.platform,'3170000','sqlite3.exe')
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
        print(path)
        sqliteDatabaseFilePath=os.path.join(path,'view','_opal.sqlite')
        sqlitePath=os.path.join(path,'sqlite',sys.platform,'3170000')
        sqlitePath=os.path.abspath(sqlitePath)
        os.chdir(sqlitePath)
        print(os.getcwd())
        print(os.listdir(os.getcwd()))
        return sqlitePath, sqliteDatabaseFilePath
    
    def executeProcess(self):
        sqlitePath,sqliteDatabaseFilePath=self.getSqlitePath()
#         cmd=["echo", "hello world"]
#         sqliteDatabaseFilePath="C:\Documents and Settings\vijay\git\OpalDatabaseVisualizer\src\view\_opal.sqlite"
        query="select * from book"
        cmd=['sqlite3.exe', sqliteDatabaseFilePath, query]
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE,  stderr=None)
        try:
            outs, errs = proc.communicate()
            print(outs, errs)

        except Exception as e:
            proc.kill()
            outs, errs = proc.communicate()

if __name__ == '__main__':
    sqliteConnect=SqliteConnect()
    sqliteConnect.getSqlitePath()
    sqliteConnect.executeProcess()
    pass