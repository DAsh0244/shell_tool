import numpy as np
# from constants import *
import constants as CON
import random
import os

data = np.zeros(CON.BUFSIZE, dtype=np.float64)
time = np.zeros(len(data), dtype=np.)


def fin_read(samples=CON.samples, sample_rate=CON.sample_rate, min=CON.min, max=CON.max,expand=False, *args, **kwargs):
    if samples > len(data) and not expand:
        samples = len(data)
    for i in range(0, samples):
        data[i] = random.randint(1, 12)
    print("Acquired {} points".format(samples))


def con_read(sample_rate=CON.sample_rate, min=CON.min, max=CON.max, *args, **kwargs):
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

