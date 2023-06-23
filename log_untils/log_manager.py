#! python3
# _*_ coding: utf-8 _*_
# @Time : 2023/6/24 0:26 
# @Author : Jovan
# @File : log_manager.py
# @desc :
import os
import sys
import loguru


class LogManager:
    def __init__(self, log_name=None, level="INFO", rotation="100 MB", retention="30 days", compression="zip"):
        '''
        :param log_name:日志的名字
        :param level: 日志的等级
        :param rotation: 每个日志文件的大小
        :param retention: 保存的天数
        :param compression: 文件格式
        '''
        self.logger = loguru.logger
        self.logger.remove()
        self.colorize_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{file}</cyan> |" \
                               " <cyan>{process}:{thread}</cyan> | <cyan>{function}:{line}</cyan> | <cyan>{message}</cyan>"
        self.foramt = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} " \
                      "| {process}:{thread} | {function}:{line} | {message}"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        os.makedirs(os.path.join(parent_dir, 'logs'), exist_ok=True)
        log_file = os.path.join(parent_dir, 'logs', log_name if log_name else 'app.log')
        # backtrace, trace 用于错误查找,可开启
        if log_name:
            self.logger.add(
                log_file,
                level=level,
                format=self.foramt,
                rotation=rotation,
                retention=retention,
                compression=compression,
                colorize=True,
                backtrace=False,
                diagnose=False,
                encoding='utf-8'
            )
        self.logger.add(sys.stdout, level=level, colorize=True, format=self.colorize_format)

    def get_logger(self):
        return self.logger


def main():
    log_manager = LogManager(log_name='log.txt', level='DEBUG')
    logger = log_manager.get_logger()
    logger.info(f"asadasds")


if __name__ == '__main__':
    main()
