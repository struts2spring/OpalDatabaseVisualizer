'''
Created on 11-Dec-2016

@author: vijay
'''


import wx

import wx.aui
import wx.wizard
import os
from src.view.TreePanel import CreatingTreePanel
from wx.lib.agw import aui

from src.view.worksheet.WorksheetPanel import   CreateWorksheetTabPanel
from src.view.history.HistoryListPanel import HistoryPanel
from src.view.Constant import ID_newConnection, ID_openConnection,\
    ID_newWorksheet, ID_UPDATE_CHECK, ID_SQL_LOG, ID_SQL_EXECUTION
from wx import ID_PREFERENCES
from src.view.preference.OpalPreferences import OpalPreference
from src.view.connection.GetConnect import CreatingNewConnectionPanel
from src.view.connection.NewConnectionWizard import SelectDatabaseNamePage,\
    TitledPage


# ID_UPDATE_CHECK = wx.NewId()
# ID_newConnection = wx.NewId()
# ID_openConnection = wx.NewId()
# ID_newWorksheet = wx.NewId()
# ID_preferences = wx.NewId()
#---------------------------------------------------------------------------


class DatabaseMainFrame(wx.Frame):

    def __init__(self, parent):
        title = "Opal Database Visualizer"
        style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)
        
        print('1----------------------->', os.getcwd())
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
            
        imageLocation=os.path.join(path,  "images")
        image = wx.Image(os.path.join(imageLocation, "Opal_database.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        
        self.SetIcon(icon)
        self.SetMinSize(wx.Size(400, 300))
        self.createMenuBar()
        self.createStatusBar()
#         self.creatingTreeCtrl()
        
        try:
            self.createAuiManager()
        except Exception as ex:
            ex.print_stack_trace()
#         self.creatingToolbar()
        
#         self.creatingTreeCtrl()
        self.bindingEvent()
        self._mgr.Update()  
    def creatingTreeCtrl(self):
        # Create a TreeCtrl
        treePanel = CreatingTreePanel(self)


        return treePanel
    #---------------------------------------------    

         
    def constructToolBar(self):
        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        tb1.AddLabelTool(id=ID_newConnection, label="New Connection", shortHelp="New Database Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "connect.png")))
        tb1.AddSeparator()
        
        tb1.AddLabelTool(id=ID_openConnection, label="Open Connection", shortHelp="Open Database Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "database_connect.png")))
        tb1.AddLabelTool(id=ID_newWorksheet, label="Script", shortHelp="Script", bitmap=wx.Bitmap(os.path.join("..", "images", "script.png")))
        tb1.AddLabelTool(id=wx.ID_PREFERENCES, label="Preferences", shortHelp="Preferences", bitmap=wx.Bitmap(os.path.join("..", "images", "preference.png")))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        return tb1

    
    def createAuiManager(self):
        print('createAuiManager')
        # tell FrameManager to manage this frame
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0      
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
        print('------------------------------------------------------------------------->',path)
        path = os.path.abspath(os.path.join(path, "images"))
        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))    
        self._perspectives = []
        
        
        
        # add a bunch of panes
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("test1").Caption("Pane Caption").Top().CloseButton(True).MaximizeButton(True))
                # add the toolbars to the manager

        self._mgr.AddPane(self.constructToolBar(), aui.AuiPaneInfo().
                          Name("tb1").Caption("Big Toolbar").
                          ToolbarPane().Top().CloseButton(True).
                          LeftDockable(False).RightDockable(False).Gripper(True))    
        
        self._mgr.AddPane(self.creatingTreeCtrl(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "folder_database.png"))).
                          Name("databaseNaviagor").Caption("Database Navigator").Dockable(True).Movable(True).MinSize(wx.Size(300, 100)).
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True).MinimizeButton(True))
    
        self._mgr.AddPane(self.constructSqlPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "script.png"))).
                          Name("sqlExecution").Caption("SQL execution").LeftDockable(True).
                          Center().CloseButton(True).MaximizeButton(True).MinimizeButton(True))
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
#                           Name("test9").Caption("Min Size 200x100").
#                           BestSize(wx.Size(200, 100)).MinSize(wx.Size(200, 100)).
#                           Bottom().Layer(1).CloseButton(True).MaximizeButton(True))      

  
#         self._mgr.AddPane(self.constructHistoryPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join("..", "images", "sql.png"))).
#                           Name("test1").Caption("Client Size Reporter").Dockable(True).Movable(True).LeftDockable(True).
#                           Bottom().Layer(0).Position(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True).PinButton(visible=True).GripperTop())
        
            
        self._mgr.AddPane(self.constructHistoryPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "sql.png"))).
                          Name("sqlLog").Caption("SQL Log").Dockable(True).BestSize(wx.Size(200, 200)).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True))
        
            
        self._mgr.GetPane("tb1").Show()
        self.perspective_default = self._mgr.SavePerspective()
        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()
        # "commit" all changes made to FrameManager
        self._mgr.Update()        

    def constructHistoryPane(self):
        musicdata = {
            1 : ('SELECT * FROM T_MDUR_MDL_RSV;', 'Local_App_Owner' , '1482325584593'  , 'SQL'   , '1', ' 0.225'),
            2 : ('select * from author;', 'Local_App_Owner_' , '1482325584593'  , 'SQL'   , '1', ' 0.225'),
            
        }
        musicdata = musicdata.items()
        musicdata.sort()
        musicdata = [[str(k)] + list(v) for k, v in musicdata]
        historyPanel = HistoryPanel(self, data=musicdata)
        return historyPanel
    def constructSqlPane(self):
        worksheet = CreateWorksheetTabPanel(self)      
          
        return worksheet
    
    def getCurrentCursorPosition(self):
        lineNo=1
        column=1
        return "Line "+str(lineNo)+" , Column "+str(column)
        
    def createStatusBar(self):
        print('creating status bar')
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText("Welcome Opal Database Visualizer", 1)
        
    def createMenuBar(self):
        print('creating menu bar')
                # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        qmi = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit \tCtrl+Q')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16,16))
        qmi.SetBitmap(bmp)
        file_menu.AppendItem(qmi)
        
        edit_menu = wx.Menu()
        
        undoBmp = wx.MenuItem(file_menu, wx.ID_UNDO, "Undo \tCtrl+Z")
        undoBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, (16,16)))
        
        redoBmp = wx.MenuItem(file_menu, wx.ID_REDO, "Redo \tShift+Ctrl+Z")
        redoBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, (16,16)))
        
        cutBmp = wx.MenuItem(file_menu, wx.ID_CUT, "Cut \tCtrl+X")
        cutBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, (16,16)))
        
        copyBmp = wx.MenuItem(file_menu, wx.ID_COPY, "Copy \tCtrl+C")
        copyBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (16,16)))
        
        pasteBmp = wx.MenuItem(file_menu, wx.ID_PASTE, "Paste \tCtrl+V")
        pasteBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16,16)))
        
        edit_menu.AppendItem(undoBmp)
        edit_menu.AppendItem(redoBmp)
        edit_menu.AppendItem(cutBmp)
        edit_menu.AppendItem(copyBmp)
        edit_menu.AppendItem(pasteBmp)
        
