from logging import StreamHandler
import logging, sys

LOGGER = logging.Logger("delta.logger")
LOGGER.setLevel(logging.INFO)

stream_handler = StreamHandler(sys.stdout)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')
formatter = logging.Formatter(LOG_FORMAT)

stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)