import logging, colorlog

FORMAT = "% (log_color)s%(levelname)s%(reset)s - %(name)s - %(message)s".replace(" ", "")

_handler = colorlog.StreamHandler()
_handler.setFormatter(colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s%(reset)s | %(asctime)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.addHandler(_handler)
        logger.propagate = False
    return logger