#         edit_menu.Append(wx.ID_COPY, "Copy \tCtrl+C")
#         edit_menu.Append(wx.ID_PASTE, "Paste \tCtrl+V")
        
        window_menu = wx.Menu()
                
        preferenceBmp = wx.MenuItem(window_menu, wx.ID_PREFERENCES, "&Preferences")
        preferenceBmp.SetBitmap(wx.Bitmap(os.path.join("..", "images", "preference.png")))
                
        window_menu.AppendSeparator()
        childViewMenu = wx.Menu()
        childViewMenu.Append(ID_SQL_EXECUTION, 'SQL Execution')
        childViewMenu.Append(ID_SQL_LOG, 'SQL Log')
        window_menu.AppendMenu(wx.ID_VIEW_LIST, "Show &View",childViewMenu)
        window_menu.AppendItem(preferenceBmp)
        
        help_menu = wx.Menu()
        
        aboutBmp = wx.MenuItem(help_menu, wx.ID_HELP, "&About Opal Database Visualizer")
        aboutBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16,16)))
        updateCheckBmp = wx.MenuItem(help_menu, ID_UPDATE_CHECK, "Check for &Updates")
        updateCheckBmp.SetBitmap(wx.Bitmap(os.path.join("..", "images", "object_refresh.png")))
                
        
        help_menu.AppendItem(updateCheckBmp)
        help_menu.AppendItem(aboutBmp)
        
        mb.Append(file_menu, "&File")
        mb.Append(edit_menu, "&Edit")
        mb.Append(window_menu, "&Window")
        mb.Append(help_menu, "&Help")
        self.SetMenuBar(mb)
        
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_HELP)
        
        self.Bind(wx.EVT_MENU, self.onOpenConnection, id=ID_openConnection)
        self.Bind(wx.EVT_MENU, self.onNewConnection, id=ID_newConnection)
        self.Bind(wx.EVT_MENU, self.onNewWorksheet, id=ID_newWorksheet)
        self.Bind(wx.EVT_MENU, self.onPreferences, id=ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.onSqlLog, id=ID_SQL_LOG)
        self.Bind(wx.EVT_MENU, self.onSqlExecution, id=ID_SQL_EXECUTION)
    
    def OnClose(self, event):
