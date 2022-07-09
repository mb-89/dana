import logging
import sys

from . import __metadata__

log = logging.getLogger(__metadata__.__projname__)


def getLogger():
    setupLogging()
    return log


def setupLogging():
    if not log.handlers:
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(relativeCreated)08d %(levelname)s: %(message)s"
        )
        log._fmt = formatter

        logging.addLevelName(logging.DEBUG, "DBG ")
        logging.addLevelName(logging.INFO, "INFO")
        logging.addLevelName(logging.WARNING, "WARN")
        logging.addLevelName(logging.ERROR, "ERR ")

        # add to console
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(log._fmt)
        log.addHandler(ch)
