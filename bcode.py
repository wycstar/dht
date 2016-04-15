#!/usr/bin/python python
# -*- coding: utf-8 -*-


def decode_int(code, index):
    index += 1
    newIndex = code.index('e', index)
    n = int(code[index:newIndex])
    if code[index] == '-':
        if code[index + 1] == '0':
            raise ValueError
    elif code[index] == '0' and newIndex != index+1:
        raise ValueError
    return (n, newIndex+1)


def decode_string(code, index):
    colon = code.index(':', index)
    n = int(code[index:colon])
    if code[index] == '0' and colon != index+1:
        raise ValueError
    colon += 1
    return (code[colon:colon+n], colon+n)


def decode_list(code, index):
    result, index = [], index+1
    while code[index] != 'e':
        v, index = DECODE_FUNC[code[index]](code, index)
        result.append(v)
    return (result, index + 1)


def decode_dict(code, index):
    result, index = {}, index+1
    while code[index] != 'e':
        k, index = decode_string(code, index)
        result[k], index = DECODE_FUNC[code[index]](code, index)
    return (result, index + 1)

DECODE_FUNC = {
    "i": decode_int,
    "d": decode_dict,
    "l": decode_list,
    "0": decode_string,
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


def bdecode(code):
    result, index = DECODE_FUNC[code[0]](code, 0)
    return result


def wtypes(code):
    if isinstance(code, int) or isinstance(code, bool):
        return "i"
    elif isinstance(code, str):
        return "s"
    elif isinstance(code, tuple) or isinstance(code, list):
        return "l"
    elif isinstance(code, dict):
        return "d"


def encode_int(code, result):
    result.extend(('i', str(code), 'e'))


def encode_bool(code, result):
    if code:
        encode_int(1, result)
    else:
        encode_int(0, result)


def encode_string(code, result):
    result.extend((str(len(code)), ':', code))


def encode_list(code, result):
    result.append('l')
    for i in code:
        ENCODE_FUNC[wtypes(i)](i, result)
    result.append('e')


def encode_dict(code, result):
    result.append('d')
    ilist = code.items()
    ilist = sorted(ilist)
    for k, v in ilist:
        result.extend((str(len(k)), ':', k))
        ENCODE_FUNC[wtypes(v)](v, result)
    result.append('e')


ENCODE_FUNC = {
    "i": encode_int,
    "s": encode_string,
    "l": encode_list,
    "d": encode_dict
}


def bencode(code):
    lResult = []
    ENCODE_FUNC[wtypes(code)](code, lResult)
    return ''.join(lResult)

if __name__ == '__main__':
    code = {
        "a": "b",
        "c": ["d", 123],
        "f": {
            "a": "q"
        },
        "g": 456
    }
    print(bencode(code))
    print(bdecode('d1:a1:b1:cl1:di123ee1:fd1:a1:qe1:gi456ee'))
