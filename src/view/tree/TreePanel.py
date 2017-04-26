#!/usr/bin/python
'''
Created on 13-Dec-2016

@author: vijay
'''
import wx
import os
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.Constant import ID_newWorksheet, keyMap, ID_CONNECT_DB,\
    ID_DISCONNECT_DB, ID_ROOT_NEW_CONNECTION, ID_ROOT_REFERESH
from src.view.table.CreateTable import CreatingTableFrame
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter,\
    ManageSqliteDatabase

class CreatingTreePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        sqlExecuter = SQLExecuter()
        self._treeList = sqlExecuter.getObject()
        self.treeMap = {}
        self.searchItems = {}
        self.tree = databaseNavigationTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter table name")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.RecreateTree()
        
#         self.tree.SetExpansionState(self.expansionState)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnTreeRightUp)
        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        try:
            for category, items in self._treeList[1]:
                self.searchItems[category] = []
                for childItem in items:
    #                 if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)
        except Exception as e:
            print(e)
        wx.EndBusyCursor()
        self.RecreateTree()   
    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
#         searchMenu = self.filter.GetMenu().GetMenuItems()
#         fullSearch = searchMenu[1].IsChecked()
        fullSearch = False
            
        if evt:
            if fullSearch:
                # Do not`scan all the demo files for every char
                # the user input, use wx.EVT_TEXT_ENTER instead
                return

　
                    
        self.createDefaultNode()
                    
        self.tree.Expand(self.root)

        
        self.tree.Thaw()
        self.searchItems = {}

    
    #---------------------------------------------
    def createDefaultNode(self):
        print("TreePanel.createDefaultNode")
        sqlExecuter = SQLExecuter()
        dbList = sqlExecuter.getListDatabase()
        
        
        fullSearch = False
        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Connections")
        self.tree.SetItemImage(self.root, 0)
        data=dict()
        data['depth']=0
        self.tree.SetItemPyData(self.root, data)
        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The native treectrl on MSW has a bug where it doesn't draw
        # all of the text for an item if the font is larger than the
        # default.  It seems to be clipping the item's label as if it
        # was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo:
            treeFont.SetPointSize(treeFont.GetPointSize() + 2)
            
        treeFont.SetWeight(wx.BOLD)
        catFont.SetWeight(wx.BOLD)
        self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        for db in dbList:
            data=dict()
            data['depth']=1
            data['connection_name']=db[1]
            data['db_file_path']=db[2]
            if db[3]==3:
                image=17
            elif db[3]==1:
                image=16
#             elif db[3]==1:
#                 image=16
            
            # Appending connections
            self.addNode(targetNode=self.root, nodeLabel=db[1],pydata=data, image=image)

　
　
        if firstChild:
            self.tree.Expand(firstChild)
        if filter:
            self.tree.ExpandAll()
        elif expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False      
            
    def addNode(self, targetNode=None, nodeLabel='label', pydata=None, image=16):  
        nodeCreated = self.tree.AppendItem(targetNode, nodeLabel, image=image)
        self.tree.SetItemFont(nodeCreated, self.tree.GetFont())
        self.tree.SetItemPyData(nodeCreated, pydata)
        return nodeCreated     
    #---------------------------------------------
 
    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
#         print("OnItemExpanded: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
#         print("OnItemCollapsed: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item == self.tree.GetSelection():
            print(self.tree.GetItemText(item) + " Overview")
        event.Skip()
    #---------------------------------------------
    def OnSelChanged(self, event):
        print('OnSelChanged')
    #---------------------------------------------
    def OnTreeRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)

        if item:
            self.tree.item = item
            self.tree.item
            print("OnRightClick: %s, %s, %s" % (self.tree.GetItemText(item), type(item), item.__class__) + "\n")
            self.tree.SelectItem(item)
            if self.tree.GetItemText(self.tree.item) != 'Connections':
                print('parent', self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)))

    #---------------------------------------------
    def OnTreeRightUp(self, event):
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         print('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            e.print_stack_trace()
        print('------------------------------------------------------------------------->', path)
        path = os.path.abspath(os.path.join(path, "images"))
        
        item = self.tree.item     
        
        if not item:
            event.Skip()
            return
        print('OnTreeRightUp')

        
        menu = wx.Menu()
        data=self.tree.GetPyData(item)
        rightClickDepth=data['depth']
        if rightClickDepth == 0:
            rootNewConnection = menu.Append(ID_ROOT_NEW_CONNECTION, "New connection ")
            
            refreshBmp = wx.MenuItem(menu, ID_ROOT_REFERESH, "&Refresh")
            refreshBmp.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "database_refresh.png"))))
            rootRefresh = menu.AppendItem(refreshBmp)
            
            self.Bind(wx.EVT_MENU, self.onRootRefresh, rootRefresh)
            self.Bind(wx.EVT_MENU, self.onRootNewConnection, rootNewConnection)
        elif rightClickDepth == 1:
            item1 = menu.Append(ID_DISCONNECT_DB, "Disconnect")
            item2 = menu.Append(ID_CONNECT_DB, "Connect")
            
            sqlEditorBmp = wx.MenuItem(menu, ID_newWorksheet, "SQL Editor in new Tab")
            sqlEditorBmp.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "script.png"))))
            item3 = menu.AppendItem(sqlEditorBmp)
            
            item4 = menu.Append(wx.ID_ANY, "Properties")
            
            refreshBmp = wx.MenuItem(menu, wx.ID_REFRESH, "&Refresh")
            refreshBmp.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "database_refresh.png"))))
            item5 = menu.AppendItem(refreshBmp)
            
            
            item6 = menu.Append(wx.ID_ANY, "Edit Connection")
            menu.AppendSeparator()
            item7 = wx.MenuItem(menu, wx.ID_ANY, "&Smile!\tCtrl+S", "This one has an icon")
            item7.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "index.png"))))
            menu.AppendItem(item7)
            
