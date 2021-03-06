import logging.config
import os
import tempfile

logger = logging.getLogger('extensive')


LOG_SETTINGS = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': os.path.join(tempfile.gettempdir(),'OpalDatabaseVisualizer.log'),
        'mode': 'a',
        'maxBytes': 10485760,
        'backupCount': 5,
    },

},
'formatters': {
    'detailed': {
        'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s',
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
print(os.path.join(tempfile.gettempdir()))