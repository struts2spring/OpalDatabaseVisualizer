'''
Created on 05-Feb-2017

@author: vijay
'''
import wx



class CreatingFindAndReplaceFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(400, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
#         self.pnl = pnl = MainPanel(self)        
        self.findAndReplacePanel = CreatingFindAndReplacePanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        self.Show()
    def OnCloseFrame(self, event):
        print('OnCloseFrame')
        self.OnExitApp(event)
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        print('OnExitApp')
        self.Destroy()

#---------------------------------------------------------------------------
class CreatingFindAndReplacePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
#         import  wx.lib.rcsizer  as rcs
#         sizer = rcs.RowColSizer()
#         sizer = wx.GridBagSizer(hgap=3, vgap=3)
        sizer = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        
        h1.Add((1,1), -1, wx.ALL) # this is a spacer
        schemaNameLabel = wx.StaticText(self, -1, "Find:")
        schemaNameText = wx.TextCtrl(self, -1, '', size=(400, -1))
        
        tableNameLabel = wx.StaticText(self, -1, "Replace with:")
        tableNameText = wx.TextCtrl(self, -1, '', size=(400, -1))
        
        h1.Add(schemaNameLabel, 0, wx.ALL, 2)
        h1.Add(schemaNameText, 0, wx.ALL, 2)
        
        h2.Add((1,1), -1, wx.ALL) # this is a spacer
        h2.Add(tableNameLabel, 0, wx.ALL, 2)
        h2.Add(tableNameText, 0, wx.ALL, 2)
        
        
        
        # first the static box
        box_00 = wx.StaticBox(self, -1, 'Direction')
        # then the sizer
        staticBoxSizer_00 = wx.StaticBoxSizer(box_00, wx.VERTICAL)
        # first the static box
        box_01 = wx.StaticBox(self, -1, 'Scope')
        # then the sizer
        staticBoxSizer_01 = wx.StaticBoxSizer(box_01, wx.VERTICAL)
        # first the static box
        box_10 = wx.StaticBox(self, -1, 'Option')
        # then the sizer
        staticBoxSizer_11 = wx.StaticBoxSizer(box_10, wx.VERTICAL)
#         sizer.AddGrowableCol(0)
#         sizer.AddGrowableCol(1)
        vBox.Add(h1, 0, wx.EXPAND , 0)  
        vBox.Add(h2, 0, wx.EXPAND , 0)  
        vBox.Add(staticBoxSizer_00, 0, wx.EXPAND , 0)  
        vBox.Add(staticBoxSizer_01, 0, wx.EXPAND , 0)  
        vBox.Add(staticBoxSizer_11, 0, wx.EXPAND , 0)  
#         vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#         vBox.Add(self.tb, 0, wx.EXPAND)
#         vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)        
#---------------------------------------------------------------------------

      
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingFindAndReplaceFrame(None, 'Find / Replace')
    app.MainLoop()
