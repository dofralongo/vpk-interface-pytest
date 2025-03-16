#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2022/5/10 18:54
# @File    :
# @describe:
"""

import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host


if __name__ == '__main__':
    l_host = get_host_ip()
    print(l_host)