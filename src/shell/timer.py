class Timer(object):
    def __init__(self, start, sample_rate, length):
        super(Timer, self).__init__()
        self.entries = length
        self._start = start
        self._delta = 1.0 / sample_rate
        # self.current_time = start

    def __len__(self):
        return self.entries

    def __getitem__(self, index):
        try:
            if isinstance(index, slice):
                # index handling
                start_index = index.start
                stop_index = index.stop
                if (start_index is None) and (stop_index is None):
                    raise Exception('Not Implemented yet')
                elif (start_index is None) and isinstance(stop_index, int):
                    start_index = 0
                    # raise Exception('Not Implemented yet')
                elif (stop_index is None) and isinstance(start_index, int):
                    stop_index = self.entries
                    # raise Exception('Not Implemented yet')
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
                return [(start + (self._delta * step)) for step in steps]

            else:
                if (-self.entries - 1) >= index or index >= self.entries:
                    raise IndexError('invalid index')
                elif index >= 0:
                    return self._start + (index * self._delta)
                else:
                    end = self._start + (self._delta * self.entries)
                    return end + self._delta * (index)
        except Exception as e:
            return e

    def __repr__(self):
        return 'Timer Object with start:{}, delta:{}, entries:{}'.format(self._start, self._delta, self.entries)
        # obj = []
        # for i in range(0, self.entries):
        #     obj.append(self.__getitem__(i))
        # return obj

if __name__ == '__main__':
    time = Timer(1, 100, 100)
    print('time[0] = {}'.format(time[0]))
    print('time[1] = {}'.format(time[1]))
    print('time[99] = {}'.format(time[99]))
    print('time[-1] = {}'.format(time[-1]))
    print('time[0:2] = {}'.format(time[0:2]))
    print('time[:2] = {}'.format(time[:2]))
    print('time[98:] = {}'.format(time[98:]))
    print('time[-3:-1] = {}'.format(time[-3:-1]))
    print('time[-1:-3] = {}'.format(time[-1:-3]))
