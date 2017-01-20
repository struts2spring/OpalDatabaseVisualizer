'''
Created on 11-Jan-2017

@author: vijay
'''
import wx
import  wx.lib.mixins.listctrl  as  listmix
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin
import datetime
import os
from collections import OrderedDict
from src.view.images import images
try:
    from agw import ultimatelistctrl as ULC
except ImportError:  # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC
#---------------------------------------------------------------------------

dataTypeList = ['INTEGER', 'TEXT', 'NULL', 'REAL', 'BLOB', 'NUMERIC']

headerList = ["S. No.", "icon", "Column name", "Data type", "Primary Key", "Allow Null", "Unique", "Auto Increment", "Default Value"]
# listctrldata = {
# 0 : ("", "Column name1", "", "", "", ""),
# # 1 : ("", "Column name2", "", "", "", ""),
# # 2 : ("", "Column name3", "", "", "", "")
# }

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
class CreatingTableFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.allowAuiFloating = False 
        self.SetMinSize((640, 480))
        CreatingTablePanel(self)
#         self.creatingToolbar()
        self.Center()
        self.CreateStatusBar()
    
    def OnCloseFrame(self, event):
        self.Destroy()



class TableListCtrl(ULC.UltimateListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin, CheckListCtrlMixin):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, agwStyle=0):
        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
             
                
class CreatingTablePanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS | wx.SUNKEN_BORDER)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.tableDict = dict()
        self.tableDict['tableName'] = 'Table 1'
        self.tableDict['columns'] = list()




        ####################################################################
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        tableNameLabel = wx.StaticText(self, -1, "Table Name:")
        tableNameText = wx.TextCtrl(self, -1, "table1", size=(250, -1))
        hBox1.Add(tableNameLabel, 1, wx.RIGHT, 15)
        hBox1.Add(tableNameText, 0, wx.CENTER, 15)
        vBox1.Add(hBox1)
        
        
        self.tb = self.creatingToolbar()
        
        self.imageId = dict()
        self.imageList = ULC.PyImageList(16, 16)
        self.imageId["key.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "..", "images", "key.png"))))
        self.imageId["textfield.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "..", "images", "textfield.png"))))
        self.imageId["unique_constraint.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "..", "images", "unique_constraint.png"))))
        self.imageId["unique_constraint.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join("..", "..", "images", "unique_constraint.png"))))

        self.list = TableListCtrl(self, -1,
                                         agwStyle=wx.LC_REPORT
                                         # | wx.BORDER_SUNKEN
                                         | wx.BORDER_NONE
                                         | wx.LC_EDIT_LABELS
                                         # | wx.LC_SORT_ASCENDING
                                         # | wx.LC_NO_HEADER
                                         | wx.LC_VRULES
                                         | wx.LC_HRULES
                                         # | wx.LC_SINGLE_SEL
                                         | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.list.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        
#         self.list.CheckItem(4)
#         self.list.CheckItem(7)
        self.PopulateList()
        self.evenBinding()

        
        vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        vBox.Add(self.tb, 0, wx.EXPAND)
        vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
        
    def evenBinding(self):
        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(ULC.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(ULC.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(ULC.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(ULC.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(ULC.EVT_LIST_END_DRAG, self.OnEndDrag)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
               
    def PopulateList(self):

        self.list.Freeze()
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)
        boldfont.SetUnderlined(True)
        
        for idx, header in enumerate(headerList):    
            info = ULC.UltimateListItem()
            info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info._image = []
            info._format = 0
            info._kind = 1
            info._font = font
            info._text = header
            self.list.InsertColumnInfo(idx, info)
            width = len(header) * 10
            if width < 40:
                width = 50
            if header == 'Data type':
                width = 160
            self.list.SetColumnWidth(idx, width)

        self.display()
        self.list.Thaw()
        self.list.Update()
     
    def addRow(self):
        
        if len(self.tableDict['columns']) == 0:
            columnIcon = 'key.png'
            dataType = dataTypeList[0]
            isPrimaryKey = True
        else:
            columnIcon = 'textfield.png'
            dataType = dataTypeList[1]
            isPrimaryKey = False
        column = {
          'id':len(self.tableDict['columns']) + 1,
          'columnIcon':columnIcon,
          'columnName':'column '+str(len(self.tableDict['columns']) + 1),
          'dataType':dataType,
          'isPrimaryKey':isPrimaryKey,
          "isNullable":False,
          'isUnique':False,
          "autoIncrement":False,
          "description": 'No'
          
          }
#         for column in self.tableDict.columns:
        self._itemId = self.list.InsertStringItem(column['id'], str(column['id']), 0)
        self.list.SetStringItem(self._itemId , 1, '', imageIds=[self.imageId[column['columnIcon']]] , it_kind=0)
        self.list.SetStringItem(self._itemId , 2, column['columnName'], it_kind=0)
        self.list.SetStringItem(self._itemId , 3, column['dataType'], it_kind=0)
        self.list.SetStringItem(self._itemId , 4, '' if column['isPrimaryKey'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 5, '' if column['isNullable'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 6, '' if column['isUnique'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 7, '' if column['autoIncrement'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 8, column['description'], it_kind=0)
        
        
        item = self.list.GetItem(self._itemId, 4)
        item.Check(isPrimaryKey)
        self.list.SetItem(item)
        
        
        self.tableDict['columns'].append(column)
        print(self.tableDict)    
        self.display()
    def removeRow(self): 
        try:
            if self.list.GetFocusedItem() != -1:
                print(self.list.GetSelectedItemCount())
                selectedItem = self.list.GetFocusedItem()
#                 self.list.Select(selectedItem._itemId-1, True)
                self.list.DeleteItem(self.list.GetFocusedItem())
        except KeyError:
            pass
#         print(self.listctrldata)
#         self.display()
    def display(self):
        pass
        
   
    def ChangeStyle(self, checks):

        style = 0
        for check in checks:
            if check.GetValue() == 1:
                style = style | eval("ULC." + check.GetLabel())
        
        if self.list.GetAGWWindowStyleFlag() != style:
            self.list.SetAGWWindowStyleFlag(style)
            
    def creatingToolbar(self):
        tb = wx.ToolBar(self, style=wx.TB_FLAT)
        tsize = (24, 24)
        plus_bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, tsize)
        minus_bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_TOOLBAR, tsize)
        goUp_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, tsize)
        goDown_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, tsize)

        tb.SetToolBitmapSize(tsize)
        
        # tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        tb.AddLabelTool(10, "Add a column", plus_bmp, shortHelp="Add a column", longHelp="Add a new Column")
        self.Bind(wx.EVT_TOOL, self.onAddColumnClick, id=10)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        # tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        tb.AddLabelTool(20, "Remove a column", minus_bmp, shortHelp="Remove a column", longHelp="Remove a column")
        self.Bind(wx.EVT_TOOL, self.onRemoveColumnClick, id=20)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        tb.AddSeparator()
        tb.AddSimpleTool(30, goUp_bmp, "Move field up", "move column up'")
        self.Bind(wx.EVT_TOOL, self.onMoveUpClick, id=30)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=30)

        tb.AddSimpleTool(40, goDown_bmp, "Move field down", "move column down")
        self.Bind(wx.EVT_TOOL, self.onMoveDownClick, id=40)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=40)

        tb.AddSeparator()
        tb.Realize()
        return tb

    def onAddColumnClick(self, event):
        print('onAddColumn clicked')
        self.addRow()
        
    def onRemoveColumnClick(self, event):
        print('onRemoveColumnClick clicked')
        self.removeRow()
        
    def onMoveUpClick(self, event):
        print('onMoveUpClick clicked')
        
    def onMoveDownClick(self, event):
        print('onMoveDownClick clicked')
        
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)


    def OnTimer(self, event):

        for key, renderer in self.renderers.items():
            renderer.UpdateValue()
            self.list.RefreshItem(key)
        
    
    def OnIdle(self, event):

        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()


    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()

        print("x, y = %s\n" % str((x, y)))
        
        item, flags = self.list.HitTest((x, y))
#         item, flags,subItem = self.list.HitTestSubItem((x, y))
        print('---right down:', item, ':', flags)

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.list.Select(item)
            print('right down:', item)

        event.Skip()


    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        print(self.list._mainWin._selStore._itemsSel)
        self.currentItem = event.m_itemIndex
        print("OnItemSelected: %s, %s, %s, %s\n" % (self.currentItem,
                                                            self.list.GetItemText(self.currentItem),
                                                            self.getColumnText(self.currentItem, 1),
                                                            self.getColumnText(self.currentItem, 2)))

        if self.list.GetPyData(self.currentItem):
            print("PYDATA = %s\n" % repr(self.list.GetPyData(self.currentItem)))

        if self.currentItem == 10:
            print("OnItemSelected: Veto'd selection\n")
            # event.Veto()  # doesn't work
            # this does
            self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()


    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        print("OnItemDeselected: %d\n" % evt.m_itemIndex)

# #        # Show how to reselect something we don't want deselected
# #        if evt.m_itemIndex == 11:
# #            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        print("OnItemActivated: %s\nTopItem: %s\n" % (self.list.GetItemText(self.currentItem), self.list.GetTopItem()))

    def OnBeginEdit(self, event):
        print("OnBeginEdit\n")
        event.Allow()

    def OnItemDelete(self, event):
        print("OnItemDelete\n")

    def OnColClick(self, event):
        print("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        print("OnColRightClick: %d %s\n" % (event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                                        item.GetWidth(), item.GetImage())))

    def OnColBeginDrag(self, event):
        print("OnColBeginDrag\n")
        # # Show how to not allow a column to be resized
        # if event.GetColumn() == 0:
        #    event.Veto()


    def OnColDragging(self, event):
        print("OnColDragging\n")

    def OnColEndDrag(self, event):
        print("OnColEndDrag\n")

    def OnBeginDrag(self, event):   
        print(event.GetIndex())
        data=wx.PyTextDataObject()
        index=event.GetIndex()
        print(self.list.GetdragcursorData())
        
        
        dropSource=wx.DropSource(self)
        dropSource.SetData(index)
        res=dropSource.DoDragDrop(flag=wx.Drag_DefaultMove)
#         dragItem=self.list.
        print("OnBeginDrag\n")
                

    def OnEndDrag(self, event):        
        print("OnEndDrag\n")

    def OnDoubleClick(self, event):
        print("OnDoubleClick item %s\n" % self.list.GetItemText(self.currentItem))
        event.Skip()

    def OnRightClick(self, event):
        print("OnRightClick %s\n" % self.list.GetItemText(self.currentItem))
        print('GetColumn:', self.list.GetSizeTuple())
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.onDeleteSelected, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.onDeleteAllItems, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "Delete Selected")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def getAllSelectedItem(self):
        countSel = 0
        selectedIndexSet = set()
        count = self.list._mainWin.GetItemCount()
        for line in xrange(count):
            if self.list._mainWin.GetLine(line).IsHighlighted():
                countSel += 1
                selectedIndexSet.add(line)
        return countSel, selectedIndexSet

    def onDeleteSelected(self, event):
        countSel, selectedIndexSet1 = self.getAllSelectedItem()
        index = self.list.GetFirstSelected()
        selectedIndexSet = set()
        while index != -1:
            selectedIndexSet.add(self.list.GetItemText(index))
            print("      %s: %s" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
#             self.list.DeleteItem(index)
            index = self.list.GetNextSelected(index)
            if index>-1:
                selectedIndexSet.add(self.list.GetItemText(index))
                
        count = self.list._mainWin.GetItemCount()
        for line in xrange(count):
            if self.list._mainWin.GetItem(line):
                countSel += 1
                selectedIndexSet.add(line)
        self.list._mainWin.GetItemCount()
        
        for idx in self.list:
            if idx > -1:
                try:
                    self.list.DeleteItem(idx)
                except Exception as e:
                    print(idx, e)
        print(selectedIndexSet)
#                 print(idx, item)

    def OnPopupTwo(self, event):
        print("Selected items:")
        index = self.list.GetFirstSelected()

        while index != -1:
            print("      %s: %s" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
#             self.list.Dele
            index = self.list.GetNextSelected(index)

        print("\n")

    def OnPopupThree(self, event):
        print("Popup three")
        self.list.ClearAll()
        wx.CallAfter(self.PopulateList)
        

    def onDeleteAllItems(self, event):
        self.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.list.GetItem(self.currentItem)
        print(("%s, %s, %s") % (item._text, item._itemId, self.list.GetItemData(self.currentItem)))

    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingTableFrame(None, 'table creation')
    frame.Show()
    app.MainLoop()
