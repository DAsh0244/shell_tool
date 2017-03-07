import numpy as np
import constants as CON
import random
import os
from timer import Timer

data = np.zeros(0)
# data = np.zeros(CON.buf_size_, dtype=np.float64)
# time = np.zeros(CON.buf_size_, dtype=np.float64)
# time = CON.Time(length=len(data), time_step=1.0/CON.sample_rate_, initial=0.0)
time = Timer(0, CON.sample_rate_, 0)
'''
for index[i]  time[i] = time[0] + i*time_step
'''


def buffer_resize(data_size, _dtype=np.float64, maintain=False):
    global data, time
    if maintain:
        buff_size = len(data)
        if buff_size > data_size:
            data = np.concatenate([data, np.zeros(data_size-buff_size, dtype=data.dtype)])
            time = np.concatenate([time, np.zeros(data_size-buff_size, dtype=time.dtype)])
        else:
            data = data[0:data_size]
            time = time[0:data_size]
    else:
        data = np.zeros(data_size, _dtype)
        time = np.zeros(data_size, _dtype)


def fin_read(samples, sample_rate=CON.sample_rate_,
             min=CON.min_, max=CON.max_, expand=True, *args, **kwargs):
    global data, time  # -- may be needed?
    # buffer_resize(samples)
    buf_size = len(data)
    if samples > buf_size:
        if not expand:
            samples = buf_size
            print('truncated')
        else:
            buffer_resize(samples)
            print('extended')
    for i in range(buf_size-1, len(data)-1):
        data[i] = random.randint(1, 12)
    time = Timer(0, sample_rate, samples)
    # for i in range(1, samples):
    #     time[i] = time[i-1] + time_step
    print("Acquired {} points".format(samples))
    print('Time taken: {} seconds'.format(time[-1]))


def con_read(sample_rate=CON.sample_rate_, min=CON.min_, max=CON.max_, *args, **kwargs):
    print("Acquired {} points".format(sample_rate))


def view(entries: int, tail: bool, *args, **kwargs):
    if tail:
        print(data[-int(entries):])
    else:
        print(data[0:int(entries)])


def get_path():
    import os
    path = './'
    try:
        path = os.path.join(os.getcwd(), 'OUTPUT')
    except FileNotFoundError:
        os.mkdir('OUTPUT')
        path = os.path.join(os.getcwd(), 'OUTPUT')
    return path

def save(file_name, path=get_path(), *args, **kwargs):
    filename, extension = file_name.split('.')
    key = data.dtype.name
    delim_dict = {'txt': ' ',
                  'mat': ' ',
                  'csv': ',',
                  'gz' : ' '
                  }
    fmt_dict = {'float64': '%.18e',
                'float32': '%.9e',
                'float': '%.9e',
                # 'int32'  : '',
                # 'int64'  : '',
                # 'int': '',
                }
    np.savetxt(os.path.join(path, filename) + '.' + extension, data,
               delimiter=delim_dict[extension], fmt=fmt_dict.get(key, '%.18e'))
    np.savetxt(os.path.join(path, filename)+ '_t.' + extension, time,
               delimiter=delim_dict[extension], fmt=fmt_dict.get(key, '%.18e'))
