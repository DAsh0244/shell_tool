import numpy as np
# from constants import *
import constants as CON
import random
import os

data = np.zeros(CON.BUFSIZE, dtype=np.float64)


def fin_read(samples=CON.samples, sample_rate=CON.sample_rate, min=CON.min, max=CON.max, *args, **kwargs):
    for i in range(0, samples):
        data[i] = random.randint(0, 12)
    print("Acquired {} points".format(samples))


def con_read(sample_rate=CON.sample_rate, min=CON.min, max=CON.max, *args, **kwargs):
    print("Acquired {} points".format(sample_rate))


def view(entries, tail, *args, **kwargs):
    if not entries:
        entries = int(len(data)/3)
    if not tail:
        print(data[0:int(entries)])
    else:
        print(data[-int(entries)])


def save(path, filename, extension):

    delim_dict = {'.txt': ' ',
                  '.mat': ' ',
                  '.csv': ',',
                  '.gz' : ' '
                  }

    np.savetxt(os.path.join(path, filename) + extension, data, delimiter=delim_dict[extension])

