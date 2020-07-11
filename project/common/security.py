#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
安全验证相关
"""
import bleach

content = 'an evil() example'


def check_xss(inputs: str) -> bool:
    """ 检测输入文本是否有 XSS 攻击可能
    message: 内容疑似有XSS攻击，请重新输入内容
    """
    return bleach.clean(inputs) != inputs


print(f"is xss? {check_xss(content)}")

if __name__ == "__main__":
    pass
