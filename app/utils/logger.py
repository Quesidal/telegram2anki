import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s->%(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'providers': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'controllers': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'use_cases': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}
logging.config.dictConfig(LOGGING_CONFIG)
