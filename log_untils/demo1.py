import sys
import loguru


class LogManager:
    def __init__(self, file_path=None, level="INFO", rotation="500 MB", retention="30 days", compression="zip"):
        """
        :param file_path: 日志文件路径，默认为 None，即不写入文件。
        :param level: 输出到控制台的最低级别，默认为 "INFO"。
        :param rotation: 日志文件轮换大小，默认为 "500 MB"。
        :param retention: 日志文件保留时间，默认为 "30 days"。
        :param compression: 日志文件压缩格式，默认为 "zip"，可选的值有："gz"、"bz2"、"xz"、"lzma"、"tar"、"tar.gz" 等。
        """
        self.logger = loguru.logger
        self.logger.remove()

        if file_path:
            self.logger.add(
                file_path,
                rotation=rotation,
                retention=retention,
                compression=compression,
                serialize=True
            )
        self.logger.add(sys.stdout, level=level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
