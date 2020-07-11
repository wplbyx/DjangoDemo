#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
"""
import time
from datetime import datetime

# 基础配置项
BITS_CENTER = 5  # 数据中心 占位长度
BITS_WORKER = 5  # 工作机器 占位长度
BITS_TIMESTAMP = 39  # 时间位 占位长度
BITS_SEQUENCES = 14  # 序列位 占用长度
BITS_WORKER_ID = BITS_CENTER + BITS_WORKER  # 机器位 占位长度

# 相关掩码
MASK_CENTER = (-1 << BITS_CENTER) ^ -1        # 计算数据中心掩码
MASK_WORKER = (-1 << BITS_WORKER) ^ -1        # 计算工作机器掩码
MASK_SEQUENCE = (-1 << BITS_SEQUENCES) ^ -1   # 计算序列号掩码
MASK_TIMESTAMP = (-1 << BITS_TIMESTAMP) ^ -1  # 时间戳掩码，从高位开始获取

# 元时间戳 `2020-01-01 00:00:01+00` (10毫秒刻度，12位长度，可以使用174年)
EPOCH_TIMESTAMP = 157780800100


class MySnowFlake:
    """ MySonyflake 分布式 uid 生成算法, 原生Snowflake的改进：
    +------+--------------+-------------+------------+
    | sign |  timestamps  |  worker id  |  sequence  |
    +------+--------------+-------------+------------+
      1bit      39bits        10bits        14bits

    timestamps:  时间位，39位精确到10毫秒，可用174年
    worker id:   机器位，最多支持2^10=1024个服务实例
    sequence:    序列位，支持同一秒，同一个服务，能生成的不同ID个数
    """

    def __init__(self, center, worker):
        """
        初始化服务实例对象
        :param center: 数据中心编号，总共32个
        :param worker: 每个数据中心的服务实例编号，一共32个
        """
        self.last_timestamp = EPOCH_TIMESTAMP  # 第一次启动设置元时间
        self.center = center  # 数据中心编号
        self.worker = worker  # 工作机器编号
        self.worker_id = ((self.center & MASK_CENTER) << BITS_CENTER) | (self.worker & MASK_WORKER)  # 计算工作机器id
        self.sequence = 0  # 当前序列号 递增
        self.sequence_max = (1 << BITS_SEQUENCES) - 1  # 计算最大序列号

    @property
    def status(self):
        """ 查看当前状态 """
        ts = (self.last_timestamp + EPOCH_TIMESTAMP) / 100
        return {
            "Data center": self.center,
            "Data worker": self.worker,
            "Last Datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)),
            "Last timestamp": self.last_timestamp,
            "Worker id": self.worker_id,
            "Sequence": self.sequence
        }

    @staticmethod
    def analysis(uid):
        """ 解析雪花ID """
        timestamp = ((-1 << BITS_TIMESTAMP) ^ -1) & (uid >> (BITS_WORKER_ID + BITS_SEQUENCES))
        worker_id = ((-1 << BITS_WORKER_ID) ^ -1) & (uid >> BITS_SEQUENCES)
        sequence = ((-1 << BITS_SEQUENCES) ^ -1) & uid
        center = MASK_CENTER & (worker_id >> BITS_WORKER)
        worker = MASK_WORKER & worker_id

        # time.mktime(25174413314916353)
        ts = (timestamp + EPOCH_TIMESTAMP) / 100  # 10毫秒级时间戳
        return {
            "Data center": center,
            "Data worker": worker,
            "Datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)),
            "Timestamp": timestamp,
            "Worker id": worker_id,
            "Sequence": sequence
        }

    def next_id(self):
        """ 生成雪花ID """
        current_timestamp = int(time.time() * 100)  # 10毫秒刻度

        # 时钟回拨，当前时钟回拨到元时间之前
        if current_timestamp < self.last_timestamp:
            raise Exception(f"Clock moved backwards! {current_timestamp} < {self.last_timestamp}")

        # 时钟自然递增，今入下一个时钟周期
        if current_timestamp > self.last_timestamp:
            self.sequence = 0
            self.last_timestamp = current_timestamp

        self.sequence += 1
        if self.sequence > self.sequence_max:
            delay = datetime.fromtimestamp(current_timestamp) - datetime.fromtimestamp(self.last_timestamp)
            time.sleep(delay.seconds)
            return self.next_id()

        # 0 | timestamps | worker_id | sequence
        return ((current_timestamp - EPOCH_TIMESTAMP) << (BITS_WORKER_ID + BITS_SEQUENCES)) | \
               (self.worker_id << BITS_SEQUENCES) | self.sequence


# 多次被导入时，会重复创建改实例吗？博客场景的应用 基本上不会出问题
snow_flake = MySnowFlake(2, 2)


def new_id():
    return snow_flake.next_id()


if __name__ == '__main__':
    """ Module test. """
    from pprint import pprint

    current_id = snow_flake.next_id()
    print(f"uid: {current_id}")

    pprint(snow_flake.status)
    print("=" * 20)
    time.sleep(1)
    pprint(MySnowFlake.analysis(current_id))  # test: 25174413314916353
