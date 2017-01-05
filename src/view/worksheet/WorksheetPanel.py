'''
Created on 15-Dec-2016

@author: vijay
'''
import wx
from src.view.worksheet.EditorPanel import CreatingEditorPanel
from src.view.worksheet.ResultListPanel import ResultPanel
import os
from wx.lib.splitter import MultiSplitterWindow

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
        print 'adding tab'
        if name == 'Start Page':
            pass
        else:
            worksheetPanel = CreatingWorksheetWithToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN)
            self._nb.AddPage(worksheetPanel, name, imageId=0)

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        

#         sizer.Fit(self)
class CreatingWorksheetWithToolbarPanel(wx.Panel):
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
        print 'CreatingWorksheetWithToolbarPanel.executeSQL'
    
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
        splitter = MultiSplitterWindow(self, id=-1, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        editorPanel = CreatingEditorPanel(splitter)
        self.resultPanel = ResultPanel(splitter, data=self.getData())
        splitter.AppendWindow(editorPanel)
        splitter.AppendWindow(self.resultPanel)
        splitter.SetOrientation(wx.VERTICAL)
        splitter.SizeWindows()  
        
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
        musicdata = {
        1 : ("Bad English", "The Price Of Love", "Rock"),
        2 : ("DNA featuring Suzanne Vega", "Tom's Diner", "Rock"),
        3 : ("George Michael", "Praying For Time", "Rock"),
        4 : ("Gloria Estefan", "Here We Are", "Rock"),
        5 : ("Linda Ronstadt", "Don't Know Much", "Rock"),
        6 : ("Michael Bolton", "How Am I Supposed To Live Without You", "Blues"),
        7 : ("Paul Young", "Oh Girl", "Rock"),
        8 : ("Paula Abdul", "Opposites Attract", "Rock"),
        9 : ("Richard Marx", "Should've Known Better", "Rock"),
        10: ("Rod Stewart", "Forever Young", "Rock"),
        11: ("Roxette", "Dangerous", "Rock"),
        12: ("Sheena Easton", "The Lover In Me", "Rock"),
        13: ("Sinead O'Connor", "Nothing Compares 2 U", "Rock"),
        14: ("Stevie B.", "Because I Love You", "Rock"),
        15: ("Taylor Dayne", "Love Will Lead You Back", "Rock"),
        16: ("The Bangles", "Eternal Flame", "Rock"),
        17: ("Wilson Phillips", "Release Me", "Rock"),
        18: ("Billy Joel", "Blonde Over Blue", "Rock"),
        19: ("Billy Joel", "Famous Last Words", "Rock"),
        20: ("Janet Jackson", "State Of The World", "Rock"),
        21: ("Janet Jackson", "The Knowledge", "Rock"),
        22: ("Spyro Gyra", "End of Romanticism", "Jazz"),
        23: ("Spyro Gyra", "Heliopolis", "Jazz"),
        24: ("Spyro Gyra", "Jubilee", "Jazz"),
        25: ("Spyro Gyra", "Little Linda", "Jazz"),
        26: ("Spyro Gyra", "Morning Dance", "Jazz"),
        27: ("Spyro Gyra", "Song for Lorraine", "Jazz"),
        28: ("Yes", "Owner Of A Lonely Heart", "Rock"),
        29: ("Yes", "Rhythm Of Love", "Rock"),
        30: ("Billy Joel", "Lullabye (Goodnight, My Angel)", "Rock"),
        31: ("Billy Joel", "The River Of Dreams", "Rock"),
        32: ("Billy Joel", "Two Thousand Years", "Rock"),
        33: ("Janet Jackson", "Alright", "Rock"),
        34: ("Janet Jackson", "Black Cat", "Rock"),
        35: ("Janet Jackson", "Come Back To Me", "Rock"),
        36: ("Janet Jackson", "Escapade", "Rock"),
        37: ("Janet Jackson", "Love Will Never Do (Without You)", "Rock"),
        38: ("Janet Jackson", "Miss You Much", "Rock"),
        39: ("Janet Jackson", "Rhythm Nation", "Rock"),
        40: ("Cusco", "Dream Catcher", "New Age"),
        41: ("Cusco", "Geronimos Laughter", "New Age"),
        42: ("Cusco", "Ghost Dance", "New Age"),
        43: ("Blue Man Group", "Drumbone", "New Age"),
        44: ("Blue Man Group", "Endless Column", "New Age"),
        45: ("Blue Man Group", "Klein Mandelbrot", "New Age"),
        46: ("Kenny G", "Silhouette", "Jazz"),
        47: ("Sade", "Smooth Operator", "Jazz"),
        48: ("David Arkenstone", "Papillon (On The Wings Of The Butterfly)", "New Age"),
        49: ("David Arkenstone", "Stepping Stars", "New Age"),
        50: ("David Arkenstone", "Carnation Lily Lily Rose", "New Age"),
        51: ("David Lanz", "Behind The Waterfall", "New Age"),
        52: ("David Lanz", "Cristofori's Dream", "New Age"),
        53: ("David Lanz", "Heartsounds", "New Age"),
        54: ("David Lanz", "Leaves on the Seine", "New Age"),
        }
        music = musicdata.items()
        music.sort()
        music = [[str(k)] + list(v) for k, v in music] 
        self.data = music
        self.resultPanel.Layout()
    def getData(self):
        # Get the data from the ListCtrl sample to play with, converting it
        # from a dictionary to a list of lists, including the dictionary key
        # as the first element of each sublist.
        
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
