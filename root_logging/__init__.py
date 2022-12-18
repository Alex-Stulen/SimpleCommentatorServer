MODULE_NAME = 'root_logging'

"""
import logging
from logging import handlers

# Initialized logger
LOGGER_ROOT = os.path.join(BASE_DIR, 'root_logging')

LOGGER_NAME = 'main'
LOGGER_FILE = LOGGER_NAME + '.log'

LOGGER_LOGS = os.path.join(LOGGER_ROOT, 'logs')

LOGGER_FILEPATH = os.path.join(LOGGER_LOGS, LOGGER_FILE)

if not os.path.exists(LOGGER_LOGS):
    os.mkdir(LOGGER_LOGS)

if not os.path.exists(LOGGER_FILEPATH):
    open(LOGGER_FILEPATH, 'a').close()

LOGGER_FILE_HANDLER = handlers.RotatingFileHandler(filename=LOGGER_FILEPATH, maxBytes=50 ** (1024 * 2), backupCount=10)
LOGGER = Logger(name=LOGGER_NAME, level=logging.DEBUG, handler=LOGGER_FILE_HANDLER)
"""
