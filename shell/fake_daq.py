import numpy as np
import constants as CON
import random
import os

data = np.zeros(CON.buf_size_, dtype=np.float64)
time = np.zeros(CON.buf_size_, dtype=np.float64)


def buffer_resize(data_size, _dtype=np.float64, maintain=False):
    global data, time
    if maintain:
        buff_size = len(data)
        if buff_size > data_size:
            data = np.concatenate([data, np.zeros(data_size-buff_size)], _dtype=data.dtype)
            time = np.concatenate([time, np.zeros(data_size-buff_size)], _dtype=time.dtype)
        else:
            data = data[0:data_size]
            time = time[0:data_size]
    else:
        data = np.zeros(data_size, _dtype)
        time = np.zeros(data_size, _dtype)


def fin_read(samples=CON.samples_, sample_rate=CON.sample_rate_,
             min=CON.min_, max=CON.max_, expand=False, *args, **kwargs):
    global data, time  # -- may be needed?
    time_step = 1.0 / sample_rate
    if samples > len(data):
        if not expand:
            samples = len(data)
        else:
            data = np.zeros(samples, dtype=np.float64)
    for i in range(0, samples):
        data[i] = random.randint(1, 12)
    for i in range(1, samples):
        time[i] = time[i-1] + time_step
    print("Acquired {} points".format(samples))
    print('Time taken: {} seconds'.format(time[samples - 1]))


def con_read(sample_rate=CON.sample_rate_, min=CON.min_, max=CON.max_, *args, **kwargs):
    print("Acquired {} points".format(sample_rate))


def view(entries: int, tail: bool, *args, **kwargs):
    if tail:
        print(data[-int(entries):])
    else:
        print(data[0:int(entries)])


def save(path, filename, extension):
    key = data.dtype.name
    delim_dict = {'.txt': ' ',
                  '.mat': ' ',
                  '.csv': ',',
                  '.gz' : ' '
                  }
    fmt_dict = {'float64': '%.18e',
                'float32': '%.9e',
                'float': '%.9e',
                # 'int32'  : '',
                # 'int64'  : '',
                # 'int': '',
                }
    np.savetxt(os.path.join(path, filename) + extension, data,
               delimiter=delim_dict[extension], fmt=fmt_dict.get(key, '%.18e'))
