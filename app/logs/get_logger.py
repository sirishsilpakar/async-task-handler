import configparser
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from requestvars import g

load_dotenv(".env")


class RequestIdLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        """Initializes a log record with an additional 'request_id' attribute representing the request ID"""
        super().__init__(*args, **kwargs)
        self.request_id = g().id if hasattr(g(), "id") else "NONE"


class RequestFormatter(logging.Formatter):
    def format(self, record):
        """Formats a log record by including the 'request_id' attribute

        Args:
            None

        Returns:
            str: A formatted log
        """
        record.request_id = getattr(
            record, "request_id", g().id if hasattr(g(), "id") else "NONE"
        )
        return super().format(record)


def setup_logging(config_file: str, deploy_env: str):
    """Module to setup a logger which stores the application logs into a file

    Args:
        config_file (str): Path of the ini config file for logger

    Returns:
        logging: A logging object
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    log_file_path_template = config.get("log_config", "log_file_path")
    current_datetime = datetime.now().strftime("%Y-%m-%d")
    log_file_path = log_file_path_template.format(datetime=current_datetime)

    log_level = "DEBUG" if deploy_env == "dev" else "INFO"
    log_format = config.get("log_config", "log_format")

    interval = int(config.get("time_rotation", "interval"))
    backup_count = int(config.get("time_rotation", "backup_count"))

    logger = logging.getLogger("app_logger")
    logger.setLevel(log_level)

    file_handler = TimedRotatingFileHandler(
        log_file_path, when="midnight", interval=interval, backupCount=backup_count
    )
    file_handler.setFormatter(RequestFormatter(log_format))
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RequestFormatter(log_format))
    logger.addHandler(stream_handler)

    return logger


logger = setup_logging(
    config_file=os.getenv("LOG_CONFIG"), deploy_env=os.getenv("DEPLOYMENT_ENV")
)
