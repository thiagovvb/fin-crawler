import logging
import sys

class Logger:
    @staticmethod
    def get_logger(name=__name__):
        
        logger = logging.getLogger(name)
        if not logger.handlers:
            formatter = logging.Formatter(
                '[%(levelname)s] - %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.setLevel(logging.DEBUG)
        return logger
