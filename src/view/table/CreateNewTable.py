import wx
import wx.grid
import wx.stc
import os
import random
from src.view.worksheet.EditorPanel import CreatingEditorPanel

class CreateTableFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.tableDict = dict()
        self.setData(self.tableDict)
        
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.allowAuiFloating = False 
        self.SetMinSize((640, 480))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonPanel = CreateButtonPanel(self)
        
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        self.createTablePanel = CreateTablePanel(splitter)
        self.createTablePanel.setData(self.tableDict)
        self.createTablePanel.headPanel.setData(self.tableDict)
        self.editorPanel = CreatingEditorPanel(splitter, -1)
#         self.sstc = wx.stc.StyledTextCtrl(splitter, -1)
        splitter.SetMinimumPaneSize(20)
        splitter.SplitHorizontally(self.createTablePanel, self.editorPanel)
        sizer.Add(splitter, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.SetSizer(sizer)
#         self.creatingTable = CreatingTablePanel(splitter)
#         grid = SimpleGrid(self)
        self.Center()
        self.createNewTableStatusBar()
        self.Show(True)
        
        
    def setData(self, tableDict=None):
        self.tableDict = tableDict
        self.tableDict['schemaName'] = 'schema_1'
        self.tableDict['tableName'] = 'Table_1'
#         self.tableDict['columns'] = dict()    
        
    def OnCloseFrame(self, event):
        self.Destroy()
    def createNewTableStatusBar(self):
        print('creating status bar')
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText("Welcome Opal Database Visualizer", 1)
    def getCurrentCursorPosition(self):
        lineNo = 1
        column = 1
        return "Line " + str(lineNo) + " , Column " + str(column)
class CreateTableHeadPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent     
        import  wx.lib.rcsizer  as rcs
        sizer = rcs.RowColSizer()
#         vBox = wx.BoxSizer(wx.VERTICAL)
        self.tableDict=dict()
        self.setData(self.tableDict)

        
        schemaNameLabel = wx.StaticText(self, -1, "Schema Name:")
        self.schemaNameText = wx.TextCtrl(self, -1, '', size=(250, -1))
        
        tableNameLabel = wx.StaticText(self, -1, "Table Name:")
        self.tableNameText = wx.TextCtrl(self, -1, '', size=(250, -1))
        
        sizer.Add(schemaNameLabel, flag=wx.EXPAND, row=1, col=1)
        sizer.Add(self.schemaNameText, row=1, col=2)
        
        sizer.Add(tableNameLabel, flag=wx.EXPAND, row=2, col=1)
        sizer.Add(self.tableNameText, row=2, col=2)
        

#         vBox.Add(sizer)
        self.SetSizer(sizer)
#         self.Layout()

    def setData(self, tableDict=None):
        if tableDict and len(tableDict)>1:
            self.tableDict=tableDict
            self.schemaNameText.SetValue(self.tableDict['schemaName'])
            self.tableNameText.SetValue(self.tableDict['tableName'])
        else:
            self.tableDict['schemaName']=''
            self.tableDict['tableName']=''
        
class CreateButtonPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent         
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, 50, "Ok", (20, 220))
        okButton.SetToolTipString("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onOkClick, okButton)
        
        cancelButton = wx.Button(self, 51, "Cancel", (20, 220))
        cancelButton.SetToolTipString("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

#         b.SetBitmap(images.Mondrian.Bitmap,
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
#                     #wx.RIGHT
#                     #wx.TOP
#                     #wx.BOTTOM
#                     )
        hbox.Add(okButton)    
        hbox.Add(cancelButton)    
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
    def onOkClick(self, event):
        print('onOkClick')

    def onCancelButtonClick(self, event):
        self.GetTopLevelParent().Destroy()
        
class CreateTablePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        #######################################33
#         self.row = dict()
#         self.row[0] = ["icon", "Column name", "Data type", "Primary key", "Allow null", "Unique", "Auto increment", "Default value"]
#         self.row[1] = ["1", "One", "INT", "1", "0", "1", "1", None ]        
        
        self.headPanel = CreateTableHeadPanel(self)
        self.tb = self.creatingToolbar()
        self.grid = SimpleGrid(self)

        
        vBox.Add(self.headPanel, 0, wx.EXPAND)
        vBox.Add(self.tb, 0, wx.EXPAND)
        vBox.Add(self.grid, 0, wx.EXPAND)
        
        #######################################33
        
#         sizer.Add(self.headPanel, 1, wx.EXPAND , 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        
    def setData(self, tableDict=None):
        if tableDict:
            self.tableDict=tableDict
            self.tableDict['rows']=list()
            self.tableDict['row']=dict()
            self.tableDict['row'][0] = ["icon", "Column name", "Data type", "Primary key", "Allow null", "Unique", "Auto increment", "Default value"]

    def getData(self):
        return self.tableDict

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
        
        rowNum = len(self.tableDict['row'])
        columnName="Column_" + str(rowNum)
        isPrimaryKey = "0"
        isAutoIncrement = "0"
        isNotNull="0"
        isUnique='0'
        default=None
        if rowNum == 1:
            iconIndex = 0  # random.choice([0, 1, 2, 3])
            datatype = "INTEGER"  # random.choice(["INTEGER", "TEXT"])
            isPrimaryKey = "1"
            isNotNull='0'
            isUnique='0'
        elif rowNum > 1:
            iconIndex = 1  # random.choice([0, 1, 2, 3])
            datatype = "VARCHAR"  # random.choice(["INTEGER", "TEXT"])
            isPrimaryKey = "0"
        
        if isPrimaryKey == "1":
            isAutoIncrement = "1"
           
        self.tableDict['row'][rowNum] = [str(iconIndex), columnName, datatype, isPrimaryKey, "0", isUnique, isAutoIncrement, default ]        
        
        
        self.tableDict['rows'].append({
            'rowNum':rowNum,
            "columnName":columnName,
            'dataType': datatype,
            'isPrimaryKey':isPrimaryKey,
            'isAutoIncrement':isAutoIncrement,
            'isNotNull':isNotNull,
            'isUnique':isUnique,
            'default': default
            })
        
            
#         data.append(row)
        grid = self.GetTopLevelParent().createTablePanel.grid
        grid.addData(data=self.tableDict['row'])
        
        self.updateTableEditorPanel()
#         table=self.GetTopLevelParent().createTablePanel.grid
#         tableData=table.data
#         table.AppendRow()
#         self.GetTopLevelParent().createTablePanel.grid.addData()
#         print(tableData)
        
    def updateTableEditorPanel(self):
        tableDict=self.GetTopLevelParent().createTablePanel.tableDict
        self.GetTopLevelParent().editorPanel.sstc.SetText(self.createSql(tableDict))
        
    def createSql(self, tableDict=None):    
        '''
        This method creates sql script for create table sql.
        '''
        sqlList = list()
        if tableDict:
            sqlList.append("CREATE")
            if 'temp' in tableDict.keys():
                sqlList.append("TEMP")
            sqlList.append('TABLE')
            if 'ifNotExists' in  tableDict.keys():
                sqlList.append('IF NOT EXISTS')
            if 'schemaName' in tableDict.keys():
                sqlList.append("'" + tableDict['schemaName'] + "'.'" + tableDict['tableName'] + "'")
            else:
                sqlList.append("'" + tableDict['tableName'] + "'")
            sqlList.append('(')
            print(tableDict['rows'])
            for idx, column in enumerate(tableDict['rows']):
                sqlList.append("'" + column['columnName'] + "'")
                sqlList.append(column['dataType'])
                if column['isPrimaryKey']=='1':
                    sqlList.append('PRIMARY KEY')
                    if column['isAutoIncrement']=='1':
                        sqlList.append('AUTOINCREMENT')
                elif column['isNotNull']=='1':
                    sqlList.append('NOT NULL')
                elif column['isUnique']=='1':
                    sqlList.append('UNIQUE')
                elif column['isUnique']=='1':
                    sqlList.append('UNIQUE')
                elif 'check' in column.keys():
                    sqlList.append('CHECK ( ' + column['check'] + ' )')
                elif 'default' in column.keys():
                    sqlList.append('DEFAULT ' + str(column['default']))
                
                sqlList.append(',')
            sqlList.pop()
            sqlList.append(')')  
            sqlList.append(';')  
        sql = " ".join(sqlList)
#         formatedSql=sqlparse.format(sql, encoding=None)
        return sql                      
    def onRemoveColumnClick(self, event):
        print('onRemoveColumnClick clicked')
        self.removeRow()
#         self.updateItemStatus(event.GetIndex(), event.GetItem())
        
    def onMoveUpClick(self, event):
        print('onMoveUpClick clicked')
        
    def onMoveDownClick(self, event):
        print('onMoveDownClick clicked')
class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1, size=(400, 300))
#         data=dict()
#         data['colLabels']=["icon","Column name","Data type","Primary key","Allow null","Unique","Auto increment","Default value"]
#         data['row']=[["1","One","INT",True, False,True,True, None ]]
#         colLabels=data['colLabels']
#         tableBase = GenericTable(data=data['row'], colLabels=colLabels)
#         self.SetTable(tableBase)
        self.CreateGrid(1, 1)
        self.dataTypeList = [("INTEGER", 0), ("VARCHAR", 1), ("TEXT", 2), ("REAL", 3), ("BLOB", 4), ("NUMERIC", 5)]
        self.checkBoxColumns = [3, 4, 5, 6]
        self.textBoxColumns = [1, 7]
        self.comboBoxList = [2]
        self.iconColumns = [0]
        
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
        self.bmpList = list()
        keyBmp = wx.Bitmap(os.path.abspath(os.path.join(path, "key.png")))  # 0 for primary key column
        textfieldBmp = wx.Bitmap(os.path.abspath(os.path.join(path, "textfield.png")))  # 1 for varchar, char, text column
        unique_constraintBmp = wx.Bitmap(os.path.abspath(os.path.join(path, "unique_constraint.png")))  # 2 for unique key column
        datetimeBmp = wx.Bitmap(os.path.abspath(os.path.join(path, "datetime.png")))  # 3 for datetime field column
        integerBmp = wx.Bitmap(os.path.abspath(os.path.join(path, "column.png")))  #  4 for integer key column
        self.bmpList.append(keyBmp)  # 0 for primary key
        self.bmpList.append(textfieldBmp)  # 1 for varchar , text, char,
        self.bmpList.append(unique_constraintBmp)  # 2 for unique column
        self.bmpList.append(datetimeBmp)  # 3 for datetime
        self.bmpList.append(integerBmp)  #  4 for integer key column
        
        self.lastSelectedCell = None
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.bindAllEvent()
    
    def bindAllEvent(self):
        # test all the events
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
 
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)
 
        self.Bind(wx.grid.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.OnColSize)
 
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)
 
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        
    ########################### Check box start ###################################    
    def OnCellLeftClick(self, evt):
        print("OnCellLeftClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                 evt.GetCol(),
                                                 evt.GetPosition()))
        row = evt.GetRow()
        col = evt.GetCol()
        if col in self.checkBoxColumns:
            print(self.GetCellValue(row, col))
            self.toggleCheckBox(row, col)
