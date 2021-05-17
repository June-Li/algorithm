# from distutils.core import setup
# from Cython.Build import cythonize
#
# setup(ext_modules=cythonize(["main.py", "tools/print_my.py"]))
# # python setup_v1.py build_ext

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : setup_v1.py
# @Time    : 2018/12/04
# @Author  : spxcds (spxcds@gmail.com)

import os
import sys
import shutil
import numpy
import tempfile

from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

import platform


def get_root_path(root):
    if os.path.dirname(root) in ['', '.']:
        return os.path.basename(root)
    else:
        return get_root_path(os.path.dirname(root))


def copy_file(src, dest):
    if os.path.exists(dest):
        return

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copyfile(src, dest)


def touch_init_file():
    init_file_name = os.path.join(tempfile.mkdtemp(), '__init__.py')
    with open(init_file_name, 'w'):
        pass
    return init_file_name


init_file = touch_init_file()
print(init_file)


def compose_extensions(root='.'):
    for file_ in os.listdir(root):
        abs_file = os.path.join(root, file_)

        if os.path.isfile(abs_file):
            if abs_file.endswith('.py'):
                extensions.append(Extension(get_root_path(abs_file) + '.*', [abs_file]))
            elif abs_file.endswith('.c') or abs_file.endswith('.pyc'):
                continue
            else:
                copy_file(abs_file, os.path.join(build_root_dir, abs_file))
            if abs_file.endswith('__init__.py'):
                copy_file(init_file, os.path.join(build_root_dir, abs_file))

        else:
            if os.path.basename(abs_file) in ignore_folders:
                continue
            if os.path.basename(abs_file) in conf_folders:
                copy_file(abs_file, os.path.join(build_root_dir, abs_file))
            compose_extensions(abs_file)


if __name__ == '__main__':
    build_root_dir = 'build/lib.' + platform.system().lower() + '-' + platform.machine() + '-' + str(
        sys.version_info.major) + '.' + str(sys.version_info.minor)

    print(build_root_dir)

    extensions = []
    ignore_folders = ['build']  # , 'test', 'tests']
    conf_folders = ['conf']
    compose_extensions(os.path.abspath('.'))
    os.remove(init_file)

    setup(
        name='my_project',
        version='1.0',
        ext_modules=cythonize(
            extensions,
            nthreads=16,
            compiler_directives=dict(always_allow_keywords=True),
            include_path=[numpy.get_include()]),
        cmdclass=dict(build_ext=build_ext))
