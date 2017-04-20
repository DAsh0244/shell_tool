import math


def _precision_and_scale(x):
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return magnitude, 0
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return magnitude + scale, scale


class Timer(object):

    def __init__(self, start, sample_rate, length, precision=None):
        """
        Custom timer object designed to genreate time vectors from specific characteristics
        as an alternative to using an array to store evenly sampled time-step values. 
        Sacrifices speed for memory footprint. for large time vectors, this may be useful
        
        This is slicable and indexable for both the positive and negative indicies 
        --may be turned into an iterable generator later.
        
        :param start: time offset to start time vector from. 
        :param sample_rate: samples rate to be used to generate teh even timesteps.
        :param length: number of entries to generate, used in checking 'index' errors for corresponding values.
        :param precision: <optional> digits of precision to specify for. If not given, timer will try to guess number.
                          If  value is lower than min calculated, will be overridden by minimum number calculated.
        """
        super(Timer, self).__init__()
        self.entries = length
        self._start = start
        self._delta = 1.0 / sample_rate
        required = _precision_and_scale(self._delta)[1]
        if precision is None:
            self._precision = required
        else:
            if precision < required:
                print('precision({}) is smaller than required. using precision {}'.format(precision, required))
                self._precision = required
            else:
                self._precision = precision

    def __len__(self):
        return self.entries

    def __getitem__(self, index):
        if isinstance(index, slice):
            start_index = index.start
            stop_index = index.stop
            if (start_index is None) and (stop_index is None):
                raise Exception('Not Implemented yet')
            elif (start_index is None) and isinstance(stop_index, int):
                start_index = 0
            elif (stop_index is None) and isinstance(start_index, int):
                stop_index = self.entries
            elif -self.entries >= start_index or start_index >= self.entries:
                raise IndexError('invalid starting index')
            elif -self.entries >= stop_index or stop_index >= self.entries:
                raise IndexError('invalid ending index')
            else:
                if start_index < 0:
                    start_index = self.entries + start_index
                elif start_index > self.entries:
                    start_index = self.entries
                if stop_index < 0:
                    stop_index = self.entries + stop_index
                elif stop_index > self.entries:
                    stop_index = self.entries
            steps = range(0, (stop_index - start_index))
            start = self._start + start_index * self._delta
            return [round(start + (self._delta * step), self._precision) for step in steps]
        else:
            if (-self.entries - 1) >= index or index >= self.entries:
                raise IndexError('invalid index')
            elif index >= 0:
                return round((self._start + (index * self._delta)), self._precision)
            else:
                end = self._start + (self._delta * self.entries)
                return round((end + self._delta * index), self._precision)

    def __repr__(self):
        return 'Timer Object with start:{}, delta:{}, entries:{}, precision:{}'.format(self._start, self._delta,
                                                                                       self.entries, self._precision)

    def savetxt(self, file_name):
        with open(file_name, 'a') as file:
            for entry in range(0, self.entries):
                file.write('{:.{width}f}{}'.format(self[entry], '\n', width=self._precision))


if __name__ == '__main__':
    time = Timer(0, 200, 100, precision=1)
    print(time)
    print('time[0] = {}'.format(time[0]))
    print('time[1] = {}'.format(time[1]))
    print('time[99] = {}'.format(time[99]))
    print('time[-1] = {}'.format(time[-1]))
    print('time[0:2] = {}'.format(time[0:2]))
    print('time[:2] = {}'.format(time[:2]))
    print('time[98:] = {}'.format(time[98:]))
    print('time[-3:-1] = {}'.format(time[-3:-1]))
    print('time[-1:-3] = {}'.format(time[-1:-3]))
    time.savetxt('../OUTPUT/test.txt')
