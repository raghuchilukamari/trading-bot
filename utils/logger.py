import logging

def get_logger():
# Configure the logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    return logger
