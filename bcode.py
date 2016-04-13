#!/usr/bin/python python
# -*- coding: utf-8 -*-

tbcode = "d1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe"


def decode_int(x):
    pass


def decode_string(x):
    pass


def decode_dict(x):
    pass


def decode_list(x):
    pass

DECODE_FUNC = {
    "i": decode_int,
    "d": decode_dict,
    "l": decode_list,
    "1": decode_string,
    "2": decode_string,
    "3": decode_string,
    "4": decode_string,
    "5": decode_string,
    "6": decode_string,
    "7": decode_string,
    "8": decode_string,
    "9": decode_string
}


def decode(x):
    try:

