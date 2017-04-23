'''
Created on Feb 26, 2017

@author: vijay
'''
import json


class ReadWriteTreeJson(object):
    def __init__(self):
        pass
    
    def readTreeJson(self):
        with open('tree.json') as data_file:
            self.treeData = json.loads(data_file.read())
        
        print(json.dumps(self.treeData, indent=4, sort_keys=True))
#         print(self.treeData)
if __name__ == '__main__':
    readWritejson=ReadWriteTreeJson()
    readWritejson.readTreeJson()