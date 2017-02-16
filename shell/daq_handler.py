import numpy as np
from PyDAQmx import *
import constants as CON


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


def fin_read(sample_rate=CON.sample_rate_, samples=CON.samples_, min=CON.min_, max=CON.max_):
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,min,max,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",sample_rate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, 10.0, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


def con_read(sample_rate=CON.sample_rate_, samples=CON.samples_, min=CON.min_, max=CON.max_):
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,min,max,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",sample_rate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, 10.0, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


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
