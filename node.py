#!/usr/bin/python python
# -*- coding: utf-8 -*-

import threading
import time
from bcode import bencode
from utils import random_trans_id, get_version


class Node(object):
    def __init__(self, host, port, _id):
        self._id = _id
        self.host = host
        self.port = port
        self.trans = {}
        self.remote_tokens = {}
        self.local_tokens = {}
        self.lock = threading.Lock()
        self.access_time = time.time()

    def add_trans(self, name, info_hash=None):
        trans_id = random_trans_id()
        with self.lock:
            self.trans[trans_id] = {
                    "name": name,
                    "info_hash": info_hash,
                    "access_time": int(time.time())
            }
        return trans_id

    def delete_trans(self, trans_id):
        with self.lock:
            del self.trans[trans_id]

    def add_token(self, info_hash, token):
        with self.lock:
            self.remote_tokens[info_hash] = token

    def get_token(self, info_hash):
        return self.remote_tokens.get(info_hash, None)

    def delete_token(self, info_hash):
        with self.lock:
            del self.remote_tokens[info_hash]

    def add_local_token(self, info_hash, token):
        with self.lock:
            self.local_tokens[info_hash] = token

    def get_local_token(self, info_hash):
        return self.local_tokens.get(info_hash, None)

    def delete_local_token(self, info_hash):
        with self.lock:
            del self.local_tokens[info_hash]

    def update_access(self, unixtime=None):
        with self.lock:
            if unixtime:
                self.access_time = unixtime
            else:
                self.access_time = time.time()

    def _sendmessage(self, message, sock=None, trans_id=None, lock=None):
        message["v"] = get_version()
        if trans_id:
            message["t"] = trans_id
        encoded = bencode(message)
        if sock:
            if lock:
                with lock:
                    sock.sendto(encoded, (self.host, self.port))
            else:
                sock.sendto(encoded, (self.host, self.port))

    def send_protocol_error(self, msg, socket=None, trans_id=None, lock=None):
        message = {
            "y": "e",
            "e": [203, msg]}
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def ping(self, socket=None, sender_id=None, lock=None):
        trans_id = self.add_trans("ping")
        message = {
            "y": "q",
            "q": "ping",
            "a": {
                "id": sender_id
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def pong(self, socket=None, trans_id=None, sender_id=None, lock=None):
        message = {
            "y": "r",
            "r": {
                "id": sender_id
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def find_node(self, target_id, socket=None, sender_id=None, lock=None):
        trans_id = self.add_trans("find_node")
        message = {
            "y": "q",
            "q": "find_node",
            "a": {
                "id": sender_id,
                "target": target_id
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def found_node(self, found_nodes, socket=None, trans_id=None, sender_id=None, lock=None):
        message = {
            "y": "r",
            "r": {
                "id": sender_id,
                "nodes": found_nodes
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def get_peers(self, info_hash, socket=None, sender_id=None, lock=None):
        trans_id = self.add_trans("get_peers", info_hash)
        message = {
            "y": "q",
            "q": "get_peers",
            "a": {
                "id": sender_id,
                "info_hash": info_hash
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def got_peers(self, token, values, nodes, socket=None, trans_id=None, sender_id=None, lock=None):
        if len(values) == 0:
            message = {
                "y": "r",
                "r": {
                    "id": sender_id,
                    "token": token,
                    "nodes": nodes
                }
            }
        else:
            message = {
                "y": "r",
                "r": {
                    "id": sender_id,
                    "token": token,
                    "values": values
                }
            }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)

    def announce_peer(self, token, info_hash, socket=None, sender_id=None, lock=None):
        trans_id = self.add_trans("announce_peer", info_hash)
        message = {
            "y": "q",
            "q": "announce_peer",
            "a": {
                "id": sender_id,
                "info_hash": info_hash,
                "implied_port": 1,
                "port": self.port,
                "token": token
            }
        }
        self._sendmessage(message, socket, trans_id=trans_id, lock=lock)
