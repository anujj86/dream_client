import logging
import os
from config import config, project_name
from logging.handlers import RotatingFileHandler

config_name = os.environ.get("CONFIG_TYPE") or "default"
BASE_DIR = config.BASE_DIR

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def add_logger():
    log_filename = "emissions-backend.log"
    handler = RotatingFileHandler(
        os.path.join(BASE_DIR, "logs", log_filename), maxBytes=5000000, backupCount=2
    )
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s]: %(lineno)s:%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)
    logger.info("logging initialzed successfully")