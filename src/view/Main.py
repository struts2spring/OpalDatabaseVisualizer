'''
Created on 11-Dec-2016

@author: vijay
'''
import wx
import tempfile
import os
print(wx.version())
from src.view.MainFrame import DatabaseMainFrame


import logging

if __name__ == "__main__":
    print(tempfile.gettempdir())
#     logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)-8s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=os.path.join(tempfile.gettempdir(),'OpalDatabaseVisualizer.log'),
#                     filemode='w')

#     logger = logging.getLogger('extensive')
#     logger.info("This is from Runner ")

    app = wx.App()
    
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()
