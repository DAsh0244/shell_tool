class Timer(object):
    def __init__(self, start, sample_rate, length):
        super(Timer, self).__init__()
        self.entries = length
        self._start = start
        self._time_step = 1.0/sample_rate
        self.current_time = start

    def __getitem__(self, index):
        return self._start + (index * self._time_step)