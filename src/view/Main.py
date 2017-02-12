'''
Created on 11-Dec-2016

@author: vijay
'''
import wx
print(wx.version())
from src.view.MainFrame import DatabaseMainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()