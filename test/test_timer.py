from unittest import TestCase
from shell import timer

__author__ = 'Danyal Ahsanullah'
__version__ = '1.0.0'
__project__ = 'shell'


class TestTimer(TestCase):
    def test_indexing(self):
        __name__ = 'test_indexing'
        sample_rate = 1000
        start = 0
        length = 10
        end = start + length/sample_rate
        time = timer.Timer(start, sample_rate, length)
        self.assertRaises(expected_exception=IndexError, args=time.__getitem__(length))
        self.assertRaises(expected_exception=IndexError, args=time.__getitem__(-length + 1))
        for i in range(0, length):
            self.assertAlmostEqual(start + (i/sample_rate), time[i], places=7, msg='Unexpected Time value mismatch')
        for i in range(-length, 0, 1):
            self.assertAlmostEqual(end + (i / sample_rate), time[i], places=7, msg='Unexpected Time value mismatch')

    def test_slicing(self):
        __name__ = 'test_slicing'
        sample_rate = 1000
        start = 0
        length = 10
        end = start + length/sample_rate
        time = timer.Timer(start, sample_rate, length)

        stop = 2

        index = slice(start, stop)
        vals = time[index]
        for i in range(start, stop):
            self.assertAlmostEqual(start + (i/sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        index = slice(stop)
        vals = time[index]
        for i in range(start, stop):
            self.assertAlmostEqual(start + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        # TODO implement slicing tests
        index = slice(length-stop, None)
        vals = time[index]
        for i in range(length-stop, length):
            self.assertAlmostEqual(start + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        print('time[-3:-1] = {}'.format(time[-3:-1]))
        index = slice(-1-stop, -1)
        vals = time[index]
        for i in range(-length, 0, -1):
            self.assertAlmostEqual(end + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        print('time[-1:-3] = {}'.format(time[-1:-3]))
        index = slice(-1-stop, -1)
        vals = time[index]
        for i in range(length - stop, length):
            self.assertAlmostEqual(start + (i / sample_rate), vals[i], places=7, msg='Unexpected Time value mismatch')

        raise Exception('Not Yet Implemented -- {}'.format(self.test_slicing.__name__))


if __name__ == '__main__':
    import unittest
    unittest.main()
