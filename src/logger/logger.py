import logging
import logging.config

logName = 'current_running.log'

dictConfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(levelname)s %(module)s  %(lineno)d %(message)s",
        },
    },
    'handlers': {
        'debug': {
            'formatter': 'standard',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'normal': {
            'formatter': 'standard',
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': logName,
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'root': {
        'handlers': ['normal'],
        'level': logging.DEBUG,
        'propagate': True
    }
}


def loggerConfig(logName=None):
    if logName:
        dictConfig['handlers']['normal']['filename'] = logName

    logging.config.dictConfig(dictConfig)
