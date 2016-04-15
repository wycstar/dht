#!/usr/bin/python python
# -*- coding: utf-8 -*-

import threading
import random


def strxor(str1, str2):
    if len(str1) > len(str2):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(str1[:len(str2)], str2)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(str1, str2[:len(str1)])])


class RoutingTable(object):
    def __init__(self):
        self.nodes = {}
        self.bad_nodes = {}
        self.lock = threading.Lock()

    def get_close_nodes(self, target, num=3):
        if len(self.nodes) == 0:
            raise RuntimeError("No nodes in routing table!")
        with self.lock:
            nodes = [(node_id, self.nodes[node_id]) for node_id in self.nodes]
        nodes.sort(key=lambda x: strxor(target, x[0]))
        return nodes[:num]

    def update_node(self, node_id, node):
        with self.lock:
            if node_id in self.bad_nodes:
                return
            if node_id not in self.nodes:
                self.nodes[node_id] = node
            self.nodes[node_id].update_access()

    def remove_node(self, node_id):
        with self.lock:
            if node_id in self.nodes:
                self.bad_nodes[node_id] = self.nodes[node_id]
                del self.nodes[node_id]

    def get_nodes(self):
        return self.nodes

    def count(self):
        return len(self.nodes)

    def bad_count(self):
        return len(self.bad_nodes)

    def node_by_trans(self, trans_id):
        with self.lock:
            for node_id in self.nodes:
                if trans_id in self.nodes[node_id].trans:
                    return self.nodes[node_id]
        return None

    def node_by_id(self, node_id):
        with self.lock:
            if node_id in self.nodes:
                return self.nodes[node_id]
        return None

    def sample(self, num):
        with self.lock:
            return random.sample(self.nodes.items(), num)

if __name__ == '__main__':
    r = RoutingTable()
    print(strxor('abcd', 'bnms'))
