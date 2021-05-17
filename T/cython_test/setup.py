#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C)2017 SenseDeal AI, Inc. All Rights Reserved
#

"""
File: setup.py
Author: lzl
E-mail: zll@sensedeal.ai
Last modified: 2019/3/1
Description:
"""

from distutils.core import setup
from Cython.Build import cythonize
import os
import sys
import shutil
import platform


if os.path.exists('./xmpoc'):
    shutil.rmtree('./xmpoc')
if os.path.exists('./build'):
    shutil.rmtree('./build')
lib_path = platform.system().lower() + '-' + platform.machine() + '-' + str(sys.version_info.major) + '.' + str(sys.version_info.minor)
out_dir = './build/lib.' + lib_path + '/'

shutil.copytree('../clean_project/xmpoc', './xmpoc')


def all_path(dirname):
    result = []  # 所有的文件
    count = 0
    for maindir, subdir, file_name_list in os.walk(dirname):
        if count != 0:
            py_flag = False
            for filename in file_name_list:
                if filename.endswith('.py'):
                    py_flag = True
            if not os.path.exists(os.path.join(maindir, '__init__.py')) and py_flag:
                open(os.path.join(maindir, '__init__.py'), 'w').close()
            for filename in file_name_list:
                if filename.endswith('.py') and filename != 'setup.py' and filename != 'metrics.py' \
                        and '/config' not in maindir and '/configs' not in maindir:
                    apath = os.path.join(maindir, filename)
                    result.append(apath)
                else:
                    out_ = out_dir + maindir.replace('./xmpoc', '')
                    if not os.path.exists(out_):
                        os.makedirs(out_)
                    shutil.copy(maindir + '/' + filename, out_ + '/' + filename)
        count += 1
    return result[::-1]

try:
    setup(
        nthreads=16,
        ext_modules=cythonize(all_path('.'))
    )
except:
    print('出错了')

# for name in all_path('.'):
#     # if '__init__.py' not in name:
#     if os.path.exists(name.replace('.py', '.c')):
#         os.remove(name.replace('.py', '.c'))
#         # os.remove(name)

# shutil.rmtree('build')

shutil.rmtree('./xmpoc/')
shutil.move(out_dir, './xmpoc')
shutil.rmtree('./build/')
shutil.copy('../clean_project/xmpoc/src/run.py', './xmpoc/src/run.py')
shutil.copy('../clean_project/xmpoc/src/PaddleOCR/OCRModel.py', './xmpoc/src/PaddleOCR/OCRModel.py')
