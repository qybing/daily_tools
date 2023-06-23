import os
from typing import Dict, Any
from loguru import logger as log


class LogManager:
    def __init__(self, config=None):
        """
        创建一个日志管理器，使用Loguru进行日志记录。

        Args:
            config: 日志配置， dict对象， 可选，默认为None。
                file_rotation: 日志文件自动切割的大小限制，可选，默认为'10 MB'。
                file_retention: 日志文件自动切割后，保留的天数，可选，默认为'7 days'。
                file_compression: 日志文件自动切割后，压缩算法，可选，默认为'zip'。
                log_path: 在磁盘上保存日志文件的文件夹，可选，默认为'./logs/'。
                log_level: 日志的输出级别，可选，默认为'DEBUG'。
                log_format: 日志的输出格式，可选，默认为'{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | {name: <15} | {line: >4} | {message}'。

        """
        if config is None:
            config = {}

        self._log_path = config.get("log_path", "./logs")
        os.makedirs(self._log_path, exist_ok=True)

        self._log_level = config.get("log_level", "DEBUG")
        self._log_format = config.get("log_format", "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | {name} | {function} | {line} | {message}")

        file_rotation = config.get("file_rotation", "10 MB")
        file_retention = config.get("file_retention", "7 days")
        file_compression = config.get("file_compression", "zip")

        log_format = "<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        handlers_list = [
            {"sink": os.path.join(self._log_path, "app.log"),
             "level": self._log_level,
             "rotation": file_rotation,
             "retention": file_retention,
             "compression": file_compression,
             "format": log_format}
        ]

        log.configure(handlers=handlers_list, level=self._log_level)

    def get_logger(self, logger_name: str, logger_config: Dict[str, Any]):
        """
        获取日志器。

        Args:
            logger_name: logger的名称，用于在日志传递过程中唯一标识此logger。
            logger_config: 这个logger应该使用的配置，dict对象，包括以下键值对。
                handlers: 可选，list对象，额外的handlers列表，比如 email_sender。
                filters: 可选，list对象，额外的filters列表，比如禁止特定的消息入日志记录。

        Returns:
            返回一个 LoguruLogger 对象。
        """
        handlers = logger_config.get("handlers", [])
        filters = logger_config.get("filters", [])

        logger = log.bind(name=logger_name)
        for handler in handlers:
            logger.add(**handler)

        for filter_dict in filters:
            logger.add_filter(filter_dict['filter'], **filter_dict.get('kwargs', {}))

        return logger

    @property
    def log_path(self):
        return self._log_path

    @property
    def log_level(self):
        return self._log_level

    @property
    def log_format(self):
        return self._log_format


if __name__ == '__main__':
    # 创建一个日志管理器
    log_config = {
        "file_rotation": "10 MB",
        "file_retention": "7 days",
        "file_compression": "zip",
        "log_path": "./logs",
        "log_level": "DEBUG",
        "log_format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | {name} | {function} | {line} | {message}"
    }
    log_mgr = LogManager(config=log_config)
    logger = log_mgr.get_logger("test_logger", logger_config={"handlers": [], "filters": []})
    # 记录一些日志
    logger.debug("Debug message")
    logger.info("Informational message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")