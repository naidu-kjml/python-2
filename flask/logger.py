#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import os
import logging
import uuid
from logging import Handler, FileHandler, StreamHandler


class PathFileHandler(FileHandler):
    def __init__(self, path, filename, mode='a', encoding=None, delay=False):
        filename = os.fspath(filename)
        if not os.path.exists(path):
            os.mkdir(path)
        self.baseFilename = os.path.join(path, filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        if delay:
            Handler.__init__(self)
            self.stream = None
        else:
            StreamHandler.__init__(self, self._open())


class Loggers(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
        'error': logging.ERROR, 'critical': logging.CRITICAL
    }

    def __init__(self, filename='{uid}.log'.format(uid=uuid.uuid4()), level='info', log_dir='log',
                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', dir_par_or_abs='abs'):
        self.logger = logging.getLogger(filename)
        if dir_par_or_abs == 'abs':
            abspath = os.path.dirname(os.path.abspath(__file__))
        elif dir_par_or_abs == 'par':
            abspath = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
        self.directory = os.path.join(abspath, log_dir)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        stream_handler = logging.StreamHandler()  # 往屏幕上输出
        stream_handler.setFormatter(format_str)
        stream_handler.setLevel(logging.INFO)
        file_handler = PathFileHandler(path=self.directory, filename=filename, mode='a', encoding='utf-8')
        file_handler.setFormatter(format_str)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)


if __name__ == "__main__":
    txt = "aaa"
    log = Loggers(level='info')
    log.logger.info(4)
    log.logger.info(5)
    log.logger.debug(txt)