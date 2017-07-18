#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
daq_utils.py
Author: Danyal Ahsanullah
Date: 4/24/2017
License: N/A
Description: basic utility functions for DAQ modules
"""
import os
import numpy as np
from utils import constants as con
from utils.timer import Timer

data = np.zeros(0)
time = Timer.get_timer('list', 0, con.sample_rate_, 0)
con.chunk_ = 1000


def buffer_resize(data_size, _dtype=np.float64, maintain=False):
    global data, time
    time.entries = data_size
    if maintain:
        buff_size = len(data)
        if buff_size > data_size:
            data = np.concatenate([data, np.zeros(data_size-buff_size, dtype=data.dtype)])
        else:
            data = data[0:data_size-1]
    else:
        data = np.zeros(data_size, _dtype)


def process_running(run_event):
    import sys
    import time
    from collections import deque
    i = 0
    while run_event.is_set():
        spinner_str = '/-\|'
        spinner = deque(spinner_str, maxlen=len(spinner_str))
        sys.stdout.write('\r'+spinner[i])
        sys.stdout.flush()
        i = (i+1) if i < len(spinner_str) - 1 else 0
        time.sleep(0.3)


def kb_int(run_event):
    x = []
    while run_event.is_set():
        temp = input('press any key to terminate\n')
        if temp is not None:
            x.append(temp)
            run_event.clear()
            break


def view(entries: int, tail: bool, *args, **kwargs):
    if tail:
        vals = data[-int(entries):]
    else:        vals = data[0:int(entries)]
    return vals


def get_path(file=None):
    path = os.path.join(os.getcwd(), 'OUTPUT')
    if not os.path.isdir(path):
        os.mkdir('OUTPUT')
    if file:
        path = os.path.join(path, file)
    return path


def save(file_name, path=None, delim=None, *args, **kwargs):
    if not path:
        path = get_path()
    filename, extension = file_name.split('.')
    key = data.dtype.name
    delim_dict = {'txt': ' ',
                  'mat': ' ',
                  'csv': ',',
                  'gz': ' '
                  }
    fmt_dict = {'float64': '%.14f',
                'float32': '%.9f',
                'float': '%.9f',
                # 'int32'  : '%d',
                # 'int64'  : '%d',
                # 'int': '%d',
                }
    if not delim:
        delim = delim_dict[extension]
    #  TODO: Data blocking for multiple smaller files
    np.savetxt(os.path.join(path, filename) + '.' + extension, data,
               delimiter=delim, newline=os.linesep, fmt=fmt_dict.get(key, '%.14f'))
    time.savetxt(os.path.join(path, filename) + '_t.' + extension)


def quit_save(q, file, s, *args, **kwargs):
    if not (q or file):
        choice = input('save contents of session to file? (y/n):')
        if choice.lower == 'y':
            save(s + '.txt')
    if file:
        save(file)
