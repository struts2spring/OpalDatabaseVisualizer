'''
Created on 13-Dec-2016

@author: vijay
'''
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
import wx
from src.view.images import catalog, images
import os
from src.connect.sqlite.Connect import ConnectSqlite
from src.view.Constant import ID_newWorksheet, keyMap
from src.view.table.CreateTable import CreatingTableFrame


_demoPngs = ["database", "table", "view", "indexs", "moredialog", "core",
     "book", "customcontrol", "morecontrols", "layout", "process",
     "clipboard", "images", "miscellaneous"]
# _treeList = [
#     # new stuff
#     (
#      'Tables', [
#         'Appearance',
#         'Search',
#         'Workspace',
#         'Keys'
#         ]
#      ),
#     (
#      'Views', [
#         'Email book',
#         'Open cloud',
#         'Configure device',
#         ]
#      ),
#     (
#      'Indexs', [
#         'Email book',
#         'Open cloud',
#         'Configure device',
#         ]
#      )
# 
# ]

# _treeList=[(u'table', [u'author', u'author_book_link', u'book', u'book_format', u'book_format_link']), (u'index', [u'author', u'book'])]
_treeList = [(u'table', [[u'author', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'author_name', u'VARCHAR', 1, None, 0), (2, u'about_author', u'VARCHAR', 0, None, 0), (3, u'email', u'VARCHAR', 0, None, 0), (4, u'created_on', u'DATETIME', 0, None, 0)]], [u'author_book_link', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_id', u'INTEGER', 0, None, 0), (2, u'author_id', u'INTEGER', 0, None, 0), (3, u'created_on', u'DATETIME', 0, None, 0)]], [u'book', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_name', u'VARCHAR', 1, None, 0), (2, u'sub_title', u'VARCHAR', 0, None, 0), (3, u'isbn_10', u'VARCHAR', 0, None, 0), (4, u'isbn_13', u'VARCHAR', 0, None, 0), (5, u'series', u'VARCHAR', 0, None, 0), (6, u'dimension', u'VARCHAR', 0, None, 0), (7, u'customer_review', u'VARCHAR', 0, None, 0), (8, u'book_description', u'VARCHAR', 0, None, 0), (9, u'edition_no', u'VARCHAR', 0, None, 0), (10, u'publisher', u'TEXT', 0, None, 0), (11, u'book_format', u'VARCHAR', 0, None, 0), (12, u'in_language', u'VARCHAR', 0, None, 0), (13, u'published_on', u'DATETIME', 0, None, 0), (14, u'has_cover', u'VARCHAR', 0, None, 0), (15, u'has_code', u'VARCHAR', 0, None, 0), (16, u'book_path', u'VARCHAR', 0, None, 0), (17, u'rating', u'VARCHAR', 0, None, 0), (18, u'uuid', u'VARCHAR', 0, None, 0), (19, u'tag', u'VARCHAR', 0, None, 0), (20, u'book_file_name', u'VARCHAR', 0, None, 0), (21, u'book_img_name', u'VARCHAR', 0, None, 0), (22, u'wish_listed', u'VARCHAR', 0, None, 0), (23, u'itEbookUrlNumber', u'VARCHAR', 0, None, 0), (24, u'created_on', u'DATETIME', 0, None, 0)]], [u'book_format', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'file_name', u'VARCHAR', 0, None, 0), (2, u'file_type', u'VARCHAR', 1, None, 0), (3, u'file_size', u'VARCHAR', 0, None, 0), (4, u'created_on', u'DATETIME', 0, None, 0)]], [u'book_format_link', [(0, u'id', u'INTEGER', 1, None, 1), (1, u'book_format_id', u'INTEGER', 0, None, 0), (2, u'book_id', u'INTEGER', 0, None, 0), (3, u'created_on', u'DATETIME', 0, None, 0)]]]), (u'index', [[u'author', []], [u'book', []]]), (u'view', [[u'book_author', []]])]


class CreatingTreePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        connectSqlite = ConnectSqlite()
        self._treeList = connectSqlite.getObject()
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
        

        databaseLeaf = self.tree.AppendItem(self.root, 'database', image=16)
        for category, items in self._treeList[1]:
            count += 1
#             print "1: ", category, items
            itemList = list()
            if filter:
                if fullSearch:
                    items = self.searchItems[category]
                else:
#                     print items
                    for item in items:
                        if type(item) != list:
                            if filter.lower() in item.lower():
                                itemList.append(item)
                            else:
                                itemList.append(item[1].lower())
#             items=itemList
#             print itemList
#                     items = [item for item in items if filter.lower() in item.lower()]
            if items:
#                 print "2: ", category, count
                child = self.tree.AppendItem(databaseLeaf, category + ' (' + str(len(items)) + ')', image=count)
                self.tree.SetItemFont(child, catFont)
                self.tree.SetItemPyData(child, count)
                if not firstChild: firstChild = child
                for childItem in items:
                    imageCount = count
