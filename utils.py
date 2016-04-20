#!/usr/bin/python python
# -*- coding: utf-8 -*-

import struct
import socket
import hmac
import hashlib
import random
import binascii
import codecs

__node_id_bits__ = 160
__trans_id_bits__ = 32


def random_string(len):
    seed = 'abcdef0123456789'
    return ''.join([random.choice(seed) for i in range(len)])


def random_node_id():
    return random_string(20)


def random_trans_id():
    return random_string(20)


def dottedQuadToNum(ip):
    hexn = ''.join(["%02X" % int(i) for i in ip.split('.')])
    return int(hexn, 16)


def numToDottedQuad(n):
    d = 256 * 256 * 256
    q = []
    x = 0
    while x < 4:
        m, n = divmod(n, d)
        q.append(str(int(m)))
        d /= 256
        x += 1
    return '.'.join(q)


def strxor(str1, str2):
    if len(str1) > len(str2):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(str1[:len(str2)], str2)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(str1, str2[:len(str1)])])

if __name__ == '__main__':
    print(random_node_id())
    a = random_node_id()
    b = random_node_id()
    print(a)
    print(b)
    print()
