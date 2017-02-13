import numpy as np
from PyDAQmx import *

from constants import *

data = np.zeros(BUFSIZE, dtype=np.float64)


def fin_read(sample_rate=sample_rate_, samples=samples_,min=min_,max=max_):
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,min,max,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",sample_rate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, 10.0, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


def con_read(sample_rate=sample_rate_, samples=samples_,min=min_,max=max_):
    analog_input = Task()
    read = int32()
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,min,max,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",sample_rate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,samples)
    analog_input.StartTask()
    analog_input.ReadAnalogF64(samples, 10.0, DAQmx_Val_GroupByChannel, data, len(data), byref(read), None)
    print("Acquired {} points".format(read.value))


def view(entries=10, tail=False):
    if not tail:
        print(data[0:entries])
    else:
        print(data[-entries])
