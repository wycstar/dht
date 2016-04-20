#!/usr/bin/env python
# -*-coding:utf-8-*-

import requests
import json
import libtorrent as lt
import os


def import2json(path):
    d = {}
    f = open(path, 'r')
    for line in f.readlines():
        line = line.strip()
        if line in d:
            d[line] += 1
        else:
            d[line] = 1
    # for k, v in d.items():
    #    print("%s %d" % (k, v))
        # print(k v)
    return d

if __name__ == '__main__':
    # print(os.getcwd() + '/test.txt')
    # import2json(os.getcwd() + '/test.txt')
    headers = {'content-type': 'multipart/form-data'}
    payload = {
        'auth': 'D5015A95E57B0183B10450210EA27E57',
        'ac': 'download',
        'hash': 'F4583D23C62DE4DDF75739DE2135589F7BBBF187'}
    r = requests.post("http://www.torrent.org.cn/api.php",
                      files=dict(auth='D5015A95E57B0183B10450210EA27E57',
                                 ac='download',
                                 hash='F4583D23C62DE4DDF75739DE2135589F7BBBF187'))
    print(r.text)
