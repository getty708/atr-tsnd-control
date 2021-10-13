import logging

LOGGING_LEVEL_OBJ = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}

def setup_logger(name, logfile=None, log_level="DEBUG"):
    """ Returns logger object with custom setting.
    Args:
        name (str): name of logger.
        logfile (str, optional): (Default: None)
        log_level (str, optional): {DEBUG, INFO}
    Returns:
        logging.logger
    """
    assert type(log_level) == str or log_level is None
    log_level = LOGGING_LEVEL_OBJ[log_level]

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logfile is not None:
        # create file handler
        fh = logging.FileHandler(logfile, mode="w")
        fh.setLevel(log_level)
        fh_formatter = logging.Formatter(log_format)
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)  # add the handlers to the logger
    else:
        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch_formatter = logging.Formatter(log_format)
        ch.setFormatter(ch_formatter)

    return logger