#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
constants.py
Author: Danyal Ahsanullah
Date: 4/24/2017
License: N/A
Description: Fake simulated DAQ lib to simulate the api of a NI's DAQmx drivers
"""

import os
import random
import threading
import numpy as np
from collections import deque
from utils.timer import Timer
from utils import constants as con
from utils import daq_utils as dq
from datetime import datetime as dt

FAKE = True


def fin_read(samples, sample_rate=con.sample_rate_, min=con.min_, max=con.max_, expand=True, *args, **kwargs):
    # global data, time  # -- may be needed?
    buf_size = len(dq.data)
    if samples > buf_size:
        if not expand:
            samples = buf_size
            # print('truncated')
        else:
            dq.buffer_resize(samples)
            buf_size = samples
            # print('extended')
    for i in range(0, buf_size):
        dq.data[i] = random.uniform(1, 12)
    dq.time = Timer.get_timer('list', 0, sample_rate, samples)
    print('Acquired {} points'.format(samples))
    print('Time taken: {} seconds'.format(dq.time[-1]))
    # return 'Acquired {} points'.format(samples) + '\n' + 'Time taken: {} seconds'.format(dq.time[-1] + '\n')


def con_read(sample_rate=con.sample_rate_, min=con.min_, max=con.max_, file_name: str=None, *args, **kwargs):
    """
    
    :param sample_rate: 
    :param min: 
    :param max: 
    :param file_name: 
    :return: number of points read
    """
    if file_name is None:
        file_name = '{}_OUTPUT.txt'.format(dt.now().strftime('%d-%b-%Y--%H-%M-%f'))
    run_event = threading.Event()
    run_event.set()
    it = threading.Thread(target=dq.kb_int, args=(run_event,))
    pt = threading.Thread(target=dq.process_running, args=(run_event,))
    print('reading...')
    it.start()
    pt.start()
    j = 0
    vals = deque()
    chunk = np.zeros(con.chunk_)
    filename, extension = file_name.split('.')
    with open(os.path.join(dq.get_path(), file_name), 'a') as file:
        while run_event.is_set():
            reading = random.uniform(1, 12)
            vals.append(reading)
            index = j % con.chunk_
            chunk[index] = reading
            if index == 0 and j != 0:
                [file.write('{}{}'.format(val, '\n')) for val in chunk]
                chunk = np.zeros(con.chunk_)
            j += 1
        if j % con.chunk_ != 0:
            [file.write('{}\n'.format(val)) for val in chunk[:j % con.chunk_]]
    print("Acquired {} points".format(j))
    dq.time = Timer.get_timer('list', 0, sample_rate, j)
    dq.time.savetxt(os.path.join(dq.get_path(), filename + '_t.' + extension))
    it.join()
    pt.join()
    dq.data = np.array(vals)
    return j


if __name__ == '__main__':
    # print(len(data))
    print(con_read(file_name='test.txt') == len(dq.data))
    # print(data)