#             wx.CallLater(100,self.toggleCheckBox(row,col))
        evt.Skip()
    def toggleCheckBox(self, row, col):
        try:
            self.cb.Value = not self.cb.Value
            self.lastSelectedCell = (row, col)
            self.afterCheckBox(self.cb.Value, row=row, col=col)
        except Exception as e:
            print(e)

    def afterCheckBox(self, isChecked, row=None, col=None):
        print('afterCheckBox', self.GridCursorRow, isChecked)
        self.isChecked = isChecked
        targetRow = row
        targetCol = 0
        if self.isChecked:
            self.SetCellValue(row, col, '1')
            # Setting image icon for primary key
            self.SetCellValue(targetRow, targetCol, "0")
        else:
            self.SetCellValue(row, col, '0')
            
            dataType = self.GetCellValue(row, 2)
            if dataType == 'INTEGER':
                # setting image icon for integer column
                self.SetCellValue(targetRow, targetCol, "4")
            elif dataType in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                for d in  ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                    if dataType.lower().startswith(d.lower()):
                        self.SetCellValue(targetRow, targetCol, "1")
                        break
                # setting image icon for integer column
            
        self.Refresh()
        
    def OnEditorCreated(self, evt):
        print("OnEditorCreated: (%d, %d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetControl()))
        row = evt.GetRow()
        col = evt.GetCol()
        
        # In this example, all cells in row 0 are GridCellChoiceEditors,
        # so we need to setup the selection list and bindings. We can't
        # do this in advance, because the ComboBox control is created with
        # the editor.
        if col in self.comboBoxList:
            # Get a reference to the underlying ComboBox control.
            self.comboBox = evt.GetControl()
            
            # Bind the ComboBox events.
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnGridComboBox)
            self.comboBox.Bind(wx.EVT_TEXT, self.OnGridComboBoxText)
            
            # Load the initial choice list.
            for (item, data) in self.dataTypeList:
                self.comboBox.Append(item, data)
        elif col in self.checkBoxColumns:
            self.lastSelectedCell = (row, col)
            self.cb = evt.Control
            self.cb.WindowStyle |= wx.WANTS_CHARS
            self.cb.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
            self.cb.Bind(wx.EVT_CHECKBOX, self.onCheckBox)  
            
        print("After change OnEditorCreated: (%d, %d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetControl().Value))   
        evt.Skip()
        
    def onKeyDown(self, evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows - 1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols - 1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()
    def onCheckBox(self, evt):
        print(self.lastSelectedCell)
        if self.lastSelectedCell:
            self.afterCheckBox(evt.IsChecked(), row=self.lastSelectedCell[0], col=self.lastSelectedCell[1])

        

    ########################### Check box close ###################################    
                 
    def OnCellRightClick(self, evt):
        print("OnCellRightClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetPosition()))
        evt.Skip()
 
    def OnCellLeftDClick(self, evt):
        print("OnCellLeftDClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetPosition()))
        evt.Skip()
 
    def OnCellRightDClick(self, evt):
        print("OnCellRightDClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                   evt.GetCol(),
                                                   evt.GetPosition()))
        evt.Skip()
 
    def OnLabelLeftClick(self, evt):
        print("OnLabelLeftClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetPosition()))
        evt.Skip()
 
    def OnLabelRightClick(self, evt):
        print("OnLabelRightClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                   evt.GetCol(),
                                                   evt.GetPosition()))
        evt.Skip()
 
    def OnLabelLeftDClick(self, evt):
        print("OnLabelLeftDClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                   evt.GetCol(),
                                                   evt.GetPosition()))
        evt.Skip()
 
    def OnLabelRightDClick(self, evt):
        print("OnLabelRightDClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                    evt.GetCol(),
                                                    evt.GetPosition()))
        evt.Skip()
 
    def OnRowSize(self, evt):
        print("OnRowSize: row %d, %s\n" % (evt.GetRowOrCol(),
                                           evt.GetPosition()))
        evt.Skip()
 
    def OnColSize(self, evt):
        print("OnColSize: col %d, %s\n" % (evt.GetRowOrCol(),
                                           evt.GetPosition()))
        evt.Skip()
 
    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print("OnRangeSelect: %s  top-left %s, bottom-right %s\n" % (msg, evt.GetTopLeftCoords(),
                                                                     evt.GetBottomRightCoords()))
        evt.Skip()
 
 
    def OnCellChange(self, evt):
 
        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        sourceValue = self.GetCellValue(evt.GetRow(), evt.GetCol())
        print("OnCellChange: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition()), sourceValue)
        sourceRow = evt.GetRow()
        sourceCol = evt.GetCol()
        
        
        if sourceCol == 2:
            targetRow = sourceRow
            targetCol = 0
            if sourceValue in ["INTEGER", "INT"]:
                self.SetCellValue(targetRow, targetCol, "4")
            elif sourceValue.upper() in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
#                 self.SetCellValue(targetRow, targetCol,"1")
                isPrimaryKey = self.GetCellValue(sourceRow, 3)
                if not isPrimaryKey == 1:
                    for d in  ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                        if sourceValue.lower().startswith(d.lower()):
                            self.SetCellValue(targetRow, targetCol, "1")
                            break
        self.Refresh()
#         if value == 'no good':
#             self.moveTo = evt.GetRow(), evt.GetCol()
#         #All cells have a value, regardless of the editor.
#         print 'Changed cell: (%u, %u)' % (Row, Col)
#         print 'value: %s' % self.grid1.GetCellValue(Row, Col)
#         
#         #Row 0 means a GridCellChoiceEditor, so we should have associated
#         #an index and client data.
#         if Row == 0:
#             print 'index: %u' % self.index
#             print 'data: %s' % self.data
#         
#         print ''            #blank line to make it pretty.
#         event.Skip()
    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print("OnSelectCell: %s (%d,%d) %s\n" % (msg, evt.GetRow(),
                                                 evt.GetCol(), evt.GetPosition()))
 
        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
 
        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()
#         if row > -1 and col > -1:
#             value = self.GetCellValue(row, col)
#      
#             if value == 'no good 2':
#                 return  # cancels the cell selection
     
        evt.Skip()
 
 
    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to edit this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return
 
        print("OnEditorShown: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(),
                                               evt.GetPosition()))
        evt.Skip()
 
 
    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return
 
        print("OnEditorHidden: (%d,%d) %s\n" % (evt.GetRow(),
                                                evt.GetCol(),
                                                evt.GetPosition()))
        evt.Skip()
 
 


    # This method fires when the underlying GridCellChoiceEditor ComboBox
    # is done with a selection.
    def OnGridComboBox(self, event):
        # Save the index and client data for later use.
        self.index = self.comboBox.GetSelection()
        self.data = self.comboBox.GetClientData(self.index)
        
        print('ComboBoxChanged: %s' % self.comboBox.GetValue())
        print('ComboBox index: %u' % self.index)
        print('ComboBox data: %u\n' % self.data)
        event.Skip()        
        
        
        
        
    # This method fires when any text editing is done inside the text portion
    # of the ComboBox. This method will fire once for each new character, so
    # the print statements will show the character by character changes.
    def OnGridComboBoxText(self, event):
        # The index for text changes is always -1. This is how we can tell
        # that new text has been entered, as opposed to a simple selection
        # from the drop list. Note that the index will be set for each character,
        # but it will be -1 every time, so the final result of text changes is
        # always an index of -1. The value is whatever text that has been 
        # entered. At this point there is no client data. We will have to add
        # that later, once all of the text has been entered.
        self.index = self.comboBox.GetSelection()
        
        print('ComboBoxText: %s' % self.comboBox.GetValue())
        print ('ComboBox index: %u\n' % self.index)
#         self.updateGridCell()
        event.Skip()
           
    def updateGridCell(self):
        '''
        This method will be called as soon as a comboBox value changes.
        '''
        pass
                     
    def addData(self, data=None):
#         print(self.GetRowSizes())
#         print(self.GetColSizes())
        self.ClearGrid()
        
        if data and len(data) > 0:
            print('rows:', self.GetNumberRows())
            print('cols:', self.GetNumberCols())
    #         self.DeleteRows()
            currentRows, currentCols = (self.GetNumberRows(), self.GetNumberCols())
            newRows = len(data) - 1
            newCols = len(data[0])
    #         self.AppendRows(numRows=len(data)-1, updateLabels=True)   
    #         if len(data) > 0 :
    #             self.AppendCols(numCols=len(data[0]), updateLabels=True)  
            if newRows < currentRows:
                # - Delete rows:
                self.DeleteRows(0, currentRows - newRows, True)
    
            if newRows > currentRows:
                # - append currentRows:
                self.AppendRows(newRows - currentRows)
                
                
            if newCols < currentCols:
                # - Delete rows:
                self.DeleteCols(pos=0, numCols=currentCols - newCols, updateLabels=True)
    
            if newCols > currentCols:
                # - append currentRows:
                self.AppendCols(newCols - currentCols)
            
    
            self.fillTableData(data)
        else:
            numCols = self.GetNumberCols()
            numRows = self.GetNumberRows()
            if numRows > 0:
                self.DeleteRows(pos=0, numRows=numRows, updateLabels=True)
            if numCols > 0:
                self.DeleteCols(pos=0, numCols=numCols, updateLabels=True)
            
        self.Refresh()
#         self.Update()
    
    def fillTableData(self, data=None):  
        for dataKey, dataValue in data.items():
            print(dataKey, dataValue)
            for idx, colValue in enumerate(dataValue):
#                 print(idx, dataValue)
                if dataKey == 0:
                    self.SetColLabelValue(idx, str(colValue))
                elif dataKey > 0 and idx == 2:
                    # Create the GridCellChoiceEditor with a blank list. Items will
                    # be added later at runtime. "allowOthers" allows the user to
                    # create new selection items on the fly.
                    tChoiceEditor = wx.grid.GridCellChoiceEditor([], allowOthers=True)
                    self.SetCellEditor(dataKey - 1, idx, tChoiceEditor)
                    
                    selectedDataType = None
                    for dataType in self.dataTypeList:
                        print(dataType[0], colValue)
                        if dataType[0] == colValue:
                            selectedDataType = dataType
                            break
                    self.SetCellValue(dataKey - 1, idx, selectedDataType[0])
                    
                elif dataKey > 0 and idx in self.comboBoxList:
                    self.SetCellValue(dataKey - 1, idx, str(colValue))      
                elif dataKey > 0 and idx in self.checkBoxColumns:
                    attr = wx.grid.GridCellAttr()
                    attr.SetEditor(wx.grid.GridCellBoolEditor())
                    attr.SetRenderer(wx.grid.GridCellBoolRenderer())
                    self.SetColAttr(idx, attr)  
                    self.SetCellValue(dataKey - 1, idx, str(colValue))    
                elif dataKey > 0 and idx in self.textBoxColumns:
                    self.SetCellValue(dataKey - 1, idx, str(colValue))  
                elif dataKey > 0 and idx in self.iconColumns:
                    print("self.iconColumns:", self.iconColumns)
                    attr = wx.grid.GridCellAttr()
                    attr.SetRenderer(GridCellIconRenderer(self.bmpList))
                    self.SetColAttr(idx, attr)  
                    self.SetCellValue(dataKey - 1, idx, str(colValue))
                    
class GridCellIconRenderer(wx.grid.PyGridCellRenderer):
    """
    Utility class for displaying an icon in a table column.
    """
    
    def __init__(self, *arg, **kw):
        super(GridCellIconRenderer, self).__init__()
        self.bmpList = arg[0]
        self.selectBmpIndex = 0
                  
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):  
        self.selectBmpIndex = grid.GetCellValue(row, col)
        try: 
            selectedBmp = self.bmpList[int(self.selectBmpIndex)]
        except Exception as e:
            print(e) 
        
        image = wx.MemoryDC()
        image.SelectObject(selectedBmp)
        # clear the background
        dc.SetBackgroundMode(wx.SOLID)
        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)        
        # copy the image but only to the size of the grid cell
        width, height = selectedBmp.GetWidth(), selectedBmp.GetHeight()

        if width > rect.width - 2:
            width = rect.width - 2

        if height > rect.height - 2:
            height = rect.height - 2

        dc.Blit(rect.x + 1, rect.y + 1, width, height,
                image,
                0, 0, wx.COPY, True)
                      
class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels

        
    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.data)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return len(self.data[0])

    def GetColLabelValue(self, *args, **kw):
        if self.colLabels:
            return self.colLabels[args[0]]
        else:
            return super(GenericTable, self).GetColLabelValue(*args, **kw)
        
    def GetRowLabelValue(self, *args, **kw):
        if self.rowLabels:
            return self.rowLabels[args[0]]
        else:
            return super(GenericTable, self).GetRowLabelValue(*args, **kw)
        
    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        return False

    def GetValue(self, row, col):
        """Return the value of a cell"""
        return self.data[row][col]

    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        pass       
    
    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return None
    

                   
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreateTableFrame(None, 'table creation')
    frame.Show()
    app.MainLoop()
