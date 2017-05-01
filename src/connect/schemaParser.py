'''
Created on 25-Dec-2016

@author: vijay
'''
import json
import logging

logger = logging.getLogger('extensive')
class Table():
    def __init__(self, name):
        self._name = name
        self._columns = []
        
    def addColumn(self, column):
        self._columns.append(column)
        
    def __repr__(self):
        return 'Table({!r})'.format(self._name)
    
    def __iter__(self):
        return iter(self._columns)
    
#     def depth_first(self):
#         yield self
#         for c in self:
#             yield c.depth_first()
            
class Column():
    def __init__(self, name, dataType, notNull, pk, unique, autoIncrement):
        self._name = name
        self._dataType = dataType
        self._notNull = notNull
        self._pk = pk
        self._unique = unique
        self._autoIncrement = autoIncrement
    
    def __repr__(self):
        return 'Column{!r})'.format(self._name)
    def __str__(self):
        return '({!s},{!s})'.format(self._name, self._dataType)
if __name__ == '__main__':
    
    table=Table('Employee')
    col1=Column('col1','dataType', 'notNull', 'pk', 'unique', 'autoIncrement' )
    table.addColumn(col1 )
#     table.addColumn('col2')
#     table.addColumn('col3')
    print(table)
    print(col1)
#     print table.depth_first()
#     print json.dump(table)
    pass
