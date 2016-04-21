#!/usr/bin/env python
# -*-coding:utf-8-*-

import requests
import json
import libtorrent as lt
import os
from bcode import bdecode, bencode


def import2json(path):
    d = {}
    f = open(path, 'r')
    for line in f.readlines():
        line = line.strip()
        if line in d:
            d[line] += 1
        else:
            d[line] = 1
    return d


def downloadFromXunlei():
    baseUrl = 'http://bt.box.n0808.com/'
    path = os.getcwd()
    hashPath = path + '/test.txt'
    extName = '.torrent'
    sep = os.sep
    torrNum = 0
    for item in import2json(hashPath).keys():
        item = item.upper()
        r = requests.get(baseUrl +
                         item[:2] + sep +
                         item[-2:] + sep +
                         item + extName)
        if r.status_code == 200:
            with open((path + sep + item + extName), 'wb') as f:
                f.write(r.content)
            torrNum += 1
            print(torrNum)


def getInfo():
    path = os.getcwd()
    sep = os.sep
    torrentSet = [filename for filename in os.listdir(path) if filename.split('.')[-1] == 'torrent']
    for i in torrentSet:
        with open(path + sep + i, 'rb') as f:
            c = bdecode(str(f.read())[2:-1])
            print(c.keys())
            # print(str(f.read())[2:-1])
        break

if __name__ == '__main__':
    getInfo()
