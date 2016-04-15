#!/usr/bin/python python
# -*- coding: utf-8 -*-

import struct
import socket
import hmac
import hashlib
import random

__node_id_bits__ = 160
__trans_id_bits__ = 32


def random_string(len):
    seed = 'abcdef123456789'
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


def decode_nodes(nodes):
    nrnodes = len(nodes) / 26
    nodes = struct.unpack("!" + "20sIH" * nrnodes, nodes)
    for i in range(nrnodes):
        node_id, ip, port = nodes[i * 3], numToDottedQuad(nodes[i * 3 + 1]), nodes[i * 3 + 2]
        yield node_id, ip, port


def encode_nodes(nodes):
    n = []
    for node in nodes:
        n.extend([node[0], dottedQuadToNum(node[1].host), node[1].port])
    return struct.pack("!" + "20sIH" * len(nodes), *n)


def pack_host(host):
    try:
        addr = socket.inet_pton(socket.AF_INET, host)
    except (ValueError, socket.error):
        addr = socket.inet_pton(socket.AF_INET6, host)
    return addr


def pack_port(port):
    return chr(port >> 8) + chr(port % 256)


def unpack_host(host):
    if len(host) == 4:
        return socket.inet_ntop(socket.AF_INET, host)
    elif len(host) == 16:
        return socket.inet_ntop(socket.AF_INET6, host)


def unpack_port(port):
    return (ord(port[0]) << 8) + ord(port[1])


def unpack_hostport(addr):
    if len(addr) == 6:
        host = addr[:4]
        port = addr[4:6]
    if len(addr) == 18:
        host = addr[:16]
        port = addr[16:18]
    return (unpack_host(host), unpack_port(port))


def pack_hostport(host, port):
    host = pack_host(host)
    port = pack_port(port)
    return host + port


def get_version():
    return "BT\x00\x01"


def create_token(key, info_hash, node_id):
    return hmac.new(key, info_hash+node_id, hashlib.sha1).digest()

if __name__ == '__main__':
    print(random_node_id())