#             self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
            self.Bind(wx.EVT_MENU, self.onDisconnectDb, item1)
            self.Bind(wx.EVT_MENU, self.onConnectDb, item2)
            self.Bind(wx.EVT_MENU, self.onOpenSqlEditorTab, item3)
            self.Bind(wx.EVT_MENU, self.onProperties, item4)
            self.Bind(wx.EVT_MENU, self.onRefresh, item5)
            self.Bind(wx.EVT_MENU, self.onEditConnection, item6)

            

        elif rightClickDepth == 2:
            if 'table' in self.tree.GetItemText(item):
                newTableItem = menu.Append(wx.ID_ANY, "Create new table")
                item2 = menu.Append(wx.ID_ANY, "Refresh  \tF5")
                self.Bind(wx.EVT_MENU, self.onNewTable, newTableItem)
            if 'view' in self.tree.GetItemText(item):
                newTableItem = menu.Append(wx.ID_ANY, "Create new view")
                item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, self.onNewTable, newTableItem)
            if 'index' in self.tree.GetItemText(item) :
                newTableItem = menu.Append(wx.ID_ANY, "Create new index")
                item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, self.onNewTable, newTableItem)
                
        elif 'Columns' in self.tree.GetItemText(item) :
            item1 = menu.Append(wx.ID_ANY, "Create new column")
            
        elif 'table' in self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)) : 
            print(self.tree.GetItemText(item))
            item1 = menu.Append(wx.ID_ANY, "Edit table")
            self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        elif 'Column' in self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)) : 
            print(self.tree.GetItemText(item))
            item1 = menu.Append(wx.ID_ANY, "Edit column")
            item1 = menu.Append(wx.ID_ANY, "Create new column")
            self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        
        
        
        self.PopupMenu(menu)
        menu.Destroy() 
    
    def onRootRefresh(self, event):
        print('onRootRefresh')
    def onRootNewConnection(self, event):
        print('onRootNewConnection')
    def OnItemBackground(self, event):
        print('OnItemBackground')
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        self.tree.EditLabel(item)
    def onConnectDb(self, event):
        print('onConnectDb')
#         item = self.tree.GetSelection() 
        selectedItemId=self.tree.GetSelection()
        self.getNodeOnOpenConnection(selectedItemId)
#         self.addNode(targetNode=, nodeLabel='got conncted',pydata=data, image=16)
        # Todo change icon to enable
        selectedItemText=self.tree.GetItemText(self.tree.GetSelection())
        self.setAutoCompleteText(selectedItemText)
        self.openWorksheet()
    
    def setAutoCompleteText(self, selectedItemText):
        '''
        This is to set autocomplete text as we connect to database
        '''
        print(selectedItemText)
        tb1=self.GetTopLevelParent()._mgr.GetPane("tb1").window
        choice=self.GetTopLevelParent()._ctrl.GetChoices()
        textCtrl=self.GetTopLevelParent()._ctrl
        textCtrl.SetValue(selectedItemText)
#         textCtrl.SetSelection(choice.index(selectedItemText))
        textCtrl.SetInsertionPointEnd()
        textCtrl.SetSelection( -1, -1 )
        textCtrl._showDropDown( False )
    
    def onDisconnectDb(self, event):
        print('onDisconnectDb')
        selectedItem = self.tree.GetSelection()
        if selectedItem:
            self.tree.DeleteChildren(selectedItem)
            # Todo change icon to dissable
    def onOpenSqlEditorTab(self, event):
        print('onOpenSqlEditorTab')
        self.openWorksheet()
    def openWorksheet(self):
        sqlExecutionTab=self.GetTopLevelParent()._mgr.GetPane("sqlExecution")
        sqlExecutionTab.window.addTab("Worksheet")

    def onProperties(self, event):
        print('onProperties')
    def onRefresh(self, event):
        print('onRefresh')
    def onEditConnection(self, event):
        print('onEditConnection')

    def onNewTable(self, event):
        print('onNewTable')
        tableFrame = CreatingTableFrame(None, 'Table creation')
        
        
    def getNodeOnOpenConnection(self, selectedItemId):
        '''
        This method will return database node on open connection
        '''
        print('getNodeOnOpenConnection')
        data=self.tree.GetPyData(selectedItemId)
        connectionName=data['connection_name']
        databaseAbsolutePath=data['db_file_path']
        dbObjects = ManageSqliteDatabase(connectionName=connectionName ,databaseAbsolutePath=databaseAbsolutePath).getObject()

        for dbObject in dbObjects[1]:
            for k0,v0 in dbObject.iteritems():
                print(k0,v0)
                data=dict()
                data['depth']=2
                image=2
                nodeLabel= k0 + ' (' + str(len(v0)) + ')'
                child0= self.addNode(targetNode=selectedItemId, nodeLabel=nodeLabel, pydata=data, image=image) 
                if 'table' == k0 :
                    # setting image for 'table'
                    image = 4
                elif 'index'== k0 :
                    # setting image for 'index'
                    image = 5
                elif 'view'== k0 :
                    # setting image for 'view'
                    image = 6
