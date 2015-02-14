# coding=utf-8

"""
This file contains TODO: Describe File
"""
from math import log

__author__ = 'Matt Eland'

def format_size(num):
    """Human friendly file size
    :type num: int
    :param num: The size in bytes
    """
    if num > 1:
        unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024 ** exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % num_decimals
        return format_string.format(quotient, unit)

    if num == 0:
        return '0 bytes'

    if num == 1:
        return '1 byte'