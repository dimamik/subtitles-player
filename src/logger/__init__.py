import logging
import logging.config
from datetime import datetime

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


def logger_config(log_name=None):
    now = datetime.now()
    if log_name:
        dictConfig['handlers']['normal']['filename'] = log_name
    else:
        dictConfig['handlers']['normal']['filename'] = now.strftime('%Y-%m-%d') + ".log"

    logging.config.dictConfig(dictConfig)


if __name__ == '__main__':
    logger_config()
    logging.error("THIS IS LOG ERROR")
