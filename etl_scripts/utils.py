import logging , os

def get_logger(name: str, log_file: str = "logs/etl_logs.log", level=logging.INFO,console=False):
    # create a directory folder inside which u will store ur logs
    # manually creation of directory is not recommended in production
    # with the help of makedirs , our code is becoming robust
    os.makedirs(os.path.dirname(log_file),exist_ok=True)
    # created a logger instance with name ETL_logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Avoid adding multiple duplicate handlers 
    # (LOGGERS ARE CACHED INTERNALLY )
    # we are not creating logger each time , we just addressing the one that's 
    # already created
    if not logger.handlers:
        #File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file__formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file__formatter)
        logger.addHandler(file_handler)

        # Console handler
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_formatter = logging.Formatter("%(levelname)s: %(message)s")
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

    return logger




