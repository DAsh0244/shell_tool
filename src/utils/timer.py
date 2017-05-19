#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
timer.py
Author: Danyal Ahsanullah
Date: 4/20/2017
License: N/A
Description: Timer object used to provide a low memory overhead timer at the cost of computational time 
"""


def _precision_and_scale(x):
    """
    finds the number of digits precision to use for a number
    :param x: number to find its magnitude and precision
    :return: tuple of total min length needed to display number, and decimal digits of precision
    
    EX: _precision_and_scale(010.250) -> (4,2)
    """
    import math
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


class TimerBase(object):
    def __init__(self, start, sample_rate, length, precision=None):
        """
        :param start: time offset to start time vector from. 
        :param sample_rate: samples rate to be used to generate teh even timesteps.
        :param length: number of entries to generate, used in checking 'index' errors for corresponding values.
        :param precision: <optional> digits of precision to specify for. If not given, timer will try to guess number.
                          If  value is lower than min calculated, will be overridden by minimum number calculated.
        """
        self.entries = length
        self._start = start
        self._delta = 1.0 / sample_rate
        self.__type__ = 'base'
        required = _precision_and_scale(self._delta)[1]
        if precision is None:
            self._precision = required
        else:
            if precision < required:
                # print('precision ({}) is smaller than required. using precision {}'.format(precision, required))
                self._precision = required
            else:
                self._precision = precision

    def __len__(self):
        """ returns the length of the simulated time vector"""
        return self.entries

    def __str__(self):
        return 'Timer Object with start:{}, delta:{}, entries:{}, precision:{}'.format(self._start, self._delta,
                                                                                       self.entries, self._precision)

    def __repr__(self):
        return '"{}" object with dict: {}'.format(type(self).__name__, self.__dict__)

    # def __str__(self):
    #     return 'Timer Object with start:{}, delta:{}, entries:{}, precision:{}'.format(self._start, self._delta,
    #                                                                                    self.entries, self._precision)

    def set_length(self, length):
        self.entries = int(length)


class TimerList(TimerBase):
    """
    Custom timer object designed to generate time vectors from specific characteristics
    as an alternative to using an array to store evenly sampled time-step values. 
    Sacrifices speed for memory footprint. for large time vectors, this may be useful

    This is slice-able and index-able for both the positive and negative indices 
    --may be turned into an iterable generator later.    
    """
    def __init__(self, *args, **kwargs):
        super(TimerList, self).__init__(*args, **kwargs)
        self.__type__ = 'timer_list'

    def __getitem__(self, index):
        """
        used for normal index slicing and indexing 
        :param index: either an integer or slice object used to slice the values
        :return: list of values that are defined by :param index
        """
        if isinstance(index, slice):
            start_index = index.start
            stop_index = index.stop
            if index.step is None:
                index_step = 1
            else:
                index_step = index.step

            if (start_index is None) and (stop_index is None):
                steps = range(0, self.entries, index_step)
                return [round(self._start + (self._delta * step), self._precision) for step in steps]
            elif (start_index is None) and isinstance(stop_index, int):
                start_index = 0
            elif (stop_index is None) and isinstance(start_index, int):
                stop_index = self.entries
            elif -self.entries >= start_index or start_index >= self.entries:
                raise IndexError('invalid starting index, index must be within range of [{},{})'.format(-self.entries,
                                                                                                        self.entries-1))
            elif -self.entries >= stop_index or stop_index >= self.entries:
                raise IndexError('invalid ending index, index must be within range of [{},{})'.format(-self.entries,
                                                                                                      self.entries-1))
            else:
                if start_index < 0:
                    start_index = self.entries + start_index
                elif start_index > self.entries:
                    start_index = self.entries
                if stop_index < 0:
                    stop_index = self.entries + stop_index
                elif stop_index > self.entries:
                    stop_index = self.entries
            steps = range(0, (stop_index - start_index), index_step)
            start = self._start + start_index * self._delta
            return [round(start + (self._delta * step), self._precision) for step in steps]
        elif isinstance(index, int):
            if (-self.entries - 1) >= index or index >= self.entries:
                raise IndexError('Invalid index')
            elif index >= 0:
                return round((self._start + (index * self._delta)), self._precision)
            else:
                end = self._start + (self._delta * self.entries)
                return round((end + self._delta * index), self._precision)
        else:
            raise TypeError('list indices must be integers or slices, not {}'.format(type(index).__name__))

    def savetxt(self, file_name):
        """
        saves time vector as a text file for later use with data sets.
        :param file_name: 'path/to/desired/file/<filename>.<ext>'
        """
        with open(file_name, 'a') as file:
            for entry in range(0, self.entries):
                file.write('{:.{width}f}{}'.format(self[entry], '\n', width=self._precision))


class TimerGenerator(TimerBase):
    """
    Custom timer object designed to generate time vectors from specific characteristics
    as an alternative to using an array to store evenly sampled time-step values. 
    Sacrifices speed for memory footprint. for large time vectors, this may be useful

    This is slice-able and index-able for both the positive and negative indices 
    --may be turned into an iterable generator later.    
    """
    def __init__(self, *args, **kwargs):
        super(TimerGenerator, self).__init__(*args, **kwargs)
        self.__type__ = 'timer_generator'

    def __getitem__(self, index):
        """
        used for normal index slicing and indexing 
        :param index: either an integer or slice object used to slice the values
        :return: list of values that are defined by :param index
        """
        if isinstance(index, slice):
            start_index = index.start
            stop_index = index.stop
            if index.step is None:
                index_step = 1
            else:
                index_step = index.step

            if (start_index is None) and (stop_index is None):
                steps = range(0, self.entries, index_step)
                return (round(self._start + (self._delta * step), self._precision) for step in steps)
            elif (start_index is None) and isinstance(stop_index, int):
                start_index = 0
            elif (stop_index is None) and isinstance(start_index, int):
                stop_index = self.entries
            elif -self.entries >= start_index or start_index >= self.entries:
                raise IndexError('invalid starting index, index must be within range of [{},{})'.format(-self.entries,
                                                                                                        self.entries-1))
            elif -self.entries >= stop_index or stop_index >= self.entries:
                raise IndexError('invalid ending index, index must be within range of [{},{})'.format(-self.entries,
                                                                                                      self.entries-1))
            else:
                if start_index < 0:
                    start_index = self.entries + start_index
                elif start_index > self.entries:
                    start_index = self.entries
                if stop_index < 0:
                    stop_index = self.entries + stop_index
                elif stop_index > self.entries:
                    stop_index = self.entries
            steps = range(0, (stop_index - start_index), index_step)
            start = self._start + start_index * self._delta
            return (round(start + (self._delta * step), self._precision) for step in steps)
        elif isinstance(index, int):
            if (-self.entries - 1) >= index or index >= self.entries:
                raise IndexError('invalid index')
            elif index >= 0:
                return round((self._start + (index * self._delta)), self._precision)
            else:
                end = self._start + (self._delta * self.entries)
                return round((end + self._delta * index), self._precision)
        else:
            raise TypeError('list indices must be integers or slices, not {}'.format(type(index).__name__))

    def savetxt(self, file_name):
        """
        saves time vector as a text file for later use with data sets.
        :param file_name: 'path/to/desired/file/<filename>.<ext>'
        """
        with open(file_name, 'a') as file:
            # noinspection PyTypeChecker
            for entry in self[:]:
                file.write('{:.{width}f}{}'.format(entry, '\n', width=self._precision))


class Timer(object):
    """
    factory pattern for timer objects.    
    depending on boolean got value generator, will either return a TimerList or Timer Generator object.
    """
    @staticmethod
    def get_timer(timer_type='list', *args, **kwargs):
        if 'list' in timer_type.lower():
            return TimerList(*args, **kwargs)
        elif 'gen' in timer_type.lower():
            return TimerGenerator(*args, **kwargs)
        else:
            raise TypeError('"timer_type" argument must be either "list" or "gen"')


if __name__ == '__main__':
    """
    simplified testing setup
    """
    time1 = Timer.get_timer('list', 0, 200, 100, precision=1)
    time2 = Timer.get_timer('gen', 0, 200, int(1e7), precision=1)

    print(time1)
    print(repr(time1))

    # single integer indexing
    print('time1[0] = {}'.format(time1[0]))
    print('time1[1] = {}'.format(time1[1]))
    print('time1[99] = {}'.format(time1[99]))
    print('time1[-1] = {}'.format(time1[-1]))

    # positive slicing start/stop given
    print('time1[0:10] = {}'.format(time1[0:10]))

    # positive slicing start/stop/steps given
    print('time1[0:10:2] = {}'.format(time1[0:10:2]))

    # positive slicing with stop/step given
    print('time1[:10] = {}'.format(time1[:10]))
    print('time1[:10:2] = {}'.format(time1[:10:2]))

    # positive slicing with start/step given
    print('time1[90:] = {}'.format(time1[90:]))
    print('time1[90::2] = {}'.format(time1[90::2]))

    # none indexing & step indexing
    print('time1[:] = {}'.format(time1[:]))
    print('time1[::2] = {}'.format(time1[::2]))

    # negative indexing
    print('time1[-10:-1] = {}'.format(time1[-10:-1]))
    print('time1[-10:-1:2] = {}'.format(time1[-10:-1:2]))
    print('time1[-10:-1:-2] = {}'.format(time1[-10:-1:-2]))  # SHOULD return empty list
    print('time1[-1:-10] = {}'.format(time1[-1:-10]))  # SHOULD return empty list
    print('time1[-1:-10:2] = {}'.format(time1[-1:-10:2]))  # SHOULD return empty list

    time1.savetxt('../OUTPUT/test.txt')
    time2.savetxt('../OUTPUT/test2.txt')

    # for i in time2[:]:
    #     print(i)
