'''
Created on 11-Dec-2016

@author: vijay
'''


import wx
# import wx.aui
import os
from src.view.TreePanel import CreatingTreePanel
from wx.lib.agw import aui

ID_About = wx.NewId()
ID_newDatabaseConnection = wx.NewId()
ID_openDatabaseConnection = wx.NewId()
#---------------------------------------------------------------------------

# class MainPanel(wx.Panel):
#     """
#     Just a simple derived panel where we override Freeze and Thaw so they are
#     only used on wxMSW.    
#     """
#     def Freeze(self):
#         if 'wxMSW' in wx.PlatformInfo:
#             return super(MainPanel, self).Freeze()
#                          
#     def Thaw(self):
#         if 'wxMSW' in wx.PlatformInfo:
#             return super(MainPanel, self).Thaw()
class DatabaseMainFrame(wx.Frame):

    def __init__(self, parent):
        title = "Opal Database Visualizer"
        style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)
#         self.SetIcon(GetMondrianIcon())
        self.SetMinSize(wx.Size(400, 300))
#         self.pnl = pnl = MainPanel(self)
        self.createMenuBar()
        self.createStatusBar()
#         self.creatingTreeCtrl()
        
        self.bindingEvent()
        
        self.createAuiManager()
#         self.creatingToolbar()
        
#         self.creatingTreeCtrl()
        self._mgr.Update()  
    def creatingTreeCtrl(self):
        # Create a TreeCtrl
        treePanel=CreatingTreePanel(self)


        return treePanel
    #---------------------------------------------    

         
    def constructToolBar(self):
        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(48, 48))
        tb1.AddLabelTool(id=ID_newDatabaseConnection, label="New Connection", shortHelp="New Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "new.png")))
        tb1.AddSeparator()
        
        tb1.AddLabelTool(id=ID_newDatabaseConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
        tb1.AddLabelTool(id=ID_newDatabaseConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        return tb1

    
    def createAuiManager(self):
        # tell FrameManager to manage this frame
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0      
        
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
                          ToolbarPane().Top().
                          LeftDockable(False).RightDockable(False))    
        self._mgr.AddPane(self.creatingTreeCtrl(), aui.AuiPaneInfo().Name("databaseNaviagor").Caption("Database Navigator").
                          Dockable(True).Movable(True).MinSize(wx.Size(300, 100)).Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
    
        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().Name("test4").Caption("SQL execution").LeftDockable(True).
                          Center().CloseButton(True).MaximizeButton(True).MinimizeButton(True))
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
#                           Name("test9").Caption("Min Size 200x100").
#                           BestSize(wx.Size(200, 100)).MinSize(wx.Size(200, 100)).
#                           Bottom().Layer(1).CloseButton(True).MaximizeButton(True))        
        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test1").Caption("Client Size Reporter").Dockable(True).Movable(True).LeftDockable(True).
                          Bottom().Layer(0).Position(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True).PinButton(visible=True).GripperTop())
        
            
        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("sqlLog").Caption("SQL Log").Dockable(True).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True))    
        
            
        self._mgr.GetPane("tb1").Show()
        self.perspective_default = self._mgr.SavePerspective()
        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()
        # "commit" all changes made to FrameManager
        self._mgr.Update()        
        
    def createStatusBar(self):
        print('creating status bar')
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To wxPython!", 1)
        
    def createMenuBar(self):
        print('creating menu bar')
                # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")
        help_menu = wx.Menu()
        help_menu.Append(ID_About, "About...")
        mb.Append(file_menu, "File")
        mb.Append(help_menu, "Help")
        self.SetMenuBar(mb)
        
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)
        

    
    def OnClose(self, event):
#         self._mgr.UnInit()
#         del self._mgr
        self.Destroy()    
    
    def OnExit(self, event):
        self.Close() 
        
    def OnAbout(self, event):
        print('OnAbout')
        msg = "Opal Database Visualizer \n" + \
              "An advanced Database tool for developers, DBAs and analysts.\n" + \
              "(c) BSD"
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
