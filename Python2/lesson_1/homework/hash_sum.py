#!/bin/env python3

import magic
import hashlib
import os

path_to_file1 = os.path.join('files', 'file1', 'parts.md5')
path_to_file2 = os.path.join('files', 'file2', 'parts.md5')
path1 = os.path.join('files', 'file1')
path2 = os.path.join('files', 'file2')

with open(path_to_file1, 'r', encoding='UTF-8') as f:
    data = f.read()

h = hashlib.md5()
hash_list = []
for file in os.listdir(path1):
    h.update(os.path.join(path1, file).encode('koi8-r'))
    hash_list.append(h.hexdigest())

res_file = os.path.join(path1, 'res_file')
with open(res_file, 'w', encoding='UTF-8') as f:
    for line in data.split('\n')[:-1]:
        if line in hash_list:
            ord_file = os.listdir(path1)[hash_list.index(line)]
            f2 = open(ord_file)
            f.write(f2.read())
            f2.close()

# for file in os.listdir(os.path.join('files', 'file1')):
#     h.update(os.path.join('files', 'file1', file).encode('koi8-r'))
#
#



