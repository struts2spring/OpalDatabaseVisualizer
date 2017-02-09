'''
Created on 15-Dec-2016

@author: vijay
'''
import wx
from src.view.worksheet.EditorPanel import CreatingEditorPanel
from src.view.worksheet.ResultListPanel import ResultPanel
import os

import wx.aui as aui
from src.view.Constant import ID_RUN

ID_executeScript = wx.NewId()

class CreateWorksheetTabPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent

        # Attributes
        self._nb = aui.AuiNotebook(self)
        if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "..", "images")
#             playImage=wx.Bitmap(os.path.join("..","..", "images", "play.png"))
        elif "view" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "images")
        imgList = wx.ImageList(16, 16)
        imgList.Add(wx.Bitmap(os.path.join(imageLocation, "sql_script.png")))
        
        self._nb.AssignImageList(imgList) 
        
        self.addTab()
#         self._nb.AddPage(worksheetPanel, "2", imageId=0)
        # Layout
        
        self.__DoLayout()

    def addTab(self, name='Start Page'):
        if name == 'Start Page':
            pass
        else:
            worksheetPanel = CreatingWorksheetWithToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN)
#             worksheetPanel.worksheetPanel.editorPanel
            name='Worksheet '+str(len(self.GetPages(type(worksheetPanel))))
            self._nb.AddPage(worksheetPanel, name, imageId=0)
            self.Bind(aui.EVT__AUINOTEBOOK_TAB_RIGHT_DOWN, self.onTabRightDown, self._nb)
            self.Bind(aui.EVT_AUINOTEBOOK_BG_DCLICK, self.onBgDoubleClick, self._nb)

    def onBgDoubleClick(self, event):
        print('onBgDoubleClick')
        name='Worksheet '
        self.addTab(name)
    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        
    def SetCurrentPage(self, page):
        """
        Set the current page to the page given
        """
        n = self._nb.GetPageIndex(page)
        if n!=-1:
            self._nb.SetSelection(n)
            return True
        return False    
    
    def GetCurrentPage(self):
        """
        Get the current active Page page
        """
        num  = self._nb.GetSelection()
        if num==-1:
            page = None
        else:
            page = self._nb.GetPage(num)
        return page

    def GetPages(self, page_type):
        """
        Get all the Page pages of a particular type
        """
        npages = self._nb.GetPageCount()
        res = []
        for n in range(0,npages):
            page = self._nb.GetPage(n)
            if isinstance(page, page_type):
                res.append(page)
        return res        
    def onTabRightDown(self, event):
        print('rightdown PopUp')

        pos = self.ScreenToClient(wx.GetMousePosition())
        self.popupmenu = wx.Menu()
        for text in "Close,Close Others,Close Other tabs to the left,Close &All".split(','):
            item = self.popupmenu.Append(-1, text)
        print(self.GetCurrentPage())
        self.PopupMenu(self.popupmenu, pos)
#         tab = event.GetEventObject()
#         num = tab.GetActivePage()
#         conpage = tab.GetWindowFromIdx(num)
#         menu = conpage.GetPageMenu()
#         date = DateControlPop(self, -1, pos = (30,30))
#         self.PopupMenu(menu)
#         menu.Destroy()
        
#         self.popmenu=None
#         if self.popmenu:
#             self.popmenu.Destroy()
#             self.popmenu = None
#         fileMenu = wx.Menu()   
#         imp = wx.Menu()
#         imp.Append(wx.ID_ANY, 'Import newsfeed list...') 
#         fileMenu.AppendMenu(wx.ID_ANY, 'I&mport', imp)
#         self.popmenu.Append(fileMenu)
#         self.PopupMenu(self.popmenu, event.GetPosition())

#         sizer.Fit(self)
class CreatingStartPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        worksheetToolbar = self.constructWorksheetToolBar()
        worksheetPanel = CreatingWorksheetPanel(self)
        self.bindingEvent()
        ####################################################################
        vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
class CreatingWorksheetWithToolbarPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        worksheetToolbar = self.constructWorksheetToolBar()
        self.worksheetPanel = CreatingWorksheetPanel(self)
        self.worksheetPanel.setResultData()
        self.bindingEvent()
        ####################################################################
        vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructWorksheetToolBar(self):
        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        playImage = None
        if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "..", "images")
#             playImage=wx.Bitmap(os.path.join("..","..", "images", "play.png"))
        elif "view" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "images")
#             playImage=wx.Bitmap(os.path.join("..", "images", "play.png"))
            
#         playImage=wx.Bitmap(os.path.join(imageLocation, "sql_exec.png"))
        tb1.AddLabelTool(id=ID_RUN, label="Run", shortHelp="run single line ", bitmap=wx.Bitmap(os.path.join(imageLocation, "sql_exec.png")))
        tb1.AddLabelTool(id=ID_executeScript, label="Run Script", shortHelp="execute script ", bitmap=wx.Bitmap(os.path.join(imageLocation, "sql_script_exec.png")))
        tb1.AddSeparator()
        tb1.AddLabelTool(id=ID_executeScript, label="Run Script", shortHelp="execute script ", bitmap=wx.Bitmap(os.path.join(imageLocation, "abc.png")))
        
#         tb1.AddLabelTool(id=ID_openConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
#         tb1.AddLabelTool(id=ID_newConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        return tb1     
    
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.executeSQL, id=ID_RUN)
    def executeSQL(self, event):
        print('CreatingWorksheetWithToolbarPanel.executeSQL')
#         x=self.GetParent()
#         creatingEditorPanel=self.GetChildren()[1].splitter.Children[0]
#         resultPanel=self.GetChildren()[1].splitter.Children[1]
#         resultPanel.createDataViewCtrl(data=music,headerList=["Artist","Title","Genre"])
#         resultPanel.setModel(music)
#         resultPanel.Layout()
    
class CreatingWorksheetPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        
#         self._nb = wx.Notebook(self)

        
        ####################################################################
        self.data = dict()
#         worksheetToolbar = self.constructWorksheetToolBar()
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D)
#         splitter = MultiSplitterWindow(self, id=-1, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        self.editorPanel = CreatingEditorPanel(splitter)
        self.resultPanel = ResultPanel(splitter, data=self.getData())
        splitter.SetMinimumPaneSize(20)
        splitter.SplitHorizontally(self.editorPanel, self.resultPanel)
#         splitter.AppendWindow(self.editorPanel)
#         splitter.AppendWindow(self.resultPanel)
#         splitter.SetOrientation(wx.VERTICAL)
#         splitter.SizeWindows()  
        
#         editorPanel = CreatingEditorPanel(self)
        ####################################################################
        vBox.Add(splitter , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(editorPanel , 1, wx.EXPAND | wx.ALL)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
    def SetOrientation(self, value):
        if value:
            self.splitter.SetOrientation(wx.VERTICAL)
        else:
            self.splitter.SetOrientation(wx.HORIZONTAL)
        self.splitter.SizeWindows()        
    
    def setResultData(self, data=None):  
        print('setResultData')
        self.data=data
#         self.data = music
        self.resultPanel.Layout()
    def getData(self):
        # Get the data from the ListCtrl sample to play with, converting it
        # from a dictionary to a list of lists, including the dictionary key
        # as the first element of each sublist.
#         self.data=music
        return self.data
    
    #---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = CreateWorksheetTabPanel(frame)
    panel.addTab()
    panel.addTab("123")
    frame.Show()
    app.MainLoop()
