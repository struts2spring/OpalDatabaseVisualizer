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
import logging.config

LOG_SETTINGS = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'INFO',
        'formatter': 'detailed',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'INFO',
        'formatter': 'detailed',
        'filename': os.path.join(tempfile.gettempdir(),'OpalDatabaseVisualizer.log'),
        'mode': 'a',
        'maxBytes': 10485760,
        'backupCount': 5,
    },

},
'formatters': {
    'detailed': {
        'format': '%(asctime)s %(module)-17s line:%(lineno)-4d ' \
        '%(levelname)-8s %(message)s',
    },
    'email': {
        'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
        'Line: %(lineno)d\nMessage: %(message)s',
    },
},
'loggers': {
    'extensive': {
        'level':'DEBUG',
        'handlers': ['file', ]
        },
}
}
logging.config.dictConfig(LOG_SETTINGS)
if __name__ == "__main__":
#     print(tempfile.gettempdir())
#     logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)-8s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=os.path.join(tempfile.gettempdir(),'OpalDatabaseVisualizer.log'),
#                     filemode='w')

    logger = logging.getLogger('extensive')
    logger.info("This is from Runner ")

    app = wx.App()
    
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()
