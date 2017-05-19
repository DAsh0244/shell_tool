#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
test_timer.py
Author: Danyal Ahsanullah
Date: 4/15/2017
License: N/A
Description: Timer structure tests
"""
from unittest import TestCase

from timer import Timer

__version__ = '1.0.0'


class TestTimer(TestCase):
    def test_indexing(self):
        __name__ = 'test_indexing'
        sample_rate = 1000
        start = 0
        length = 10
        end = start + length/sample_rate
        time = Timer.get_timer('list', start, sample_rate, length)
        self.assertRaises(IndexError, time.__getitem__, length)
        self.assertRaises(IndexError, time.__getitem__, (-length - 1))
        for i in range(0, length):
            self.assertAlmostEqual(start + (i/sample_rate), time[i], places=7, msg='Unexpected Time value mismatch')
        for i in range(-length, 0, 1):
            self.assertAlmostEqual(end + (i / sample_rate), time[i], places=7, msg='Unexpected Time value mismatch')

    def test_positive_slicing(self):
        sample_rate = 1000
        start = 0
        length = 10
        end = start + length/sample_rate
        time = Timer.get_timer('list', start, sample_rate, length)
        stop = 3

        index = slice(start, stop)
        vals = time[index]
        for i in range(start, stop):
            self.assertAlmostEqual(start + (i/sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        index = slice(stop)
        vals = time[index]
        for i in range(start, stop):
            self.assertAlmostEqual(start + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        def test_negative_slicing(self):
            sample_rate = 1000
            start = 0
            length = 10
            end = start + length / sample_rate
            time = Timer.get_timer('list', start, sample_rate, length)
            stop = 3
            negative_start = length - stop
            index = slice(negative_start, None)
            vals = time[index]
            for i in range(negative_start, length):
                self.assertAlmostEqual(start + (i / sample_rate), vals[i % negative_start], places=7,
                                       msg='Unexpected Time value mismatch')

            index = slice(-1 - stop, -1)
            vals = time[index]
            for i in range(-length, 0, -1):
                self.assertAlmostEqual(end + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

            index = slice(-1, -1 - stop)
            vals = time[index]
            self.assertFalse(vals)  # should be empty list

    # TODO implement slicing step tests
    def test_step_slicing(self):
        raise Exception('Not Yet Implemented -- {}'.format(self.test_step_slicing.__name__))


if __name__ == '__main__':
    import unittest
    unittest.main()
