# import numpy as np
# import constants as con
# import os
# from timer import Timer
from PyDAQmx import *
from daq_utils import *
from math import ceil


def fin_read(samples, sample_rate=con.sample_rate_,
             min=con.min_, max=con.max_, expand=True, *args, **kwargs):
    # global data, time  # -- may be needed?
    # buffer_resize(samples)
    buf_size = len(data)
    if samples > buf_size:
        if not expand:
            samples = buf_size
            print('Warning: data buffer truncated')
        else:
            buffer_resize(samples)
            # print('extended')
    timeout = ceil(samples * (1.0/sample_rate))
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0", "", DAQmx_Val_Cfg_Default, min, max, DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("", sample_rate, DAQmx_Val_Rising,DAQmx_Val_FiniteSamps, samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, timeout, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


def con_read(sample_rate=con.sample_rate_, min=con.min_, max=con.max_, file_name='OUTPUT.txt', *args, **kwargs):
    import threading
    from collections import deque
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
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0", "", DAQmx_Val_Cfg_Default, min, max, DAQmx_Val_Volts, None)
    analog_input.CfgSampClkTiming("", sample_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, samples)
    analog_input.StartTask()
    timeout = ceil(con.chunk_ * (1.0/sample_rate))
    with open(os.path.join(get_path(), file_name), 'a') as file:
        while run_event.is_set():
            analog_input.ReadAnalogF64(con.chunk_, timeout, DAQmx_Val_GroupByChannel,
                                       chunk, con.chunk_, byref(read), None)
            [file.write('{}{}'.format(val, '\n')) for val in chunk]
            chunk = np.zeros(con.chunk_)
            j += con.chunk_
        print("Acquired {} points".format(j))
        global time
        time = Timer(0, sample_rate, j*con.chunk_)
        time.savetxt(os.path.join(get_path(), filename + '_t.' + extension))
        it.join()
        pt.join()
    return j


if __name__ == '__main__':
    # print(len(data))
    print(con_read(file_name='test.txt') == len(data))
    # print(data)