#                     if DoesModifiedExist(childItem):
#                         image = len(_demoPngs)
#                     print "3: ", category, childItem, count
                    if 'table' in category :
                        imageCount = 4
                    elif 'index' in category :
                        imageCount = 5
                    elif 'view' in category :
                        imageCount = 6
                    try:
                        if type(childItem) == list:
                            tableNameNode = self.tree.AppendItem(child, childItem[0], image=imageCount)
                            self.tree.SetItemPyData(tableNameNode, count)
                            
                            if 'table' in category :
                                imageCount = 11
                                columnsNode = self.tree.AppendItem(tableNameNode, 'Columns', image=imageCount)
                                self.tree.SetItemPyData(columnsNode, count)
                                imageCount = 11
                                uniqueKeysNode = self.tree.AppendItem(tableNameNode, 'Unique Keys', image=imageCount)
                                self.tree.SetItemPyData(uniqueKeysNode, count)
                                imageCount = 11
                                foreignKeyNode = self.tree.AppendItem(tableNameNode, 'Foreign Keys', image=imageCount)
                                self.tree.SetItemPyData(foreignKeyNode, count)
                                imageCount = 11
                                referencesNode = self.tree.AppendItem(tableNameNode, 'References', image=imageCount)
                                self.tree.SetItemPyData(referencesNode, count)
                                
                            secondLevelItems = childItem[1]
                            for secondLevelChild in secondLevelItems:  
                                if 'table' in category :
#                                     print 'secondLevelChild:', secondLevelChild
                                    if secondLevelChild[5] == 1:
                                        imageCount = 9
                                    if secondLevelChild[2] == 'VARCHAR':
                                        imageCount = 8
                                    if secondLevelChild[2] == 'VARCHAR':
                                        imageCount = 8
                                    if secondLevelChild[2] == 'INTEGER' and secondLevelChild[5] == 0:
                                        imageCount = 8
                                    if secondLevelChild[2] == 'DATETIME':
                                        imageCount = 14
                                secondLevelChildItem = self.tree.AppendItem(columnsNode, secondLevelChild[1], image=imageCount)
                                self.tree.SetItemPyData(secondLevelChildItem, count)
                            self.treeMap[childItem[0]] = tableNameNode
                            
                            if current and (childItem, category) == current:
                                selectItem = columnsNode
                    except Exception as e:
                        print(e)
                    
        self.tree.Expand(self.root)
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
        
        self.tree.Thaw()
        self.searchItems = {}

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
        if self.tree.GetItemText(item) == 'database':
            item1 = menu.Append(wx.ID_ANY, "Disconnect")
            item2 = menu.Append(wx.ID_ANY, "Connect")
            
            sqlEditorBmp = wx.MenuItem(menu, ID_newWorksheet, "SQL Editor")
            sqlEditorBmp.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "script.png"))))
            item3 = menu.AppendItem(sqlEditorBmp)
            
            item4 = menu.Append(wx.ID_ANY, "Properties")
            
            refreshBmp = wx.MenuItem(menu, wx.ID_REFRESH, "&Refresh")
            refreshBmp.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "database_refresh.png"))))
            item5 = menu.AppendItem(refreshBmp)
            
            
            item6 = menu.Append(wx.ID_ANY, "Edit Connection")
            menu.AppendSeparator()
            item7 = wx.MenuItem(menu, wx.ID_ANY, "&Smile!\tCtrl+S", "This one has an icon")
            item7.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "index.png"))))
            menu.AppendItem(item7)
            
            self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
            
        if self.tree.GetItemText(self.tree.item) == 'Connections':
            item1 = menu.Append(wx.ID_ANY, "Refresh \tF5")
        elif self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)) == 'database':
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
    
    def OnItemBackground(self):
        print('OnItemBackground')
    def onNewTable(self, event):
        print('onNewTable')
        tableFrame = CreatingTableFrame(None, 'Table creation')
        
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
        imgList = wx.ImageList(16, 16)

        # add the image for modified demos.

        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "database.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "database_category.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "folder_view.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "folder.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "table.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "view.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "index.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "column.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "string.png"))))  # 8
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "key.png"))))  # 9
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "foreign_key_column.png"))))  # 10
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "columns.png"))))  # 11
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "unique_constraint.png"))))  # 12
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "reference.png"))))  # 13
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "datetime.png"))))  # 14
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "columns.png"))))  # 15
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "images", "sqlite.png"))))  # 16
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
    treeImageLevel = dict()
    treeImageLevel[(0, 0)] = (0, 'database.png')
    treeImageLevel[(1, 0)] = (0, 'database_category.png')
    treeImageLevel[(1, 1)] = (0, 'folder_view.png')
    treeImageLevel[(1, 2)] = (0, 'folder.png')
    
    print(treeImageLevel[(0, 0)])
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = CreatingTreePanel(frame, preferenceName='asfd')
    frame.Show()
    app.MainLoop()
