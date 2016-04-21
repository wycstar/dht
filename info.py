#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from time import localtime, strftime
from base64 import b64encode
from bencode import bdecode


def getInfo():
    torrNum = 0
    path = os.getcwd()
    sep = os.sep
    torrentSet = [filename for filename in os.listdir(path) if filename.split('.')[-1] == 'torrent']
    for i in torrentSet:
        torrNum += 1
        with open(path + sep + i, 'rb') as f:
            d = {}
            c = bdecode(f.read())
            try:
                d['creation_date'] = strftime('%Y-%m-%d', localtime(c['creation date']))
                if 'files' not in c['info']:
                    d['type'] = 'single'
                    d['file_num'] = 1
                    d['file_name'] = c['info']['name']
                    d['file_size'] = c['info']['length']
                    d['size'] = c['info']['length']
                else:
                    d['type'] = 'multi'
                    d['file_num'] = len(c['info']['files'])
                    d['file_info'] = [dict(file_size=x['length'],
                                           file_name=sum(x['path'])) for x in c['info']['files']]
                    d['size'] = sum([x['file_size'] for x in d['file_info']])
                d['name'] = c['info']['name']
                d['magnet'] = 'magnet:?xt=urn:btih:' + i.split('.')[0].lower()
                d['thunder'] = 'thunder://' + b64encode('AA' + d['magnet'] + 'ZZ')
            except KeyError:
                print('$$$$$$$$$$$$$$$$$$$$$$$$$')
                print(i)
                continue
            if d['type'] == 'single':
                print('TName: %s' % d['name'])
                print('FName: %s' % d['file_name'])
                print(' Date: %s' % d['creation_date'])
                print(' Size: %d' % d['file_size'])
                print('  Num: %d' % d['file_num'])
                print('MLink: %s' % d['magnet'])
                print('TLink: %s' % d['thunder'])
            else:
                print('TName: %s' % d['name'])
                print(' Date: %s' % d['creation_date'])
                print(' Size: %d' % d['size'])
                print('  Num: %d' % d['file_num'])
                for i in d['file_info']:
                    print('    %s    %d' % (i['file_name'][:10], i['file_size']))
                print('MLink: %s' % d['magnet'])
                print('TLink: %s' % d['thunder'])
            print('-------------------------')
    print(torrNum)

if __name__ == '__main__':
    getInfo()
    '''
    path = os.getcwd()
    sep = os.sep
    file = '361C3B67F562F2E7F4D10EA22022D26BEDA88286.torrent'
    with open(path + sep + file, 'rb') as f:
        d = {}
        c = bdecode(f.read())
        for i in c['info']['files']:
            print i
    '''
