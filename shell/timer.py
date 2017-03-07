class Timer(object):
    def __init__(self, start, sample_rate, length):
        super(Timer, self).__init__()
        self.entries = length
        self._start = start
        self._time_step = 1.0/sample_rate
        self.current_time = start

    def __getitem__(self, index):
        try:
            if index >= 0:
                return self._start + (index * self._time_step)
            else:
                return (self.entries * self._time_step) - (self._time_step * (index + 1))
        except Exception as e:
            return e

    def __repr__(self):
        obj = []
        for i in range(0, self.entries):
            obj.append(self.__getitem__(i))
        return obj