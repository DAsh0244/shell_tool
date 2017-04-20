# import numpy as np
# import constants as con
# import os
# from timer import Timer
import random
from daq_utils import *
FAKE = True


def fin_read(samples, sample_rate=con.sample_rate_, min=con.min_, max=con.max_, expand=True, *args, **kwargs):
    # global data, time  # -- may be needed?
    # buffer_resize(samples)
    buf_size = len(data)
    if samples > buf_size:
        if not expand:
            samples = buf_size
            # print('truncated')
        else:
            buffer_resize(samples)
            # print('extended')
    for i in range(buf_size-1, len(data)-1):
        data[i] = random.randint(1, 12)
    time = Timer(0, sample_rate, samples)
    print("Acquired {} points".format(samples))
    print('Time taken: {} seconds'.format(time[-1]))


def con_read(sample_rate=con.sample_rate_, min=con.min_, max=con.max_, file_name=None, *args, **kwargs):
    """
    
    :param sample_rate: 
    :param min: 
    :param max: 
    :param file_name: 
    :param args: 
    :param kwargs: 
    :return: number of reads
    """
    import threading
    from collections import deque
    from datetime import datetime as dt
    file_name = '{}_OUTPUT.txt'.format(dt.now().strftime('%d-%b-%Y--%H-%M-%f'))
    print(file_name)
    run_event = threading.Event()
    run_event.set()
    it = threading.Thread(target=kb_int, args=(run_event,))
    pt = threading.Thread(target=process_running, args=(run_event,))
    print('reading...')
    it.start()
    pt.start()
    j = 0
    vals = deque()
    chunk = np.zeros(con.chunk_)
    filename, extension = file_name.split('.')
    with open(os.path.join(get_path(), file_name), 'a') as file:
        while run_event.is_set():
            reading = random.randint(1, 12)
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
    global time
    time = Timer(0, sample_rate, j)
    time.savetxt(os.path.join(get_path(), filename + '_t.' + extension))
    it.join()
    pt.join()
    global data
    data = np.array(vals)
    return j


if __name__ == '__main__':
    # print(len(data))
    print(con_read(file_name='test.txt') == len(data))
    # print(data)
