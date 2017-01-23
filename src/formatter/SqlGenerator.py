'''
Created on 21-Jan-2017

@author: vijay
'''
import sqlparse


class JsonToSql():
    '''
    {
    'temp':[True, False],
    'schemaName': 'Schema_1',
    'tableName':'Table_1',
    'ifNotExists':[True,False],
    'columns':[{
                'columnName':'Column_1',
                'dataType':['INTEGER', 'TEXT', 'NUMERIC', 'INTEGER', 'REAL', 'NONE'],
                'isNotNull': [True, False],
                'isUnique': [True, False],
                'isPrimaryKey':[True, False]
                'isAutoIncrement':[True, False],
                'default':'some value'
                }]
    }
    '''
    def __init__(self):
        self.tableDict = {
                      'temp':True,
                      'schemaName': 'Schema_1',
                      'tableName':'Table_1',
                      'ifNotExists':True,
                      'columns':[{
                                  'columnName':'Column_1',
                                  'dataType':'INTEGER',
                                  'isNotNull': True,
                                  'isUnique': True,
                                  'isPrimaryKey':True,
                                  'isAutoIncrement':True,
                                  'check':'some expression',
                                  'default':'some value',
                                  },
                                 {
                                  'columnName':'Column_2',
                                  'dataType':'TEXT',
                                  'isNotNull': True,
                                  'isUnique': True,
                                  'isPrimaryKey':False,
                                  'isAutoIncrement':False,
                                  'default':'some value',
                                  
                                  }
                                 
                                 ]
                      }
        self.tableConstraint = {
                           'constraintName':'Constraint_1',
                           'constraintType':['PRIMARY KEY', 'UNIQUE', 'CHECK', 'FOREIGN KEY'],
                           
                           }
    
    
#     def createTable(self):
        
        
        
        
#     def createConstraint(self):
        
#     def conflictclause(self):
#         pass
    
    
    
    def createSql(self):
        
        sqlList = list()
        sqlList.append("CREATE")
        if self.tableDict['temp']:
            sqlList.append("TEMP")
        sqlList.append('TABLE')
        if self.tableDict['ifNotExists']:
            sqlList.append('IF NOT EXISTS')
        if 'schemaName' in self.tableDict.keys():
            sqlList.append(self.tableDict['schemaName'] + '.' + self.tableDict['tableName'])
        else:
            sqlList.append(self.tableDict['tableName'])
        sqlList.append('(')
        for column in self.tableDict['columns']:
            sqlList.append(column['columnName'])
            sqlList.append(column['dataType'])
            if column['isPrimaryKey']:
                sqlList.append('PRIMARY KEY')
                if column['isAutoIncrement']:
                    sqlList.append('AUTOINCREMENT')
            elif column['isNotNull']:
                sqlList.append('NOT NULL')
            elif column['isUnique']:
                sqlList.append('UNIQUE')
            elif column['isUnique']:
                sqlList.append('UNIQUE')
            elif 'check' in column.keys():
                sqlList.append('CHECK ( '+column['check']+' )')
            elif 'default' in column.keys():
                sqlList.append('DEFAULT '+column['default'])
            
            sqlList.append(',')
        sqlList.pop()
        sqlList.append(')')  
        sql=" ".join(sqlList)
        formatedSql=sqlparse.format(sql, encoding=None)
        return formatedSql

if __name__ == '__main__':
    jsonToSql = JsonToSql()
    formatedSql=jsonToSql.createSql()
    print(formatedSql)
    pass
