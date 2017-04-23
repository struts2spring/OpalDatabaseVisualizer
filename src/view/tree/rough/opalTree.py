import wx
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
from wx import TreeCtrl


class TreeData():
    '''
    class to get tree data from database
    '''
    def __init__(self):
        self.treeData=None
        
    def getTreeData(self):
        self.treeData = SQLExecuter().getObject()
        return self.treeData 

class OpalTreeCtrl(TreeCtrl):
    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.SetInitialSize((100, 80))
        
        
        
class CreatingTreePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.createTree()
        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
    
    def createTree(self):
        '''
        Method is responsible for creating tree.
        '''
        TreeData().getTreeData()

if __name__=='__main__':
    print('main')
    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingTreePanel(frame, preferenceName='Opal Tree')
    except:
        pass    
    frame.Show()
    app.MainLoop()