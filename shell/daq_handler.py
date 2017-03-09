import numpy as np
from PyDAQmx import *
import constants as CON
import os
from timer import Timer

# data = np.zeros(CON.buf_size_, dtype=np.float64)
data = np.zeros(0, dtype=np.float64)
time = Timer(0, CON.sample_rate_, CON.buf_size_)
# time = CON.Time(length=len(data), time_step=1.0/CON.sample_rate_, initial=0.0)
'''
for index[i]  time[i] = time[0] + i*time_step
'''
# time = np.zeros(CON.buf_size_, dtype=np.float64)


def buffer_resize(data_size, _dtype=np.float64, maintain=False, *args, **kwargs):
    global data, time
    if _dtype != data.dtype:
        data = data.astype(_dtype)
    if maintain:
        buff_size = len(data)
        if buff_size > data_size:
            data = np.concatenate([data, np.zeros(data_size-buff_size, dtype=data.dtype)])
            # time = np.concatenate([time, np.zeros(data_size-buff_size, dtype=time.dtype)])
        else:
            data = data[0:data_size]
            # time = time[0:data_size]
    else:
        data = np.zeros(data_size, _dtype)
        # time = np.zeros(data_size, _dtype)


def fin_read(sample_rate=CON.sample_rate_, samples=CON.samples_, min=CON.min_, max=CON.max_, expand=True, *args, **kwargs):
    from math import ceil
    timeout = ceil(samples * (1.0/sample_rate))
    buf_size = len(data)
    if samples > buf_size:
        if not expand:
            # samples = buf_size
            print('truncated')
        else:
            buffer_resize(samples)
            # print('extended')
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0", "", DAQmx_Val_Cfg_Default, min, max, DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("", sample_rate, DAQmx_Val_Rising,DAQmx_Val_FiniteSamps, samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, timeout, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


def con_read(sample_rate=CON.sample_rate_, samples=CON.samples_, min=CON.min_, max=CON.max_, *args, **kwargs):
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0", "", DAQmx_Val_Cfg_Default, min, max, DAQmx_Val_Volts, None)
    analog_input.CfgSampClkTiming("", sample_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, 10.0, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


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
    #  TODO: Data blocking for multiple smaller files
    np.savetxt(os.path.join(path, filename) + extension, data,
               delimiter=delim_dict[extension], fmt=fmt_dict.get(key, '%.18e'))
    with open(os.path.join(path, filename) + '_t.' + extension, 'w') as time_file:
        temp_time = time.initial
        for i in range(0, len(data)):
            time_file.write('{:.18e}'.format(temp_time))
            temp_time += time.time_step

