#!/usr/bin/python
'''
Created on 13-Dec-2016

@author: vijay
'''
import wx
import os
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.images import catalog, images
# from src.connect.sqlite.Connect import ConnectSqlite
from src.view.Constant import ID_newWorksheet, keyMap, ID_CONNECT_DB,\
    ID_DISCONNECT_DB
from src.view.table.CreateTable import CreatingTableFrame
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter,\
    ManageSqliteDatabase
import json
import pprint


_demoPngs = ["database", "table", "view", "indexs", "moredialog", "core",
     "book", "customcontrol", "morecontrols", "layout", "process",
     "clipboard", "images", "miscellaneous"]

_treeList = [(u'table', [[u'author', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'author_name', u'VARCHAR', 1, None, 0), (2, u'about_author', u'VARCHAR', 0, None, 0), (3, u'email', u'VARCHAR', 0, None, 0), (4, u'created_on', u'DATETIME', 0, None, 0)]], [u'author_book_link', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_id', u'INTEGER', 0, None, 0), (2, u'author_id', u'INTEGER', 0, None, 0), (3, u'created_on', u'DATETIME', 0, None, 0)]], [u'book', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_name', u'VARCHAR', 1, None, 0), (2, u'sub_title', u'VARCHAR', 0, None, 0), (3, u'isbn_10', u'VARCHAR', 0, None, 0), (4, u'isbn_13', u'VARCHAR', 0, None, 0), (5, u'series', u'VARCHAR', 0, None, 0), (6, u'dimension', u'VARCHAR', 0, None, 0), (7, u'customer_review', u'VARCHAR', 0, None, 0), (8, u'book_description', u'VARCHAR', 0, None, 0), (9, u'edition_no', u'VARCHAR', 0, None, 0), (10, u'publisher', u'TEXT', 0, None, 0), (11, u'book_format', u'VARCHAR', 0, None, 0), (12, u'in_language', u'VARCHAR', 0, None, 0), (13, u'published_on', u'DATETIME', 0, None, 0), (14, u'has_cover', u'VARCHAR', 0, None, 0), (15, u'has_code', u'VARCHAR', 0, None, 0), (16, u'book_path', u'VARCHAR', 0, None, 0), (17, u'rating', u'VARCHAR', 0, None, 0), (18, u'uuid', u'VARCHAR', 0, None, 0), (19, u'tag', u'VARCHAR', 0, None, 0), (20, u'book_file_name', u'VARCHAR', 0, None, 0), (21, u'book_img_name', u'VARCHAR', 0, None, 0), (22, u'wish_listed', u'VARCHAR', 0, None, 0), (23, u'itEbookUrlNumber', u'VARCHAR', 0, None, 0), (24, u'created_on', u'DATETIME', 0, None, 0)]], [u'book_format', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'file_name', u'VARCHAR', 0, None, 0), (2, u'file_type', u'VARCHAR', 1, None, 0), (3, u'file_size', u'VARCHAR', 0, None, 0), (4, u'created_on', u'DATETIME', 0, None, 0)]], [u'book_format_link', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_format_id', u'INTEGER', 0, None, 0), (2, u'book_id', u'INTEGER', 0, None, 0), (3, u'created_on', u'DATETIME', 0, None, 0)]]]), (u'index', [[u'author', []], [u'book', []]]), (u'view', [[u'book_author', []]])]


class CreatingTreePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        sqlExecuter = SQLExecuter()
        self._treeList = sqlExecuter.getObject()
#         pprint(self._treeList)
#         self._treeList=_treeList
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
        self.tree.SetItemPyData(self.root, 0)
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
#         if not self.tree.IsItemEnabled(item):
#             event.Skip()
#             return

#         # Item Text Appearance
#         ishtml = self.tree.IsItemHyperText(item)
#         back = self.tree.GetItemBackgroundColour(item)
#         fore = self.tree.GetItemTextColour(item)
#         isbold = self.tree.IsBold(item)
#         font = self.tree.GetItemFont(item)          

#         self.popupID1 = wx.NewId()
#         self.popupID2 = wx.NewId()
#         self.popupID3 = wx.NewId()
#         self.popupID4 = wx.NewId()
#         self.popupID5 = wx.NewId()
#         self.popupID6 = wx.NewId()
#         self.popupID7 = wx.NewId()
#         self.popupID8 = wx.NewId()
#         self.popupID9 = wx.NewId()
# 
#         self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
#         self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
#         self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
#         self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
#         self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
#         self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
#         self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
#         self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
#         self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)
        
        menu = wx.Menu()
        data=self.tree.GetPyData(item)
        rightClickDepth=data['depth']
        if rightClickDepth == 0:
            item1 = menu.Append(wx.ID_ANY, "Refresh \tF5")
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
#         pprint(dbObjects)
#         for category, items in dbObjects:
#             print(category)
        for dbObject in dbObjects[1]:
            for k0,v0 in dbObject.iteritems():
                print(k0,v0)
                data=dict()
                data['depth']=2
                image=2
                nodeLabel= k0 + ' (' + str(len(v0)) + ')'
                child0= self.addNode(targetNode=selectedItemId, nodeLabel=nodeLabel, pydata=data, image=image) 
                if 'table' == k0 :
                    image = 4
                elif 'index'== k0 :
                    image = 5
                elif 'view'== k0 :
                    image = 6
#                 child = self.tree.AppendItem(selectedItemId, k0 + ' (' + str(len(items)) + ')', image=count)
                for v00 in v0:
                    for k1, v1 in v00.iteritems():
                        # Listing tables
                        data=dict()
                        data['depth']=3
                        nodeLabel= k1 + ' (' + str(len(v1)) + ')'
                        child1= self.addNode(targetNode=child0, nodeLabel=nodeLabel, pydata=data, image=image) 
                        
                        print(k1,v1)
                        if k0=='table':
                            data = dict()
                            data['depth']=4
                            child1_1= self.addNode(targetNode=child1, nodeLabel='Columns', pydata=data, image=11) 
                            child1_2= self.addNode(targetNode=child1, nodeLabel='Unique Keys', pydata=data, image=11) 
                            child1_3= self.addNode(targetNode=child1, nodeLabel='Foreign Keys', pydata=data, image=11) 
                            child1_4= self.addNode(targetNode=child1, nodeLabel='References', pydata=data, image=11) 
                        for v2 in v1:
                            if k0=='table':
                                data=dict()
                                data['depth']=4
                                nodeLabel= v2[1]
                                child2= self.addNode(targetNode=child1_1, nodeLabel=nodeLabel, pydata=data, image=0) 
                                print(v2)
#             child = self.tree.AppendItem(selectedItemId, dbObjects + ' (' + str(len(items)) + ')', image=count)
#         self.tree.SetItemFont(child, catFont)
#         self.tree.SetItemPyData(child, count)
#         if not firstChild: firstChild = child
#         for childItem in items:
#             imageCount = count
# #                     if DoesModifiedExist(childItem):
# #                         image = len(_demoPngs)
# #                     print "3: ", category, childItem, count
#             if 'table' in category :
#                 imageCount = 4
#             elif 'index' in category :
#                 imageCount = 5
#             elif 'view' in category :
#                 imageCount = 6
#             try:
#                 if type(childItem) == list:
#                     tableNameNode = self.tree.AppendItem(child, childItem[0], image=imageCount)
#                     self.tree.SetItemPyData(tableNameNode, count)
#                     
#                     if 'table' in category :
#                         imageCount = 11
#                         columnsNode = self.tree.AppendItem(tableNameNode, 'Columns', image=imageCount)
#                         self.tree.SetItemPyData(columnsNode, count)
#                         imageCount = 11
#                         uniqueKeysNode = self.tree.AppendItem(tableNameNode, 'Unique Keys', image=imageCount)
#                         self.tree.SetItemPyData(uniqueKeysNode, count)
#                         imageCount = 11
#                         foreignKeyNode = self.tree.AppendItem(tableNameNode, 'Foreign Keys', image=imageCount)
#                         self.tree.SetItemPyData(foreignKeyNode, count)
#                         imageCount = 11
#                         referencesNode = self.tree.AppendItem(tableNameNode, 'References', image=imageCount)
#                         self.tree.SetItemPyData(referencesNode, count)
#                         
#                     secondLevelItems = childItem[1]
#                     for secondLevelChild in secondLevelItems:  
#                         if 'table' in category :
# #                                     print 'secondLevelChild:', secondLevelChild
#                             if secondLevelChild[5] == 1:
#                                 imageCount = 9
#                             if secondLevelChild[2] == 'VARCHAR':
#                                 imageCount = 8
#                             if secondLevelChild[2] == 'VARCHAR':
#                                 imageCount = 8
#                             if secondLevelChild[2] == 'INTEGER' and secondLevelChild[5] == 0:
#                                 imageCount = 8
#                             if secondLevelChild[2] == 'DATETIME':
#                                 imageCount = 14
#                         secondLevelChildItem = self.tree.AppendItem(columnsNode, secondLevelChild[1], image=imageCount)
#                         self.tree.SetItemPyData(secondLevelChildItem, count)
#                     self.treeMap[childItem[0]] = tableNameNode
#                     
#                     if current and (childItem, category) == current:
#                         selectItem = columnsNode
#             except Exception as e:
#                 print(e)   
#         self.addNode()
#         child = self.tree.AppendItem(databaseLeaf, category + ' (' + str(len(items)) + ')', image=count)
#         self.tree.SetItemFont(child, catFont)
#         self.tree.SetItemPyData(child, count)
        
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
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "column.png"))))# 7
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