#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
"""
import logging


# 阿里云日志服务配置
# END_POINT = 'cn-zhangjiakou-intranet.log.aliyuncs.com'  # 内网入口
END_POINT = 'cn-zhangjiakou.log.aliyuncs.com'  # 公网入口
ACCESS_KEY_ID = 'LTAI9NCrpRyyu4r4'
ACCESS_KEY = 'cuCHRJhvrvJJ4Wt9QyLZ1RR2uxpEi6'
PROJECT = 'sixue-manage2.0'


class CustomLogger:
    """ 封装自定义日志记录器

    使用方式：

    logger = CustomLogger("request")  # request 是 setting.py 配置文件里的一个配置项
    logger.error("error message...")

    """

    def __init__(self, name):
        """ name: 指定一个logger配置名称 """
        self._name = name
        self._logger = logging.getLogger(name)

    def _proxy(self, level, message):
        """
        一系列日志记录封装, 可以额外处理其他操作：
        1. 本地记录日志
        2. 阿里云网络日志
        3. 系统故障发送邮件
        ...
        """
        logger_function = getattr(self._logger, level)  # 获取对应等级的日志记录器[info,debug,error,warning...]

        logger_function(message)  # 本地记录日志

    # 4个日志记录等级：debug[10] < info[20] < warning[30] < error[40]

    def info(self, message):
        return self._proxy("info", message)

    def debug(self, message):
        return self._proxy("debug", message)

    def error(self, message):
        return self._proxy("error", message)

    def warning(self, message):
        return self._proxy("warning", message)

