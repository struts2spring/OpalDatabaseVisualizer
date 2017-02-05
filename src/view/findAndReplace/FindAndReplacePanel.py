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
#---------------------------------------------------------------------------

      
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingFindAndReplaceFrame(None, 'Find / Replace')
    app.MainLoop()