#                 child = self.tree.AppendItem(selectedItemId, k0 + ' (' + str(len(items)) + ')', image=count)
                for v00 in v0:
                    for k1, v1 in v00.iteritems():
                        # Listing tables
                        data=dict()
                        data['depth']=3
                        nodeLabel= k1 + ' (' + str(len(v1)) + ')'
                        if k0=='table':
                            image = 4
                        child1= self.addNode(targetNode=child0, nodeLabel=nodeLabel, pydata=data, image=image) 
                        
                        print(k1,v1)
                        if k0 == 'table':
                            data = dict()
                            data['depth']=4
                            # setting  image for 'Columns', 'Unique Keys', 'Foreign Keys', 'References'
                            image=11
                            
                            child1_1= self.addNode(targetNode=child1, nodeLabel='Columns', pydata=data, image=image) 
                            child1_2= self.addNode(targetNode=child1, nodeLabel='Unique Keys', pydata=data, image=image) 
                            child1_3= self.addNode(targetNode=child1, nodeLabel='Foreign Keys', pydata=data, image=image) 
                            child1_4= self.addNode(targetNode=child1, nodeLabel='References', pydata=data, image=image) 
                        for v2 in v1:
                            if k0=='table':
                                data=dict()
                                data['depth']=4
#                                  (cid integer, name text, type text, nn bit, dflt_value, pk bit)
                                nodeLabel= v2[1]
                                
                                if v2[5]==1:
                                    # setting primary key image
                                    image=9
                                elif v2[5]==0 and v2[2]== 'INTEGER':
                                    # setting INTEGER image
                                    image=7
                                elif v2[5]==0 and v2[2]== 'VARCHAR':
                                    # setting VARCHAR image
                                    image=18
                                child2= self.addNode(targetNode=child1_1, nodeLabel=nodeLabel, pydata=data, image=image) 
                                print(v2)
        
class databaseNavigationTree(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in database page
    '''
    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.BuildTreeImageList()
#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)
        self.eventdict = {
#                           'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
#                           'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
#                           'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
#                           'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
#                           'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
#                           'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
#                           'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
#                           'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey,
#                           'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
#                           'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink
                          }
        self.SetInitialSize((100, 80))
        
            
    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item
    #---------------------------------------------

    def OnKey(self, event):
        print('onkey')
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()            
    def BuildTreeImageList(self):
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         print('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            e.print_stack_trace()
        print('------------------------------------------------------------------------->', path)
        path = os.path.abspath(os.path.join(path, "images"))
        imgList = wx.ImageList(16, 16)

        # add the image for modified demos.

        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "database.png"))))# 0
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "database_category.png"))))# 1
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "folder_view.png"))))# 2
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "folder.png"))))# 3
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "table.png"))))# 4
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "view.png"))))# 5
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "index.png"))))# 6
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "column.png"))))# 7 using to show integer column
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "string.png"))))  # 8
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "key.png"))))  # 9
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "foreign_key_column.png"))))  # 10
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "columns.png"))))  # 11
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "unique_constraint.png"))))  # 12
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "reference.png"))))  # 13
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "datetime.png"))))  # 14
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "columns.png"))))  # 15
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "sqlite.png"))))  # 16
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "h2.png"))))  # 17
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "textfield.png"))))  # 18
#         imgList.Add(wx.Bitmap(path2))
#         for png in _demoPngs:
#             imgList.Add(catalog[png].GetBitmap())
            

        self.AssignImageList(imgList)

    def GetItemIdentity(self, item):
        return self.GetPyData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(databaseNavigationTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(databaseNavigationTree, self).Thaw()
#---------------------------------------------------------------------------

class MainPanel(wx.Panel):
    """
    Just a simple derived panel where we override Freeze and Thaw so they are
    only used on wxMSW.    
    """
    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()
#---------------------------------------------------------------------------
if __name__ == '__main__':
#     treeImageLevel = dict()
#     treeImageLevel[(0, 0)] = (0, 'database.png')
#     treeImageLevel[(1, 0)] = (0, 'database_category.png')
#     treeImageLevel[(1, 1)] = (0, 'folder_view.png')
#     treeImageLevel[(1, 2)] = (0, 'folder.png')
#     
#     print(treeImageLevel[(0, 0)])
    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingTreePanel(frame, preferenceName='asfd')
    except:
        pass
    frame.Show()
    app.MainLoop()