#         self._mgr.UnInit()
#         del self._mgr
        self.Destroy()    
    
    def OnExit(self, event):
        self.Close() 
        
    def onOpenConnection(self, event):
        print('onOpenConnection')
    def onNewConnection(self, event):
        print('onNewConnection')
        wizard = wx.wizard.Wizard(self, -1, "Simple Wizard")
        page1 = SelectDatabaseNamePage(wizard, "Select new connection type")
        page2 = TitledPage(wizard, "Connection settings")
        page3 = TitledPage(wizard, "Page 3")
        page4 = TitledPage(wizard, "Page 4")
        page1.sizer.Add(wx.StaticText(page1, -1, "Testing the wizard"))
        page4.sizer.Add(wx.StaticText(page4, -1, "This is the last page."))
        wx.wizard.WizardPageSimple_Chain(page1, page2)
        wx.wizard.WizardPageSimple_Chain(page2, page3)
        wx.wizard.WizardPageSimple_Chain(page3, page4)
        wizard.FitToPage(page1)
    
        if wizard.RunWizard(page1):
            print("Success")
    
        wizard.Destroy()        
        self.Show()
#         newConnectionFrame=CreatingNewConnectionPanel(self)
#         newConnectionFrame = CreatingNewConnectionFrame(None, "Opal preferences")
        
    def onNewWorksheet(self, event):
        print('onNewWorksheet')
#         all_panes = self._mgr.GetAllPanes()
        sqlExecutionTab=self.GetTopLevelParent()._mgr.GetPane("sqlExecution")
        sqlExecutionTab.window.addTab("Worksheet")
        
    def onPreferences(self, event):
        print('onPreferences')
        frame1 = OpalPreference(None, "Opal preferences")
        
    def onSqlLog(self, event):
        print('onSqlLog')
        sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("sqlLog").Show()
        self.GetTopLevelParent()._mgr.Update()
        
    def onSqlExecution(self, event):
        print('onSqlExecution')
        sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("sqlExecution").Show()
        self.GetTopLevelParent()._mgr.Update()
        
    def OnAbout(self, event):
        print('OnAbout')
#         msg=u"\u00A9"
        msg = u"""Opal Database Visualizer 
Version : 0.1 Release 
Build : 0.1 Release 
An advanced Database tool for developers, DBAs and analysts.
This product includes software developed by other open source projects.
\u00A9 BSD"""
#         msg=msg.unicode('utf-8')
        dlg = wx.MessageDialog(self, msg, "Opal Database Visualizer",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
                              wx.Size(width, height), self._mgr)
        return ctrl
        
        
class SizeReportCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, mgr=None):

        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER)

        self._mgr = mgr

#         self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)

        size = self.GetClientSize()
        s = ("Size: %d x %d") % (size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height = height + 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2))

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = ("Layer: %d") % pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 1))

            s = ("Dock: %d Row: %d") % (pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 2))

            s = ("Position: %d") % pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 3))

            s = ("Proportion: %d") % pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 4))


    def OnEraseBackground(self, event):
        # intentionally empty
        pass


    def OnSize(self, event):

        self.Refresh()
        event.Skip()
        


if __name__ == "__main__":
    app = wx.App()
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()
